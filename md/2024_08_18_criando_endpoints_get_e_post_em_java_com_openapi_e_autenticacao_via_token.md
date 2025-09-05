---
title: "Criando Endpoints Get E Post Em Java Com Openapi E Autenticação Via Token"
date: "18/08/2024"
author: "Christian Mulato"
description: "Artigo técnico sobre criando endpoints get e post em java com openapi e autenticação via token"
category: "Java & Spring"
tags: ['Java', 'Spring', 'APIs', 'DevOps', 'IA']
featured_image: "img/2024_08_18_criando_endpoints_get_e_post_em_java_com_openapi_e_autenticacao_via_token_featured.jpg"
---

# Criando Endpoints Get E Post Em Java Com Openapi E Autenticação Via Token

![Endpoint com Framework Spring Boot utilizando linguagem Java.](img/image_not_found.png)

Endpoint com Framework Spring Boot utilizando linguagem Java\.

__Criando Endpoints GET e POST em Java com OpenAPI e Autenticação via Token__

[![Christian Mulato](img/image_not_found.png)](https://www.linkedin.com/in/chmulato/)

__[Christian Mulato](https://www.linkedin.com/in/chmulato/)__

Desenvolvedor Java Sênior na Develcode

18 de agosto de 2024

__1\. Introdução__

Neste artigo, vamos aprender a criar __*endpoints*__ __GET__ e em uma aplicação Java utilizando Spring Boot e OpenAPI\. Além disso, vamos configurar a autenticação via __token JWT__ para proteger nossos __*endpoints*__\.

__2\. Configuração do Projeto__

Primeiro, vamos configurar nosso projeto __*Spring Boot *__\*\[vide rodapé\]\. No pom\.xml, adicione as seguintes dependências:

![](img/image_not_found.png)

Importando as dependências das bibliotecas necessárias para o Spring Boot\.

__3\. Criando o Endpoint GET__

Vamos criar um __*endpoint*__ __GET__ que retorna uma lista de itens\. Primeiro, crie um controlador:

![](img/image_not_found.png)

Classe Java para a criação do endpoint GET

__4\. Criando o Endpoint POST__

Agora, vamos criar um __*endpoint*__ __POST__ que adiciona um novo item:

![](img/image_not_found.png)

Classe Java para a criação do endpoint POST

__5\. Configurando a Autenticação via Token JWT__

Para proteger nossos __*endpoints*__, vamos configurar a autenticação via__ token JWT__\. Primeiro, crie uma classe para gerar e validar tokens JWT:

![](img/image_not_found.png)

Classe Java para a criação do Token de autenticação\.

__6\. Configurando o Spring Security__

Agora, configure o __Spring Security__ para usar o JWT:

![](img/image_not_found.png)

Classe Java para o controle de acesso ao endpoint\.

__7\. Documentando com OpenAPI__

Finalmente, vamos documentar nossos __*endpoints*__ com __OpenAPI__\. Adicione as anotações no controlador:

![](img/image_not_found.png)

Classe Java com os endpoint GET e POST\.

__8\. Conclusão__

Neste artigo, aprendemos a criar __*endpoints*__ __GET__ e __POST__ em Java utilizando __Spring Boot__ e __OpenAPI__, além de configurar a autenticação via __token JWT__ para proteger nossos __*endpoints*__\. Com essas ferramentas, podemos criar APIs seguras e bem documentadas\.

Nota: 

- __*Spring Boot*__ é um *framework* baseado no [*Spring*](https://spring.io/) que simplifica o desenvolvimento de aplicações Java, eliminando a necessidade de configurações extensas\. Ele oferece uma abordagem opinativa para a configuração, permitindo que os desenvolvedores criem rapidamente aplicações robustas e prontas para produção com configurações padrão sensatas\. Com recursos como inicializadores automáticos, servidores embutidos e uma vasta gama de bibliotecas integradas, o Spring Boot facilita a criação de micros serviços e aplicações web escaláveis e de alta performance\.

