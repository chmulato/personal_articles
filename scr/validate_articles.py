#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUSCA: VALIDADOR DE ARTIGOS - DETECTOR DE DUPLICATAS E VALIDAÇÃO CSS
=================================================================
Este script verifica:
1. Artigos duplicados (por conteúdo e título)
2. Formatação CSS padrão
3. Estrutura HTML consistente
4. Links e referências quebradas
5. Meta tags obrigatórias

Autor: Sistema Automatizado
Versão: 1.0
Data: 2025-09-05
"""

import os
import re
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Set
from datetime import datetime
from collections import defaultdict
import difflib

# Configuração de logging
log_dir = os.path.join(os.path.dirname(__file__), 'log')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'validation_report.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class ArticleValidator:
    """Classe principal para validação de artigos"""
    
    def __init__(self, articles_dir: str = "articles"):
        self.articles_dir = Path(articles_dir)
        self.report = {
            'duplicates': [],
            'css_issues': [],
            'structure_issues': [],
            'broken_links': [],
            'missing_meta': [],
            'statistics': {}
        }
        
        # Padrões CSS obrigatórios
        self.required_css = [
            'assets/css/article.css',
            'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css',
            'https://fonts.googleapis.com/css2?family=Inter:'
        ]
        
        # Meta tags obrigatórias
        self.required_meta = [
            'charset',
            'viewport',
            'description',
            'author',
            'keywords',
            'og:type',
            'og:url',
            'og:title',
            'og:description',
            'twitter:card'
        ]
        
        # Estrutura HTML obrigatória
        self.required_structure = [
            '<header class="header">',
            '<nav class="nav">',
            '<div class="nav-container">',
            '<main class="main">',
            '<article class="article">',
            '<footer class="footer">'
        ]

    def calculate_content_hash(self, content: str) -> str:
        """Calcula hash do conteúdo para detectar duplicatas"""
        # Remove espaços em branco e elementos variáveis (datas, URLs específicas)
        clean_content = re.sub(r'\s+', ' ', content.lower())
        clean_content = re.sub(r'\d{4}_\d{2}_\d{2}', 'DATE_PLACEHOLDER', clean_content)
        clean_content = re.sub(r'https?://[^\s<>"]+', 'URL_PLACEHOLDER', clean_content)
        
        return hashlib.md5(clean_content.encode('utf-8')).hexdigest()

    def extract_title_from_html(self, content: str) -> str:
        """Extrai título do HTML"""
        title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1)
            # Remove " | Christian Mulato Dev Blog" se presente
            title = re.sub(r'\s*\|\s*Christian Mulato Dev Blog\s*$', '', title)
            return title.strip()
        return "Título não encontrado"

    def extract_h1_from_html(self, content: str) -> str:
        """Extrai o primeiro H1 do HTML"""
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        if h1_match:
            h1_content = h1_match.group(1)
            # Remove tags HTML do conteúdo
            h1_content = re.sub(r'<[^>]+>', '', h1_content)
            return h1_content.strip()
        return "H1 não encontrado"

    def find_duplicate_articles(self) -> List[Dict]:
        """Encontra artigos duplicados por conteúdo e título"""
        logging.info("BUSCA: Procurando artigos duplicados...")
        
        content_hashes = defaultdict(list)
        title_groups = defaultdict(list)
        h1_groups = defaultdict(list)
        
        html_files = list(self.articles_dir.glob("*.html"))
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Hash do conteúdo
                content_hash = self.calculate_content_hash(content)
                content_hashes[content_hash].append(str(html_file))
                
                # Agrupamento por título
                title = self.extract_title_from_html(content)
                title_groups[title.lower()].append(str(html_file))
                
                # Agrupamento por H1
                h1 = self.extract_h1_from_html(content)
                h1_groups[h1.lower()].append(str(html_file))
                
            except Exception as e:
                logging.error(f"Erro ao processar {html_file}: {e}")
        
        duplicates = []
        
        # Duplicatas por conteúdo
        for content_hash, files in content_hashes.items():
            if len(files) > 1:
                duplicates.append({
                    'type': 'content_identical',
                    'files': files,
                    'reason': f'Conteúdo idêntico (hash: {content_hash[:8]})'
                })
        
        # Duplicatas por título
        for title, files in title_groups.items():
            if len(files) > 1 and title != "título não encontrado":
                duplicates.append({
                    'type': 'title_duplicate',
                    'files': files,
                    'reason': f'Título duplicado: "{title}"'
                })
        
        # Duplicatas por H1
        for h1, files in h1_groups.items():
            if len(files) > 1 and h1 != "h1 não encontrado":
                duplicates.append({
                    'type': 'h1_duplicate',
                    'files': files,
                    'reason': f'H1 duplicado: "{h1}"'
                })
        
        self.report['duplicates'] = duplicates
        return duplicates

    def validate_css_formatting(self, html_file: Path) -> List[str]:
        """Valida se o CSS está formatado corretamente"""
        issues = []
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar CSS obrigatórios
            for required_css in self.required_css:
                if required_css not in content:
                    issues.append(f"CSS ausente: {required_css}")
            
            # Verificar se há CSS inline (não recomendado)
            inline_css = re.findall(r'style\s*=\s*["\'][^"\']*["\']', content)
            if inline_css:
                issues.append(f"CSS inline encontrado (não recomendado): {len(inline_css)} ocorrências")
            
            # Verificar se o highlight.js está configurado
            if 'highlight.min.js' not in content:
                issues.append("Script highlight.js ausente")
            
            # Verificar se há códigos sem highlighting
            code_blocks = re.findall(r'<pre[^>]*>.*?</pre>', content, re.DOTALL)
            for i, block in enumerate(code_blocks):
                if 'class=' not in block or 'language-' not in block:
                    issues.append(f"Bloco de código {i+1} sem classe de linguagem para highlighting")
            
        except Exception as e:
            issues.append(f"Erro ao validar CSS: {e}")
        
        return issues

    def validate_html_structure(self, html_file: Path) -> List[str]:
        """Valida a estrutura HTML padrão"""
        issues = []
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar estrutura obrigatória
            for required_element in self.required_structure:
                if required_element not in content:
                    issues.append(f"Elemento estrutural ausente: {required_element}")
            
            # Verificar DOCTYPE
            if not content.strip().startswith('<!DOCTYPE html>'):
                issues.append("DOCTYPE HTML5 ausente ou incorreto")
            
            # Verificar lang attribute
            if 'lang="pt-BR"' not in content:
                issues.append('Atributo lang="pt-BR" ausente')
            
            # Verificar se há apenas um H1
            h1_count = len(re.findall(r'<h1[^>]*>', content))
            if h1_count == 0:
                issues.append("Nenhum H1 encontrado")
            elif h1_count > 1:
                issues.append(f"Múltiplos H1 encontrados ({h1_count})")
            
        except Exception as e:
            issues.append(f"Erro ao validar estrutura HTML: {e}")
        
        return issues

    def validate_meta_tags(self, html_file: Path) -> List[str]:
        """Valida se as meta tags obrigatórias estão presentes"""
        issues = []
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for meta_tag in self.required_meta:
                if meta_tag == 'charset':
                    if 'charset="UTF-8"' not in content:
                        issues.append("Meta charset UTF-8 ausente")
                elif meta_tag == 'viewport':
                    if 'name="viewport"' not in content:
                        issues.append("Meta viewport ausente")
                elif meta_tag.startswith('og:'):
                    if f'property="{meta_tag}"' not in content:
                        issues.append(f"Open Graph meta ausente: {meta_tag}")
                elif meta_tag.startswith('twitter:'):
                    if f'property="{meta_tag}"' not in content:
                        issues.append(f"Twitter meta ausente: {meta_tag}")
                else:
                    if f'name="{meta_tag}"' not in content:
                        issues.append(f"Meta tag ausente: {meta_tag}")
        
        except Exception as e:
            issues.append(f"Erro ao validar meta tags: {e}")
        
        return issues

    def check_broken_links(self, html_file: Path) -> List[str]:
        """Verifica links quebrados (apenas links locais)"""
        issues = []
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Encontrar todos os links locais
            local_links = re.findall(r'href\s*=\s*["\']([^"\']*)["\']', content)
            
            for link in local_links:
                if link.startswith('http'):
                    continue  # Skip external links
                
                if link.startswith('#'):
                    continue  # Skip anchors
                
                # Resolve relative path
                if link.startswith('../'):
                    link_path = self.articles_dir.parent / link[3:]
                else:
                    link_path = self.articles_dir / link
                
                if not link_path.exists():
                    issues.append(f"Link quebrado: {link}")
        
        except Exception as e:
            issues.append(f"Erro ao verificar links: {e}")
        
        return issues

    def generate_validation_report(self) -> Dict:
        """Gera relatório completo de validação"""
        logging.info("BUSCA: INICIANDO VALIDAÇÃO DE ARTIGOS")
        logging.info("=" * 50)
        
        html_files = list(self.articles_dir.glob("*.html"))
        
        if not html_files:
            logging.error(f"Nenhum arquivo HTML encontrado em {self.articles_dir}")
            return self.report
        
        logging.info(f"Encontrados {len(html_files)} arquivos HTML para validar")
        
        # 1. Verificar duplicatas
        duplicates = self.find_duplicate_articles()
        
        # 2. Validar cada arquivo
        for html_file in html_files:
            logging.info(f"Validando: {html_file.name}")
            
            # Validação CSS
            css_issues = self.validate_css_formatting(html_file)
            if css_issues:
                self.report['css_issues'].append({
                    'file': str(html_file),
                    'issues': css_issues
                })
            
            # Validação estrutura HTML
            structure_issues = self.validate_html_structure(html_file)
            if structure_issues:
                self.report['structure_issues'].append({
                    'file': str(html_file),
                    'issues': structure_issues
                })
            
            # Validação meta tags
            meta_issues = self.validate_meta_tags(html_file)
            if meta_issues:
                self.report['missing_meta'].append({
                    'file': str(html_file),
                    'issues': meta_issues
                })
            
            # Verificação links
            link_issues = self.check_broken_links(html_file)
            if link_issues:
                self.report['broken_links'].append({
                    'file': str(html_file),
                    'issues': link_issues
                })
        
        # 3. Estatísticas
        self.report['statistics'] = {
            'total_files': len(html_files),
            'duplicates_found': len(duplicates),
            'css_issues_count': len(self.report['css_issues']),
            'structure_issues_count': len(self.report['structure_issues']),
            'meta_issues_count': len(self.report['missing_meta']),
            'link_issues_count': len(self.report['broken_links']),
            'validation_date': datetime.now().isoformat()
        }
        
        return self.report

    def print_report(self):
        """Imprime relatório formatado"""
        print("\n" + "=" * 80)
        print("BUSCA: RELATÓRIO DE VALIDAÇÃO DE ARTIGOS")
        print("=" * 80)
        
        stats = self.report['statistics']
        print(f"ESTATÍSTICAS GERAIS:")
        print(f"   Total de arquivos: {stats['total_files']}")
        print(f"   Duplicatas encontradas: {stats['duplicates_found']}")
        print(f"   Arquivos com problemas CSS: {stats['css_issues_count']}")
        print(f"   Arquivos com problemas estruturais: {stats['structure_issues_count']}")
        print(f"   Arquivos com meta tags ausentes: {stats['meta_issues_count']}")
        print(f"   Arquivos com links quebrados: {stats['link_issues_count']}")
        
        # Duplicatas
        if self.report['duplicates']:
            print(f"\nPROCESSANDO ARTIGOS DUPLICADOS ({len(self.report['duplicates'])}):")
            print("-" * 50)
            for i, dup in enumerate(self.report['duplicates'], 1):
                print(f"{i}. {dup['reason']}")
                for file in dup['files']:
                    print(f"   ARQUIVO {Path(file).name}")
                print()
        
        # Problemas CSS
        if self.report['css_issues']:
            print(f"\nCSS PROBLEMAS DE CSS ({len(self.report['css_issues'])}):")
            print("-" * 50)
            for issue in self.report['css_issues']:
                print(f"ARQUIVO {Path(issue['file']).name}")
                for problem in issue['issues']:
                    print(f"   ERRO: {problem}")
                print()
        
        # Problemas estruturais
        if self.report['structure_issues']:
            print(f"\nESTRUTURA PROBLEMAS ESTRUTURAIS ({len(self.report['structure_issues'])}):")
            print("-" * 50)
            for issue in self.report['structure_issues']:
                print(f"ARQUIVO {Path(issue['file']).name}")
                for problem in issue['issues']:
                    print(f"   ERRO: {problem}")
                print()
        
        # Meta tags ausentes
        if self.report['missing_meta']:
            print(f"\nTAG META TAGS AUSENTES ({len(self.report['missing_meta'])}):")
            print("-" * 50)
            for issue in self.report['missing_meta']:
                print(f"ARQUIVO {Path(issue['file']).name}")
                for problem in issue['issues']:
                    print(f"   ERRO: {problem}")
                print()
        
        # Links quebrados
        if self.report['broken_links']:
            print(f"\nLINK LINKS QUEBRADOS ({len(self.report['broken_links'])}):")
            print("-" * 50)
            for issue in self.report['broken_links']:
                print(f"ARQUIVO {Path(issue['file']).name}")
                for problem in issue['issues']:
                    print(f"   ERRO: {problem}")
                print()
        
        # Resumo final
        total_issues = (
            stats['duplicates_found'] +
            stats['css_issues_count'] +
            stats['structure_issues_count'] +
            stats['meta_issues_count'] +
            stats['link_issues_count']
        )
        
        print("=" * 80)
        if total_issues == 0:
            print("SUCESSO: PARABÉNS! Nenhum problema encontrado nos artigos!")
        else:
            print(f"ATENÇÃO  TOTAL DE PROBLEMAS ENCONTRADOS: {total_issues}")
            print("Consulte o relatório acima para detalhes e correções.")
        
        print(f"DATA: Validação realizada em: {stats['validation_date']}")
        print("=" * 80)

    def save_report_to_file(self, filename: str = None):
        """Salva relatório em arquivo JSON"""
        import json
        
        if filename is None:
            json_dir = Path("c:/dev/personal_articles/scr/json")
            json_dir.mkdir(exist_ok=True)
            filename = json_dir / "validation_report.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, ensure_ascii=False, indent=2)
        
        logging.info(f"ARQUIVO Relatório salvo em: {filename}")

def main():
    """Função principal"""
    print("BUSCA: VALIDADOR DE ARTIGOS - DETECTOR DE DUPLICATAS E VALIDAÇÃO CSS")
    print("=" * 70)
    
    # Verificar se estamos no diretório correto
    if not Path("articles").exists():
        print("ERRO: Diretório 'articles' não encontrado!")
        print("Execute este script a partir da raiz do projeto.")
        return
    
    # Executar validação
    validator = ArticleValidator()
    validator.generate_validation_report()
    validator.print_report()
    validator.save_report_to_file()
    
    print("\nSUCESSO: Validação concluída!")
    print("ARQUIVO Log detalhado salvo em: scr/log/validation_report.log")
    print("Relatório JSON salvo em: scr/json/validation_report.json")

if __name__ == "__main__":
    main()





