#!/usr/bin/env python3
"""
Script para converter todos os arquivos DOCX para HTML usando o conversor profissional
"""

import logging
import time
from pathlib import Path
from professional_converter import ProfessionalDocxConverter

def main():
    """Converte todos os arquivos DOCX"""
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('conversion_log.txt'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    # Diretórios
    workspace = Path(__file__).parent.parent
    docx_dir = workspace / "docx"
    
    # Verificar se o diretório existe
    if not docx_dir.exists():
        logger.error(f"Diretório DOCX não encontrado: {docx_dir}")
        return
    
    # Criar conversor
    converter = ProfessionalDocxConverter()
    
    # Encontrar todos os arquivos DOCX
    docx_files = list(docx_dir.glob("*.docx"))
    
    if not docx_files:
        logger.warning("Nenhum arquivo DOCX encontrado")
        return
    
    logger.info(f"📚 Encontrados {len(docx_files)} arquivos DOCX para conversão")
    
    # Estatísticas
    start_time = time.time()
    converted = 0
    failed = 0
    
    for docx_file in docx_files:
        try:
            logger.info(f"🔄 Processando: {docx_file.name}")
            
            # Converter
            markdown_content, metadata = converter.docx_to_markdown(docx_file)
            
            if markdown_content:
                # Salvar Markdown
                md_file = converter.md_dir / f"{docx_file.stem}.md"
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                # Converter para HTML
                html_content = converter.markdown_to_html(markdown_content, metadata)
                html_file = converter.articles_dir / f"{docx_file.stem}.html"
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                logger.info(f"✅ Convertido: {docx_file.name}")
                converted += 1
            else:
                logger.error(f"❌ Falha na conversão: {docx_file.name}")
                failed += 1
                
        except Exception as e:
            logger.error(f"❌ Erro processando {docx_file.name}: {e}")
            failed += 1
    
    # Estatísticas finais
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info(f"\n{'='*50}")
    logger.info(f"📊 RELATÓRIO DE CONVERSÃO")
    logger.info(f"{'='*50}")
    logger.info(f"Total de arquivos: {len(docx_files)}")
    logger.info(f"Convertidos: {converted}")
    logger.info(f"Falharam: {failed}")
    logger.info(f"Tempo total: {duration:.2f} segundos")
    logger.info(f"Média por arquivo: {duration/len(docx_files):.2f} segundos")
    
    if converted > 0:
        logger.info(f"\n✅ Conversão concluída! {converted} artigos prontos.")
    else:
        logger.warning("\n⚠️ Nenhum arquivo foi convertido com sucesso.")

if __name__ == "__main__":
    main()
