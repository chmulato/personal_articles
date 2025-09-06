#!/usr/bin/env python3
"""
Conversor DOCX para Markdown
===========================
Converte arquivos DOCX para Markdown usando Pandoc.

Autor: Sistema Build
Data: Setembro 2025
"""

import subprocess
import logging
import shutil
import re
from pathlib import Path
from typing import Optional

import sys
from pathlib import Path

# Adiciona o diretório build_system ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import *
from utils.file_manager import FileManager

logger = logging.getLogger(__name__)

class DocxConverter:
    """Conversor de arquivos DOCX para Markdown."""
    
    def __init__(self):
        """Inicializa o conversor."""
        self.file_manager = FileManager()
        
    def check_pandoc_available(self) -> bool:
        """
        Verifica se o Pandoc está disponível no sistema.
        
        Returns:
            bool: True se Pandoc estiver disponível
        """
        try:
            result = subprocess.run(['pandoc', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def convert_to_markdown(self, docx_file: Path) -> Optional[Path]:
        """
        Converte arquivo DOCX para Markdown.
        
        Args:
            docx_file (Path): Caminho para o arquivo DOCX
            
        Returns:
            Optional[Path]: Caminho para o arquivo MD gerado ou None se falhou
        """
        if not self.check_pandoc_available():
            logger.error("Pandoc não encontrado. Instale pandoc para continuar.")
            return None
        
        md_file = MD_DIR / f"{docx_file.stem}.md"
        
        # Cria diretório temporário específico para este artigo
        temp_media_dir = Path("temp_media") / docx_file.stem
        temp_media_dir.mkdir(parents=True, exist_ok=True)
        
        # Comando pandoc com opções otimizadas
        cmd = [
            'pandoc',
            str(docx_file),
            '-o', str(md_file),
            '--wrap=none',
            f'--extract-media={temp_media_dir}'
        ]
        
        try:
            logger.info(f"Convertendo: {docx_file.name} → {md_file.name}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if md_file.exists() and md_file.stat().st_size > 0:
                    # Processa e renomeia as imagens extraídas
                    self._process_extracted_images(docx_file.stem, temp_media_dir, md_file)
                    logger.info(f"Conversão bem-sucedida: {md_file.name}")
                    return md_file
                else:
                    logger.error(f"Arquivo MD vazio ou não criado: {md_file}")
                    return None
            else:
                logger.error(f"Erro no pandoc: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Erro na conversão DOCX→MD: {e}")
            return None
    
    def post_process_markdown(self, md_file: Path) -> bool:
        """
        Pós-processa o arquivo Markdown para melhorar formatação.
        
        Args:
            md_file (Path): Caminho para o arquivo MD
            
        Returns:
            bool: True se processamento foi bem-sucedido
        """
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Correções básicas de formatação
            content = self._fix_markdown_formatting(content)
            
            # Salva conteúdo processado
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"Pós-processamento concluído: {md_file.name}")
            return True
            
        except Exception as e:
            logger.error(f"Erro no pós-processamento: {e}")
            return False
    
    def _process_extracted_images(self, article_stem: str, temp_media_dir: Path, md_file: Path):
        """
        Processa e renomeia imagens extraídas seguindo o padrão YYYY_MM_DD_IMAGE_00X
        
        Args:
            article_stem (str): Nome base do artigo (ex: 2025_09_07_decisoes_tecnicas...)
            temp_media_dir (Path): Diretório temporário das imagens
            md_file (Path): Arquivo markdown para atualizar referências
        """
        import re
        import shutil
        
        # Extrai a data do nome do arquivo (assume formato YYYY_MM_DD_...)
        date_match = re.match(r'(\d{4}_\d{2}_\d{2})', article_stem)
        if not date_match:
            logger.warning(f"Não foi possível extrair data de: {article_stem}")
            return
        
        date_prefix = date_match.group(1)
        
        # Procura por imagens extraídas
        media_subdir = temp_media_dir / "media"
        if not media_subdir.exists():
            logger.info(f"Nenhuma imagem encontrada para: {article_stem}")
            return
        
        # Lista todas as imagens
        image_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']:
            image_files.extend(media_subdir.glob(ext))
        
        if not image_files:
            logger.info(f"Nenhuma imagem encontrada para: {article_stem}")
            return
        
        # Ordena por nome para consistência
        image_files.sort()
        
        # Lê o conteúdo do markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Renomeia e move imagens
        for i, img_file in enumerate(image_files, 1):
            # Nome novo seguindo padrão YYYY_MM_DD_IMAGE_001
            new_name = f"{date_prefix}_IMAGE_{i:03d}{img_file.suffix}"
            final_path = IMG_DIR / new_name
            
            # Cria diretório se não existir
            final_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Move a imagem
            shutil.copy2(img_file, final_path)
            logger.info(f"Imagem renomeada: {img_file.name} → {new_name}")
            
            # Atualiza referências no markdown
            old_ref = f"temp_media\\{article_stem}\\media\\{img_file.name}"
            new_ref = f"assets/img/{new_name}"
            md_content = md_content.replace(old_ref, new_ref)
            
            # Tenta também outros possíveis padrões de referência
            old_ref2 = f"media/{img_file.name}"
            md_content = md_content.replace(old_ref2, new_ref)
        
        # Salva o markdown atualizado
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.info(f"Processadas {len(image_files)} imagens para {article_stem}")

    def _fix_markdown_formatting(self, content: str) -> str:
        """
        Aplica correções de formatação no conteúdo Markdown.
        
        Args:
            content (str): Conteúdo original
            
        Returns:
            str: Conteúdo corrigido
        """
        import re
        
        # Remove linhas vazias excessivas
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Corrige formatação de código inline
        content = re.sub(r'`([^`]+)`', r'`\1`', content)
        
        # Corrige formatação de blocos de código
        content = re.sub(r'```(\w+)?\n', r'```\1\n', content)
        
        # Remove espaços em branco no final das linhas
        content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
        
        # Garante quebra de linha no final do arquivo
        if not content.endswith('\n'):
            content += '\n'
        
        return content
    
    def convert_batch(self, docx_files: list) -> dict:
        """
        Converte múltiplos arquivos DOCX.
        
        Args:
            docx_files (list): Lista de arquivos DOCX
            
        Returns:
            dict: Resultados da conversão
        """
        results = {
            'successful': [],
            'failed': [],
            'total': len(docx_files)
        }
        
        for docx_file in docx_files:
            md_file = self.convert_to_markdown(docx_file)
            
            if md_file:
                # Pós-processa o arquivo
                if self.post_process_markdown(md_file):
                    results['successful'].append({
                        'docx': docx_file,
                        'md': md_file
                    })
                else:
                    results['failed'].append(docx_file)
            else:
                results['failed'].append(docx_file)
        
        # Limpeza de arquivos temporários
        self.file_manager.cleanup_temp_files()
        
        return results
