---
title: "Csonline – Parte Iii - Segurança Jwt Autorização Por Papéis E Testes 100 Verdes"
date: "09/08/2025"
author: "Christian Mulato"
description: "Artigo técnico sobre csonline – parte iii - segurança jwt autorização por papéis e testes 100 verdes"
category: "Java & Spring"
tags: ['Java', 'Spring', 'Docker', 'APIs', 'Testes', 'DevOps']
featured_image: "img/2025_08_09_csonline_parte_iii_seguranca_jwt_autorizacao_por_papeis_e_testes_100_verdes_featured.jpg"
---

# Csonline – Parte Iii - Segurança Jwt Autorização Por Papéis E Testes 100 Verdes

![Evolução da aplicação CSOnline - Gestão de Centro de Distribuição (CDs)](img/image_not_found.png)

Evolução da aplicação CSOnline \- Gestão de Centro de Distribuição \(CDs\)

__CSOnline – Parte III: Segurança JWT, Autorização por Papéis e Testes 100% Verdes__

__[![Christian Mulato, #OPEN_TO_WORK](img/image_not_found.png)](https://www.linkedin.com/in/chmulato/)__

__[Christian Mulato ](https://www.linkedin.com/in/chmulato/)__

Desenvolvedor Java Sênior | Especialista em Back\-end | Jakarta, Spring Boot, REST APIs, Docker | Engenheiro Químico

9 de agosto de 2025

__O que evoluiu nesta fase__

Nesta terceira etapa avançamos em segurança, qualidade e preparo para a integração total do __*frontend *Vue __com o __*backend *Jakarta EE__\. O sistema agora possui autenticação JWT robusta, autorização por papéis coerente nos endpoints, suíte de testes completa e scripts de desenvolvimento mais amigáveis\.

Principais destaques:

- Segurança ponta a ponta com __JWT __\(autenticação\) e autorização por papéis \(@RolesAllowed\)
- Matriz de permissões alinhada aos casos de uso reais \(__ADMIN, BUSINESS, COURIER, CUSTOMER__\)
- Testes de controladores, serviços e repositórios estabilizados \(__191 testes passando__\)
- Ambiente de testes isolado \(test\.mode\), base limpa por execução e Jackson registrado
- Endpoint de envio de SMS dedicado e ajustes finos em regras de acesso
- Prontos para integrar o SPA em __Vue __com os endpoints REST e tokens JWT

__Segurança: autenticação e autorização__

- Implementamos um filtro de autenticação JWT \(__*JwtAuthenticationFilter*__\) que valida o token do header Authorization e propaga para o contexto os dados do usuário \(login, role, id\)\.
- Criamos um filtro de autorização \(__*AuthorizationFilter*__\) que lê as anotações @RolesAllowed nos recursos e aplica a decisão com base no papel do usuário autenticado\.
- Ajustamos as anotações de segurança nos controladores para refletir a regra de negócio:

1. __Users:__ criação, atualização e exclusão restritas a ADMIN
2. __Teams: __atualização e exclusão restritas a ADMIN
3. __Prices:__ listagem por business permitida a ADMIN e BUSINESS
4. __SMS:__ deleção e busca por entrega restritas a ADMIN e BUSINESS; novo POST /sms/\{id\}/send

__Resultado:__ respostas 401 e 403 passaram a refletir corretamente a ausência de token ou falta de permissão, e as operações válidas retornam 2xx como esperado\.

__Testes: cobertura confiável do backend__

- *BaseControllerJerseyTest *ativa o modo de teste \(test\.mode\) e garante limpeza da base entre cenários, evitando interferência entre casos\.
- Reescrevemos e ampliamos os testes dos módulos Price \(repository/service/controller\), além de padronizar os de Courier, Customer, Delivery, SMS, Team e User para sempre enviar os headers de autorização corretos\.
- Resolvemos falhas pontuais \(401/403/415/400/500\) com ajustes em headers, content\-type e alinhamento de payloads\.
- Estado atual: 191 testes, todos passando, garantindo estabilidade para a próxima fase\.

__DX e automação__

- Scripts PowerShell simplificam o ciclo de desenvolvimento \(build, deploy no __WildFly 31__, testes e verificação de saúde\)\.
- Logs mais claros com __Log4j2 __ajudam no diagnóstico durante os testes\.
- Documentação atualizada para orientar a configuração de ambiente e execução\.

__Integração Frontend \(Vue\) ↔ Backend \(Jakarta\)__

Com a segurança e os contratos estabilizados, o próximo passo é ligar o __SPA __em __Vue __aos endpoints REST com JWT:

- Cliente HTTP com injeção automática do token JWT
- Tratamento padronizado de erros 401/403 no frontend \(ex\.: redireciono ao login/avisos de permissão\)
- Guards de rota por papel \(ADMIN, BUSINESS, COURIER, CUSTOMER\)
- Habilitar CORS conforme necessário e mapear escopos de cada módulo \(Users, Teams, Deliveries, SMS, Prices\)

__Como contribuir__

- __Frontend:__ integrar telas ao *backend*, melhorar UX/UI, criar guards por papel, estados vazios e feedbacks\.
- __Backend:__ refinar validações, paginação/ordenação de listagens, monitoramento e métricas\.
- __QA:__ cenários E2E \(Cypress/Playwright\) para fluxos críticos de autenticação e autorização\.
- __DevOps:__ pipelines de CI/CD e empacotamento para ambientes \(__dev/homolog/prod__\)\.

Faça um fork do repositório em [__https://github\.com/chmulato/csonline__](https://github.com/chmulato/csonline) e confira a documentação em __doc/INDEX\.md__\. Pull Requests são bem\-vindos\!

