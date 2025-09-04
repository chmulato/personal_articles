---
title: "Implementando E Documentando Apis Restful Com Openapi E Spring Boot Um Guia Prático"
date: "26/08/2024"
author: "Christian Mulato"
description: "Artigo técnico sobre implementando e documentando apis restful com openapi e spring boot um guia prático"
category: "Java & Spring"
tags: ['Java', 'Spring', 'APIs', 'Testes', 'Maven', 'DevOps']
featured_image: "img/2024_08_26_implementando_e_documentando_apis_restful_com_openapi_e_spring_boot_um_guia_pratico_featured.jpg"
---

# Implementando E Documentando Apis Restful Com Openapi E Spring Boot Um Guia Prático

![OPenAPI Rest](img/image_not_found.png)

OPenAPI Rest

__Implementando e Documentando APIs RESTful com OpenAPI e Spring Boot: Um Guia Prático__

[![Christian Mulato](img/image_not_found.png)](https://www.linkedin.com/in/chmulato/)

__[Christian Mulato](https://www.linkedin.com/in/chmulato/)__

Desenvolvedor Java Sênior na Develcode

26 de agosto de 2024

__1\. Introdução__

 

No desenvolvimento de __*APIs RESTful*__, a padronização e a clareza na documentação são essenciais para garantir uma comunicação eficiente entre desenvolvedores e a integração de serviços\. O __*OpenAPI*__ surge como uma solução robusta para descrever APIs de forma padronizada e legível tanto por humanos quanto por máquinas\. No ecossistema Java, especialmente com o uso do __Spring Boot__, o OpenAPI se destaca por facilitar a definição de __*endpoints*__, a geração automática de documentação e a validação de contratos\. Este artigo explora como implementar operações __*GET*__ e __*POST*__ utilizando OpenAPI e __*YAML*__, destacando as principais classes e configurações necessárias em um projeto Spring Boot\. Através de exemplos práticos, veremos como o OpenAPI pode simplificar o desenvolvimento e a manutenção de APIs, promovendo uma maior eficiência e colaboração no desenvolvimento de software\.

 

__2\. Definição__

 

__OpenAPI__ é uma especificação para descrever __*APIs RESTful*__ de forma padronizada e legível tanto por humanos quanto por máquinas\. No mundo Java, especialmente com frameworks como Spring Boot, o OpenAPI é utilizado para documentar e definir endpoints de APIs, facilitando a comunicação entre desenvolvedores e a integração de serviços\. Ele permite a geração automática de documentação, validação de contratos e até mesmo a criação de clientes e servidores a partir das especificações definidas em arquivos YAML ou JSON\.

Vamos começar com uma visão geral de como definir operações GET e POST usando __*OpenAPI *__e YAML\.

 

__3\. Estrutura Básica do OpenAPI__

 

Um arquivo __*OpenAPI *__geralmente começa com algumas informações básicas sobre a API, como título, descrição e versão\. Aqui está um exemplo básico: 

![](img/image_not_found.png)

Exemplo básico de um arquivo OpenAPI\.

__4\. Definindo uma Operação GET__

 

A operação GET é usada para recuperar dados de um servidor\. Aqui está um exemplo de como definir uma operação GET para obter uma lista de usuários:

![](img/image_not_found.png)

Arquivo de configuração YAML para o endpoint de GET\.

 

__5\. Definindo uma Operação POST__

 

A operação POST é usada para enviar dados ao servidor, geralmente para criar um novo recurso\. Aqui está um exemplo de como definir uma operação POST para adicionar um novo usuário:

![](img/image_not_found.png)

Arquivo de configuração YAML para o endpoint de POST\.

__6\. Mapeamentos nos Arquivos YAML__

 

No exemplo acima, usamos o campo paths para definir os __*endpoints*__ /users e especificamos as operações GET e POST\.

Cada operação tem um resumo \(summary\), uma descrição do corpo da requisição \(__*requestBody*__\), e as respostas possíveis \(__*responses*__\)\.

- __GET:__ Não requer um corpo de requisição e retorna uma lista de usuários\.
- __POST:__ Requer um corpo de requisição com os dados do novo usuário e retorna uma confirmação de criação\.

Esses exemplos cobrem o básico de como definir operações GET e POST em um arquivo OpenAPI usando YAML\.

Para implementar operações GET e POST em uma API Java usando OpenAPI, você pode usar o Spring Boot, que facilita bastante o processo\.

Aqui no tópico 7 estão as principais classes e anotações que você precisará:

 

__7\. Classe Principal da Aplicação__

 

A classe principal da sua aplicação Spring Boot deve ser anotada com @SpringBootApplication\. Aqui você também pode configurar o __*OpenAPI*__\.

![](img/image_not_found.png)

Exemplo de classe Java com Spring Boot\.

 __8\. Controlador \(Controller\)__

 

Os controladores são responsáveis por lidar com as requisições HTTP\. Aqui está um exemplo de um controlador com operações GET e POST\.

![](img/image_not_found.png)

Exemplo de classe Java do tipo Controller com o Spring Boot\.

__9\. Modelo \(Model\)__

 

A classe modelo representa os dados que serão manipulados pela API\.

![](img/image_not_found.png)

Exemplo de classe Java bean\.

 

__10\. Dependências no pom\.xml__

 

Para habilitar o suporte ao OpenAPI e Swagger, você precisa adicionar as seguintes dependências ao seu arquivo __*pom\.xml*__:

![](img/image_not_found.png)

Exemplo de notação para a dependência Maven do OpenAPI\.

Para criar uma API com operações GET e POST usando OpenAPI e Spring Boot, é essencial configurar a classe principal da aplicação, definir controladores para os endpoints, criar modelos para representar os dados e adicionar as dependências necessárias no arquivo __*pom\.xml*__\. Essas etapas garantem que a API seja bem estruturada, documentada e fácil de manter, promovendo uma integração eficiente e uma comunicação clara entre os desenvolvedores\.

Resumo:

- __Classe Principal:__ Configura o Spring Boot e o OpenAPI\.
- __Controlador: __Define os endpoints GET e POST\.
- __Modelo:__ Representa os dados manipulados pela API\.
- __Dependências:__ Adiciona suporte ao OpenAPI e Swagger\.

Essas são as classes e configurações básicas necessárias para criar uma API com operações GET e POST usando OpenAPI e Spring Boot\.

 

__11\. Estrutura de arquivos__

 

Os arquivos YAML do OpenAPI geralmente são colocados na pasta __*src/main/resources*__ do seu projeto __*Spring Boot*__\.

Esta é a localização padrão para arquivos de configuração e recursos estáticos em projetos Spring Boot\.

Aqui está um exemplo de como a estrutura do seu projeto pode ficar:

![](img/image_not_found.png)

Estrutura de pastas dentro do código Java\.

 

__12\. Configuração do Spring Boot para Usar o Arquivo YAML__

 

Para que o Spring Boot reconheça e utilize o arquivo YAML do OpenAPI, você pode configurar o caminho no seu arquivo __*application\.yml*__:

![](img/image_not_found.png)

Arquivo de configuração YAML chamado\.

__13\. Acessando a Documentação__

 

Depois de configurar, você pode acessar a documentação gerada pelo __OpenAPI __no seguinte caminho:

- __JSON:__ http://localhost:8080/v3/api\-docs
- __YAML:__ http://localhost:8080/v3/api\-docs\.yaml
- __Swagger UI:__ http://localhost:8080/swagger\-ui\.html

Após configurar o Spring Boot para reconhecer e utilizar o arquivo YAML do OpenAPI, a documentação gerada pode ser acessada em diferentes formatos, como JSON e YAML, além da interface __*Swagger UI*__\. Isso facilita a visualização e o teste dos *endpoints* da API, garantindo que a documentação esteja sempre atualizada e acessível para todos os envolvidos no desenvolvimento e manutenção da API\.

Resumo:

- __Localização:__ Coloque o arquivo YAML do OpenAPI em__* src/main/resources/openapi/*__\.
- __Configuração:__ Configure o caminho no __*application\.yml*__\.
- __Acesso:__ Acesse a documentação gerada nos caminhos especificados\.

__14\. Conclusão__

O uso do __*OpenAPI*__ no desenvolvimento de __*APIs RESTful *__com Java, especialmente em conjunto com o Spring Boot, oferece uma série de benefícios que vão desde a padronização e clareza na documentação até a facilitação da integração de serviços\. Através da definição de operações GET e POST em arquivos YAML, desenvolvedores podem criar APIs robustas e bem documentadas, promovendo uma comunicação eficiente e uma melhor colaboração entre equipes\. Além disso, a capacidade de gerar automaticamente documentação e validar contratos garante que as APIs sejam consistentes e confiáveis\. Com o OpenAPI, o processo de desenvolvimento de APIs se torna mais ágil e organizado, permitindo que as equipes se concentrem em entregar valor e inovação\. Ao adotar essa especificação, desenvolvedores Java podem garantir que suas APIs não apenas atendam aos requisitos técnicos, mas também ofereçam uma experiência de uso clara e intuitiva para todos os envolvidos\.

