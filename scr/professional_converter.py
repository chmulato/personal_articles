#!/usr/bin/env python3
"""
Professional DOCX to HTML Converter
Conversão profissional DOCX → MD → HTML para artigos técnicos
Christian Mulato Dev Blog
"""

import os
import re
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import mammoth
import markdown
from bs4 import BeautifulSoup
from PIL import Image
import base64

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProfessionalDocxConverter:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.docx_dir = self.base_dir / "docx"
        self.md_dir = self.base_dir / "md"
        self.articles_dir = self.base_dir / "articles" 
        self.img_dir = self.articles_dir / "img"
        
        # Criar diretórios se não existirem
        self.md_dir.mkdir(exist_ok=True)
        self.articles_dir.mkdir(exist_ok=True)
        self.img_dir.mkdir(exist_ok=True)
        
        # Configurações do Markdown
        self.md_extensions = [
            'codehilite',
            'fenced_code',
            'tables',
            'toc',
            'attr_list',
            'def_list',
            'footnotes',
            'admonition'
        ]
        
        # Configurações de estilo para Mammoth
        self.style_map = """
        p[style-name='Heading 1'] => h1
        p[style-name='Heading 2'] => h2  
        p[style-name='Heading 3'] => h3
        p[style-name='Heading 4'] => h4
        p[style-name='Code'] => pre
        p[style-name='Quote'] => blockquote
        """
        
    def extract_images_from_docx(self, docx_path: Path) -> str:
        """Extrai conteúdo do DOCX convertendo para HTML"""
        try:
            # Configurar Mammoth com opções mais robustas
            options = {
                "style_map": self.style_map,
                "convert_image": self.create_image_converter(docx_path)
            }
            
            # Converter DOCX para HTML
            with open(docx_path, 'rb') as docx_file:
                result = mammoth.convert_to_html(docx_file, **options)
                
                if result.messages:
                    logger.warning(f"Avisos na conversão: {[msg.message for msg in result.messages]}")
                
                return result.value
                
        except Exception as e:
            logger.warning(f"Erro com Mammoth para {docx_path}: {e}")
            # Fallback: converter sem imagens
            try:
                with open(docx_path, 'rb') as docx_file:
                    result = mammoth.convert_to_html(docx_file)
                    return result.value
            except Exception as e2:
                logger.error(f"Falha completa na conversão de {docx_path}: {e2}")
                return ""
    
    def create_image_converter(self, docx_path: Path):
        """Cria função para converter imagens com tratamento robusto de erros"""
        def convert_image(image):
            try:
                # Gerar nome único
                img_count = len(list(self.img_dir.glob(f"{docx_path.stem}*")))
                filename = f"{docx_path.stem}_image{img_count + 1}"
                
                # Determinar extensão baseada no content_type
                if hasattr(image, 'content_type'):
                    if 'jpeg' in image.content_type or 'jpg' in image.content_type:
                        filename += '.jpg'
                    elif 'png' in image.content_type:
                        filename += '.png'
                    else:
                        filename += '.png'
                else:
                    filename += '.png'
                
                # Caminho da imagem
                img_path = self.img_dir / filename
                
                # Salvar imagem com múltiplas tentativas
                try:
                    # Método 1: usar open()
                    if hasattr(image, 'open'):
                        with open(img_path, 'wb') as f:
                            with image.open() as img_stream:
                                f.write(img_stream.read())
                        logger.info(f"📸 Imagem salva (método 1): {filename}")
                        return {"src": f"img/{filename}"}
                
                except AttributeError:
                    try:
                        # Método 2: usar read() direto
                        if hasattr(image, 'read'):
                            with open(img_path, 'wb') as f:
                                f.write(image.read())
                            logger.info(f"📸 Imagem salva (método 2): {filename}")
                            return {"src": f"img/{filename}"}
                    except:
                        pass
                
                except Exception as e:
                    logger.warning(f"Erro na extração da imagem: {e}")
                    
                # Fallback: placeholder
                logger.warning(f"Usando placeholder para imagem")
                return {"src": "img/placeholder.png"}
                    
            except Exception as e:
                logger.warning(f"Erro geral no processamento de imagem: {e}")
                return {"src": "img/placeholder.png"}
        
        return mammoth.images.img_element(convert_image)
    
    def docx_to_markdown(self, docx_path: Path) -> Tuple[str, Dict]:
        """Converte DOCX para Markdown com metadados"""
        try:
            logger.info(f"Convertendo {docx_path.name} para Markdown...")
            
            # Extrair conteúdo HTML
            html_content = self.extract_images_from_docx(docx_path)
            
            if not html_content:
                logger.error(f"Falha ao extrair conteúdo de {docx_path}")
                return "", {}
            
            # Usar BeautifulSoup para processar HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extrair título
            title = self.extract_title(soup, docx_path.stem)
            
            # Processar imagens e código
            self.process_images_in_soup(soup)
            self.process_code_blocks(soup)
            
            # Converter para Markdown
            markdown_content = self.html_to_markdown(soup)
            
            # Gerar metadados
            metadata = self.generate_metadata(title, docx_path)
            
            # Combinar frontmatter + conteúdo
            frontmatter = self.generate_frontmatter(metadata)
            full_markdown = f"{frontmatter}\n\n{markdown_content}"
            
            return full_markdown, metadata
            
        except Exception as e:
            logger.error(f"Erro na conversão de {docx_path}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return "", {}
    
    def extract_title(self, soup: BeautifulSoup, fallback: str) -> str:
        """Extrai título do documento"""
        # Procurar por h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        
        # Procurar por primeiro parágrafo em negrito
        strong = soup.find('strong')
        if strong and len(strong.get_text().strip()) > 10:
            return strong.get_text().strip()
        
        # Usar nome do arquivo como fallback
        return fallback.replace('_', ' ').title()
    
    def process_images_in_soup(self, soup: BeautifulSoup):
        """Processa imagens no HTML para melhor formatação"""
        for img in soup.find_all('img'):
            # Criar container profissional para imagem
            img_container = soup.new_tag('div', **{'class': 'image-container'})
            
            # Adicionar alt text se não houver
            if not img.get('alt'):
                img['alt'] = 'Imagem do artigo'
            
            # Mover imagem para container
            img.wrap(img_container)
            
            # Adicionar legenda se houver texto próximo
            next_p = img_container.find_next_sibling('p')
            if next_p and len(next_p.get_text().strip()) < 100:
                caption = soup.new_tag('div', **{'class': 'image-caption'})
                caption.string = next_p.get_text().strip()
                img_container.append(caption)
                next_p.decompose()
    
    def process_code_blocks(self, soup: BeautifulSoup):
        """Processa blocos de código para melhor formatação"""
        # Procurar por elementos pré-formatados
        for pre in soup.find_all('pre'):
            # Adicionar linguagem baseada no conteúdo
            code_text = pre.get_text()
            language = self.detect_code_language(code_text)
            
            if language:
                pre['class'] = f'language-{language}'
                
            # Criar container profissional
            code_container = soup.new_tag('div', **{'class': 'code-block'})
            
            # Adicionar título se possível detectar
            if 'class' in code_text.lower() or 'public' in code_text.lower():
                title = soup.new_tag('div', **{'class': 'code-title'})
                title.string = f"Exemplo em {language.upper() if language else 'Código'}"
                code_container.append(title)
            
            pre.wrap(code_container)
    
    def detect_code_language(self, code_text: str) -> Optional[str]:
        """Detecta linguagem de programação baseada no conteúdo"""
        code_lower = code_text.lower()
        
        # Java
        if any(keyword in code_lower for keyword in ['public class', 'import java', '@override', 'system.out']):
            return 'java'
        
        # Python
        if any(keyword in code_lower for keyword in ['def ', 'import ', 'print(', 'if __name__']):
            return 'python'
        
        # JavaScript
        if any(keyword in code_lower for keyword in ['function', 'const ', 'let ', 'var ', 'console.log']):
            return 'javascript'
        
        # SQL
        if any(keyword in code_lower for keyword in ['select ', 'insert ', 'update ', 'create table']):
            return 'sql'
        
        # XML/HTML
        if '<' in code_text and '>' in code_text:
            return 'xml'
        
        # JSON
        if code_text.strip().startswith('{') and code_text.strip().endswith('}'):
            return 'json'
        
        return None
    
    def html_to_markdown(self, soup: BeautifulSoup) -> str:
        """Converte HTML processado para Markdown"""
        markdown_lines = []
        
        for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'pre', 'blockquote', 'div']):
            if element.name in ['h1', 'h2', 'h3', 'h4']:
                level = '#' * int(element.name[1])
                markdown_lines.append(f"{level} {element.get_text().strip()}")
                markdown_lines.append("")
                
            elif element.name == 'p':
                text = element.get_text().strip()
                if text:
                    markdown_lines.append(text)
                    markdown_lines.append("")
                    
            elif element.name in ['ul', 'ol']:
                for li in element.find_all('li'):
                    prefix = '- ' if element.name == 'ul' else '1. '
                    markdown_lines.append(f"{prefix}{li.get_text().strip()}")
                markdown_lines.append("")
                
            elif element.name == 'pre':
                language = ''
                if 'class' in element.attrs:
                    class_attr = element.attrs['class'][0]
                    if 'language-' in class_attr:
                        language = class_attr.replace('language-', '')
                
                markdown_lines.append(f"```{language}")
                markdown_lines.append(element.get_text().strip())
                markdown_lines.append("```")
                markdown_lines.append("")
                
            elif element.name == 'blockquote':
                for line in element.get_text().strip().split('\n'):
                    markdown_lines.append(f"> {line.strip()}")
                markdown_lines.append("")
                
            elif element.has_attr('class') and 'image-container' in element.get('class', []):
                img = element.find('img')
                caption_div = element.find('div', class_='image-caption')
                
                if img:
                    alt_text = img.get('alt', 'Imagem')
                    src = img.get('src', '')
                    markdown_lines.append(f"![{alt_text}]({src})")
                    
                    if caption_div:
                        markdown_lines.append(f"*{caption_div.get_text().strip()}*")
                    
                    markdown_lines.append("")
        
        return '\n'.join(markdown_lines)
    
    def generate_metadata(self, title: str, docx_path: Path) -> Dict:
        """Gera metadados do artigo"""
        # Extrair data do nome do arquivo
        date_match = re.search(r'(\d{4})_(\d{2})_(\d{2})', docx_path.stem)
        if date_match:
            year, month, day = date_match.groups()
            date_str = f"{day}/{month}/{year}"
        else:
            date_str = datetime.now().strftime('%d/%m/%Y')
        
        # Categorizar baseado no título/conteúdo
        category = self.categorize_article(title, docx_path.stem)
        
        # Gerar tags baseadas no título
        tags = self.generate_tags(title, docx_path.stem)
        
        return {
            'title': title,
            'date': date_str,
            'author': 'Christian Mulato',
            'description': f'Artigo técnico sobre {title.lower()}',
            'category': category,
            'tags': tags,
            'featured_image': f'img/{docx_path.stem}_featured.jpg'
        }
    
    def categorize_article(self, title: str, filename: str) -> str:
        """Categoriza artigo baseado no título e nome do arquivo"""
        content = f"{title} {filename}".lower()
        
        if any(word in content for word in ['java', 'spring', 'maven', 'jpa', 'hibernate']):
            return 'Java & Spring'
        elif any(word in content for word in ['docker', 'kubernetes', 'devops', 'ci', 'cd']):
            return 'DevOps & Containers'
        elif any(word in content for word in ['api', 'rest', 'graphql', 'microserviços']):
            return 'APIs & Microserviços'
        elif any(word in content for word in ['arquitetura', 'design', 'patterns', 'clean']):
            return 'Arquitetura de Software'
        elif any(word in content for word in ['ia', 'inteligência', 'artificial', 'machine']):
            return 'IA & Tecnologia'
        elif any(word in content for word in ['teste', 'tdd', 'unit', 'test']):
            return 'Testes & Qualidade'
        else:
            return 'Desenvolvimento'
    
    def generate_tags(self, title: str, filename: str) -> List[str]:
        """Gera tags baseadas no título e nome do arquivo"""
        content = f"{title} {filename}".lower()
        tags = []
        
        # Tags técnicas
        tech_tags = {
            'java': ['Java'],
            'spring': ['Spring', 'Spring Boot'],
            'docker': ['Docker', 'Containers'],
            'api': ['APIs', 'REST'],
            'microserviços': ['Microserviços', 'Arquitetura'],
            'test': ['Testes', 'TDD'],
            'kafka': ['Apache Kafka', 'Mensageria'],
            'arquitetura': ['Arquitetura', 'Design Patterns'],
            'ia': ['IA', 'Inteligência Artificial'],
            'devops': ['DevOps', 'CI/CD']
        }
        
        for keyword, related_tags in tech_tags.items():
            if keyword in content:
                tags.extend(related_tags)
        
        # Tags padrão se nenhuma encontrada
        if not tags:
            tags = ['Desenvolvimento', 'Tecnologia', 'Programação']
        
        # Limitar a 6 tags e remover duplicatas
        return list(dict.fromkeys(tags))[:6]
    
    def generate_frontmatter(self, metadata: Dict) -> str:
        """Gera frontmatter YAML"""
        tags_str = str(metadata['tags'])
        
        return f"""---
title: "{metadata['title']}"
date: "{metadata['date']}"
author: "{metadata['author']}"
description: "{metadata['description']}"
category: "{metadata['category']}"
tags: {tags_str}
featured_image: "{metadata['featured_image']}"
---"""
    
    def markdown_to_html(self, markdown_content: str, metadata: Dict) -> str:
        """Converte Markdown para HTML profissional"""
        try:
            # Configurar Markdown com extensões
            md = markdown.Markdown(
                extensions=self.md_extensions,
                extension_configs={
                    'codehilite': {
                        'css_class': 'highlight',
                        'use_pygments': True,
                        'noclasses': False,
                        'linenos': True
                    },
                    'toc': {
                        'anchorlink': True,
                        'title': 'Índice'
                    }
                }
            )
            
            # Extrair frontmatter
            content_without_frontmatter = re.sub(r'^---.*?---\s*', '', markdown_content, flags=re.DOTALL)
            
            # Converter para HTML
            html_content = md.convert(content_without_frontmatter)
            
            # Aplicar template profissional
            return self.apply_professional_template(html_content, metadata)
            
        except Exception as e:
            logger.error(f"Erro na conversão MD→HTML: {e}")
            return ""
    
    def apply_professional_template(self, content: str, metadata: Dict) -> str:
        """Aplica template HTML profissional"""
        tags_html = " ".join([f'<span class="tag">{tag}</span>' for tag in metadata.get('tags', [])])
        
        return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{metadata.get('description', '')}">
    <meta name="author" content="{metadata.get('author', 'Christian Mulato')}">
    <meta name="keywords" content="{', '.join(metadata.get('tags', []))}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{metadata.get('title', '')}">
    <meta property="og:description" content="{metadata.get('description', '')}">
    <meta property="og:type" content="article">
    <meta property="og:author" content="{metadata.get('author', 'Christian Mulato')}">
    <meta property="og:article:published_time" content="{metadata.get('date', '')}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{metadata.get('title', '')}">
    <meta name="twitter:description" content="{metadata.get('description', '')}">
    
    <title>{metadata.get('title', '')} | Christian Mulato Dev Blog</title>
    
    <!-- Fonts e Styles -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Fira+Code:wght@300;400;500;600&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="../assets/css/main.css">
    <link rel="stylesheet" href="../assets/css/article.css">
    
    <!-- Prism.js para syntax highlighting -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-tomorrow.min.css" rel="stylesheet">
    
    <!-- Schema.org structured data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{metadata.get('title', '')}",
        "description": "{metadata.get('description', '')}",
        "author": {{
            "@type": "Person",
            "name": "{metadata.get('author', 'Christian Mulato')}"
        }},
        "datePublished": "{metadata.get('date', '')}",
        "category": "{metadata.get('category', '')}"
    }}
    </script>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <a href="../index.html" class="nav-brand">← Voltar ao Blog</a>
            <div class="nav-links">
                <a href="../index.html">Artigos</a>
                <a href="https://www.linkedin.com/in/chmulato/" target="_blank">LinkedIn</a>
                <a href="https://github.com/chmulato" target="_blank">GitHub</a>
            </div>
        </div>
    </nav>

    <article class="article-container">
        <header class="article-header">
            <div class="article-meta">
                <span class="category">{metadata.get('category', 'Desenvolvimento')}</span>
                <time class="date" datetime="{metadata.get('date', '')}">{metadata.get('date', '')}</time>
            </div>
            <h1 class="article-title">{metadata.get('title', '')}</h1>
            <div class="author-info">
                <span>Por <a href="https://www.linkedin.com/in/chmulato/" target="_blank">{metadata.get('author', 'Christian Mulato')}</a></span>
            </div>
            <div class="article-tags">
                {tags_html}
            </div>
        </header>
        
        <div class="article-content">
            {content}
        </div>
    </article>

    <footer class="article-footer">
        <div class="footer-content">
            <p>&copy; 2025 {metadata.get('author', 'Christian Mulato')}. Todos os direitos reservados.</p>
            <div class="footer-links">
                <a href="https://www.linkedin.com/in/chmulato/" target="_blank">LinkedIn</a>
                <a href="https://github.com/chmulato" target="_blank">GitHub</a>
            </div>
        </div>
    </footer>
    
    <!-- Scripts -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/plugins/autoloader/prism-autoloader.min.js"></script>
    
    <!-- Copy code functionality -->
    <script>
        // Adicionar botões de copiar código
        document.querySelectorAll('pre code').forEach((block) => {{
            const button = document.createElement('button');
            button.className = 'copy-button';
            button.textContent = 'Copiar';
            button.onclick = () => {{
                navigator.clipboard.writeText(block.textContent);
                button.textContent = 'Copiado!';
                setTimeout(() => button.textContent = 'Copiar', 2000);
            }};
            block.parentNode.appendChild(button);
        }});
    </script>
