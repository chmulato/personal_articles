#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRETOR MASSIVO DE ARTIGOS
============================
Este script corrige os principais problemas identificados nos artigos:
1. Adiciona footers ausentes
2. Adiciona classes de linguagem nos blocos de código
3. Remove H1s duplicados (mantém apenas o principal)
4. Verifica imagens faltantes

Autor: Sistema Automatizado
Versão: 1.0
Data: 2025-09-05
"""

import os
import re
import logging
from pathlib import Path
from typing import List, Dict

# Configuração de logging
log_dir = os.path.join(os.path.dirname(__file__), 'log')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'fix_mass_articles.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def add_footer_if_missing(content: str) -> tuple[str, bool]:
    """Adiciona footer se ausente"""
    footer_html = '''
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-info">
                <h3>Christian Mulato</h3>
                <p>Desenvolvedor Java Sênior especializado em Spring Boot, APIs REST e arquitetura de microsserviços.</p>
            </div>
            <div class="footer-links">
                <a href="https://www.linkedin.com/in/chmulato/" target="_blank">LinkedIn</a>
                <a href="https://github.com/chmulato" target="_blank">GitHub</a>
                <a href="../index.html">Artigos</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025 Christian Mulato. Todos os direitos reservados.</p>
        </div>
    </footer>
    
    <!-- Theme Toggle Button -->
    <button id="themeToggle" class="theme-toggle" aria-label="Alternar tema">
        <span id="themeIcon">🌙</span>
    </button>
    
    <script>
        // Tema manager
        class ThemeManager {
            constructor() {
                this.themeToggle = document.getElementById('themeToggle');
                this.themeIcon = document.getElementById('themeIcon');
                this.init();
            }
            
            init() {
                const savedTheme = localStorage.getItem('theme');
                const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
                const currentTheme = savedTheme || systemTheme;
                
                this.setTheme(currentTheme);
                this.updateIcon(currentTheme);
                
                this.themeToggle.addEventListener('click', () => this.toggleTheme());
            }
            
            toggleTheme() {
                const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                
                this.setTheme(newTheme);
                this.updateIcon(newTheme);
                localStorage.setItem('theme', newTheme);
            }
            
            setTheme(theme) {
                document.documentElement.setAttribute('data-theme', theme);
            }
            
            updateIcon(theme) {
                this.themeIcon.textContent = theme === 'light' ? '🌙' : '☀️';
                this.themeToggle.setAttribute('aria-label', 
                    theme === 'light' ? 'Ativar tema escuro' : 'Ativar tema claro');
            }
        }
        
        // Inicializar quando DOM carregar
        document.addEventListener('DOMContentLoaded', () => {
            new ThemeManager();
        });
    </script>
</body>
</html>'''

    if '<footer class="footer">' not in content:
        # Encontrar a posição antes do </body>
        body_end = content.rfind('</body>')
        if body_end != -1:
            content = content[:body_end] + footer_html
            return content, True
    
    return content, False

def fix_code_blocks(content: str) -> tuple[str, int]:
    """Adiciona classes de linguagem nos blocos de código"""
    fixes = 0
    
    # Padrão para blocos <pre><code> sem classe
    pattern = r'<pre><code>([^<]+)</code></pre>'
    
    def determine_language(code_content: str) -> str:
        """Determina a linguagem do código baseado no conteúdo"""
        code_lower = code_content.lower().strip()
        
        # Java patterns
        if any(keyword in code_lower for keyword in ['public class', '@component', '@service', '@repository', 'spring', 'import java']):
            return 'java'
        # XML patterns
        elif code_lower.startswith('<?xml') or '<beans' in code_lower or '<dependency>' in code_lower:
            return 'xml'
        # JSON patterns
        elif code_content.strip().startswith('{') and '"' in code_content:
            return 'json'
        # JavaScript/Node.js patterns
        elif any(keyword in code_lower for keyword in ['const ', 'let ', 'var ', 'function', 'node', 'npm', 'require(', '=>']):
            return 'javascript'
        # SQL patterns
        elif any(keyword in code_lower for keyword in ['select ', 'insert ', 'update ', 'delete ', 'create table']):
            return 'sql'
        # Shell/Bash patterns
        elif code_content.strip().startswith('$') or 'chmod' in code_lower or 'sudo' in code_lower:
            return 'bash'
        # YAML patterns
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*:', code_content.strip()):
            return 'yaml'
        # Default
        else:
            return 'text'
    
    def replace_code_block(match):
        nonlocal fixes
        code_content = match.group(1)
        language = determine_language(code_content)
        fixes += 1
        return f'<pre><code class="language-{language}">{code_content}</code></pre>'
    
    content = re.sub(pattern, replace_code_block, content, flags=re.DOTALL)
    
    return content, fixes

def remove_duplicate_h1s(content: str) -> tuple[str, int]:
    """Remove H1s duplicados, mantendo apenas o principal (dentro de article-title)"""
    # Encontrar todos os H1s
    h1_pattern = r'<h1[^>]*>(.*?)</h1>'
    h1_matches = list(re.finditer(h1_pattern, content, re.DOTALL))
    
    if len(h1_matches) <= 1:
        return content, 0
    
    # Identificar o H1 principal (dentro de article-title)
    main_h1_found = False
    removals = 0
    
    # Processar de trás para frente para não afetar as posições
    for match in reversed(h1_matches):
        h1_tag = match.group(0)
        
        # Se é o H1 principal (com classe article-title), manter
        if 'class="article-title"' in h1_tag:
            main_h1_found = True
            continue
        
        # Se já encontramos o principal ou este não é o principal, remover
        if main_h1_found or 'class="article-title"' not in h1_tag:
            content = content[:match.start()] + content[match.end():]
            removals += 1
    
    return content, removals

def check_missing_images(content: str, article_path: str) -> List[str]:
    """Verifica imagens faltantes"""
    missing_images = []
    img_pattern = r'src=["\']([^"\']+)["\']'
    
    for match in re.finditer(img_pattern, content):
        img_src = match.group(1)
        if img_src.startswith('http'):
            continue  # Skip external images
        
        # Construir caminho absoluto da imagem
        article_dir = os.path.dirname(article_path)
        img_path = os.path.join(article_dir, img_src)
        
        if not os.path.exists(img_path):
            missing_images.append(img_src)
    
    return missing_images

def process_article(file_path: str) -> Dict:
    """Processa um artigo individual"""
    result = {
        'file': os.path.basename(file_path),
        'footer_added': False,
        'code_blocks_fixed': 0,
        'h1s_removed': 0,
        'missing_images': [],
        'success': False
    }
    
    try:
        # Ler conteúdo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Adicionar footer se ausente
        content, footer_added = add_footer_if_missing(content)
        result['footer_added'] = footer_added
        
        # 2. Corrigir blocos de código
        content, code_fixes = fix_code_blocks(content)
        result['code_blocks_fixed'] = code_fixes
        
        # 3. Remover H1s duplicados
        content, h1_removals = remove_duplicate_h1s(content)
        result['h1s_removed'] = h1_removals
        
        # 4. Verificar imagens faltantes
        result['missing_images'] = check_missing_images(content, file_path)
        
        # Salvar apenas se houve mudanças
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        result['success'] = True
        
    except Exception as e:
        logging.error(f"Erro ao processar {file_path}: {str(e)}")
        result['error'] = str(e)
    
    return result

def main():
    """Função principal"""
    logging.info("=== INICIANDO CORREÇÃO MASSIVA DE ARTIGOS ===")
    
    articles_dir = "c:/dev/personal_articles/articles"
    html_files = [f for f in os.listdir(articles_dir) if f.endswith('.html')]
    
    logging.info(f"Encontrados {len(html_files)} arquivos HTML para processar")
    
    results = []
    total_footers = 0
    total_code_fixes = 0
    total_h1_removals = 0
    total_missing_images = 0
    
    for i, filename in enumerate(html_files, 1):
        file_path = os.path.join(articles_dir, filename)
        
        logging.info(f"[{i}/{len(html_files)}] Processando: {filename}")
        
        result = process_article(file_path)
        results.append(result)
        
        if result['success']:
            total_footers += 1 if result['footer_added'] else 0
            total_code_fixes += result['code_blocks_fixed']
            total_h1_removals += result['h1s_removed']
            total_missing_images += len(result['missing_images'])
            
            if result['missing_images']:
                logging.warning(f"  Imagens faltantes em {filename}: {result['missing_images']}")
    
    # Relatório final
    logging.info("=== RELATÓRIO FINAL ===")
    logging.info(f"📄 Arquivos processados: {len(html_files)}")
    logging.info(f"📋 Footers adicionados: {total_footers}")
    logging.info(f"💻 Blocos de código corrigidos: {total_code_fixes}")
    logging.info(f"🏷️ H1s duplicados removidos: {total_h1_removals}")
    logging.info(f"🖼️ Total de imagens faltantes: {total_missing_images}")
    
    logging.info("=== CORREÇÃO CONCLUÍDA ===")

if __name__ == "__main__":
    main()
