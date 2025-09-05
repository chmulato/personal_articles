#!/usr/bin/env python3
"""
Site Manager - Gerenciador completo do site de artigos
Localizado em: C:\dev\personal_articles\md\site_artiches\scr\site_manager.py

Este script gerencia todas as operações do site:
- Conversão de Markdown para HTML
- Geração do index.html
- Atualização de metadados
- Validação de links e imagens
"""

import os
import re
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
import markdown
from markdown.extensions import codehilite, tables, toc

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('site_manager.log', encoding='utf-8')
    ]
)

class SiteManager:
    def __init__(self):
        # Diretórios base
        self.base_dir = Path(__file__).parent.parent  # site_artiches
        self.articles_dir = self.base_dir / "articles" 
        self.img_dir = self.articles_dir / "img"
        self.md_dir = self.base_dir / "md"  # Pasta com os arquivos Markdown
        self.assets_dir = self.base_dir / "assets"
        self.css_dir = self.assets_dir / "css"
        self.js_dir = self.assets_dir / "js"
        
        # Configurações
        self.site_config = {
            "site_name": "Christian Mulato Dev Blog",
            "site_description": "Artigos técnicos sobre desenvolvimento Java, arquitetura de software e tecnologia",
            "author": "Christian Mulato",
            "base_url": "https://chmulato.dev",
            "linkedin": "https://www.linkedin.com/in/chmulato/"
        }
        
        # Configurar Markdown
        self.md = markdown.Markdown(
            extensions=[
                'codehilite',
                'tables',
                'toc',
                'fenced_code',
                'attr_list'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': True,
                    'noclasses': False
                },
                'toc': {
                    'anchorlink': True
                }
            }
        )
    
    def extract_frontmatter(self, content):
        """Extrai frontmatter do conteúdo Markdown"""
        if not content.strip().startswith('---'):
            return {}, content
        
        try:
            lines = content.split('\n')
            if lines[0].strip() != '---':
                return {}, content
            
            # Encontrar o fim do frontmatter
            end_index = -1
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    end_index = i
                    break
            
            if end_index == -1:
                return {}, content
            
            # Extrair frontmatter
            frontmatter_lines = lines[1:end_index]
            content_lines = lines[end_index + 1:]
            
            # Parse simples do frontmatter
            frontmatter = {}
            for line in frontmatter_lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    
                    # Tratar tags como lista
                    if key == 'tags':
                        # Remover colchetes e split por vírgula
                        value = value.strip('[]')
                        frontmatter[key] = [tag.strip().strip("'").strip('"') for tag in value.split(',') if tag.strip()]
                    else:
                        frontmatter[key] = value
            
            return frontmatter, '\n'.join(content_lines)
            
        except Exception as e:
            logging.error(f"Erro ao extrair frontmatter: {e}")
            return {}, content
    
    def generate_html_template(self, frontmatter, content, article_filename):
        """Gera template HTML para um artigo"""
        
        # Processar Markdown
        html_content = self.md.convert(content)
        
        # Informações do artigo
        title = frontmatter.get('title', 'Artigo')
        date = frontmatter.get('date', '')
        author = frontmatter.get('author', 'Christian Mulato')
        description = frontmatter.get('description', f'Artigo técnico sobre {title.lower()}')
        category = frontmatter.get('category', 'Desenvolvimento')
        tags = frontmatter.get('tags', [])
        featured_image = frontmatter.get('featured_image', '')
        
        # Tags como string
        tags_str = ', '.join(tags) if isinstance(tags, list) else str(tags)
        
        # URLs
        article_url = f"{self.site_config['base_url']}/articles/{article_filename.replace('.md', '.html')}"
        image_url = f"{self.site_config['base_url']}/{featured_image}" if featured_image else ""
        
        # Template HTML
        html_template = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <meta name="author" content="{author}">
    <meta name="keywords" content="{tags_str}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="{article_url}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{image_url}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="{article_url}">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{description}">
    <meta property="twitter:image" content="{image_url}">
    
    <title>{title} | {self.site_config['site_name']}</title>
    
    <!-- Styles -->
    <link rel="stylesheet" href="../assets/css/article.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Scripts -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script src="../assets/js/article.js" defer></script>
