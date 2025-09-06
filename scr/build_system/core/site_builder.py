#!/usr/bin/env python3
"""
Construtor do Site
================
Constrói a estrutura final do site com índice e navegação.

Autor: Sistema Build
Data: Setembro 2025
"""

import sys
from pathlib import Path

# Adiciona o diretório build_system ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import logging
from datetime import datetime
from typing import List, Dict

from config.settings import *
from utils.file_manager import FileManager
from utils.normalizer import extract_date_from_filename

logger = logging.getLogger(__name__)

class SiteBuilder:
    """Construtor da estrutura final do site."""
    
    def __init__(self):
        """Inicializa o construtor do site."""
        self.file_manager = FileManager()
    
    def collect_articles_metadata(self) -> List[Dict]:
        """
        Coleta metadados de todos os artigos HTML.
        
        Returns:
            List[Dict]: Lista de metadados dos artigos
        """
        articles = []
        html_files = ARTICLES_DIR.glob("*.html")
        
        for html_file in html_files:
            if html_file.name == 'index.html':
                continue
                
            metadata = self._extract_metadata_from_html(html_file)
            if metadata:
                articles.append(metadata)
        
        # Ordena por data (mais recentes primeiro)
        articles.sort(key=lambda x: x.get('date_iso') or '0000-00-00', reverse=True)
        
        return articles
    
    def _extract_metadata_from_html(self, html_file: Path) -> Dict:
        """
        Extrai metadados de um arquivo HTML.
        
        Args:
            html_file (Path): Caminho para o arquivo HTML
            
        Returns:
            Dict: Metadados extraídos
        """
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            import re
            
            # Extrai título
            title_match = re.search(r'<h1 class="post-title">(.*?)</h1>', content, re.DOTALL)
            title = title_match.group(1).strip() if title_match else html_file.stem
            
            # Extrai data
            date_match = re.search(r'<time datetime="([^"]+)">', content)
            date_iso = date_match.group(1) if date_match else None
            
            # Extrai descrição do meta tag
            desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
            description = desc_match.group(1) if desc_match else f"Artigo sobre {title}"
            
            # Extrai palavras-chave
            keywords_match = re.search(r'<meta name="keywords" content="([^"]+)"', content)
            keywords = keywords_match.group(1).split(', ') if keywords_match else []
            
            # Extrai imagem destacada
            img_match = re.search(r'<img src="assets/img/([^"]+)"[^>]*class="img-responsive"', content)
            featured_image = img_match.group(1) if img_match else None
            
            # Informações de data formatada
            date_formatted = None
            if date_iso:
                try:
                    date_obj = datetime.fromisoformat(date_iso)
                    date_formatted = date_obj.strftime("%d/%m/%Y")
                except:
                    pass
            
            return {
                'filename': html_file.name,
                'title': title,
                'description': description,
                'date_iso': date_iso,
                'date_formatted': date_formatted,
                'keywords': keywords,
                'featured_image': featured_image,
                'url': html_file.name
            }
            
        except Exception as e:
            logger.warning(f"Erro ao extrair metadados de {html_file}: {e}")
            return None
    
    def generate_index_html(self, articles: List[Dict]) -> bool:
        """
        Gera o arquivo index.html principal.
        
        Args:
            articles (List[Dict]): Lista de artigos
            
        Returns:
            bool: True se gerado com sucesso
        """
        try:
            # Template do índice
            index_template = self._get_index_template()
            
            # Gera lista de artigos
            articles_html = self._generate_articles_list_html(articles)
            
            # Dados para o template
            template_data = SITE_CONFIG.copy()
            template_data.update({
                'title': 'Início',
                'articles_list': articles_html,
                'total_articles': len(articles),
                'latest_article': articles[0] if articles else None
            })
            
            # Aplica template
            index_content = index_template.format(**template_data)
            
            # Salva arquivo
            index_file = ARTICLES_DIR / 'index.html'
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            logger.info(f"Índice gerado: {len(articles)} artigos listados")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar índice: {e}")
            return False
    
    def _generate_articles_list_html(self, articles: List[Dict]) -> str:
        """Gera HTML da lista de artigos."""
        if not articles:
            return '<p>Nenhum artigo encontrado.</p>'
        
        html_parts = ['<div class="articles-grid">']
        
        for article in articles:
            article_html = f'''
            <article class="article-card">
                {self._get_article_image_html(article)}
                <div class="article-content">
                    <h2><a href="{article['url']}">{article['title']}</a></h2>
                    <div class="article-meta">
                        <time datetime="{article['date_iso']}">{article['date_formatted']}</time>
                    </div>
                    <p class="article-excerpt">{article['description']}</p>
                    <div class="article-tags">
                        {self._get_tags_html(article['keywords'])}
                    </div>
                </div>
            </article>'''
            
            html_parts.append(article_html)
        
        html_parts.append('</div>')
        
        return '\n'.join(html_parts)
    
    def _get_article_image_html(self, article: Dict) -> str:
        """Gera HTML da imagem do artigo."""
        if article.get('featured_image'):
            return f'''
            <div class="article-image">
                <a href="{article['url']}">
                    <img src="assets/img/{article['featured_image']}" alt="{article['title']}" class="img-responsive">
                </a>
            </div>'''
        
        return '<div class="article-image-placeholder"></div>'
    
    def _get_tags_html(self, keywords: List[str]) -> str:
        """Gera HTML das tags."""
        if not keywords:
            return ''
        
        tags_html = []
        for keyword in keywords[:5]:  # Máximo 5 tags
            tags_html.append(f'<span class="tag">{keyword}</span>')
        
        return ' '.join(tags_html)
    
    def _get_index_template(self) -> str:
        """Retorna template do índice."""
        return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_name} - {site_description}</title>
    <meta name="description" content="{site_description}">
    <meta name="author" content="{author}">
    
    <!-- CSS -->
    <link rel="stylesheet" href="assets/css/main.css">
    <link rel="stylesheet" href="assets/css/article.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <h1><a href="index.html">{site_name}</a></h1>
            <nav class="main-nav">
                <a href="index.html" class="active">Início</a>
                <a href="#sobre">Sobre</a>
            </nav>
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            <section class="hero">
                <h2>Artigos Técnicos</h2>
                <p>{site_description}</p>
                <div class="stats">
                    <span class="stat-item">{total_articles} Artigos Publicados</span>
                </div>
            </section>
            
            <section class="articles-section">
                {articles_list}
            </section>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2025 {author}. Todos os direitos reservados.</p>
        </div>
    </footer>

    <script src="assets/js/main.js"></script>
