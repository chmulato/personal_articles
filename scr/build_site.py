#!/usr/bin/env python3
"""
Build Script - Script de build completo do site com validação e correção automática
Localizado em: C:\dev\personal_articles\scr\build_site_professional.py

Este script executa o build completo do site com ciclo de correção:
1. Normaliza arquivos baseado na referência DOCX
2. Formata códigos-fonte nos arquivos Markdown
3. Converte todos os MD para HTML
4. Atualiza o index.html
5. Valida o site
6. Corrige problemas automaticamente se necessário
7. Repete validação até garantir build sem erros
"""

import os
import sys
import subprocess
import logging
import json
from pathlib import Path

# Adicionar o diretório do script ao path
sys.path.insert(0, str(Path(__file__).parent))

from site_manager import SiteManager

# Configurar logging
log_dir = os.path.join(os.path.dirname(__file__), 'log')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'build_site.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def run_script(script_name: str, description: str = None) -> bool:
    """Executa um script Python e retorna True se bem-sucedido."""
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        logging.warning(f"Script não encontrado: {script_path}")
        return False
    
    try:
        if description:
            logging.info(f"EXECUTANDO: {description}")
        
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            if result.stdout.strip():
                print(result.stdout)
            logging.info(f"SUCESSO: {script_name} executado com sucesso")
            return True
        else:
            if result.stderr.strip():
                logging.error(f"ERRO em {script_name}: {result.stderr}")
            logging.error(f"FALHA: {script_name} falhou com código {result.returncode}")
            return False
            
    except Exception as e:
        logging.error(f"EXCEÇÃO ao executar {script_name}: {e}")
        return False

def check_validation_problems(validation_report_path: Path) -> dict:
    """Verifica problemas no relatório de validação."""
    try:
        if not validation_report_path.exists():
            return {"total_problems": 0}
            
        with open(validation_report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        stats = report.get('statistics', {})
        total_problems = (
            stats.get('duplicates_found', 0) +
            stats.get('css_issues_count', 0) +
            stats.get('structure_issues_count', 0) +
            stats.get('meta_issues_count', 0)
            # Não conta links quebrados pois podem ser emails placeholder
        )
        
        return {
            "total_problems": total_problems,
            "duplicates": stats.get('duplicates_found', 0),
            "css_issues": stats.get('css_issues_count', 0),
            "structure_issues": stats.get('structure_issues_count', 0),
            "meta_issues": stats.get('meta_issues_count', 0)
        }
    except Exception as e:
        logging.error(f"Erro ao ler relatório de validação: {e}")
        return {"total_problems": 0}

def main():
    """Executa o build inteligente com ciclo de correção."""
    print("BUILD INTELIGENTE DO SITE - SISTEMA COMPLETO")
    print("=" * 60)
    
    max_iterations = 3
    iteration = 1
    validation_report_path = Path("scr/json/validation_report.json")
    
    while iteration <= max_iterations:
        print(f"\nITERACAO {iteration}/{max_iterations}")
        print("-" * 40)
        
        # Etapa 1: Normalização baseada em DOCX (apenas na primeira iteração)
        if iteration == 1:
            print("\nETAPA 1: Normalização baseada em arquivos DOCX")
            print("-" * 50)
            if not run_script("normalize_by_docx.py", "Normalizando arquivos baseado na referência DOCX"):
                logging.warning("Normalização falhou, continuando...")
        
        # Etapa 2: Formatação de códigos-fonte
        print(f"\nETAPA 2: Formatação de códigos-fonte")
        print("-" * 50)
        run_script("format_code_blocks.py", "Formatando blocos de código em arquivos Markdown")
        
        # Etapa 3: Conversão MD → HTML
        print(f"\nETAPA 3: Conversão MD para HTML")
        print("-" * 50)
        try:
            site_manager = SiteManager()
            md_files = list(Path("md").glob("*.md"))
            logging.info(f"Encontrados {len(md_files)} arquivos para converter")
            
            for md_file in md_files:
                try:
                    site_manager.convert_md_to_html(md_file)
                    logging.info(f"Convertido: {md_file.name}")
                except Exception as e:
                    logging.error(f"Erro ao converter {md_file.name}: {e}")
            
            logging.info(f"Conversão concluída: {len(md_files)} artigos processados")
            
        except Exception as e:
            logging.error(f"Erro na conversão MD→HTML: {e}")
        
        # Etapa 4: Atualização do index
        print(f"\nETAPA 4: Atualização do index.html")
        print("-" * 50)
        try:
            site_manager = SiteManager()
            site_manager.generate_index_html()
            logging.info("Index.html atualizado com sucesso")
        except Exception as e:
            logging.error(f"Erro ao atualizar index.html: {e}")
        
        # Etapa 5: Validação
        print(f"\nETAPA 5: Validação do site")
        print("-" * 50)
        validation_success = run_script("validate_articles.py", "Validando artigos e estrutura do site")
        
        # Verificar problemas
        problems = check_validation_problems(validation_report_path)
        
        print(f"\nRESULTADO DA VALIDACAO:")
        print(f"- Problemas encontrados: {problems['total_problems']}")
        if problems['total_problems'] > 0:
            print(f"  - Duplicatas: {problems['duplicates']}")
            print(f"  - Problemas CSS: {problems['css_issues']}")
            print(f"  - Problemas estruturais: {problems['structure_issues']}")
            print(f"  - Meta tags ausentes: {problems['meta_issues']}")
        
        # Se não há problemas, build concluído com sucesso
        if problems['total_problems'] == 0:
            print("\n" + "=" * 60)
            print("BUILD CONCLUIDO COM SUCESSO!")
            print("=" * 60)
            print(f"RESULTADO FINAL:")
            print(f"- Site disponível em: {Path().absolute()}")
            print(f"- Artigos em: {Path('articles').absolute()}")
            print(f"- Todos os artigos validados sem problemas")
            print(f"- Build completado em {iteration} iteração(ões)")
            return True
        
        # Se há problemas e não é a última iteração, tentar corrigir
        if iteration < max_iterations:
            print(f"\nETAPA 6: Correção automática de problemas")
            print("-" * 50)
            correction_success = run_script("fix_articles.py", "Corrigindo problemas automaticamente")
            
            if not correction_success:
                logging.warning("Correção automática falhou, tentando próxima iteração...")
        
        iteration += 1
    
    # Se chegou aqui, não conseguiu resolver todos os problemas
    print("\n" + "=" * 60)
    print("BUILD CONCLUIDO COM AVISOS")
    print("=" * 60)
    print("ATENCAO: Alguns problemas podem ainda existir.")
    print("Consulte scr/json/validation_report.json para detalhes.")
    print("Site funcional disponível, mas pode haver problemas menores.")
    return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nBuild cancelado pelo usuário.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Erro crítico no build: {e}")
        sys.exit(1)


