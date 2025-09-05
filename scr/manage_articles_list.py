#!/usr/bin/env python3
"""
Gerenciador Simples da Lista de Artigos
======================================
Script simplificado para gerenciar artigos processados.

Autor: Christian Mulato
Data: 2025-09-05
"""

import sys
from pathlib import Path

# Diretórios do projeto
PROJECT_ROOT = Path("c:/dev/personal_articles")
DOCX_DIR = PROJECT_ROOT / "docx"
ARTICLES_DIR = PROJECT_ROOT / "articles"
PROCESSED_LIST = PROJECT_ROOT / "scr" / "artigos_processados.txt"

def load_processed_articles():
    """Carrega artigos processados."""
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
    name = name.lower()
    replacements = {
        'ã': 'a', 'á': 'a', 'à': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e',
        'í': 'i', 'î': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'û': 'u',
        'ç': 'c', 'ñ': 'n'
    }
    
    for old, new in replacements.items():
        name = name.replace(old, new)
    
    name = re.sub(r'[^a-z0-9_]', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    
    return name

def get_docx_articles():
    """Retorna artigos DOCX existentes."""
    if not DOCX_DIR.exists():
        return set()
    
    docx_files = DOCX_DIR.glob("*.docx")
    return {normalize_name(f.stem) 
            for f in docx_files if not f.name.startswith("~")}

def get_html_articles():
    """Retorna artigos HTML existentes."""
    if not ARTICLES_DIR.exists():
        return set()
    
    html_files = ARTICLES_DIR.glob("*.html")
    return {f.stem for f in html_files}

def show_status():
    """Mostra status dos artigos."""
    processed = load_processed_articles()
    docx_articles = get_docx_articles()
    html_articles = get_html_articles()
    
    print("=" * 50)
    print("Status dos Artigos")
    print("=" * 50)
    print(f"Artigos processados: {len(processed)}")
    print(f"Arquivos HTML: {len(html_articles)}")
    print(f"Arquivos DOCX: {len(docx_articles)}")
    
    # Artigos novos
    new_articles = docx_articles - processed
    if new_articles:
        print(f"\nArtigos novos ({len(new_articles)}):")
        for article in sorted(list(new_articles)[:10]):  # Mostra apenas os 10 primeiros
            print(f"  - {article}")
        if len(new_articles) > 10:
            print(f"  ... e mais {len(new_articles) - 10} artigos")
    else:
        print("\nNenhum artigo novo!")

def add_article(article_name):
    """Adiciona artigo à lista."""
    processed = load_processed_articles()
    
    if article_name in processed:
        print(f"Artigo ja listado: {article_name}")
        return False
    
    try:
        with open(PROCESSED_LIST, 'a', encoding='utf-8') as f:
            f.write(f"{article_name}\n")
        print(f"Artigo adicionado: {article_name}")
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False

def sync_with_html():
    """Sincroniza lista com HTMLs existentes."""
    processed = load_processed_articles()
    html_articles = get_html_articles()
    
    missing = html_articles - processed
    if missing:
        print(f"{len(missing)} artigos HTML nao listados:")
        for article in sorted(missing):
            print(f"  + {article}")
        
        if input("\nAdicionar a lista? (s/N): ").lower() == 's':
            for article in missing:
                add_article(article)

def main():
    """Função principal."""
    if len(sys.argv) < 2:
        print("Uso: python manage_articles_list.py <comando>")
        print("\nComandos:")
        print("  status    - Mostra status atual")
        print("  sync      - Sincroniza com HTMLs")
        print("  add <nome> - Adiciona artigo")
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        show_status()
    elif command == "sync":
        sync_with_html()
    elif command == "add" and len(sys.argv) > 2:
        add_article(sys.argv[2])
    else:
        print("Comando invalido")

if __name__ == "__main__":
    main()
