#!/usr/bin/env python3
"""
Script Principal de Build
=======================
Script principal para construção completa do site a partir de arquivos DOCX.

Uso:
    python build.py                    # Build completo
    python build.py --new-only         # Apenas novos artigos
    python build.py --status           # Status do sistema
    python build.py --validate         # Validar estrutura

Autor: Sistema Build
Data: Setembro 2025
"""

import argparse
import logging
import sys
from pathlib import Path

# Adicionar diretório do build system ao path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import *
from utils.file_manager import FileManager
from core.docx_converter import DocxConverter
from core.md_to_html import MarkdownToHtmlConverter
from core.site_builder import SiteBuilder

# Configurar logging
ensure_directories()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(BUILD_LOG, encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)

class BuildManager:
    """Gerenciador principal do processo de build."""
    
    def __init__(self):
        """Inicializa o gerenciador de build."""
        self.file_manager = FileManager()
        self.docx_converter = DocxConverter()
        self.md_converter = MarkdownToHtmlConverter()
        self.site_builder = SiteBuilder()
    
    def run_full_build(self, new_only=False, rebuild=False):
        """
        Executa build completo do site.
        
        Args:
            new_only (bool): Se True, processa apenas artigos novos
            rebuild (bool): Se True, reconstrói tudo do zero
        """
        logger.info("=" * 50)
        if rebuild:
            logger.info("RECONSTRUINDO SITE COMPLETO DO ZERO")
        else:
            logger.info("INICIANDO BUILD DO SITE")
        logger.info("=" * 50)
        
        try:
            # Se rebuild, limpa tudo primeiro
            if rebuild:
                logger.info("--- LIMPEZA COMPLETA ---")
                self._clean_all_generated_files()
            
            # 1. Coleta arquivos DOCX
            docx_files = self.file_manager.get_docx_files(new_only=new_only and not rebuild)
            
            if not docx_files:
                if new_only:
                    logger.info("Nenhum arquivo DOCX novo encontrado")
                else:
                    logger.warning("Nenhum arquivo DOCX encontrado")
                return True
            
            logger.info(f"Arquivos DOCX para processar: {len(docx_files)}")
            for docx_file in docx_files:
                logger.info(f"  - {docx_file.name}")
            
            # 2. Converte DOCX para Markdown
            logger.info("\n--- FASE 1: DOCX → MARKDOWN ---")
            docx_results = self.docx_converter.convert_batch(docx_files)
            
            if docx_results['failed']:
                logger.warning(f"Falhas na conversão DOCX: {len(docx_results['failed'])}")
                for failed in docx_results['failed']:
                    logger.warning(f"  - {failed.name}")
            
            if not docx_results['successful']:
                logger.error("Nenhuma conversão DOCX foi bem-sucedida")
                return False
            
            # 3. Prepara informações dos artigos
            articles_info = {}
            for result in docx_results['successful']:
                docx_file = result['docx']
                info = self.file_manager.get_article_info(docx_file)
                articles_info[info['normalized_name']] = info
                
                # Copia imagens se necessário
                self.file_manager.copy_images_to_assets(info)
            
            # 4. Converte Markdown para HTML
            logger.info("\n--- FASE 2: MARKDOWN → HTML ---")
            md_files = [result['md'] for result in docx_results['successful']]
            html_results = self.md_converter.convert_batch(md_files, articles_info)
            
            if html_results['failed']:
                logger.warning(f"Falhas na conversão HTML: {len(html_results['failed'])}")
            
            if not html_results['successful']:
                logger.error("Nenhuma conversão HTML foi bem-sucedida")
                return False
            
            # 5. Constrói estrutura do site
            logger.info("\n--- FASE 3: CONSTRUÇÃO DO SITE ---")
            site_success = self.site_builder.build_complete_site(articles_info)
            
            if not site_success:
                logger.error("Falha na construção do site")
                return False
            
            # 6. Atualiza lista de processados
            for info in articles_info.values():
                self.file_manager.mark_article_as_processed(info)
            
            # 7. Relatório final
            logger.info("\n" + "=" * 50)
            logger.info("BUILD CONCLUÍDO COM SUCESSO")
            logger.info("=" * 50)
            logger.info(f"DOCX processados: {len(docx_results['successful'])}")
            logger.info(f"HTML gerados: {len(html_results['successful'])}")
            logger.info(f"Site atualizado com índice")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro no build: {e}")
            return False
    
    def _clean_all_generated_files(self):
        """Limpa todos os arquivos gerados (MD, HTML, imagens)."""
        import shutil
        
        logger.info("Limpando arquivos Markdown...")
        if MD_DIR.exists():
            shutil.rmtree(MD_DIR)
        MD_DIR.mkdir(parents=True, exist_ok=True)
        
        logger.info("Limpando arquivos HTML...")
        if ARTICLES_DIR.exists():
            for html_file in ARTICLES_DIR.glob("*.html"):
                html_file.unlink()
        
        logger.info("Limpando imagens...")
        if IMG_DIR.exists():
            for img_file in IMG_DIR.glob("*"):
                if img_file.is_file() and img_file.name not in ['placeholder.png', 'foto_chri.jpg']:
                    img_file.unlink()
        
        logger.info("Limpando lista de processados...")
        if PROCESSED_LIST.exists():
            PROCESSED_LIST.unlink()
        
        # Recria arquivo vazio
        PROCESSED_LIST.touch()
        
        logger.info("Limpeza completa concluída!")
    
    def show_status(self):
        """Mostra status atual do sistema."""
        logger.info("=" * 50)
        logger.info("STATUS DO SISTEMA DE BUILD")
        logger.info("=" * 50)
        
        status = self.file_manager.get_build_status()
        
        logger.info(f"Total de arquivos DOCX: {status['total_docx']}")
        logger.info(f"Artigos processados: {status['processed_count']}")
        logger.info(f"Novos para processar: {status['new_docx']}")
        
        if status['new_files']:
            logger.info("\nArquivos novos encontrados:")
            for filename in status['new_files']:
                logger.info(f"  - {filename}")
        else:
            logger.info("\nTodos os arquivos já foram processados.")
    
    def validate_structure(self):
        """Valida a estrutura do sistema."""
        logger.info("=" * 50)
        logger.info("VALIDAÇÃO DA ESTRUTURA")
        logger.info("=" * 50)
        
        # Verifica diretórios
        directories = [DOCX_DIR, MD_DIR, ARTICLES_DIR, IMG_DIR, CSS_DIR, JS_DIR]
        missing_dirs = [d for d in directories if not d.exists()]
        
        if missing_dirs:
            logger.warning("Diretórios faltando:")
            for dir_path in missing_dirs:
                logger.warning(f"  - {dir_path}")
        else:
            logger.info("✓ Todos os diretórios necessários existem")
        
        # Verifica dependências
        if not self.docx_converter.check_pandoc_available():
            logger.error("✗ Pandoc não está disponível")
        else:
            logger.info("✓ Pandoc disponível")
        
        # Verifica arquivos CSS
        css_files = [CSS_DIR / 'main.css', CSS_DIR / 'article.css']
        missing_css = [f for f in css_files if not f.exists()]
        
        if missing_css:
            logger.warning("Arquivos CSS faltando:")
            for css_file in missing_css:
                logger.warning(f"  - {css_file}")
        else:
            logger.info("✓ Arquivos CSS encontrados")

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description='Sistema de Build do Site - Converte DOCX para HTML'
    )
    
    parser.add_argument(
        '--new-only', 
        action='store_true',
        help='Processa apenas artigos novos (não listados como processados)'
    )
    
    parser.add_argument(
        '--rebuild', 
        action='store_true',
        help='Reconstrói todo o site do zero (limpa tudo antes)'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Mostra status atual do sistema'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true', 
        help='Valida estrutura do sistema'
    )
    
    args = parser.parse_args()
    
    # Instancia gerenciador
    build_manager = BuildManager()
    
    # Executa ação solicitada
    if args.status:
        build_manager.show_status()
    elif args.validate:
        build_manager.validate_structure()
    else:
        success = build_manager.run_full_build(new_only=args.new_only, rebuild=args.rebuild)
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
