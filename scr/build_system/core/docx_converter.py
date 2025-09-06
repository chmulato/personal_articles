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
        
        # Comando pandoc com opções otimizadas
        cmd = [
            'pandoc',
            str(docx_file),
            '-o', str(md_file),
            *PANDOC_OPTIONS
        ]
        
        try:
            logger.info(f"Convertendo: {docx_file.name} → {md_file.name}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if md_file.exists() and md_file.stat().st_size > 0:
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
