#!/usr/bin/env python3
"""
Configurações Centralizadas do Sistema de Build
=============================================
Todas as configurações e caminhos do sistema em um local centralizado.

Autor: Sistema Build
Data: Setembro 2025
"""

from pathlib import Path
import os

# === DIRETÓRIOS PRINCIPAIS ===
PROJECT_ROOT = Path("c:/dev/personal_articles")
DOCX_DIR = PROJECT_ROOT / "docx"
MD_DIR = PROJECT_ROOT / "md"
ARTICLES_DIR = PROJECT_ROOT / "articles"
SCR_DIR = PROJECT_ROOT / "scr"

# Diretórios de assets
ASSETS_DIR = ARTICLES_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img" 
CSS_DIR = ASSETS_DIR / "css"
JS_DIR = ASSETS_DIR / "js"

# === ARQUIVOS DE CONTROLE ===
BUILD_SYSTEM_DIR = SCR_DIR / "build_system"
PROCESSED_LIST = BUILD_SYSTEM_DIR / "processed_articles.txt"
BUILD_LOG = BUILD_SYSTEM_DIR / "build.log"

# === CONFIGURAÇÕES DE CONVERSÃO ===
PANDOC_OPTIONS = [
    "--wrap=none",
    "--extract-media=temp_media"
]

MARKDOWN_EXTENSIONS = [
    'codehilite',
    'tables', 
    'toc',
    'fenced_code',
    'nl2br'
]

# === CONFIGURAÇÕES DO SITE ===
SITE_CONFIG = {
    "site_name": "Christian Mulato Dev Blog",
    "site_description": "Artigos técnicos sobre desenvolvimento Java, arquitetura de software e tecnologia",
    "author": "Christian Mulato",
    "base_url": "",  # Para URLs relativas
    "language": "pt-BR",
    "charset": "utf-8"
}

# === TEMPLATES HTML ===
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="{language}">
<head>
    <meta charset="{charset}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {site_name}</title>
    <meta name="description" content="{description}">
    <meta name="author" content="{author}">
    <meta name="keywords" content="{keywords}">
    
    <!-- CSS -->
    <link rel="stylesheet" href="assets/css/main.css">
    <link rel="stylesheet" href="assets/css/article.css">
    <link rel="stylesheet" href="assets/css/highlight.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <h1><a href="index.html">{site_name}</a></h1>
            <nav class="main-nav">
                <a href="index.html">Início</a>
                <a href="#sobre">Sobre</a>
            </nav>
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            <article class="post">
                <header class="post-header">
                    <h1 class="post-title">{title}</h1>
                    <div class="post-meta">
                        <time datetime="{date_iso}">{date_formatted}</time>
                        <span class="post-author">Por {author}</span>
                    </div>
                    {featured_image}
                </header>
                
                <div class="post-content">
                    {content}
                </div>
                
                <footer class="post-footer">
                    <div class="author-info">
                        <img src="assets/img/{author_image}" alt="{author}" class="author-avatar">
                        <div class="author-details">
                            <strong>{author}</strong>
                            <p>Desenvolvedor Java e Arquiteto de Software</p>
                        </div>
                    </div>
                </footer>
            </article>
        </div>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; 2025 {author}. Todos os direitos reservados.</p>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="assets/js/main.js"></script>
</body>
</html>"""

# === CONFIGURAÇÕES DE LOG ===
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# === FUNÇÕES DE UTILIDADE ===
def ensure_directories():
    """Garante que todos os diretórios necessários existam."""
    directories = [
        MD_DIR, ARTICLES_DIR, ASSETS_DIR, IMG_DIR, 
        CSS_DIR, JS_DIR, BUILD_SYSTEM_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        
def get_processed_articles():
    """Carrega lista de artigos processados."""
    processed = set()
    if PROCESSED_LIST.exists():
        with open(PROCESSED_LIST, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    processed.add(line)
    return processed

def add_to_processed(article_name):
    """Adiciona artigo à lista de processados."""
    with open(PROCESSED_LIST, 'a', encoding='utf-8') as f:
        f.write(f"{article_name}\n")
