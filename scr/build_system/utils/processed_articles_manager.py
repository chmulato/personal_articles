#!/usr/bin/env python3
"""
Gerenciador da Lista de Controle de Artigos Processados
======================================================
Utilitário para gerenciar quais artigos já foram processados.

Autor: Sistema Build
Data: Setembro 2025
"""

import sys
from pathlib import Path
from datetime import datetime

# Adiciona o diretório build_system ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import *
from utils.normalizer import normalize_filename

class ProcessedArticlesManager:
    """Gerenciador da lista de artigos processados."""
    
    def __init__(self):
        """Inicializa o gerenciador."""
        self.processed_file = PROCESSED_LIST
        ensure_directories()
    
    def load_processed_list(self) -> set:
        """
        Carrega lista de artigos já processados.
        
        Returns:
            set: Conjunto de artigos processados
        """
        processed = set()
        
        if self.processed_file.exists():
            with open(self.processed_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Ignora linhas vazias e comentários
                    if line and not line.startswith('#'):
                        processed.add(line)
        
        return processed
    
    def add_processed_article(self, article_name: str):
        """
        Adiciona artigo à lista de processados.
        
        Args:
            article_name (str): Nome do artigo (será normalizado)
        """
        normalized_name = normalize_filename(article_name)
        
        # Carrega lista atual
        processed = self.load_processed_list()
        
        # Se já está na lista, não faz nada
        if normalized_name in processed:
            return False
        
        # Adiciona à lista
        with open(self.processed_file, 'a', encoding='utf-8') as f:
            f.write(f"{normalized_name}\n")
        
        return True
    
    def remove_processed_article(self, article_name: str):
        """
        Remove artigo da lista de processados (para reprocessar).
        
        Args:
            article_name (str): Nome do artigo
        """
        normalized_name = normalize_filename(article_name)
        
        # Carrega lista atual
        processed = self.load_processed_list()
        
        if normalized_name not in processed:
            return False
        
        # Remove da lista
        processed.remove(normalized_name)
        
        # Reescreve arquivo
        self._write_processed_list(processed)
        
        return True
    
    def is_processed(self, article_name: str) -> bool:
        """
        Verifica se artigo já foi processado.
        
        Args:
            article_name (str): Nome do artigo
            
        Returns:
            bool: True se já processado
        """
        normalized_name = normalize_filename(article_name)
        processed = self.load_processed_list()
        return normalized_name in processed
    
    def get_unprocessed_docx(self) -> list:
        """
        Retorna lista de arquivos DOCX não processados.
        
        Returns:
            list: Arquivos DOCX que precisam ser processados
        """
        if not DOCX_DIR.exists():
            return []
        
        # Busca todos os DOCX
        docx_files = [
            f for f in DOCX_DIR.glob("*.docx") 
            if not f.name.startswith("~")
        ]
        
        # Filtra não processados
        processed = self.load_processed_list()
        unprocessed = []
        
        for docx_file in docx_files:
            normalized_name = normalize_filename(docx_file.stem)
            if normalized_name not in processed:
                unprocessed.append(docx_file)
        
        return unprocessed
    
    def _write_processed_list(self, processed_set: set):
        """
        Reescreve arquivo com lista de processados.
        
        Args:
            processed_set (set): Conjunto de artigos processados
        """
        # Header do arquivo
        header = f"""# Lista de Controle de Artigos Processados
# ==========================================
# Este arquivo controla quais artigos DOCX já foram processados completamente
# através da cadeia: DOCX -> MD -> HTML
#
# IMPORTANTE: 
# - Apenas artigos DOCX que NÃO estão nesta lista serão processados
# - Cada linha representa um artigo já processado (formato normalizado)
# - Para reprocessar um artigo, remova-o desta lista
#
# Formato: nome_normalizado_do_arquivo (sem extensão)
# Data de atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# ==========================================

"""
        
        # Ordena lista para melhor organização
        sorted_processed = sorted(processed_set)
        
        # Escreve arquivo
        with open(self.processed_file, 'w', encoding='utf-8') as f:
            f.write(header)
            for article in sorted_processed:
                f.write(f"{article}\n")
    
    def show_status(self):
        """Mostra status da lista de controle."""
        processed = self.load_processed_list()
        unprocessed = self.get_unprocessed_docx()
        
        total_docx = len(list(DOCX_DIR.glob("*.docx"))) if DOCX_DIR.exists() else 0
        
        print("=" * 60)
        print("📋 STATUS DA LISTA DE CONTROLE")
        print("=" * 60)
        print(f"📁 Arquivo de controle: {self.processed_file}")
        print(f"📊 Total de arquivos DOCX: {total_docx}")
        print(f"✅ Artigos processados: {len(processed)}")
        print(f"⏳ Aguardando processamento: {len(unprocessed)}")
        
        if unprocessed:
            print(f"\n📂 Próximos a processar ({min(10, len(unprocessed))} primeiros):")
            for i, docx_file in enumerate(unprocessed[:10], 1):
                print(f"   {i:2}. {docx_file.name}")
            
            if len(unprocessed) > 10:
                print(f"   ... e mais {len(unprocessed) - 10} arquivos")
        else:
            print("\n✨ Todos os arquivos DOCX já foram processados!")
    
    def sync_with_html_files(self):
        """
        Sincroniza lista com arquivos HTML existentes.
        Útil para reconstruir a lista baseada nos HTMLs gerados.
        """
        if not ARTICLES_DIR.exists():
            print("❌ Diretório de artigos não encontrado")
            return
        
        # Busca arquivos HTML (exceto index.html)
        html_files = [
            f for f in ARTICLES_DIR.glob("*.html")
            if f.name != 'index.html'
        ]
        
        # Extrai nomes normalizados
        html_articles = set()
        for html_file in html_files:
            normalized_name = html_file.stem  # Remove .html
            html_articles.add(normalized_name)
        
        # Carrega lista atual
        current_processed = self.load_processed_list()
        
        # Mostra diferenças
        only_in_html = html_articles - current_processed
        only_in_list = current_processed - html_articles
        
        print("=" * 60)
        print("🔄 SINCRONIZAÇÃO COM ARQUIVOS HTML")
        print("=" * 60)
        print(f"📊 Arquivos HTML encontrados: {len(html_articles)}")
        print(f"📋 Na lista de controle: {len(current_processed)}")
        
        if only_in_html:
            print(f"\n➕ Arquivos HTML sem registro na lista ({len(only_in_html)}):")
            for article in sorted(only_in_html):
                print(f"   + {article}")
        
        if only_in_list:
            print(f"\n➖ Na lista mas sem HTML correspondente ({len(only_in_list)}):")
            for article in sorted(only_in_list):
                print(f"   - {article}")
        
        # Pergunta se quer sincronizar
        if only_in_html or only_in_list:
            print(f"\n❓ Sincronizar lista com arquivos HTML existentes? (s/N)")
            response = input().lower().strip()
            
            if response in ['s', 'sim', 'y', 'yes']:
                # Atualiza lista para coincidir com HTMLs
                self._write_processed_list(html_articles)
                print("✅ Lista sincronizada com arquivos HTML existentes!")
            else:
                print("❌ Sincronização cancelada")
        else:
            print("\n✅ Lista já está sincronizada com arquivos HTML!")

def main():
    """Função principal para uso via linha de comando."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Gerenciador da lista de controle de artigos processados'
    )
    
    parser.add_argument(
        'action',
        choices=['status', 'add', 'remove', 'sync', 'list'],
        help='Ação a executar'
    )
    
    parser.add_argument(
        'article_name',
        nargs='?',
        help='Nome do artigo (para add/remove)'
    )
    
    args = parser.parse_args()
    
    manager = ProcessedArticlesManager()
    
    if args.action == 'status':
        manager.show_status()
    
    elif args.action == 'sync':
        manager.sync_with_html_files()
    
    elif args.action == 'list':
        processed = manager.load_processed_list()
        print("📋 Artigos processados:")
        for article in sorted(processed):
            print(f"  • {article}")
    
    elif args.action == 'add':
        if not args.article_name:
            print("❌ Nome do artigo é obrigatório para 'add'")
            return
        
        if manager.add_processed_article(args.article_name):
            print(f"✅ Artigo adicionado: {normalize_filename(args.article_name)}")
        else:
            print(f"ℹ️ Artigo já estava na lista: {normalize_filename(args.article_name)}")
    
    elif args.action == 'remove':
        if not args.article_name:
            print("❌ Nome do artigo é obrigatório para 'remove'")
            return
        
        if manager.remove_processed_article(args.article_name):
            print(f"✅ Artigo removido da lista: {normalize_filename(args.article_name)}")
            print("ℹ️ Agora pode ser reprocessado no próximo build")
        else:
            print(f"❌ Artigo não estava na lista: {normalize_filename(args.article_name)}")

if __name__ == '__main__':
    main()