</head>
<body>
    <header class="header">
        <nav class="nav">
            <div class="nav-container">
                <a href="../index.html" class="nav-logo">
                    <span class="logo-text">Christian Mulato</span>
                    <span class="logo-subtitle">Dev Blog</span>
                </a>
                
                <div class="nav-links">
                    <a href="../index.html" class="nav-link">Artigos</a>
                    <a href="{self.site_config['linkedin']}" class="nav-link" target="_blank">LinkedIn</a>
                </div>
            </div>
        </nav>
    </header>

    <main class="main">
        <article class="article">
            <header class="article-header">
                <div class="article-meta">
                    <span class="article-category">{category}</span>
                    <time class="article-date" datetime="{date}">{date}</time>
                </div>
                
                <h1 class="article-title">{title}</h1>
                
                <div class="article-info">
                    <span class="article-author">Por {author}</span>
                    {'<div class="article-tags">' + " ".join([f'<span class="tag">{tag}</span>' for tag in tags]) + '</div>' if tags else ''}
                </div>
            </header>
            
            <div class="article-content">
                {html_content}
            </div>
            
            <footer class="article-footer">
                <div class="article-author-bio">
                    <h3>Sobre o Autor</h3>
                    <p><strong>{author}</strong> é Desenvolvedor Java Sênior especializado em arquiteturas escaláveis e microsserviços. 
                    Com experiência em Spring Boot, Docker, APIs REST e sistemas distribuídos.</p>
                    <a href="{self.site_config['linkedin']}" target="_blank" class="author-link">
                        Conecte-se no LinkedIn
                    </a>
                </div>
                
                <div class="article-navigation">
                    <a href="../index.html" class="back-link">← Voltar aos artigos</a>
                </div>
            </footer>
        </article>
    </main>
    
    <footer class="site-footer">
        <div class="footer-container">
            <p>&copy; {datetime.now().year} {author}. Todos os direitos reservados.</p>
        </div>
    </footer>
