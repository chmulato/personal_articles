#!/usr/bin/env python3
"""
Demonstração do Sistema de Controle de Processamento
===================================================
Mostra como funciona o controle rigoroso de artigos processados.

Autor: Sistema Build
Data: Setembro 2025
"""

import sys
from pathlib import Path

# Adiciona o diretório build_system ao path
sys.path.insert(0, str(Path(__file__).parent))

from utils.processed_articles_manager import ProcessedArticlesManager

def demo_control_system():
    """Demonstra o sistema de controle."""
    print("=" * 70)
    print("🔐 SISTEMA DE CONTROLE RIGOROSO - DEMONSTRAÇÃO")
    print("=" * 70)
    
    manager = ProcessedArticlesManager()
    
    print("\n📋 COMO FUNCIONA O CONTROLE:")
    print("   1. Arquivo 'processed_articles.txt' contém lista de artigos processados")
    print("   2. Apenas artigos DOCX NÃO listados são processados")
    print("   3. Evita reprocessamento desnecessário e conflitos")
    print("   4. Sistema atualiza lista automaticamente após processamento")
    
    print("\n📊 STATUS ATUAL:")
    processed = manager.load_processed_list()
    unprocessed = manager.get_unprocessed_docx()
    
    print(f"   ✅ Artigos já processados: {len(processed)}")
    print(f"   ⏳ Aguardando processamento: {len(unprocessed)}")
    
    if unprocessed:
        print(f"\n📂 Próximos a processar:")
        for i, docx_file in enumerate(unprocessed[:5], 1):
            print(f"      {i}. {docx_file.name}")
        if len(unprocessed) > 5:
            print(f"      ... e mais {len(unprocessed) - 5}")
    else:
        print("\n   🎉 Todos os arquivos já foram processados!")
    
    print(f"\n💡 COMANDOS ÚTEIS:")
    print("   # Ver status detalhado")
    print("   python -m utils.processed_articles_manager status")
    print("")
    print("   # Remover artigo para reprocessar")
    print("   python -m utils.processed_articles_manager remove nome_artigo")
    print("")
    print("   # Sincronizar com HTMLs existentes")
    print("   python -m utils.processed_articles_manager sync")
    print("")
    print("   # Listar todos os processados")
    print("   python -m utils.processed_articles_manager list")
    
    print(f"\n🔒 PROTEÇÃO CONTRA SOBREPOSIÇÃO:")
    print("   ✅ Evita reprocessar artigos já convertidos")
    print("   ✅ Mantém controle rigoroso de estado")
    print("   ✅ Permite reprocessamento seletivo se necessário")
    print("   ✅ Sincronização automática com arquivos HTML")
    
def demo_remove_and_readd():
    """Demonstra remoção e re-adição de artigo."""
    print("\n" + "=" * 70)
    print("🔄 DEMONSTRAÇÃO: REPROCESSAMENTO DE ARTIGO")
    print("=" * 70)
    
    manager = ProcessedArticlesManager()
    
    # Pega um artigo processado para demonstrar
    processed = manager.load_processed_list()
    if not processed:
        print("❌ Nenhum artigo processado encontrado para demonstrar")
        return
    
    sample_article = sorted(processed)[0]  # Primeiro da lista ordenada
    
    print(f"\n📝 Exemplo com artigo: {sample_article}")
    print(f"   Status atual: {'✅ Processado' if manager.is_processed(sample_article) else '⏳ Não processado'}")
    
    print(f"\n💭 Para reprocessar este artigo:")
    print(f"   1. Remover da lista:")
    print(f"      python -m utils.processed_articles_manager remove {sample_article}")
    print(f"   ")
    print(f"   2. Executar build (apenas artigos novos):")
    print(f"      python build.py --new-only")
    print(f"   ")
    print(f"   3. Artigo será reprocessado e readicionado à lista automaticamente")
    
    print(f"\n⚠️ IMPORTANTE:")
    print("   • Sistema não reprocessa artigos já na lista")
    print("   • Para forçar reprocessamento, remova da lista primeiro")
    print("   • Build --new-only é mais eficiente que build completo")
    print("   • Lista é atualizada automaticamente após processamento")

def main():
    """Executa demonstração completa."""
    demo_control_system()
    demo_remove_and_readd()
    
    print("\n" + "=" * 70)
    print("✨ SISTEMA DE CONTROLE FUNCIONANDO PERFEITAMENTE!")
    print("=" * 70)
    print("\n🎯 Benefícios Alcançados:")
    print("   ✅ Controle rigoroso de processamento")
    print("   ✅ Evita sobreposição de arquivos")
    print("   ✅ Build incremental eficiente")
    print("   ✅ Reprocessamento seletivo possível")
    print("   ✅ Sincronização automática")

if __name__ == '__main__':
    main()
