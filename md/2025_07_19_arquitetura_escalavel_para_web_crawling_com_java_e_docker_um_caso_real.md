---
title: "Arquitetura Escalável Para Web Crawling Com Java E Docker - Um Caso Real"
date: "19/07/2025"
author: "Christian Mulato"
description: "Artigo técnico sobre arquitetura escalável para web crawling com java e docker - um caso real"
category: "Java & Spring"
tags: ['Java', 'Spring', 'Docker', 'Kubernetes', 'APIs', 'Testes']
featured_image: "img/2025_07_19_arquitetura_escalavel_para_web_crawling_com_java_e_docker_um_caso_real_featured.jpg"
---

# Arquitetura Escalável Para Web Crawling Com Java E Docker - Um Caso Real

![Extraia dados da web com eficiência: veja como uma API moderna com Java e Docker resolve esse desafio.](img/image_not_found.png)

Extraia dados da web com eficiência: veja como uma API moderna com Java e Docker resolve esse desafio\.

__Arquitetura Escalável para Web Crawling com Java e Docker: Um Caso Real__

__[![Christian Mulato, #OPEN_TO_WORK](img/image_not_found.png)](https://www.linkedin.com/in/chmulato/)__

__[Christian Mulato ](https://www.linkedin.com/in/chmulato/)__

Desenvolvedor Java Sênior | Especialista em Back\-end | Jakarta, Spring Boot, REST APIs, Docker | Engenheiro Químico

19 de julho de 2025

Como projetar um sistema de crawling moderno, assíncrono e escalável com Spring Boot, RabbitMQ e Docker

__Introdução__

Neste artigo, apresento a arquitetura por trás da __Web Crawler API__, um projeto open source construído em Java que realiza buscas inteligentes e paralelas na web\. Ele foi desenvolvido para ser confiável, observável e facilmente escalável, aproveitando o melhor do ecossistema Spring, mensageria com RabbitMQ e infraestrutura com Docker/Kubernetes\.

__Uma História para Entender a Aplicação__

Imagine que você está pesquisando sobre "novas tecnologias em energia solar"\. Você entra em dezenas de sites, blogs e fóruns, abrindo página por página manualmente e procurando por qualquer menção relevante\. Isso pode levar horas, dias ou até semanas\.

Agora, imagine que você tem um assistente digital, super\-rápido, que consegue fazer isso em segundos\. Você diz a ele: "procure por 'energia solar bifacial' em todos os sites especializados"\. Esse assistente então visita automaticamente centenas de páginas, lê o conteúdo e te entrega uma lista com todas as URLs que contêm esse termo\.

Esse é o papel da __Web Crawler API__: um sistema automatizado que pode ser usado por empresas, pesquisadores ou desenvolvedores para encontrar conteúdo específico na web, de forma segura, escalável e com resultados em tempo real\.

__Motivação__

A maioria dos crawlers é feita com scripts monolíticos que não escalam, falham silenciosamente ou geram sobrecarga no servidor alvo\. O objetivo aqui foi criar uma __API REST moderna__, com:

- Processamento assíncrono
- Escalabilidade horizontal
- Separação de responsabilidades
- Monitoramento e logs estruturados
- Deploy simplificado com Docker

__Visão Geral da Arquitetura__

┌───────────────┐     ┌───────────────┐     ┌───────────────┐

│   Controller  │ ─▶ │   Service     │ ─▶  │   RabbitMQ    │

│ \(API REST\)    │     │ \(Negócio\)     │     │ \(Fila de Tarefas\)

└───────────────┘     └───────────────┘     └───────────────┘

                                              ▼

                                         ┌──────────────┐

                                         │    Worker    │

                                         │ \(Crawling\)   │

                                         └──────────────┘

                                              ▼

                                        Banco de Dados H2 

__Componentes Principais__

__Spring Boot 3\.x__

Framework principal da aplicação, usando:

- Spring Web: criação da API REST
- Spring Data JPA: abstração da camada de dados
- Spring AMQP: integração com RabbitMQ
- Spring Actuator: métricas e health check

__RabbitMQ__

Message broker que permite:

- Execução assíncrona
- Retentativa em falhas
- Paralelismo com múltiplos workers

__JSoup__

Parser HTML usado pelos workers para extrair e analisar conteúdo das páginas\.

__Docker e Docker Compose__

Permitem:

- Ambientes isolados para testes/desenvolvimento
- Execução de todos os serviços com um comando

docker\-compose up \-\-build \-d 

__Fluxo de Execução__

1. Cliente envia POST /crawl com um termo de busca
2. API gera um ID único e envia mensagem ao RabbitMQ
3. Worker escuta fila, inicia o crawling
4. URLs contendo o termo são armazenadas
5. Cliente pode consultar progresso em tempo real com GET /crawl/\{id\}

__Escalabilidade__

- __Workers são stateless__ → podem ser replicados horizontalmente
- __RabbitMQ suporta múltiplas filas e concorrência alta__
- __Separação entre API e crawler__ → desacoplamento total

__Observabilidade__

- Logs estruturados \(Spring Boot \+ Logback\)
- Health checks e métricas em /actuator
- RabbitMQ com painel web \(localhost:15672\)
- Swagger UI para testes interativos da API

__Testes e Qualidade__

- __Cobertura de código: >90%__ com JUnit 5, Mockito, Testcontainers
- __Validação de regras de negócio e concorrência__
- __Execução:__

mvn test

mvn jacoco:report 

__Deploy__

- __Local:__ Docker Compose
- __Produção:__ Kubernetes com Helm

helm install crawler\-api \./helm/web\-crawler\-api 

__Conclusão__

A arquitetura escalável e desacoplada da Web Crawler API mostra como é possível construir sistemas robustos com tecnologias modernas do ecossistema Java\. O uso de mensageria e containers garante performance e manutenibilidade, enquanto a separação de responsabilidades facilita testes, observação e evolução contínua\.

➡️ Projeto completo no GitHub: [__github\.com/chmulato/web\-crawler\-api__](https://github.com/chmulato/Spring_Web_Crawler)

*Autor: Christian Vladimir Uhdre Mulato*

[__LinkedIn__](https://www.linkedin.com/in/chmulato) · [__GitHub__](https://github.com/chmulato) · Campo Largo, PR \- Brasil

