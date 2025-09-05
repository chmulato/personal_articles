#!/usr/bin/env python3
"""
Script para remover arquivos HTML duplicados, mantendo apenas as versões com títulos legíveis
"""

import os
from pathlib import Path
import re

def clean_duplicate_articles():
    """Remove artigos duplicados do diretório articles"""
    
    articles_dir = Path("articles")
    
    if not articles_dir.exists():
        print("Diretório articles não encontrado!")
        return
    
    # Encontrar todos os arquivos HTML
    html_files = list(articles_dir.glob("*.html"))
    
    # Agrupar por base de nome (ano_mês_dia)
    file_groups = {}
    
    for file in html_files:
        name = file.stem
        
        # Extrair data base (YYYY_MM_DD)
        date_match = re.match(r'^(\d{4}_\d{2}_\d{2})', name)
        if date_match:
            date_base = date_match.group(1)
            
            if date_base not in file_groups:
                file_groups[date_base] = []
            
            file_groups[date_base].append(file)
    
    # Para cada grupo, manter apenas o arquivo com o nome mais descritivo
    removed_count = 0
    
    for date_base, files in file_groups.items():
        if len(files) > 1:
            # Ordenar por tamanho do nome (mais longo = mais descritivo)
            files.sort(key=lambda f: len(f.stem), reverse=True)
            
            # Manter o primeiro (mais descritivo), remover os outros
            keep_file = files[0]
            remove_files = files[1:]
            
            print(f"\n📅 {date_base}:")
            print(f"  ✅ Mantendo: {keep_file.name}")
            
            for remove_file in remove_files:
                print(f"  ❌ Removendo: {remove_file.name}")
                try:
                    remove_file.unlink()
                    removed_count += 1
                except Exception as e:
                    print(f"  ⚠️  Erro ao remover {remove_file.name}: {e}")
    
    print(f"\n🧹 Limpeza concluída!")
    print(f"📊 {removed_count} arquivos duplicados removidos")
    print(f"📄 {len(file_groups)} artigos únicos mantidos")
    
    # Verificar arquivos com nomes malformados
    print(f"\n🔍 Verificando arquivos malformados...")
    malformed = []
    
    remaining_files = list(articles_dir.glob("*.html"))
    for file in remaining_files:
        name = file.stem
        
        # Verificar padrões malformados
        if (name.endswith('_') or 
            name.count('_') < 3 or  # Deve ter pelo menos YYYY_MM_DD_titulo
            not re.match(r'^\d{4}_\d{2}_\d{2}_', name)):
            malformed.append(file)
    
    if malformed:
        print(f"⚠️  Encontrados {len(malformed)} arquivos com nomes malformados:")
        for file in malformed:
            print(f"  - {file.name}")
            try:
                file.unlink()
                print(f"    ❌ Removido")
                removed_count += 1
            except Exception as e:
                print(f"    ⚠️ Erro: {e}")
    else:
        print("✅ Nenhum arquivo malformado encontrado")
    
    print(f"\n🎉 Total de {removed_count} arquivos removidos")

if __name__ == "__main__":
    clean_duplicate_articles()
