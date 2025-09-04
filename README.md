# 🚀 Christian Mulato Dev Blog

[![Site Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://chmulato.dev)
[![Articles](https://img.shields.io/badge/articles-60-blue.svg)](#estatísticas)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Last Updated](https://img.shields.io/badge/updated-September%202025-informational.svg)](#)

> **Site de artigos técnicos sobre desenvolvimento Java, arquitetura de software e tecnologia moderna.**

Bem-vindo ao repositório do blog técnico do Christian Mulato! Este é um site estático gerado automaticamente a partir de artigos em Markdown, focado em desenvolvimento Java, Spring Boot, arquitetura de microsserviços e tecnologias emergentes.

## 📚 Sobre o Blog

Este blog contém uma coleção curada de artigos técnicos cobrindo:

- **☕ Java & Spring**: Desenvolvimento avançado, Spring Boot, Jakarta EE
- **🏗️ Arquitetura**: Microsserviços, Clean Architecture, Design Patterns  
- **🐳 DevOps**: Docker, Kubernetes, CI/CD, Automação
- **🔧 APIs**: REST, GraphQL, OpenAPI, Documentação
- **🧪 Testes**: TDD, Testes Unitários, Integração
- **🤖 IA & Tecnologia**: Inteligência Artificial aplicada ao desenvolvimento

## 🏗️ Estrutura do Projeto

```
site_artiches/
├── 📄 index.html                    # Página principal do site
├── 📖 README.md                     # Este arquivo
├── 📁 docx/                         # 📜 Artigos originais (176 arquivos DOCX)
├── ⚙️ assets/                       # Recursos estáticos
│   ├── 🎨 css/                     # Estilos CSS
│   │   ├── main.css                # Estilo principal
│   │   └── article.css             # Estilo dos artigos
│   └── 🔧 js/                      # JavaScript
│       ├── main.js                 # Funcionalidades principais
│       └── search.js               # Sistema de busca
├── 📰 articles/                     # Artigos publicados
│   ├── 📄 *.html                   # 60 artigos em HTML
│   └── 📁 img/                     # Recursos dos artigos
│       ├── 🖼️ *.png, *.jpeg        # 216 imagens dos artigos
│       └── 📝 *.md                 # 60 arquivos Markdown originais
└── 🛠️ scr/                         # Scripts de gerenciamento
    ├── 🎛️ site_manager.py          # Gerenciador principal
    ├── 🏗️ build_site.py            # Build completo do site
    ├── 🧹 cleanup.py               # Organização de arquivos
    └── ⚙️ config.json              # Configurações do site
```

## 🛠️ Scripts de Gerenciamento

### 🎛️ Site Manager
Ferramenta principal para gerenciar o site:

```bash
# Converter um artigo específico
python scr/site_manager.py convert "2024_03_06_aplicacao_web_java.md"

# Gerar página index (em desenvolvimento)
python scr/site_manager.py index

# Validar links e recursos (em desenvolvimento)
python scr/site_manager.py validate
```

### 🏗️ Build Completo
Executa o build completo do site:

```bash
python scr/build_site.py
```

**Funcionalidades do build:**
- ✅ Converte todos os arquivos Markdown para HTML
- ✅ Aplica templates responsivos com metadados SEO
- ✅ Processa código com syntax highlighting
- ✅ Gera estrutura de navegação
- ✅ Otimiza imagens e recursos

### 🧹 Limpeza e Organização
```bash
python scr/cleanup.py
```

## 🚀 Como Executar Localmente

### Pré-requisitos
```bash
pip install markdown
pip install pygments  # Para syntax highlighting
```

### Passos de Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/chmulato/personal_articles.git
cd personal_articles/md/site_artiches
```

2. **Execute o build:**
```bash
python scr/build_site.py
```

3. **Abra o site:**
```bash
# Windows
start index.html

# macOS
open index.html

# Linux
xdg-open index.html
```

## 📊 Estatísticas

| Métrica | Valor |
|---------|-------|
| **📰 Artigos Publicados** | 60 |
| **🖼️ Imagens** | 216 |
| **📝 Arquivos Markdown** | 60 |
| **🌐 Páginas HTML** | 60 |
| **📅 Período** | Março 2024 - Setembro 2025 |
| **🔄 Última Atualização** | 04/09/2025 |

### 📈 Distribuição de Conteúdo

- **Java & Spring**: 35 artigos (58%)
- **Arquitetura de Software**: 12 artigos (20%)
- **DevOps & Containers**: 8 artigos (13%)
- **IA & Tecnologia**: 5 artigos (9%)

## 🔧 Tecnologias Utilizadas

### Frontend
- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
- ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

### Build & Processing
- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
- ![Markdown](https://img.shields.io/badge/Markdown-000000?style=flat&logo=markdown&logoColor=white)
- **Pygments** para syntax highlighting
- **Python Markdown** para processamento

### Ferramentas
- **Mammoth**: Conversão DOCX → Markdown
- **Highlight.js**: Syntax highlighting no frontend
- **Inter Font**: Tipografia moderna

## 📋 Roadmap

### ✅ Implementado
- [x] Conversão automática DOCX → Markdown → HTML
- [x] Sistema de build automatizado
- [x] Templates responsivos com SEO
- [x] Syntax highlighting para código
- [x] Organização automática de imagens
- [x] Metadados e frontmatter padronizados

### 🚧 Em Desenvolvimento
- [ ] Sistema de busca avançada
- [ ] Geração automática de índice
- [ ] Filtros por categoria e tags
- [ ] RSS feed
- [ ] Sitemap.xml automático
- [ ] Validação de links e imagens

### 🔮 Planejado
- [ ] Sistema de comentários
- [ ] Newsletter integration
- [ ] Analytics dashboard
- [ ] PWA support
- [ ] Dark mode
- [ ] Internacionalização (EN/PT)

## 🤝 Contribuindo

Este é um projeto pessoal, mas sugestões são bem-vindas!

1. **Fork** o projeto
2. **Clone** sua fork
3. **Crie** uma branch para sua feature
4. **Commit** suas mudanças
5. **Push** para a branch
6. **Abra** um Pull Request

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Sobre o Autor

<div align="center">

![Christian Mulato](https://github.com/chmulato.png?size=150)

**Christian Mulato**  
*Senior Java Developer & Software Architect*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/chmulato/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/chmulato)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:christian.mulato@example.com)

</div>

**Especialidades:**
- ☕ **Java/Spring Boot**: Desenvolvimento de aplicações enterprise
- 🏗️ **Microserviços**: Arquitetura distribuída e escalável  
- 🐳 **DevOps**: Docker, Kubernetes, CI/CD
- 🔧 **APIs REST**: Design e documentação com OpenAPI
- 🧪 **Testes**: TDD, testes de integração e unitários
- 🤖 **IA**: Aplicação de IA no desenvolvimento de software

---

<div align="center">

**🌟 Se este conteúdo foi útil, considere dar uma estrela no repositório!**

*Construído com ❤️ usando Python, Markdown e muito ☕*

**[🚀 Visite o Site](https://chmulato.dev)** | **[📧 Entre em Contato](https://www.linkedin.com/in/chmulato/)**

</div>
