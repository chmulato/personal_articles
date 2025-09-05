---
title: "Do Caus Manual À Confiança Autamatizada"
date: "20/08/2025"
author: "Christian Mulato"
description: "Artigo técnico sobre do caus manual à confiança autamatizada"
category: "Java & Spring"
tags: ['Java', 'Spring', 'Docker', 'APIs', 'Testes', 'Arquitetura']
featured_image: "img/2025_08_20_do_caus_manual_a_confianca_autamatizada_featured.jpg"
---

# Do Caus Manual À Confiança Autamatizada

![Automação de testes de API no CSOnline](img/image_not_found.png)

Automação de testes de API no CSOnline

__Da Necessidade ao Sistema: Como Construímos uma Suite de Testes Automatizados para APIs REST__

__[![Christian Mulato, #OPEN_TO_WORK](img/image_not_found.png)](https://www.linkedin.com/in/chmulato/)__

__[Christian Mulato ](https://www.linkedin.com/in/chmulato/)__

Desenvolvedor Java Sênior | Especialista em Back\-end | Jakarta, Spring Boot, REST APIs, Docker | Engenheiro Químico

20 de agosto de 2025

__1\.1     O Desafio Inicial__

Durante o desenvolvimento do __CSOnline__, um sistema de gestão de entregas enterprise, nos deparamos com um problema comum mas crítico: como garantir que nossas APIs REST funcionassem consistentemente durante o desenvolvimento iterativo?

Com 7 módulos \(Usuários, Entregadores, Clientes, Entregas, Equipes, SMS e Preços\) e múltiplos endpoints CRUD, testar manualmente cada funcionalidade a cada deploy tornou\-se insustentável\.

__1\.2     A Primeira Abordagem__

Tudo começou com um script simples: __test\-couriers\.ps1__\. Era interativo, testava apenas um endpoint e requeria input manual\. Funcionava, mas não escalava\.

\# Primeira versão \- manual e limitada

Write\-Host "Testando endpoint de couriers\.\.\."

$response = Invoke\-RestMethod \-Uri "http://localhost:8080/csonline/api/couriers"

__1\.3     A Virada: Pensamento Sistemático__

Em agosto de 2025, decidimos abordar o problema de forma estruturada\. A ideia* *foi simples: se temos padrões na API, podemos ter padrões nos testes\.

__Decisões arquiteturais tomadas:__

- __Um script por endpoint__ \- Cada módulo teria seu próprio script de teste
- __Operações CRUD completas__ \- Não apenas GET, mas POST, PUT e DELETE
- __Tratamento de erros padronizado__ \- Feedback claro e actionable
- __Automação total__ \- Zero interação manual

__1\.4     A Implementação__

Em uma tarde intensa, nasceram 7 scripts especializados:

- test\-users\.ps1
- test\-customers\.ps1
- test\-deliveries\.ps1
- test\-teams\.ps1
- test\-sms\.ps1
- test\-login\.ps1
- health\-check\-endpoints\.ps1

Cada script seguia o mesmo padrão:

function Test\-EntityCRUD \{

    param\(\[string\]$BaseUrl, \[string\]$Entity\)

    

    try \{

        \# GET \- Lista

        $list = Invoke\-RestMethod \-Uri "$BaseUrl/$Entity"

        Write\-Host "GET /$Entity : SUCESSO \($\($list\.Count\) registros\)" \-ForegroundColor Green

        

        \# GET \- Individual \(se lista não estiver vazia\)

        if \($list\.Count \-gt 0\) \{

            $individual = Invoke\-RestMethod \-Uri "$BaseUrl/$Entity/$\($list\[0\]\.id\)"

            Write\-Host "GET /$Entity/\{id\} : SUCESSO" \-ForegroundColor Green

        \}

        

        \# POST, PUT, DELETE\.\.\.

        

    \} catch \{

        Write\-Host "ERRO em $Entity : $\($\_\.Exception\.Message\)" \-ForegroundColor Red

```json
\}

\}
```

__1\.5     As Ferramentas de Orquestração__

Não bastava ter scripts individuais\. Precisávamos de ferramentas para executá\-los de forma inteligente:

- __test\-all\-endpoints\.ps1__ \- O maestro que executa todos os testes em sequência, com opções de filtro\.
- __health\-check\-endpoints\.ps1__ \- Diagnóstico rápido que gera relatórios de status\.
- __run\-tests\.ps1__ \- Interface simplificada na raiz do projeto\.

__1\.6     As Descobertas__

Os testes revelaram insights valiosos:

- __Taxa de sucesso: 80%__ \(8 de 10 endpoints funcionando\)
- __Problemas identificados:__ Serialização circular, endpoints individuais com 404
- __Padrões de falha:__ __*LocalDateTime*__ causando problemas de __*deserialização*__

__1\.7     Os Benefícios Realizados__

- __Detecção proativa de problemas__ \- Bugs descobertos antes do deploy
- __Feedback imediato__ \- Saber em segundos se uma mudança quebrou algo
- __Documentação viva__ \- Os testes servem como especificação da API
- __*Onboarding *facilitado__ \- Novos desenvolvedores entendem rapidamente o estado do sistema

__1\.8     Lições Aprendidas__

__Técnicas:__

- __*PowerShell *__é uma ferramenta poderosa para automação de testes de API
- Padronização é fundamental para manutenibilidade
- Feedback colorido e estruturado acelera o debugging

__Organizacionais:__

- Investir tempo em automação de testes economiza horas de trabalho manual
- Testes devem ser executáveis por qualquer membro da equipe
- Documentação de testes é tão importante quanto a documentação da API

__1\.9     O Resultado__

Hoje, qualquer mudança no __CSOnline __pode ser validada em minutos:

\# Um comando para testar tudo

\.\\run\-tests\.ps1

\# Ou verificação rápida de saúde

\.\\run\-tests\.ps1 \-HealthCheck

__1\.10  Próximos Passos__

A jornada não para aqui\. Estamos expandindo para:

- Testes de carga automatizados
- Integração com CI/CD
- Testes de contratos com Pact
- Monitoramento de performance

__1\.11  Reflexão Final__

Construir ferramentas de teste não é apenas sobre encontrar bugs\. É sobre criar confiança\. Confiança para __*refatorar*__, para experimentar, para inovar\.

No desenvolvimento de software, a pergunta não é “se” algo vai quebrar, mas “quando”\. Ter uma rede de segurança robusta transforma o medo de mudança em coragem para evolução\.

__1\.12  Recursos e Contato__

__Call to Action:__ E você, como garante a qualidade das suas APIs durante o desenvolvimento? Compartilhe suas estratégias nos comentários\!

*Artigo baseado na experiência real de desenvolvimento do sistema CSOnline \- um projeto enterprise de gestão de entregas com Jakarta EE, Vue 3 e WildFly\.*

