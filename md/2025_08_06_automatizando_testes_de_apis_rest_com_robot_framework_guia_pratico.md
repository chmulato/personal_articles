---
title: "Automatizando Testes De Apis Rest Com Robot Framework - Guia Prático"
date: "06/08/2025"
author: "Christian Mulato"
description: "Artigo técnico sobre automatizando testes de apis rest com robot framework - guia prático"
category: "Java & Spring"
tags: ['Java', 'Spring', 'Docker', 'APIs', 'Testes', 'Arquitetura']
featured_image: "img/2025_08_06_automatizando_testes_de_apis_rest_com_robot_framework_guia_pratico_featured.jpg"
---

# Automatizando Testes De Apis Rest Com Robot Framework - Guia Prático

![QA automatizando testes de API com Robot Framework](img/image_not_found.png)

QA automatizando testes de API com Robot Framework

__Automatizando Testes de APIs REST com Robot Framework: Guia Prático__

__[![Christian Mulato, #OPEN_TO_WORK](img/image_not_found.png)](https://www.linkedin.com/in/chmulato/)__

__[Christian Mulato ](https://www.linkedin.com/in/chmulato/)__

Desenvolvedor Java Sênior | Especialista em Back\-end | Jakarta, Spring Boot, REST APIs, Docker | Engenheiro Químico

6 de agosto de 2025

__A Rotina de Ana, a QA que Mudou Tudo__

Ana era QA sênior numa startup de __*fintech *__em crescimento acelerado\. Todos os dias, ela chegava no escritório às 8h e já sabia o que a esperava: uma lista interminável de endpoints para testar manualmente\.

“GET /users/123”,

“POST /transactions”,

“PUT /accounts/456”

… Ana abria o Postman, configurava headers, montava payloads JSON, executava requests e anotava resultados numa planilha\. Eram mais de 50 endpoints, e cada deploy significava testar tudo novamente\.

__O pior?__ Sexta\-feira às 18h, deploy em produção\. Ana ficava até tarde validando cada endpoint crítico, um por um, enquanto o time de desenvolvimento já havia ido embora\. Se algo falhasse, rollback e fim de semana trabalhando\.

Um dia, após mais um deploy tardio que se estendeu pela madrugada, Ana decidiu: “Tem que ter um jeito melhor\.”

Foi então que ela descobriu o Robot Framework\. Em duas semanas, Ana automatizou todos os testes de API\. O que antes levava 4 horas, agora executava em 15 minutos\. Deploys de sexta viraram rotina tranquila, e Ana recuperou seus fins de semana\.

Hoje, Ana é referência em automação na empresa\. E tudo começou com uma simples keyword: 

“GET Deve Retornar 200”

O Robot Framework oferece uma abordagem baseada em palavras\-chave para automação de testes de __APIs RESTful__, combinando simplicidade de sintaxe com funcionalidades robustas\. Este guia demonstra como implementar testes automatizados legíveis e extensíveis\.

__Requisitos Técnicos__

__Ambiente necessário:__

- Python 3\.8 ou superior
- pip \(gerenciador de pacotes Python\)
- Robot Framework
- Requests Library

__Configuração do Ambiente__

pip install robotframework

pip install robotframework\-requests

__Arquitetura do Projeto__

tests/

├── resources/

│   └── keywords\.robot

├── suites/

│   └── api\_tests\.robot

└── variables/

    └── config\.robot

__Configuração de Variáveis__

__Arquivo: variables/config\.robot__

\*\*\* Variables \*\*\*

$\{BASE\_URL\}

https://api\.seuprojeto\.com/v1

__Implementação de Keywords Reutilizáveis__

__Arquivo: resources/keywords\.robot__

\*\*\* Settings

\*\*\* Library    RequestsLibrary

\*\*\* Keywords

\*\*\* Iniciar Sessão na API     Create Session    api    $\{BASE\_URL\}

GET Deve Retornar 200     \[Arguments\]    $\{endpoint\}     $\{response\}=    

GET On Session    api    $\{endpoint\}     Should Be Equal As Integers    

$\{response\.status\_code\}    200

__Casos de Teste__

__Arquivo: suites/api\_tests\.robot__

\*\*\* Settings \*\*\*

Resource    \.\./variables/config\.robot

Resource    \.\./resources/keywords\.robot

Suite Setup    Iniciar Sessão na API

\*\*\* Test Cases \*\*\*

Testar Endpoint de Status

GET Deve Retornar 200    /status

Testar Endpoint de Usuário

GET Deve Retornar 200    /users/1

__Execução dos Testes__

robot \-d results tests/suites/api\_tests\.robot

O comando gera um relatório HTML detalhado em results/report\.html com status de execução e métricas de performance\.

__Vantagens da Implementação__

- __Legibilidade:__ Sintaxe próxima à linguagem natural, facilitando compreensão por equipes não técnicas
- __Modularidade:__ Keywords reutilizáveis reduzem duplicação de código
- __Integração:__ Compatibilidade nativa com pipelines CI/CD
- __Relatórios:__ Documentação automática de resultados

__Integração com CI/CD__

__Exemplo de GitHub Actions:__

name: API Tests

on: \[push\]

jobs:

  test:

    runs\-on: ubuntu\-latest

    steps:

      \- uses: actions/checkout@v2

      \- name: Set up Python

        uses: actions/setup\-python@v2

        with:

          python\-version: 3\.11

      \- name: Install dependencies

        run: |

          pip install robotframework robotframework\-requests

      \- name: Run tests

        run: robot tests/suites/api\_tests\.robot

__Conclusão__

O __Robot Framework__ oferece uma solução robusta para automação de testes de APIs REST, combinando sintaxe acessível com funcionalidades empresariais\. A implementação de testes automatizados resulta em maior confiabilidade, redução de tempo de validação e melhoria contínua da qualidade do software\.

__Principais benefícios alcançados:__

- Redução significativa no tempo de execução de testes
-  Padronização de processos de validação
- Documentação automática de cenários de teste
- Integração seamless com ferramentas de desenvolvimento

__Recursos Adicionais: __

- Documentação oficial: [__Robot Framework__](https://robotframework.org/)
- Biblioteca de requisições: Requests Library