</body>
</html>'''
    
    def copy_essential_assets(self) -> bool:
        """
        Copia arquivos CSS/JS essenciais se não existirem.
        
        Returns:
            bool: True se operação foi bem-sucedida
        """
        try:
            # Verifica se CSS existe
            main_css = CSS_DIR / 'main.css'
            article_css = CSS_DIR / 'article.css'
            
            if not main_css.exists() or not article_css.exists():
                logger.info("Arquivos CSS não encontrados - usando CSS padrão do sistema")
                # Os arquivos já existem no sistema, não precisa criar novos
            
            # Cria JS básico se não existir
            main_js = JS_DIR / 'main.js'
            if not main_js.exists():
                basic_js = '''// JavaScript básico para o site
document.addEventListener('DOMContentLoaded', function() {
    console.log('Site carregado com sucesso');
});'''
                
                with open(main_js, 'w', encoding='utf-8') as f:
                    f.write(basic_js)
                
                logger.info("Arquivo main.js criado")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao copiar assets: {e}")
            return False
    
    def build_complete_site(self, articles_info: Dict = None) -> bool:
        """
        Constrói o site completo.
        
        Args:
            articles_info (Dict): Informações dos artigos (opcional)
            
        Returns:
            bool: True se build foi bem-sucedido
        """
        try:
            # Coleta metadados dos artigos
            articles = self.collect_articles_metadata()
            
            # Copia assets essenciais
            self.copy_essential_assets()
            
            # Gera índice
            success = self.generate_index_html(articles)
            
            if success:
                logger.info(f"Site construído com sucesso: {len(articles)} artigos")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro no build do site: {e}")
            return False
