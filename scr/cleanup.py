#!/usr/bin/env python3
"""
Cleanup Script - Organização final dos arquivos do projeto
Localizado em: C:\dev\personal_articles\md\site_artiches\scr\cleanup.py

Este script organiza e faz backup dos scripts antigos.
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

def main():
    print("🧹 ORGANIZANDO ARQUIVOS DO PROJETO")
    print("=" * 50)
    
    # Diretórios
    project_root = Path(__file__).parent.parent.parent.parent  # personal_articles
    site_dir = Path(__file__).parent.parent  # site_artiches
    scr_dir = Path(__file__).parent  # scr
    
    # Criar diretório de backup para scripts antigos
    backup_dir = project_root / "old_scripts"
    backup_dir.mkdir(exist_ok=True)
    
    # Scripts antigos para fazer backup
    old_scripts = [
        "convert_to_markdown.py",
        "convert_md_to_html.py", 
        "convert_from_img_dir.py",
        "format_articles.py",
        "format_articles_fixed.py",
        "clean_articles.py"
    ]
    
    print("📦 Fazendo backup dos scripts antigos...")
    for script in old_scripts:
        old_path = project_root / script
        if old_path.exists():
            backup_path = backup_dir / script
            shutil.move(str(old_path), str(backup_path))
            print(f"✅ Movido: {script} → old_scripts/")
    
    # Criar README para o site
    readme_content = f"""# Christian Mulato Dev Blog

Site de artigos técnicos sobre desenvolvimento Java, arquitetura de software e tecnologia.

## Estrutura do Projeto

```
site_artiches/
├── index.html              # Página principal
├── assets/                 # CSS, JS, fonts
│   ├── css/
│   └── js/
├── articles/               # Artigos HTML
│   └── img/               # Imagens e arquivos MD
└── scr/                   # Scripts de gerenciamento
    ├── site_manager.py    # Gerenciador principal
    ├── build_site.py      # Build completo
    └── cleanup.py         # Organização de arquivos
```

## Scripts Disponíveis

### Site Manager
```bash
python scr/site_manager.py convert [arquivo]  # Converter MD→HTML
python scr/site_manager.py index             # Gerar index.html
python scr/site_manager.py validate          # Validar site
```

### Build Completo
```bash
python scr/build_site.py  # Build completo do site
```

## Estatísticas

- **Artigos convertidos**: 60
- **Imagens**: 218
- **Última atualização**: {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Autor

**Christian Mulato**  
Desenvolvedor Java Sênior  
[LinkedIn](https://www.linkedin.com/in/chmulato/)

---

*Site gerado automaticamente pelos scripts em `scr/`*
"""
    
    readme_path = site_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"📄 README.md criado: {readme_path}")
    
    # Relatório final
    print("\n📊 RELATÓRIO FINAL")
    print("=" * 30)
    print(f"📂 Diretório do site: {site_dir}")
    print(f"🔧 Scripts em: {scr_dir}")
    print(f"📦 Backup de scripts antigos: {backup_dir}")
    print(f"🌐 Artigos HTML: {len(list((site_dir / 'articles').glob('*.html')))} arquivos")
    print(f"📝 Artigos MD: {len(list((site_dir / 'articles' / 'img').glob('*.md')))} arquivos") 
    print(f"� Artigos DOCX: {len(list((site_dir / 'docx').glob('*.docx')))} arquivos")
    print(f"�🖼️  Imagens: {len(list((site_dir / 'articles' / 'img').glob('*.jpeg')))} + {len(list((site_dir / 'articles' / 'img').glob('*.png')))} arquivos")
    
    print("\n🎉 ORGANIZAÇÃO CONCLUÍDA!")
    print("\nPróximos passos:")
    print("1. ✅ Scripts organizados em scr/")
    print("2. ✅ Site funcionando em site_artiches/")
    print("3. ⚠️  Implementar geração automática de index.html")
    print("4. ⚠️  Adicionar sistema de busca e filtros")
    print("5. ⚠️  Melhorar SEO e metadados")

if __name__ == "__main__":
    main()