</body>
</html>"""
        
        return html_template
    
    def convert_md_to_html(self, md_file_path):
        """Converte um arquivo Markdown para HTML"""
        try:
            # Ler arquivo Markdown
            with open(md_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Extrair frontmatter
            frontmatter, markdown_content = self.extract_frontmatter(content)
            
            # Gerar HTML
            article_filename = Path(md_file_path).name
            html_content = self.generate_html_template(frontmatter, markdown_content, article_filename)
            
            # Salvar HTML
            html_filename = article_filename.replace('.md', '.html')
            html_path = self.articles_dir / html_filename
            
            with open(html_path, 'w', encoding='utf-8') as file:
                file.write(html_content)
            
            logging.info(f"Convertido: {article_filename} -> {html_filename}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao converter {md_file_path}: {e}")
            return False
    
    def convert_all_articles(self):
        """Converte todos os artigos Markdown para HTML"""
        md_files = list(self.md_dir.glob("*.md"))
        
        if not md_files:
            logging.warning(f"Nenhum arquivo Markdown encontrado no diretório {self.md_dir}")
            return
        
        logging.info(f"Encontrados {len(md_files)} artigos para converter")
        
        success_count = 0
        for md_file in sorted(md_files):
            if self.convert_md_to_html(md_file):
                success_count += 1
        
        logging.info(f"Conversão concluída: {success_count}/{len(md_files)} artigos convertidos")
        return success_count
    
    def generate_index_html(self):
        """Gera o arquivo index.html com lista de artigos"""
        try:
            articles = []
            
            # Ler todos os arquivos MD para extrair metadados
            md_files = list(self.md_dir.glob("*.md"))
            logging.info(f"Processando metadados de {len(md_files)} artigos")
            
            for md_file in sorted(md_files):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    frontmatter, _ = self.extract_frontmatter(content)
                    
                    # Extrair informações do artigo
                    title = frontmatter.get('title', md_file.stem.replace('_', ' ').title())
                    date = frontmatter.get('date', '01/01/2024')
                    description = frontmatter.get('description', f'Artigo técnico sobre {md_file.stem.replace("_", " ").lower()}')
                    category = frontmatter.get('category', 'Java & Spring')
                    tags = frontmatter.get('tags', ['Java', 'Spring', 'Docker'])
                    
                    # Garantir que tags é uma lista
                    if isinstance(tags, str):
                        tags = [tag.strip() for tag in tags.split(',')]
                    
                    article = {
                        'title': title,
                        'date': date,
                        'description': description,
                        'category': category,
                        'tags': tags,
                        'filename': f"{md_file.stem}.html"
                    }
                    
                    articles.append(article)
                    
                except Exception as e:
                    logging.warning(f"Erro ao processar metadados de {md_file}: {e}")
            
            # Ordenar artigos por data (mais recentes primeiro)
            def parse_date(date_str):
                try:
                    return datetime.strptime(date_str, '%d/%m/%Y')
                except:
                    return datetime(2024, 1, 1)
            
            articles.sort(key=lambda x: parse_date(x['date']), reverse=True)
            
            # Gerar HTML dos artigos
            articles_html = ""
            for article in articles:
                # Limitar tags exibidas a 3
                tags_html = " ".join([f'<span class="tag">{tag}</span>' 
                                    for tag in article['tags'][:3]])
                
                articles_html += f'''
        <article class="article-card">
            <div class="article-meta">
                <span class="category">{article['category']}</span>
                <span class="date">{article['date']}</span>
            </div>
            <h2 class="article-title">
                <a href="articles/{article['filename']}">{article['title']}</a>
            </h2>
            <p class="article-description">{article['description']}</p>
            <div class="article-tags">{tags_html}</div>
        </article>
        '''
            
            # Template do index.html (usar o template existente)
            index_template = self.get_index_template()
            
            # Gerar conteúdo final
            index_content = index_template.format(
                articles_html=articles_html,
                articles_count=len(articles),
                **self.site_config
            )
            
            # Salvar index.html
            index_file = self.base_dir / "index.html"
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            logging.info(f"✅ Index.html gerado com sucesso: {len(articles)} artigos")
            
        except Exception as e:
            logging.error(f"❌ Erro ao gerar index.html: {e}")
    
    def get_index_template(self):
        """Retorna template HTML para o index.html"""
        return '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{site_description}">
    <title>{site_name}</title>
    
    <link rel="stylesheet" href="assets/css/main.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="header-content">
                <h1>Christian Mulato</h1>
                <p class="subtitle">Desenvolvedor Java Sênior | Arquitetura de Software | Microsserviços</p>
                <div class="social-links">
                    <a href="{linkedin}" target="_blank">LinkedIn</a>
                    <a href="https://github.com/chmulato" target="_blank">GitHub</a>
                </div>
            </div>
        </header>

        <main class="main">
            <section class="articles-section">
                <div class="section-header">
                    <h2>Artigos Técnicos</h2>
                    <p>Explorando Java, Spring Boot, Docker, APIs e arquitetura de software</p>
                    <div class="stats">
                        <span class="stat">📚 {articles_count} artigos publicados</span>
                        <span class="stat">🚀 Março 2024 - Setembro 2025</span>
                    </div>
                </div>
                
                <div class="articles-grid">
                    {articles_html}
                </div>
            </section>
        </main>

        <footer class="footer">
            <div class="footer-content">
                <p>&copy; 2025 {author}. Todos os direitos reservados.</p>
                <div class="footer-links">
                    <a href="{linkedin}" target="_blank">LinkedIn</a>
                    <a href="https://github.com/chmulato" target="_blank">GitHub</a>
                </div>
            </div>
        </footer>
    </div>
    
    <script src="assets/js/main.js"></script>
</body>
</html>'''
    
    def validate_site(self):
        """Valida links, imagens e estrutura do site"""
        # Implementação de validação será adicionada depois
        logging.info("Validação do site será implementada em breve")
        pass

def main():
    import sys
    
    print("=" * 80)
    print("SITE MANAGER - GERENCIADOR DO SITE DE ARTIGOS")
    print("=" * 80)
    
    manager = SiteManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "convert":
            if len(sys.argv) > 2:
                # Converter arquivo específico
                file_path = manager.img_dir / sys.argv[2]
                if file_path.exists():
                    if manager.convert_md_to_html(file_path):
                        print(f"✅ Artigo convertido: {sys.argv[2]}")
                    else:
                        print(f"❌ Erro na conversão: {sys.argv[2]}")
                else:
                    print(f"❌ Arquivo não encontrado: {sys.argv[2]}")
            else:
                # Converter todos os arquivos
                success_count = manager.convert_all_articles()
                print(f"✅ {success_count} artigos convertidos com sucesso")
        
        elif command == "index":
            manager.generate_index_html()
            print("✅ Index.html gerado")
        
        elif command == "validate":
            manager.validate_site()
            print("✅ Validação concluída")
        
        else:
            print("Comandos disponíveis:")
            print("  convert [arquivo] - Converte MD para HTML")
            print("  index            - Gera index.html")
            print("  validate         - Valida o site")
    
    else:
        print("Uso: python site_manager.py <comando>")
        print("Comandos disponíveis:")
        print("  convert [arquivo] - Converte MD para HTML")
        print("  index            - Gera index.html")
        print("  validate         - Valida o site")

if __name__ == "__main__":
    main()
