---
title: "Csonline - Parte Ii - Avanços Contínuos No Projeto"
date: "02/08/2025"
author: "Christian Mulato"
description: "Artigo técnico sobre csonline - parte ii - avanços contínuos no projeto"
category: "Java & Spring"
tags: ['Java', 'Spring', 'Docker', 'APIs', 'Testes', 'Arquitetura']
featured_image: "img/2025_08_02_csonline_parte_ii_avancos_continuos_no_projeto_featured.jpg"
---

# Csonline - Parte Ii - Avanços Contínuos No Projeto

![Acompanhe o progresso](img/image_not_found.png)

Acompanhe o progresso

__Avanços contínuos no projeto__

__[![Christian Mulato, #OPEN_TO_WORK](img/image_not_found.png)](https://www.linkedin.com/in/chmulato/)__

__[Christian Mulato ](https://www.linkedin.com/in/chmulato/)__

Desenvolvedor Java Sênior | Especialista em Back\-end | Jakarta, Spring Boot, REST APIs, Docker | Engenheiro Químico

2 de agosto de 2025

Desde nosso último artigo, o __CSOnline __tem avançado rapidamente\. O que começou como uma aplicação JSF legado agora está se transformando em uma arquitetura moderna e distribuída, com uma clara separação entre __*backend *__e __*frontend*__\. Esta evolução reflete nosso compromisso com boas práticas de desenvolvimento e preparação para os desafios do mercado atual\.

__Backend: Solidez e Maturidade__

Nosso __*backend *__Jakarta EE 10 está mais robusto do que nunca:

- __Migração completa para Jakarta EE__: Atualizamos todos os pacotes javax\.\* para jakarta\.\*, garantindo compatibilidade com os servidores de aplicação mais recentes
- __Persistência aprimorada__: Consolidamos o HSQLDB como nossa solução exclusiva de banco de dados, simplificando a configuração e implantação
- __Inicialização de dados otimizada__: Implementamos um DataInitializer com suporte a múltiplos scripts SQL, proporcionando uma experiência de desenvolvimento mais fluida
- __Documentação extensiva__: Swagger/OpenAPI completamente integrado, permitindo testes interativos de todas as APIs REST
- __Flexibilidade de configuração__: Suporte a ambientes com JTA \(produção\) e RESOURCE\_LOCAL \(desenvolvimento\), documentados detalhadamente

Os endpoints REST agora estão 100% funcionais, com testes unitários abrangentes garantindo a confiabilidade de cada operação CRUD\.

__Frontend: A revolução em Vue\.js__

O grande destaque desta fase é nosso novo __*frontend *__SPA desenvolvido em Vue\.js 3:

- __Arquitetura Composition API__: Utilizando o que há de mais moderno no ecossistema Vue
- __Módulos independentes__: Separação clara entre gestão de usuários, entregadores, empresas, entregas, equipes, SMS/WhatsApp e preços
- __Interface responsiva__: Design moderno que se adapta a qualquer dispositivo
- __Vite como build tool__: Garantindo carregamento rápido e otimizado
- __Sistema completo de navegação__: Fluxo intuitivo desde o login até o logout

O __*frontend *__já está 100% funcional com dados simulados, pronto para integração com os endpoints REST do __*backend*__\. A experiência do usuário foi cuidadosamente elaborada para garantir produtividade e facilidade de uso\.

__Integração e Deploy__

Desenvolvemos scripts PowerShell que automatizam todo o processo de build e deploy:

- __Build integrado__: __*Frontend *__e __*backend *__em um único comando
- __Configuração do WildFly 31__: Scripts para DataSource JDBC e HTTPS/SSL
- __Documentação detalhada__: Instruções passo a passo para desenvolvedores e usuários finais

Nossa documentação inclui diagramas de sequência, guias de configuração e tutoriais completos para quem deseja explorar ou contribuir com o projeto\.

__Próximos passos e oportunidades__

Estamos prestes a iniciar a fase de integração entre o __*frontend *__Vue\.js e o __*backend *__Jakarta EE\. Esta é uma excelente oportunidade para:

- __Desenvolvedores frontend__: Contribuir com componentes Vue\.js, ajustes de UX/UI e animações
- __Especialistas em Jakarta EE__: Refinar endpoints REST, otimizar queries e melhorar a segurança
- __DevOps__: Aprimorar pipelines de CI/CD e estratégias de deploy
- __QA__: Desenvolver testes automatizados E2E com Cypress ou similares

O __CSOnline __está se tornando não apenas um sistema de gestão de entregas, mas uma plataforma completa que demonstra as melhores práticas em desenvolvimento fullstack moderno\.

__Como participar__

Se você se interessou por este projeto:

1. Faça um fork do repositório: [__https://github\.com/chmulato/csonline__](https://github.com/chmulato/csonline)
2. Explore a documentação em doc/INDEX\.md
3. Veja o sistema em funcionamento seguindo o guia no README\.md
4. Proponha melhorias através de Pull Requests ou discussões no Issues

Acreditamos que o desenvolvimento colaborativo gera não apenas software de melhor qualidade, mas também comunidades mais fortes e desenvolvedores mais experientes\.

Acompanhe a evolução do __CSOnline __e faça parte desta jornada de transformação tecnológica\!

\#java \#jakartaee \#vuejs \#spa \#frontend \#backend \#fullstack \#opensource \#hsqldb \#wildfly \#devops \#linkedin \#devcommunity

