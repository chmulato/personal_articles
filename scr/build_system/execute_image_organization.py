#!/usr/bin/env python3
"""
Script executável para organizar imagens com confirmação interativa.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_organizer import ImageOrganizer

def main():
    print("🎯 ORGANIZADOR DE IMAGENS - Execução Interativa")
    print("=" * 60)
    
    # Caminhos
    images_dir = r"c:\dev\personal_articles\articles\assets\img"
    articles_dir = r"c:\dev\personal_articles\articles"
    
    # Cria organizador
    organizer = ImageOrganizer(images_dir, articles_dir)
    
    print("📋 Esta ferramenta vai:")
    print("  ✅ Analisar todas as imagens atuais")
    print("  ✅ Criar backups dos arquivos originais")
    print("  ✅ Renomear para padrão: YYYY_MM_DD_image_001.ext")
    print("  ✅ Atualizar referências nos arquivos HTML")
    print()
    
    # Executa análise primeiro
    print("🔍 Executando análise...")
    organizer.organize_images(dry_run=True)
    
    print("\n" + "="*60)
    print("⚠️  ATENÇÃO: Esta operação irá:")
    print("   • Renomear 242+ arquivos de imagem")
    print("   • Criar backups em backup_original_names/")
    print("   • Atualizar referências nos HTMLs")
    print()
    
    # Confirma execução
    while True:
        resposta = input("🤔 Deseja prosseguir com a organização? (s/N): ").lower().strip()
        
        if resposta in ['s', 'sim', 'y', 'yes']:
            print("\n🚀 Iniciando organização das imagens...")
            organizer.organize_images(dry_run=False)
            break
        elif resposta in ['n', 'nao', 'não', 'no', '']:
            print("❌ Operação cancelada pelo usuário.")
            break
        else:
            print("❓ Por favor, responda 's' para sim ou 'n' para não.")

if __name__ == "__main__":
    main()
