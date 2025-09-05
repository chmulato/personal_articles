import os
import re
import markdown
import logging
from pathlib import Path
from datetime import datetime
import os

# Configuração de logging centralizada
log_dir = Path("c:/dev/personal_articles/scr/log")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(log_dir, 'convert_md_to_html.log'), encoding='utf-8'),
    ]
)

def extract_frontmatter(content):
    """Extrai o frontmatter YAML do conteúdo Markdown"""
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

def process_markdown_content(content):
    """Processa o conteúdo Markdown, ajustando caminhos de imagem"""
    # Ajustar caminhos de imagem para o novo local
    content = re.sub(r'!\[\]\(img/image_not_found\.png\)', '', content)
    content = re.sub(r'!\[(.*?)\]\(img/(.*?)\)', r'<img src="img/\2" alt="\1" class="article-image">', content)
    
    return content

def create_html_template(frontmatter, content_html, filename):
    """Cria template HTML completo para artigo"""
    
    title = frontmatter.get('title', 'Artigo')
    description = frontmatter.get('description', 'Artigo técnico')
    author = frontmatter.get('author', 'Christian Mulato')
    date = frontmatter.get('date', 'Data não especificada')
    category = frontmatter.get('category', 'Desenvolvimento')
    tags = frontmatter.get('tags', [])
    featured_image = frontmatter.get('featured_image', 'img/default.jpg')
    
    # Converter tags para string se for lista
    if isinstance(tags, list):
        tags_str = ', '.join(tags)
        tags_meta = ', '.join(tags)
    else:
        tags_str = str(tags)
        tags_meta = str(tags)
    
    # Nome do arquivo sem extensão para URLs
    article_slug = Path(filename).stem
    
    template = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <meta name="author" content="{author}">
    <meta name="keywords" content="{tags_meta}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://chmulato.dev/articles/{article_slug}.html">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://chmulato.dev/{featured_image}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://chmulato.dev/articles/{article_slug}.html">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{description}">
    <meta property="twitter:image" content="https://chmulato.dev/{featured_image}">
    
    <title>{title} | Christian Mulato Dev Blog</title>
    
    <!-- Styles -->
    <link rel="stylesheet" href="../assets/css/article.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Scripts -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
</head>
<body>
    <div class="container">
        <header class="article-header">
            <nav class="breadcrumb">
                <a href="../../index.html">← Voltar aos Artigos</a>
            </nav>
            
            <div class="article-meta">
                <div class="category-badge" data-category="{category.lower().replace(' & ', '-').replace(' ', '-')}">{category}</div>
                <time datetime="{date}" class="article-date">{date}</time>
            </div>
            
            <h1 class="article-title">{title}</h1>
            
            <div class="article-info">
                <div class="author-info">
                    <img src="../assets/img/author.jpg" alt="{author}" class="author-avatar">
                    <div>
                        <div class="author-name">{author}</div>
                        <div class="author-title">Desenvolvedor Java Sênior</div>
                    </div>
                </div>
                
                <div class="article-tags">
                    {' '.join([f'<span class="tag">#{tag}</span>' for tag in (tags if isinstance(tags, list) else [tags])])}
                </div>
            </div>
        </header>
        
        <main class="article-content">
            {content_html}
        </main>
        
        <footer class="article-footer">
            <div class="author-bio">
                <img src="../assets/img/author.jpg" alt="{author}" class="author-bio-avatar">
                <div class="author-bio-content">
                    <h3>{author}</h3>
                    <p>Desenvolvedor Java Sênior especializado em arquiteturas escaláveis e microsserviços. 
                    Com experiência em Spring Boot, Docker, APIs REST e sistemas distribuídos.</p>
                    <div class="author-links">
                        <a href="https://www.linkedin.com/in/chmulato/" target="_blank">LinkedIn</a>
                        <a href="https://github.com/chmulato" target="_blank">GitHub</a>
                    </div>
                </div>
            </div>
            
            <div class="article-navigation">
                <a href="../../index.html" class="nav-link">
                    ← Voltar aos Artigos
                </a>
            </div>
        </footer>
    </div>
    
    <!-- Analytics -->
    <script>
        // Google Analytics ou outro sistema de analytics pode ser adicionado aqui
    </script>
