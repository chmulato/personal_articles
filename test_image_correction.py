#!/usr/bin/env python3
"""
Teste da funcionalidade de correção de caminhos de imagem integrada
"""

import sys
from pathlib import Path

# Adiciona o diretório build_system ao path
sys.path.insert(0, str(Path(__file__).parent / "scr" / "build_system"))

from core.md_to_html import MarkdownToHtmlConverter

def test_image_path_correction():
    """Testa a correção de caminhos de imagem"""
    
    # HTML de exemplo com caminho temp_media
    test_html = '''
    <div>
        <p>Este é um teste com uma imagem:</p>
        <img src="temp_media\\2024_03_06_aplicacao_web_java/assets/img/2024_03_06_IMAGE_001.png" alt="Teste">
        <p>E outra imagem:</p>
        <img src="temp_media/2024_03_06_aplicacao_web_java/assets/img/2024_03_06_IMAGE_002.jpg" alt="Teste 2">
    </div>
    '''
    
    print("🧪 Testando correção de caminhos de imagem...")
    print("\nHTML original:")
    print(test_html)
    
    # Criar instância do conversor
    converter = MarkdownToHtmlConverter()
    
    # Aplicar correção
    corrected_html = converter.fix_html_image_paths(test_html, "2024_03_06_aplicacao_web_java")
    
    print("\nHTML corrigido:")
    print(corrected_html)
    
    # Verificar se as correções foram aplicadas
    if 'assets/img/2024_03_06_IMAGE_001.png' in corrected_html:
        print("\n✅ Correção 1 aplicada com sucesso!")
    else:
        print("\n❌ Correção 1 falhou!")
    
    if 'assets/img/2024_03_06_IMAGE_002.jpg' in corrected_html:
        print("✅ Correção 2 aplicada com sucesso!")
    else:
        print("❌ Correção 2 falhou!")
    
    # Verificar se não há mais caminhos temp_media
    if 'temp_media' not in corrected_html:
        print("✅ Todos os caminhos temp_media foram removidos!")
    else:
        print("❌ Ainda existem caminhos temp_media!")

if __name__ == "__main__":
    test_image_path_correction()
