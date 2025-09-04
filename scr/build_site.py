#!/usr/bin/env python3
"""
Build Script - Script de build completo do site
Localizado em: C:\dev\personal_articles\md\site_artiches\scr\build_site.py

Este script executa o build completo do site:
1. Converte todos os MD para HTML
2. Atualiza o index.html
3. Valida links e recursos
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório do script ao path
sys.path.insert(0, str(Path(__file__).parent))

from site_manager import SiteManager

def main():
    print("🚀 INICIANDO BUILD DO SITE")
    print("=" * 50)
    
    manager = SiteManager()
    
    # Passo 1: Converter todos os artigos
    print("\n📝 Convertendo artigos MD → HTML...")
    success_count = manager.convert_all_articles()
    print(f"✅ {success_count} artigos convertidos")
    
    # Passo 2: Gerar index.html (implementar depois)
    print("\n🏠 Gerando index.html...")
    manager.generate_index_html()
    
    # Passo 3: Validar site (implementar depois)
    print("\n🔍 Validando site...")
    manager.validate_site()
    
    print("\n🎉 BUILD CONCLUÍDO!")
    print(f"📂 Site disponível em: {manager.base_dir}")
    print(f"🌐 Artigos em: {manager.articles_dir}")
    
if __name__ == "__main__":
    main()
