# Sistema de Conversão Controlada de Artigos - Versão Simplificada

Sistema simplificado que converte apenas artigos DOCX novos (não listados em `artigos_processados.txt`) para HTML.

## 📁 Estrutura

```
c:\dev\personal_articles\
├── docx/                    # Arquivos DOCX originais
├── md/                      # Arquivos Markdown intermediários
├── articles/                # Arquivos HTML finais
└── scr/                     # Scripts simplificados
    ├── artigos_processados.txt   # Lista de controle
    ├── convert_new_articles.py   # Conversor principal
    └── manage_articles_list.py   # Gerenciador da lista
```

## 🚀 Scripts Principais

### 1. **convert_new_articles.py** - Conversão Automática
Processa apenas artigos DOCX que não estão na lista.

```bash
python scr/convert_new_articles.py
```

### 2. **manage_articles_list.py** - Gerenciamento
```bash
# Ver status
python scr/manage_articles_list.py status

# Sincronizar lista com HTMLs existentes
python scr/manage_articles_list.py sync

# Adicionar artigo manualmente
python scr/manage_articles_list.py add "nome_artigo"
```

## 💡 Funcionamento

1. **Lista de Controle**: `artigos_processados.txt` contém nomes dos artigos já convertidos
2. **Normalização**: Nomes são normalizados (acentos removidos, espaços viram underscore)
3. **Conversão Seletiva**: Só processa DOCX não listados
4. **Atualização Automática**: Adiciona automaticamente à lista após conversão

## 📊 Status Atual
- **57 artigos** já processados
- **25 artigos novos** identificados
- **Sistema funcionando** sem emojis ou caracteres especiais

## ⚡ Uso Rápido

```bash
# Ver o que precisa ser processado
python scr/manage_articles_list.py status

# Converter apenas os novos
python scr/convert_new_articles.py
```

---
**Versão Simplificada - 2025-09-05**
