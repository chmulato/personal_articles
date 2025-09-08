# Christian Mulato - Blog Técnico

## Sobre

Este repositório contém o código-fonte e o sistema de compilação do meu blog técnico, que foca em desenvolvimento Java, arquitetura de software e práticas modernas de tecnologia.

**URL do Blog:** [https://chmulato.github.io/personal_articles/](https://chmulato.github.io/personal_articles/)

**Autor:** Christian Mulato  
**Foco do Conteúdo:** Desenvolvimento Java, Arquitetura de Software, DevOps e Inovação Tecnológica  
**Status:** Ativo com mais de 61 artigos publicados

## Artigos

Para uma lista cronológica completa de todos os artigos neste repositório, consulte [ARTICLES.md](ARTICLES.md).

## Visão Geral do Sistema de Compilação

Este projeto fornece um sistema de compilação automatizado que converte artigos técnicos em DOCX para um site HTML completo. O sistema apresenta controle abrangente de processamento para evitar reprocessamento e garantir compilações eficientes.

## Arquitetura do Sistema

### Componentes Principais

O sistema de compilação está organizado em uma estrutura modular em `scr/build_system/`:

```
build_system/
├── core/                              # Módulos de processamento principal
│   ├── docx_converter.py              # Conversor de DOCX para Markdown
│   ├── md_to_html.py                  # Conversor de Markdown para HTML  
│   └── site_builder.py                # Construtor completo do site
├── utils/                             # Módulos utilitários
│   ├── file_manager.py                # Operações do sistema de arquivos
│   ├── normalizer.py                  # Normalização de nomes
│   └── processed_articles_manager.py  # Controle de processamento
├── config/
│   └── settings.py                    # Configuração centralizada
├── build.py                           # Script principal de compilação
├── processed_articles.txt             # Lista de controle de processamento
└── build.log                          # Logs de operação de compilação
```

### Pipeline de Processamento

1. **Conversão DOCX**: Extrai conteúdo e mídia de arquivos DOCX usando Pandoc
2. **Processamento Markdown**: Converte DOCX para Markdown limpo com formatação adequada
3. **Geração HTML**: Transforma Markdown em HTML com realce de sintaxe
4. **Construção do Site**: Gera um site completo com CSS responsivo e navegação
5. **Gerenciamento de Ativos**: Lida com imagens, folhas de estilo e outros arquivos de mídia

## Sistema de Controle de Processamento de Artigos

### Mecanismo de Controle

O sistema implementa controle rigoroso para evitar o reprocessamento de artigos:

- **processed_articles.txt**: Contém 61 artigos processados em formato normalizado
- **Compilações Incrementais**: Processa apenas artigos NÃO presentes na lista de controle
- **Atualizações Automáticas**: Adiciona artigos à lista após processamento bem-sucedido

### Principais Recursos

**Prevenção de Sobreposição**
- Artigos na lista de controle não são reprocessados
- Proteção contra conflitos de arquivos
- Controle granular por artigo individual

**Eficiência de Processamento**  
- Compilações incrementais processam apenas novos artigos
- Tempo de processamento otimizado
- Recursos computacionais preservados

**Flexibilidade**
- Reprocessamento seletivo quando necessário  
- Sincronização com o estado real do arquivo
- Comandos simples de gerenciamento

**Robustez**
- Lista persistente entre execuções
- Registro detalhado de operações
- Validação automática de integridade

### Comandos de Gerenciamento

O utilitário `processed_articles_manager.py` fornece gerenciamento completo da lista:

```bash
# Ver status detalhado
python -m utils.processed_articles_manager status

# Remover artigo para reprocessamento
python -m utils.processed_articles_manager remove nome_do_artigo

# Sincronizar com arquivos HTML existentes
python -m utils.processed_articles_manager sync

# Listar todos os artigos processados
python -m utils.processed_articles_manager list

# Adicionar artigo manualmente
python -m utils.processed_articles_manager add nome_do_artigo
```

## Uso

### Operações Diárias

**Verificar Status do Sistema**
```bash
cd c:\dev\personal_articles\scr\build_system
python build.py --status
```

**Processar Apenas Novos Artigos (Recomendado)**
```bash
python build.py --new-only
```

**Compilação Completa (Todos os Artigos)**
```bash
python build.py
```

### Reprocessando Artigos Específicos

1. Remover da lista de controle:
```bash
python -m utils.processed_articles_manager remove nome_do_artigo
```

2. Executar compilação incremental:
```bash
python build.py --new-only
```

O sistema automaticamente:
- Detecta artigo não presente na lista
- Processa: DOCX → MD → HTML
- Adiciona de volta à lista após sucesso

## Dependências

### Software Necessário
- Python 3.x
- Pandoc (para conversão DOCX)

### Pacotes Python
- markdown
- pygments  
- python-docx
- beautifulsoup4

## Instalação e Configuração

1. Certifique-se de que o Pandoc esteja instalado em seu sistema
2. Instale as dependências Python: `pip install -r requirements.txt`
3. Navegue até o sistema de compilação: `cd scr/build_system`
4. Execute a compilação inicial: `python build.py`

O sistema validará automaticamente as dependências e a estrutura de diretórios na primeira execução.

## Estrutura do Projeto

```
personal_articles/
├── articles/                       # Artigos HTML gerados
│   └── assets/                     # Ativos para os artigos
│       ├── css/                    # Folhas de estilo
│       ├── img/                    # Imagens dos artigos
│       ├── js/                     # Scripts JavaScript
│       └── prompt_img/             # Imagens para prompts
├── docx/                           # Arquivos DOCX de origem (61 arquivos)
├── md/                             # Arquivos Markdown gerados
├── scr/                            # Código-fonte
│   └── build_system/               # Sistema de compilação
├── ARTICLES.md                     # Lista completa de artigos
├── index.html                      # Página inicial do site
└── README.md                       # Documentação do projeto
```

## Migração e Limpeza do Sistema

### Gerenciamento de Arquivos

- **Organização**: Estrutura de diretórios clara e consistente
- **Consolidação**: Arquivos CSS redundantes removidos
- **Padronização**: Estilos e estrutura HTML normalizados
- **Manutenção**: Sistema de temas e responsividade aprimorados

## Status Atual

### Estatísticas de Processamento
- Total de arquivos DOCX: 61
- Artigos processados: 61
- Aguardando processamento: 0

**Estado do Sistema**: Todos os artigos atualmente processados e atualizados

## Visão Geral do Conteúdo

Este blog contém artigos técnicos abrangendo:

- **Java & Spring**: Desenvolvimento avançado, Spring Boot, Jakarta EE
- **Arquitetura de Software**: Microsserviços, Clean Architecture, Padrões de Design
- **DevOps**: Docker, Kubernetes, CI/CD, Automação
- **APIs**: REST, GraphQL, OpenAPI, Documentação
- **Testes**: TDD, Testes Unitários, Integração
- **IA & Tecnologia**: Inteligência Artificial aplicada ao desenvolvimento
- **Mercado**: Análises e tendências do mercado de tecnologia
- **Carreira**: Desenvolvimento profissional e competências técnicas

### Distribuição de Conteúdo

- Java & Spring: ~59%
- Arquitetura de Software: ~20%
- DevOps & Containers: ~14%
- IA & Tecnologia: ~7%
- Mercado & Carreira: Em desenvolvimento

## Recursos do Site

### Sistema de Tema Claro/Escuro

O site inclui um sistema completo de alternância de temas:

**Principais Recursos**
- Botão de alternância no canto superior direito
- Persistência automática entre sessões
- Design responsivo para desktop e mobile
- Transições suaves com animações
- Detecção automática de preferência do sistema

**Implementação Técnica**
- Variáveis CSS para fácil manutenção
- LocalStorage para persistência de preferência do usuário
- Media Queries para detecção de preferência do sistema
- Rótulos ARIA para acessibilidade

**Paleta de Cores**

| Elemento         | Tema Claro  | Tema Escuro |
|------------------|-------------|-------------|
| Fundo Primário   | `#ffffff`   | `#111827`   |
| Fundo Secundário | `#f9fafb`   | `#1f2937`   |
| Texto Primário   | `#1f2937`   | `#f9fafb`   |
| Texto Secundário | `#6b7280`   | `#d1d5db`   |
| Cor de Destaque  | `#2563eb`   | `#3b82f6`   |

## Tecnologias Utilizadas

### Frontend
- HTML5
- CSS3
- JavaScript

### Compilação & Processamento
- Python
- Markdown
- Pygments para destaque de sintaxe
- Python Markdown para processamento

### Ferramentas
- Mammoth: Conversão DOCX → Markdown
- Highlight.js: Destaque de sintaxe no frontend
- Fonte Inter: Tipografia moderna

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para detalhes.

## Sobre o Autor

**Christian Mulato**  
Desenvolvedor Java Sênior & Arquiteto de Software

**Especialidades:**
- Java/Spring Boot: Desenvolvimento de aplicações empresariais
- Microsserviços: Arquitetura distribuída e escalável
- DevOps: Docker, Kubernetes, CI/CD
- APIs REST: Design e documentação com OpenAPI
- Testes: TDD, testes de integração e unitários
- IA: Inteligência Artificial aplicada ao desenvolvimento de software

**Conecte-se:**
- **Blog:** [https://chmulato.github.io/personal_articles/](https://chmulato.github.io/personal_articles/)
- **LinkedIn:** [https://www.linkedin.com/in/chmulato/](https://www.linkedin.com/in/chmulato/)

Este sistema de compilação fornece processamento confiável, eficiente e controlado de artigos técnicos a partir de arquivos DOCX de origem em um site responsivo completo.
