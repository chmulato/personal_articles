#!/usr/bin/env python3
"""
Script para organizar e renomear imagens dos artigos seguindo padrão consistente.
Padrão: YYYY_MM_DD_image_001.ext, YYYY_MM_DD_image_002.ext, etc.
"""

import os
import re
import shutil
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

class ImageOrganizer:
    def __init__(self, images_dir: str, articles_dir: str):
        self.images_dir = Path(images_dir)
        self.articles_dir = Path(articles_dir)
        self.backup_dir = self.images_dir / "backup_original_names"
        
    def create_backup_dir(self):
        """Cria diretório de backup se não existir"""
        self.backup_dir.mkdir(exist_ok=True)
        
    def extract_date_from_filename(self, filename: str) -> str:
        """Extrai data do nome do arquivo"""
        # Padrão: YYYY_MM_DD no início do nome
        date_pattern = r'^(\d{4}_\d{2}_\d{2})'
        match = re.match(date_pattern, filename)
        if match:
            return match.group(1)
        return None
    
    def get_file_extension(self, filename: str) -> str:
        """Retorna extensão do arquivo"""
        return Path(filename).suffix.lower()
    
    def analyze_current_images(self) -> Dict[str, List[str]]:
        """Analisa imagens atuais e as agrupa por data"""
        images_by_date = defaultdict(list)
        
        for img_file in self.images_dir.glob("*"):
            if img_file.is_file() and img_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                filename = img_file.name
                date = self.extract_date_from_filename(filename)
                
                if date:
                    images_by_date[date].append(filename)
                else:
                    # Imagens sem padrão de data
                    images_by_date["sem_data"].append(filename)
                    
        return dict(images_by_date)
    
    def generate_new_mapping(self, images_by_date: Dict[str, List[str]]) -> Dict[str, str]:
        """Gera mapeamento de nomes antigos para novos"""
        mapping = {}
        
        for date, filenames in images_by_date.items():
            if date == "sem_data":
                continue
                
            # Ordena por nome para consistência
            filenames.sort()
            
            # Separa imagens featured das demais
            featured_images = [f for f in filenames if 'featured' in f.lower()]
            content_images = [f for f in filenames if 'featured' not in f.lower()]
            
            counter = 1
            
            # Primeiro processa featured image
            for filename in featured_images:
                ext = self.get_file_extension(filename)
                new_name = f"{date}_featured{ext}"
                mapping[filename] = new_name
                
            # Depois processa imagens de conteúdo
            for filename in content_images:
                ext = self.get_file_extension(filename)
                new_name = f"{date}_image_{counter:03d}{ext}"
                mapping[filename] = new_name
                counter += 1
                
        return mapping
    
    def backup_original_file(self, original_name: str):
        """Cria backup do arquivo original"""
        original_path = self.images_dir / original_name
        backup_path = self.backup_dir / original_name
        
        if original_path.exists() and not backup_path.exists():
            shutil.copy2(original_path, backup_path)
    
    def rename_image_file(self, old_name: str, new_name: str) -> bool:
        """Renomeia arquivo de imagem"""
        old_path = self.images_dir / old_name
        new_path = self.images_dir / new_name
        
        if not old_path.exists():
            print(f"❌ Arquivo não encontrado: {old_name}")
            return False
            
        if new_path.exists():
            print(f"⚠️  Arquivo destino já existe: {new_name}")
            return False
            
        try:
            # Backup antes de renomear
            self.backup_original_file(old_name)
            
            # Renomeia o arquivo
            old_path.rename(new_path)
            print(f"✅ {old_name} → {new_name}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao renomear {old_name}: {e}")
            return False
    
    def update_html_references(self, old_name: str, new_name: str):
        """Atualiza referências nos arquivos HTML"""
        # Busca por arquivos HTML que possam referenciar a imagem
        date_from_old = self.extract_date_from_filename(old_name)
        if not date_from_old:
            return
            
        # Procura arquivo HTML correspondente
        html_pattern = f"{date_from_old}_*.html"
        html_files = list(self.articles_dir.glob(html_pattern))
        
        for html_file in html_files:
            try:
                content = html_file.read_text(encoding='utf-8')
                
                # Substitui referências à imagem antiga
                if old_name in content:
                    updated_content = content.replace(old_name, new_name)
                    html_file.write_text(updated_content, encoding='utf-8')
                    print(f"📝 Atualizado HTML: {html_file.name}")
                    
            except Exception as e:
                print(f"❌ Erro ao atualizar HTML {html_file.name}: {e}")
    
    def organize_images(self, dry_run: bool = True):
        """Executa organização das imagens"""
        print("🔍 Analisando imagens atuais...")
        
        # Cria backup directory
        self.create_backup_dir()
        
        # Analisa imagens atuais
        images_by_date = self.analyze_current_images()
        
        print(f"\n📊 Encontradas imagens para {len(images_by_date)} datas diferentes:")
        for date, files in images_by_date.items():
            print(f"  {date}: {len(files)} arquivos")
            
        # Gera mapeamento
        mapping = self.generate_new_mapping(images_by_date)
        
        if not mapping:
            print("❌ Nenhum arquivo para renomear encontrado.")
            return
            
        print(f"\n📋 Planejamento de renomeação ({len(mapping)} arquivos):")
        for old_name, new_name in mapping.items():
            print(f"  {old_name} → {new_name}")
            
        if dry_run:
            print("\n🔄 Modo teste ativado. Para executar as alterações, use organize_images(dry_run=False)")
            return
            
        # Confirma execução
        print(f"\n⚠️  Serão renomeados {len(mapping)} arquivos.")
        confirm = input("Confirmar execução? (s/N): ").lower().strip()
        
        if confirm != 's':
            print("❌ Operação cancelada.")
            return
            
        print("\n🚀 Iniciando renomeação...")
        
        # Executa renomeação
        success_count = 0
        for old_name, new_name in mapping.items():
            if self.rename_image_file(old_name, new_name):
                self.update_html_references(old_name, new_name)
                success_count += 1
                
        print(f"\n✅ Concluído! {success_count}/{len(mapping)} arquivos renomeados com sucesso.")
        print(f"📁 Backups salvos em: {self.backup_dir}")

def main():
    # Caminhos
    images_dir = r"c:\dev\personal_articles\articles\assets\img"
    articles_dir = r"c:\dev\personal_articles\articles"
    
    # Cria organizador
    organizer = ImageOrganizer(images_dir, articles_dir)
    
    # Executa análise em modo teste
    print("🎯 ORGANIZADOR DE IMAGENS - Padrão YYYY_MM_DD_image_XXX")
    print("=" * 60)
    
    organizer.organize_images(dry_run=True)
    
    print("\n" + "=" * 60)
    print("💡 Para executar as alterações, execute:")
    print("   organizer.organize_images(dry_run=False)")

if __name__ == "__main__":
    main()
