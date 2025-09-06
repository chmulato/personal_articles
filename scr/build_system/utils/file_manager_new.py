#!/usr/bin/env python3
"""
Gerenciador de Arquivos
=====================
Utilitários para operações com arquivos e diretórios.

Autor: Sistema Build
Data: Setembro 2025  
"""

import os
import shutil
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Adiciona o diretório build_system ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import *
from .normalizer import normalize_filename, extract_date_from_filename
from .processed_articles_manager import ProcessedArticlesManager

# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

class FileManager:
    """Gerenciador centralizado de operações com arquivos."""
    
    def __init__(self):
        """Inicializa o gerenciador de arquivos."""
        ensure_directories()
        self.processed_manager = ProcessedArticlesManager()
        
    def get_docx_files(self, new_only=False) -> List[Path]:
        """
        Retorna lista de arquivos DOCX.
        
        Args:
            new_only (bool): Se True, retorna apenas arquivos não processados
            
        Returns:
            List[Path]: Lista de arquivos DOCX
        """
        if not DOCX_DIR.exists():
            logger.warning(f"Diretório DOCX não encontrado: {DOCX_DIR}")
            return []
        
        if new_only:
            # Usa o gerenciador de processados para obter não processados
            return self.processed_manager.get_unprocessed_docx()
        else:
            # Busca todos os arquivos DOCX (exceto temporários)
            docx_files = [
                f for f in DOCX_DIR.glob("*.docx") 
                if not f.name.startswith("~")
            ]
            
            # Ordena por data (se disponível) ou nome
            docx_files.sort(key=lambda f: extract_date_from_filename(f.name) or f.name)
            
            return docx_files
    
    def get_article_info(self, docx_file: Path) -> Dict:
        """
        Extrai informações do artigo a partir do arquivo DOCX.
        
        Args:
            docx_file (Path): Caminho para o arquivo DOCX
            
        Returns:
            Dict: Informações do artigo
        """
        from .normalizer import extract_title_from_filename, extract_date_from_filename
        
        info = {
            'docx_file': docx_file,
            'normalized_name': normalize_filename(docx_file.stem),
            'title': extract_title_from_filename(docx_file.name),
            'date_info': extract_date_from_filename(docx_file.name),
            'md_file': MD_DIR / f"{docx_file.stem}.md",
            'html_file': ARTICLES_DIR / f"{normalize_filename(docx_file.stem)}.html"
        }
        
        # Formatação de data
        if info['date_info']:
            year, month, day = info['date_info']
            info['date_iso'] = f"{year:04d}-{month:02d}-{day:02d}"
            info['date_formatted'] = f"{day:02d}/{month:02d}/{year}"
        else:
            # Usa data de modificação do arquivo como fallback
            mtime = datetime.fromtimestamp(docx_file.stat().st_mtime)
            info['date_iso'] = mtime.strftime("%Y-%m-%d")
            info['date_formatted'] = mtime.strftime("%d/%m/%Y")
        
        return info
    
    def mark_article_as_processed(self, article_info: Dict):
        """
        Marca artigo como processado na lista de controle.
        
        Args:
            article_info (Dict): Informações do artigo
        """
        self.processed_manager.add_processed_article(article_info['normalized_name'])
        logger.info(f"Artigo marcado como processado: {article_info['normalized_name']}")
    
    def cleanup_temp_files(self):
        """Remove arquivos temporários gerados durante o processo."""
        temp_dirs = ['temp_media', 'media']
        
        for temp_dir in temp_dirs:
            temp_path = PROJECT_ROOT / temp_dir
            if temp_path.exists():
                try:
                    shutil.rmtree(temp_path)
                    logger.info(f"Removido diretório temporário: {temp_path}")
                except Exception as e:
                    logger.warning(f"Erro ao remover {temp_path}: {e}")
    
    def copy_images_to_assets(self, article_info: Dict):
        """
        Copia imagens do artigo para o diretório assets.
        
        Args:
            article_info (Dict): Informações do artigo
        """
        # Procura por imagens na pasta temp_media (gerada pelo pandoc)
        temp_media = PROJECT_ROOT / 'temp_media'
        if not temp_media.exists():
            return
        
        normalized_name = article_info['normalized_name']
        
        # Busca imagens no diretório temporário
        image_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif']:
            image_files.extend(temp_media.glob(f"**/{ext}"))
        
        # Copia imagens renomeando adequadamente
        for i, img_file in enumerate(image_files, 1):
            # Determina extensão apropriada
            if i == len(image_files):  # Última imagem é sempre a foto do autor
                new_name = f"{normalized_name}_image{i}.jpg"
            else:
                new_name = f"{normalized_name}_image{i}{img_file.suffix}"
            
            dest_path = IMG_DIR / new_name
            
            try:
                shutil.copy2(img_file, dest_path)
                logger.info(f"Imagem copiada: {img_file.name} → {new_name}")
            except Exception as e:
                logger.warning(f"Erro ao copiar imagem {img_file}: {e}")
    
    def validate_article_structure(self, article_info: Dict) -> bool:
        """
        Valida se o artigo tem todos os arquivos necessários.
        
        Args:
            article_info (Dict): Informações do artigo
            
        Returns:
            bool: True se válido, False caso contrário
        """
        required_files = [
            article_info['html_file']
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                logger.warning(f"Arquivo necessário não encontrado: {file_path}")
                return False
        
        return True
    
    def get_build_status(self) -> Dict:
        """
        Retorna status atual do build.
        
        Returns:
            Dict: Informações de status
        """
        all_docx = self.get_docx_files(new_only=False)
        new_docx = self.get_docx_files(new_only=True)
        processed = self.processed_manager.load_processed_list()
        
        return {
            'total_docx': len(all_docx),
            'new_docx': len(new_docx),
            'processed_count': len(processed),
            'new_files': [f.name for f in new_docx]
        }