</body>
</html>'''
    
    def convert_single_docx(self, docx_file: Path) -> bool:
        """Converte um único arquivo DOCX"""
        try:
            logger.info(f"🔄 Processando: {docx_file.name}")
            
            # 1. DOCX → Markdown
            markdown_content, metadata = self.docx_to_markdown(docx_file)
            if not markdown_content:
                return False
            
            # 2. Salvar Markdown
            md_file = self.md_dir / f"{docx_file.stem}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # 3. Markdown → HTML
            html_content = self.markdown_to_html(markdown_content, metadata)
            if not html_content:
                return False
            
            # 4. Salvar HTML
            html_file = self.articles_dir / f"{docx_file.stem}.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ Convertido: {docx_file.name} → {md_file.name} → {html_file.name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao converter {docx_file.name}: {e}")
            return False
    
    def convert_all_docx(self) -> int:
        """Converte todos os arquivos DOCX originais"""
        docx_files = [f for f in self.docx_dir.glob("*.docx") 
                     if not f.name.startswith("~") and "_improved" not in f.name]
        
        logger.info(f"🚀 Iniciando conversão de {len(docx_files)} arquivos DOCX")
        
        success_count = 0
        for docx_file in sorted(docx_files):
            if self.convert_single_docx(docx_file):
                success_count += 1
        
        logger.info(f"🎉 Conversão concluída: {success_count}/{len(docx_files)} arquivos processados")
        return success_count

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Professional DOCX to HTML Converter')
    parser.add_argument('action', choices=['convert', 'single'], 
                       help='Ação: convert (todos) ou single (arquivo específico)')
    parser.add_argument('--file', help='Arquivo DOCX específico (apenas para single)')
    
    args = parser.parse_args()
    
    converter = ProfessionalDocxConverter()
    
    if args.action == 'convert':
        success_count = converter.convert_all_docx()
        print(f"\n🎉 {success_count} arquivos convertidos com sucesso!")
        
    elif args.action == 'single':
        if not args.file:
            print("❌ Especifique um arquivo com --file")
            return
        
        docx_file = converter.docx_dir / args.file
        if not docx_file.exists():
            print(f"❌ Arquivo não encontrado: {docx_file}")
            return
        
        success = converter.convert_single_docx(docx_file)
        print("✅ Conversão concluída!" if success else "❌ Erro na conversão")

if __name__ == "__main__":
    main()