</body>
</html>'''
    
    return template

def convert_md_to_html_from_img_dir(md_file_path):
    """Converte arquivo MD para HTML a partir do diretório img"""
    try:
        # Ler arquivo MD
        with open(md_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extrair frontmatter
        frontmatter, md_content = extract_frontmatter(content)
        
        # Processar conteúdo
        processed_content = process_markdown_content(md_content)
        
        # Converter para HTML
        md_processor = markdown.Markdown(extensions=[
            'codehilite',
            'fenced_code', 
            'tables',
            'toc'
        ])
        content_html = md_processor.convert(processed_content)
        
        # Criar HTML completo
        filename = Path(md_file_path).name
        html_content = create_html_template(frontmatter, content_html, filename)
        
        # Salvar arquivo HTML no diretório articles (um nível acima)
        articles_dir = Path(md_file_path).parent.parent
        html_filename = Path(filename).stem + '.html'
        html_path = articles_dir / html_filename
        
        with open(html_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        logging.info(f"HTML gerado com sucesso: {html_filename}")
        return True
        
    except Exception as e:
        logging.error(f"Erro ao converter {md_file_path}: {str(e)}")
        return False

def convert_all_articles_from_img_dir():
    """Converte todos os arquivos MD do diretório img para HTML"""
    # Diretório onde estão os arquivos MD
    img_dir = Path("md/site_artiches/articles/img")
    
    if not img_dir.exists():
        logging.error(f"Diretório não encontrado: {img_dir}")
        return
    
    # Encontrar todos os arquivos MD
    md_files = list(img_dir.glob("*.md"))
    
    if not md_files:
        logging.info("Nenhum arquivo .md encontrado no diretório img")
        return
    
    logging.info(f"Encontrados {len(md_files)} artigos para converter")
    
    success_count = 0
    error_count = 0
    
    for md_file in sorted(md_files):
        logging.info(f"Convertendo: {md_file.name}")
        
        if convert_md_to_html_from_img_dir(str(md_file)):
            success_count += 1
        else:
            error_count += 1
    
    return success_count, error_count

def main():
    import sys
    
    print("=" * 80)
    print("CONVERSOR MD->HTML - VERSAO DIRETORIO IMG")
    print("=" * 80)
    
    if len(sys.argv) > 1:
        # Converter arquivo específico
        filename = sys.argv[1]
        img_dir = Path("md/site_artiches/articles/img")
        file_path = img_dir / filename
        
        print(f"Convertendo arquivo específico: {filename}")
        
        if file_path.exists():
            if convert_md_to_html_from_img_dir(str(file_path)):
                print(f" Conversão realizada com sucesso: {filename}")
            else:
                print(f" Erro na conversão: {filename}")
        else:
            print(f" Arquivo não encontrado: {file_path}")
    else:
        # Converter todos os arquivos
        print("Convertendo todos os artigos do diretório img...")
        success_count, error_count = convert_all_articles_from_img_dir()
        
        print("\n" + "=" * 80)
        print("RESUMO DA CONVERSÃO")
        print("=" * 80)
        print(f"Sucessos: {success_count}")
        print(f"Erros: {error_count}")
        print(f"Total processado: {success_count + error_count}")
        
        if error_count == 0:
            print("\n Todas as conversões foram concluídas com sucesso!")
        else:
            print(f"\n  {error_count} artigos apresentaram erros durante a conversão")
        
        print(f"\nPASTA: Arquivos HTML salvos em: md/site_artiches/articles/")

if __name__ == "__main__":
    main()




