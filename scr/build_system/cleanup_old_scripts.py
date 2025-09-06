#!/usr/bin/env python3
"""
Script de Limpeza - Remove scripts antigos desnecessários
========================================================
Identifica e organiza os scripts Python do sistema.

Autor: Sistema Build
Data: Setembro 2025
"""

import os
import shutil
from pathlib import Path

# Diretórios
SCR_DIR = Path("c:/dev/personal_articles/scr")
OLD_SCRIPTS_DIR = SCR_DIR / "old_scripts"

# Scripts essenciais que devem ser mantidos
ESSENTIAL_SCRIPTS = {
    "build_system/",                    # Novo sistema organizado
    "convert_md_to_html.py",           # Usado pelo novo sistema
    "site_manager.py",                 # Pode ser útil como referência
    "convert_new_articles.py",         # Pode ser útil como backup
    "manage_articles_list.py",         # Pode ser útil como backup
    "artigos_processados.txt",         # Lista de controle existente
    "README.md",                       # Documentação
    "log/",                            # Logs do sistema
    "json/"                            # Dados JSON se existirem
}

# Scripts que podem ser removidos ou movidos
SCRIPTS_TO_CLEANUP = [
    "add_themes_to_articles.py",
    "build_site.py",
    "build_site_intelligent.py", 
    "build_site_professional.py",
    "clean_duplicates.py",
    "clean_duplicates_v2.py",
    "clean_problematic_files.py",
    "clean_unicode.py",
    "convert_all_docx.py",
    "fix_articles.py",
    "fix_articles_with_progress.py",
    "fix_mass_articles.py",
    "format_code_blocks.py",
    "normalize_by_docx.py",
    "professional_converter.py",
    "remove_duplicate_images.py",
    "remove_emojis.py",
    "update_asset_paths.py",
    "update_image_paths.py",
    "validate_articles.py",
    "validate_articles_clean.py"
]

def create_backup_dir():
    """Cria diretório para scripts antigos."""
    OLD_SCRIPTS_DIR.mkdir(exist_ok=True)
    print(f"✓ Diretório de backup criado: {OLD_SCRIPTS_DIR}")

def move_old_scripts():
    """Move scripts antigos para diretório de backup."""
    moved_count = 0
    
    for script_name in SCRIPTS_TO_CLEANUP:
        script_path = SCR_DIR / script_name
        
        if script_path.exists():
            backup_path = OLD_SCRIPTS_DIR / script_name
            
            try:
                shutil.move(str(script_path), str(backup_path))
                print(f"  → Movido: {script_name}")
                moved_count += 1
            except Exception as e:
                print(f"  ✗ Erro ao mover {script_name}: {e}")
    
    print(f"✓ {moved_count} scripts movidos para backup")

def create_readme_backup():
    """Cria README no diretório de backup."""
    readme_content = """# Scripts de Backup - Sistema Antigo

Este diretório contém scripts do sistema anterior de build.

## ⚠️ Status: OBSOLETO

Estes scripts foram substituídos pelo novo sistema organizado em `build_system/`.

## 📁 Conteúdo

Scripts movidos aqui durante a reorganização do sistema de build.
Mantidos apenas como referência histórica.

## 🚀 Novo Sistema

Use o novo sistema em:
```bash
cd build_system/
python build.py --help
```

---
**Backup criado em Setembro 2025**
"""
    
    readme_path = OLD_SCRIPTS_DIR / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✓ README criado no diretório de backup")

def list_remaining_files():
    """Lista arquivos que permaneceram no diretório principal."""
    print("\n📁 Estrutura final do diretório scr/:")
    
    for item in sorted(SCR_DIR.iterdir()):
        if item.name != "old_scripts":
            if item.is_dir():
                print(f"  📁 {item.name}/")
            else:
                print(f"  📄 {item.name}")

def main():
    """Executa limpeza e organização."""
    print("=" * 60)
    print("LIMPEZA E ORGANIZAÇÃO DOS SCRIPTS")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not SCR_DIR.exists():
        print(f"✗ Diretório não encontrado: {SCR_DIR}")
        return
    
    # Criar diretório de backup
    create_backup_dir()
    
    # Mover scripts antigos
    print("\n🔄 Movendo scripts antigos...")
    move_old_scripts()
    
    # Criar README no backup
    create_readme_backup()
    
    # Mostrar estrutura final
    list_remaining_files()
    
    print("\n" + "=" * 60)
    print("✅ LIMPEZA CONCLUÍDA COM SUCESSO")
    print("=" * 60)
    print("\n💡 Para usar o novo sistema:")
    print("   cd build_system/")
    print("   python build.py --status")
    print("   python build.py --new-only")

if __name__ == '__main__':
    main()
