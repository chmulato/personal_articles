#!/usr/bin/env python3
"""
Conversor Markdown para HTML
===========================
Converte arquivos Markdown para HTML com formatação profissional.

Autor: Sistema Build
Data: Setembro 2025
"""

import re
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

import sys
from pathlib import Path

# Adiciona o diretório build_system ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import markdown
    from markdown.extensions import codehilite, tables, toc
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

from config.settings import *
from utils.normalizer import extract_title_from_filename

logger = logging.getLogger(__name__)

class MarkdownToHtmlConverter:
    """Conversor de Markdown para HTML."""
    
    def __init__(self):
        """Inicializa o conversor."""
        if not MARKDOWN_AVAILABLE:
            logger.error("Biblioteca markdown não encontrada. Instale: pip install markdown pygments")
            
        # Configurar Markdown com extensões
        self.md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
    
    def extract_frontmatter(self, content: str) -> tuple:
        """
        Extrai frontmatter YAML do conteúdo Markdown.
        
        Args:
            content (str): Conteúdo Markdown
            
        Returns:
            tuple: (frontmatter_dict, content_without_frontmatter)
        """
        if not content.startswith('---'):
            return {}, content
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content
        
        frontmatter_text = parts[1].strip()
        content_text = parts[2].strip()
        
        # Parse básico do frontmatter
        frontmatter = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                
                # Processar tags como lista
                if key == 'tags' and value.startswith('['):
                    value = value.strip('[]').replace("'", "").split(', ')
                
                frontmatter[key] = value
        
        return frontmatter, content_text
    
    def process_markdown_content(self, content: str) -> str:
        """
        Processa conteúdo Markdown e aplica melhorias.
        
        Args:
            content (str): Conteúdo Markdown
            
        Returns:
            str: Conteúdo processado
        """
        # Corrige formatação de código
        content = self._fix_code_blocks(content)
        
        # Processa imagens
        content = self._process_images(content)
        
        # Melhora formatação de listas
        content = self._improve_lists(content)
        
        return content
    
    def _fix_code_blocks(self, content: str) -> str:
        """Corrige formatação de blocos de código."""
        # Padroniza blocos de código com linguagem
        content = re.sub(
            r'```(\w+)\n(.*?)```', 
            r'```\1\n\2\n```', 
            content, 
            flags=re.DOTALL
        )
        
        # Garante quebras de linha adequadas antes/depois de código
        content = re.sub(r'\n```', r'\n\n```', content)
        content = re.sub(r'```\n', r'```\n\n', content)
        
        return content
    
    def _process_images(self, content: str) -> str:
        """Processa referências de imagens."""
        # Atualiza caminhos de imagem para assets
        content = re.sub(
            r'!\[(.*?)\]\((.*?)\)',
            lambda m: self._fix_image_path(m.group(1), m.group(2)),
            content
        )
        
        return content
    
    def _fix_image_path(self, alt_text: str, img_path: str) -> str:
        """Corrige caminho da imagem."""
        # Se já é um caminho relativo para assets, mantém
        if img_path.startswith('assets/'):
            return f'![{alt_text}]({img_path})'
        
        # Se é um nome de arquivo simples, assume que está em assets/img
        if '/' not in img_path and not img_path.startswith('http'):
            return f'![{alt_text}](assets/img/{img_path})'
        
        # Mantém URLs externos
        return f'![{alt_text}]({img_path})'
    
    def _improve_lists(self, content: str) -> str:
        """Melhora formatação de listas."""
        # Garante espaçamento adequado antes de listas
        content = re.sub(r'\n([*-]) ', r'\n\n\1 ', content)
        
        return content
    
    def fix_html_image_paths(self, html_content: str, article_filename: str) -> str:
        """
        Corrige os caminhos das imagens no HTML gerado.
        
        Args:
            html_content (str): Conteúdo HTML
            article_filename (str): Nome do arquivo do artigo (sem extensão)
            
        Returns:
            str: HTML com caminhos de imagem corrigidos
        """
        # Extrair data do nome do arquivo
        date_match = re.search(r'(\d{4})_(\d{2})_(\d{2})', article_filename)
        if not date_match:
            logger.warning(f"Não foi possível extrair data de {article_filename}")
            return html_content
            
        year, month, day = date_match.groups()
        date_prefix = f"{year}_{month}_{day}"
        
        # Padrão para encontrar imagens temp_media
        temp_media_pattern = r'src="temp_media[/\\][^"]*?[/\\]assets[/\\]img[/\\](\d{4}_\d{2}_\d{2}_IMAGE_\d{3}\.\w+)"'
        
        def replace_image_path(match):
            image_name = match.group(1)
            new_path = f'assets/img/{image_name}'
            logger.debug(f"Corrigindo caminho da imagem: {match.group(0)} → src=\"{new_path}\"")
            return f'src="{new_path}"'
        
        # Substituir os caminhos das imagens
        corrected_html = re.sub(temp_media_pattern, replace_image_path, html_content)
        
        # Também corrigir variações com barras normais
        temp_media_pattern2 = r'src="temp_media/[^"]*/assets/img/(\d{4}_\d{2}_\d{2}_IMAGE_\d{3}\.\w+)"'
        corrected_html = re.sub(temp_media_pattern2, replace_image_path, corrected_html)
        
        return corrected_html
    
    def generate_article_metadata(self, article_info: Dict, frontmatter: Dict) -> Dict:
        """
        Gera metadados completos para o artigo.
        
        Args:
            article_info (Dict): Informações básicas do artigo
            frontmatter (Dict): Frontmatter extraído do Markdown
            
        Returns:
            Dict: Metadados completos
        """
        metadata = SITE_CONFIG.copy()
        metadata.update({
            'title': frontmatter.get('title', article_info['title']),
            'description': frontmatter.get('description', f"Artigo sobre {article_info['title']}"),
            'keywords': ', '.join(frontmatter.get('tags', ['Java', 'Desenvolvimento', 'Tecnologia'])),
            'date_iso': article_info['date_iso'],
            'date_formatted': article_info['date_formatted'],
            'author_image': f"{article_info['normalized_name']}_image{self._count_images(article_info)}.jpg"
        })
        
        return metadata
    
    def _count_images(self, article_info: Dict) -> int:
        """Conta quantas imagens o artigo possui."""
        img_pattern = f"{article_info['normalized_name']}_image*.png"
        img_files = list(IMG_DIR.glob(img_pattern))
        return len(img_files) + 1  # +1 para a imagem do autor (sempre a última)
    
    def _generate_featured_image_html(self, article_info: Dict) -> str:
        """Gera HTML para imagem destacada."""
        img_name = f"{article_info['normalized_name']}_image1.png"
        img_path = IMG_DIR / img_name
        
        if img_path.exists():
            return f'''
            <div class="featured-image">
                <img src="assets/img/{img_name}" alt="{article_info['title']}" class="img-responsive">
            </div>'''
        
        return ''
    
    def convert_to_html(self, md_file: Path, article_info: Dict) -> Optional[Path]:
        """
        Converte arquivo Markdown para HTML.
        
        Args:
            md_file (Path): Caminho para o arquivo MD
            article_info (Dict): Informações do artigo
            
        Returns:
            Optional[Path]: Caminho para o arquivo HTML gerado
        """
        if not MARKDOWN_AVAILABLE:
            logger.error("Markdown não disponível")
            return None
        
        try:
            # Lê conteúdo do arquivo Markdown
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrai frontmatter
            frontmatter, content = self.extract_frontmatter(content)
            
            # Processa conteúdo
            content = self.process_markdown_content(content)
            
            # Converte para HTML
            html_content = self.md.convert(content)
            
            # Gera metadados
            metadata = self.generate_article_metadata(article_info, frontmatter)
            
            # Gera imagem destacada
            featured_image = self._generate_featured_image_html(article_info)
            metadata['featured_image'] = featured_image
            
            # Aplica template
            full_html = HTML_TEMPLATE.format(
                content=html_content,
                **metadata
            )
            
            # Corrige caminhos das imagens no HTML gerado
            full_html = self.fix_html_image_paths(full_html, md_file.stem)
            
            # Salva arquivo HTML
            html_file = article_info['html_file']
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            logger.info(f"HTML gerado: {html_file.name}")
            return html_file
            
        except Exception as e:
            logger.error(f"Erro na conversão MD→HTML: {e}")
            return None
    
    def convert_batch(self, md_files: list, articles_info: Dict) -> dict:
        """
        Converte múltiplos arquivos Markdown.
        
        Args:
            md_files (list): Lista de arquivos MD
            articles_info (Dict): Informações dos artigos
            
        Returns:
            dict: Resultados da conversão
        """
        results = {
            'successful': [],
            'failed': [],
            'total': len(md_files)
        }
        
        for md_file in md_files:
            # Encontra informações do artigo correspondente
            article_key = md_file.stem
            article_info = None
            
            for info in articles_info.values():
                if info['md_file'] == md_file:
                    article_info = info
                    break
            
            if not article_info:
                logger.warning(f"Informações não encontradas para: {md_file}")
                results['failed'].append(md_file)
                continue
            
            html_file = self.convert_to_html(md_file, article_info)
            
            if html_file:
                results['successful'].append({
                    'md': md_file,
                    'html': html_file
                })
            else:
                results['failed'].append(md_file)
        
        return results
    
    def convert_markdown_to_html(self, md_file_path: str) -> bool:
        """
        Converte um arquivo Markdown para HTML com correção automática de imagens.
        
        Args:
            md_file_path (str): Caminho para o arquivo MD
            
        Returns:
            bool: True se a conversão foi bem-sucedida
        """
        try:
            md_file = Path(md_file_path)
            if not md_file.exists():
                logger.error(f"Arquivo MD não encontrado: {md_file}")
                return False
            
            # Extrair informações básicas do arquivo
            filename_stem = md_file.stem
            
            # Criar informações básicas do artigo
            article_info = {
                'title': extract_title_from_filename(filename_stem),
                'date_iso': '2024-01-01',  # Data padrão, será extraída do nome
                'date_formatted': '1 de Janeiro de 2024',
                'normalized_name': filename_stem,
                'html_file': ARTICLES_DIR / f"{filename_stem}.html",
                'md_file': md_file
            }
            
            # Extrair data do nome do arquivo se possível
            date_match = re.search(r'(\d{4})_(\d{2})_(\d{2})', filename_stem)
            if date_match:
                year, month, day = date_match.groups()
                try:
                    date_obj = datetime(int(year), int(month), int(day))
                    article_info['date_iso'] = date_obj.strftime('%Y-%m-%d')
                    article_info['date_formatted'] = date_obj.strftime('%d de %B de %Y')
                except:
                    pass
            
            # Converter usando o método principal
            html_file = self.convert_to_html(md_file, article_info)
            
            if html_file:
                logger.info(f"Conversão bem-sucedida: {filename_stem}")
                return True
            else:
                logger.error(f"Falha na conversão: {filename_stem}")
                return False
                
        except Exception as e:
            logger.error(f"Erro na conversão MD→HTML para {md_file_path}: {e}")
            return False
