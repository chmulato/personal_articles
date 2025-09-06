#!/usr/bin/env python3
"""
Demo do Sistema de Build Organizado
==================================
Demonstração das funcionalidades do novo sistema.

Autor: Sistema Build
Data: Setembro 2025
"""

import sys
from pathlib import Path

# Adiciona o diretório build_system ao path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import *
from utils.file_manager import FileManager

def show_system_overview():
    """Mostra visão geral do sistema organizado."""
    print("=" * 70)
    print("🚀 SISTEMA DE BUILD ORGANIZADO - DEMONSTRAÇÃO")
    print("=" * 70)
    
    print("\n📁 ESTRUTURA ORGANIZADA:")
    print("   build_system/")
    print("   ├── core/              # Componentes principais")
    print("   │   ├── docx_converter.py    # DOCX → MD")
    print("   │   ├── md_to_html.py        # MD → HTML")
    print("   │   └── site_builder.py      # Construção do site")
    print("   ├── utils/             # Utilitários")
    print("   │   ├── file_manager.py      # Gerenciamento de arquivos")
    print("   │   └── normalizer.py        # Normalização de nomes")
    print("   ├── config/            # Configurações")
    print("   │   └── settings.py          # Configurações centralizadas")
    print("   └── build.py           # Script principal")
    
    print("\n💡 COMANDOS PRINCIPAIS:")
    print("   python build.py                 # Build completo")
    print("   python build.py --new-only      # Apenas novos artigos")
    print("   python build.py --status        # Status do sistema")
    print("   python build.py --validate      # Validar estrutura")
    
def show_current_status():
    """Mostra status atual do sistema."""
    file_manager = FileManager()
    status = file_manager.get_build_status()
    
    print("\n📊 STATUS ATUAL:")
    print(f"   • Total de arquivos DOCX: {status['total_docx']}")
    print(f"   • Artigos já processados: {status['processed_count']}")
    print(f"   • Novos para processar: {status['new_docx']}")
    
    if status['new_files']:
        print(f"\n   📂 Próximos {min(5, len(status['new_files']))} a processar:")
        for i, filename in enumerate(status['new_files'][:5]):
            print(f"      {i+1}. {filename}")
        
        if len(status['new_files']) > 5:
            print(f"      ... e mais {len(status['new_files']) - 5} arquivos")
    else:
        print("\n   ✅ Todos os arquivos já foram processados!")

def show_benefits():
    """Mostra benefícios do novo sistema."""
    print("\n⭐ BENEFÍCIOS DO SISTEMA ORGANIZADO:")
    print("   ✅ Estrutura modular e organizada")
    print("   ✅ Configurações centralizadas")
    print("   ✅ Logs detalhados e informativos")
    print("   ✅ Processamento apenas de arquivos novos")
    print("   ✅ Validação automática de dependências")
    print("   ✅ Build incremental inteligente")
    print("   ✅ Gerenciamento automatizado de imagens")
    print("   ✅ HTML semântico e responsivo")

def show_next_steps():
    """Mostra próximos passos sugeridos."""
    print("\n🔄 PRÓXIMOS PASSOS SUGERIDOS:")
    print("   1. Execute: python build.py --validate")
    print("      → Verifica se todas as dependências estão OK")
    print("")
    print("   2. Execute: python build.py --new-only")  
    print("      → Processa apenas os artigos novos")
    print("")
    print("   3. Acesse: c:/dev/personal_articles/articles/index.html")
    print("      → Visualiza o site gerado")
    print("")
    print("   4. Para builds futuros: python build.py --new-only")
    print("      → Processa apenas artigos adicionados recentemente")

def main():
    """Executa demonstração completa."""
    show_system_overview()
    show_current_status()
    show_benefits()
    show_next_steps()
    
    print("\n" + "=" * 70)
    print("✨ SISTEMA PRONTO PARA USO!")
    print("=" * 70)
    print("\n💡 Dica: Use 'python build.py --help' para ver todas as opções")

if __name__ == '__main__':
    main()
