#!/usr/bin/env python3
"""
Teste de conversão de um único arquivo MD para HTML com correção de imagens
"""

import sys
from pathlib import Path

# Adiciona o diretório build_system ao path
sys.path.insert(0, str(Path(__file__).parent / "scr" / "build_system"))

from core.md_to_html import MarkdownToHtmlConverter

def test_single_conversion():
    """Testa conversão de um único arquivo"""
    
    # Procurar por arquivos MD existentes
    md_dir = Path("C:/dev/personal_articles/md")
    md_files = list(md_dir.glob("*.md"))
    
    if not md_files:
        print("❌ Nenhum arquivo MD encontrado para teste")
        return
    
    # Pegar o primeiro arquivo MD
    test_file = md_files[0]
    print(f"🧪 Testando conversão do arquivo: {test_file.name}")
    
    # Criar instância do conversor
    converter = MarkdownToHtmlConverter()
    
    # Tentar conversão
    success = converter.convert_markdown_to_html(str(test_file))
    
    if success:
        print("✅ Conversão realizada com sucesso!")
        
        # Verificar se o HTML foi criado
        html_file = Path(f"C:/dev/personal_articles/articles/{test_file.stem}.html")
        if html_file.exists():
            print(f"✅ Arquivo HTML criado: {html_file.name}")
            
            # Verificar se há correções de imagem no arquivo
            content = html_file.read_text(encoding='utf-8')
            if 'temp_media' in content:
                print("⚠️  Ainda há caminhos temp_media no arquivo HTML")
            else:
                print("✅ Nenhum caminho temp_media encontrado - correções aplicadas!")
                
            # Contar quantas imagens foram corrigidas
            assets_count = content.count('assets/img/')
            if assets_count > 0:
                print(f"✅ {assets_count} referências de imagem com caminho correto encontradas")
        else:
            print("❌ Arquivo HTML não foi criado")
    else:
        print("❌ Conversão falhou")

if __name__ == "__main__":
    test_single_conversion()
