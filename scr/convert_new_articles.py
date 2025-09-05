#!/usr/bin/env python3
"""
Sistema de Conversão Controlada de Artigos
==========================================
Converte apenas arquivos DOCX que não estão na lista de processados.

Autor: Christian Mulato
Data: 2025-09-05
"""

import os
import subprocess
from pathlib import Path

# Diretórios do projeto
PROJECT_ROOT = Path("c:/dev/personal_articles")
DOCX_DIR = PROJECT_ROOT / "docx"
MD_DIR = PROJECT_ROOT / "md"
ARTICLES_DIR = PROJECT_ROOT / "articles"
SCR_DIR = PROJECT_ROOT / "scr"
PROCESSED_LIST = SCR_DIR / "artigos_processados.txt"

def load_processed_articles():
    """Carrega artigos já processados."""
    processed = set()
    if PROCESSED_LIST.exists():
        with open(PROCESSED_LIST, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    processed.add(line)
    return processed

def normalize_name(name):
    """Normaliza nome do arquivo para comparação."""
    import re
    # Remove acentos, converte para minúsculas, substitui espaços e caracteres especiais
    name = name.lower()
    replacements = {
        'ã': 'a', 'á': 'a', 'à': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e',
        'í': 'i', 'î': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'û': 'u',
        'ç': 'c',
        'ñ': 'n'
    }
    
    for old, new in replacements.items():
        name = name.replace(old, new)
    
    # Substitui espaços e caracteres especiais por underscore
    name = re.sub(r'[^a-z0-9_]', '_', name)
    # Remove underscores múltiplos
    name = re.sub(r'_+', '_', name)
    # Remove underscores no início e fim
    name = name.strip('_')
    
    return name

def get_new_docx_files():
    """Retorna apenas arquivos DOCX que não foram processados."""
    if not DOCX_DIR.exists():
        print(f"Pasta DOCX nao encontrada: {DOCX_DIR}")
        return []
    
    processed = load_processed_articles()
    docx_files = list(DOCX_DIR.glob("*.docx"))
    docx_files = [f for f in docx_files if not f.name.startswith("~")]
    
    # Filtra apenas artigos novos
    new_files = []
    for docx_file in docx_files:
        normalized_name = normalize_name(docx_file.stem)
        if normalized_name not in processed:
            new_files.append(docx_file)
    
    return new_files

def convert_docx_to_md(docx_file):
    """Converte DOCX para MD."""
    try:
        md_file = MD_DIR / f"{docx_file.stem}.md"
        cmd = ["pandoc", str(docx_file), "-o", str(md_file), "--wrap=none"]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return md_file
        else:
            print(f"Erro pandoc: {result.stderr}")
            return None
    except Exception as e:
        print(f"Erro DOCX->MD: {e}")
        return None

def convert_md_to_html(md_file):
    """Converte MD para HTML usando script existente."""
    try:
        convert_script = SCR_DIR / "convert_md_to_html.py"
        if not convert_script.exists():
            print(f"Script nao encontrado: {convert_script}")
            return None
            
        cmd = ["python", str(convert_script), str(md_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            html_file = ARTICLES_DIR / f"{md_file.stem}.html"
            return html_file if html_file.exists() else None
        else:
            print(f"Erro MD->HTML: {result.stderr}")
            return None
    except Exception as e:
        print(f"Erro conversao: {e}")
        return None

def add_to_processed_list(article_name):
    """Adiciona artigo à lista."""
    try:
        with open(PROCESSED_LIST, 'a', encoding='utf-8') as f:
            f.write(f"{article_name}\n")
    except Exception as e:
        print(f"Erro ao atualizar lista: {e}")

def main():
    """Função principal."""
    print("=" * 50)
    print("Conversao Controlada de Artigos")
    print("=" * 50)
    
    # Busca artigos novos
    new_files = get_new_docx_files()
    if not new_files:
        print("Nenhum artigo novo para processar!")
        return
    
    print(f"Processando {len(new_files)} artigos novos...")
    
    # Cria diretórios
    MD_DIR.mkdir(exist_ok=True)
    ARTICLES_DIR.mkdir(exist_ok=True)
    
    success_count = 0
    
    for docx_file in new_files:
        print(f"\n>> {docx_file.name}")
        
        # DOCX -> MD
        print("  DOCX -> MD...")
        md_file = convert_docx_to_md(docx_file)
        if not md_file:
            continue
        print("  MD criado")
        
        # MD -> HTML
        print("  MD -> HTML...")
        html_file = convert_md_to_html(md_file)
        if not html_file:
            continue
        print("  HTML criado")
        
        # Adiciona à lista
        normalized_name = normalize_name(docx_file.stem)
        add_to_processed_list(normalized_name)
        print("  Adicionado a lista")
        
        success_count += 1
    
    print(f"\n{success_count}/{len(new_files)} artigos convertidos!")

if __name__ == "__main__":
    main()
