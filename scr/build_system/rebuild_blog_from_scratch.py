#!/usr/bin/env python3
"""
Script para reconstrução completa do blog do zero
Processa todos os 59 arquivos DOCX com nomenclatura consistente das imagens
"""

import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime

# Adicionar o diretório build_system ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from docx_converter import DOCXConverter
from md_to_html import MarkdownToHTML
from site_builder import SiteBuilder
from file_manager import FileManager
from processed_articles_manager import ProcessedArticlesManager

class BlogRebuilder:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.docx_dir = self.base_dir / "docx"
        self.articles_dir = self.base_dir / "articles"
        self.md_dir = self.base_dir / "md"
        self.temp_dir = self.base_dir / "temp_media"
        
        # Inicializar componentes
        self.converter = DOCXConverter(str(self.base_dir))
        self.md_to_html = MarkdownToHTML(str(self.base_dir))
        self.site_builder = SiteBuilder(str(self.base_dir))
        self.file_manager = FileManager()
        self.processed_manager = ProcessedArticlesManager(str(self.base_dir))
        
    def clean_all_outputs(self):
        """Limpar todos os arquivos gerados anteriormente"""
        print("🧹 Limpando arquivos existentes...")
        
        # Limpar artigos HTML
        if self.articles_dir.exists():
            for html_file in self.articles_dir.glob("*.html"):
                html_file.unlink()
                print(f"  Removido: {html_file.name}")
        
        # Limpar imagens dos artigos
        img_dir = self.articles_dir / "assets" / "img"
        if img_dir.exists():
            # Manter apenas imagens essenciais
            essential_images = {'placeholder.png', 'foto_chri.jpg', 'prompt.txt', 'prompt_rd.txt'}
            for img_file in img_dir.iterdir():
                if img_file.name not in essential_images:
                    if img_file.is_file():
                        img_file.unlink()
                        print(f"  Removida imagem: {img_file.name}")
        
        # Limpar arquivos MD
        if self.md_dir.exists():
            for md_file in self.md_dir.glob("*.md"):
                md_file.unlink()
                print(f"  Removido MD: {md_file.name}")
        
        # Limpar temp_media
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print(f"  Removido diretório temporário: {self.temp_dir}")
        
        # Resetar arquivo de controle
        self.processed_manager.clear_all()
        print("  Arquivo de controle limpo")
        
        print("✅ Limpeza concluída!\n")

    def get_docx_files(self):
        """Obter lista de todos os arquivos DOCX ordenados por data"""
        docx_files = list(self.docx_dir.glob("*.docx"))
        
        # Extrair data dos nomes dos arquivos e ordenar
        def extract_date(filename):
            try:
                # Formato: YYYY_MM_DD_titulo.docx
                parts = filename.stem.split('_')
                if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
                    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                    return datetime(year, month, day)
                else:
                    return datetime.min
            except:
                return datetime.min
        
        docx_files.sort(key=extract_date)
        return docx_files

    def process_single_docx(self, docx_file, index):
        """Processar um único arquivo DOCX com nomenclatura consistente"""
        filename = docx_file.stem
        print(f"📄 Processando ({index}/59): {filename}")
        
        try:
            # 1. Converter DOCX para MD
            print(f"  🔄 Convertendo para Markdown...")
            md_success = self.converter.convert_docx_to_markdown(str(docx_file))
            
            if not md_success:
                print(f"  ❌ Erro na conversão para MD: {filename}")
                return False
            
            # 2. Organizar imagens com nomenclatura consistente
            print(f"  🖼️  Organizando imagens...")
            self.organize_images_for_article(filename)
            
            # 3. Converter MD para HTML
            print(f"  🔄 Convertendo para HTML...")
            md_file = self.md_dir / f"{filename}.md"
            if md_file.exists():
                html_success = self.md_to_html.convert_markdown_to_html(str(md_file))
                if not html_success:
                    print(f"  ❌ Erro na conversão para HTML: {filename}")
                    return False
            else:
                print(f"  ❌ Arquivo MD não encontrado: {filename}")
                return False
            
            # 4. Marcar como processado
            self.processed_manager.mark_as_processed(filename)
            print(f"  ✅ Concluído: {filename}")
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao processar {filename}: {str(e)}")
            return False

    def organize_images_for_article(self, article_name):
        """Organizar imagens de um artigo com nomenclatura consistente"""
        temp_article_dir = self.temp_dir / article_name
        target_img_dir = self.articles_dir / "assets" / "img"
        
        # Criar diretório de destino se não existir
        target_img_dir.mkdir(parents=True, exist_ok=True)
        
        if not temp_article_dir.exists():
            return
        
        # Listar todas as imagens da pasta temporária
        image_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.webp']:
            image_files.extend(temp_article_dir.glob(ext))
        
        if not image_files:
            return
        
        # Ordenar por nome para consistência
        image_files.sort(key=lambda x: x.name)
        
        # Renomear com padrão consistente
        for i, img_file in enumerate(image_files, 1):
            # Determinar extensão
            ext = img_file.suffix.lower()
            
            # Criar novo nome: YYYY_MM_DD_título_image00X.ext
            new_name = f"{article_name}_image{i:03d}{ext}"
            target_path = target_img_dir / new_name
            
            # Copiar com novo nome
            shutil.copy2(img_file, target_path)
            print(f"    📁 {img_file.name} → {new_name}")

    def update_index_stats(self):
        """Atualizar estatísticas no index.html"""
        index_file = self.base_dir / "index.html"
        if not index_file.exists():
            return
            
        try:
            content = index_file.read_text(encoding='utf-8')
            
            # Atualizar número de artigos
            content = content.replace(
                '<span class="stat">59 artigos publicados</span>',
                '<span class="stat">59 artigos publicados</span>'
            )
            
            index_file.write_text(content, encoding='utf-8')
            print("📊 Estatísticas do index.html atualizadas")
            
        except Exception as e:
            print(f"❌ Erro ao atualizar index.html: {str(e)}")

    def generate_report(self, successful, failed):
        """Gerar relatório final"""
        print("\n" + "="*60)
        print("📋 RELATÓRIO FINAL DA RECONSTRUÇÃO")
        print("="*60)
        print(f"📄 Total de arquivos DOCX: 59")
        print(f"✅ Processados com sucesso: {len(successful)}")
        print(f"❌ Falharam: {len(failed)}")
        print(f"📈 Taxa de sucesso: {(len(successful)/59*100):.1f}%")
        
        if failed:
            print(f"\n❌ Arquivos que falharam:")
            for fail in failed:
                print(f"  - {fail}")
        
        print(f"\n🎉 Reconstrução completa finalizada!")
        print(f"🌐 Site pronto em: {self.articles_dir}")

    def run_complete_rebuild(self):
        """Executar reconstrução completa"""
        print("🚀 INICIANDO RECONSTRUÇÃO COMPLETA DO BLOG")
        print("="*60)
        
        # 1. Limpar tudo
        self.clean_all_outputs()
        
        # 2. Obter arquivos DOCX
        docx_files = self.get_docx_files()
        print(f"📚 Encontrados {len(docx_files)} arquivos DOCX")
        
        # 3. Processar todos os arquivos
        print(f"\n🔄 Iniciando processamento...")
        successful = []
        failed = []
        
        for i, docx_file in enumerate(docx_files, 1):
            if self.process_single_docx(docx_file, i):
                successful.append(docx_file.stem)
            else:
                failed.append(docx_file.stem)
            print()  # Linha em branco entre arquivos
        
        # 4. Construir site
        print("🏗️  Construindo estrutura do site...")
        try:
            self.site_builder.build_site()
            print("✅ Site construído com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao construir site: {str(e)}")
        
        # 5. Atualizar estatísticas
        self.update_index_stats()
        
        # 6. Gerar relatório
        self.generate_report(successful, failed)

def main():
    # Diretório base do projeto
    base_dir = "C:/dev/personal_articles"
    
    # Confirmar antes de começar
    print("⚠️  ATENÇÃO: Esta operação vai:")
    print("   • Deletar todos os arquivos HTML existentes")
    print("   • Deletar todas as imagens organizadas")
    print("   • Deletar todos os arquivos MD")
    print("   • Reprocessar todos os 59 arquivos DOCX do zero")
    print("   • Reorganizar imagens com nomenclatura consistente")
    
    confirm = input("\n🤔 Deseja continuar? (s/N): ").lower().strip()
    
    if confirm not in ['s', 'sim', 'yes', 'y']:
        print("❌ Operação cancelada pelo usuário")
        return
    
    # Executar reconstrução
    rebuilder = BlogRebuilder(base_dir)
    rebuilder.run_complete_rebuild()

if __name__ == "__main__":
    main()
