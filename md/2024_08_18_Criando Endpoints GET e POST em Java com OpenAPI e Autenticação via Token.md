![Endpoint com Framework Spring Boot utilizando linguagem Java.](temp_media/media/image1.png){width="5.905555555555556in" height="3.3270833333333334in"}

Endpoint com Framework Spring Boot utilizando linguagem Java.

**Criando Endpoints GET e POST em Java com OpenAPI e Autenticação via Token**

[![Christian Mulato](temp_media/media/image2.jpeg){width="1.0416666666666667in" height="1.0416666666666667in"}](https://www.linkedin.com/in/chmulato/)

[**Christian Mulato**](https://www.linkedin.com/in/chmulato/)

Desenvolvedor Java Sênior na Develcode

18 de agosto de 2024

**1. Introdução**

Neste artigo, vamos aprender a criar ***endpoints*** **GET** e em uma aplicação Java utilizando Spring Boot e OpenAPI. Além disso, vamos configurar a autenticação via **token JWT** para proteger nossos ***endpoints***.

**2. Configuração do Projeto**

Primeiro, vamos configurar nosso projeto ***Spring Boot*** \*\[vide rodapé\]. No pom.xml, adicione as seguintes dependências:

![](temp_media/media/image3.png){width="5.905555555555556in" height="2.4375in"}

Importando as dependências das bibliotecas necessárias para o Spring Boot.

**3. Criando o Endpoint GET**

Vamos criar um ***endpoint*** **GET** que retorna uma lista de itens. Primeiro, crie um controlador:

![](temp_media/media/image4.png){width="5.905555555555556in" height="1.5in"}

Classe Java para a criação do endpoint GET

**4. Criando o Endpoint POST**

Agora, vamos criar um ***endpoint*** **POST** que adiciona um novo item:

![](temp_media/media/image5.png){width="5.905555555555556in" height="1.4118055555555555in"}

Classe Java para a criação do endpoint POST

**5. Configurando a Autenticação via Token JWT**

Para proteger nossos ***endpoints***, vamos configurar a autenticação via **token JWT**. Primeiro, crie uma classe para gerar e validar tokens JWT:

![](temp_media/media/image6.png){width="5.905555555555556in" height="2.532638888888889in"}

Classe Java para a criação do Token de autenticação.

**6. Configurando o Spring Security**

Agora, configure o **Spring Security** para usar o JWT:

![](temp_media/media/image7.png){width="5.905555555555556in" height="1.6583333333333334in"}

Classe Java para o controle de acesso ao endpoint.

**7. Documentando com OpenAPI**

Finalmente, vamos documentar nossos ***endpoints*** com **OpenAPI**. Adicione as anotações no controlador:

![](temp_media/media/image8.png){width="5.905555555555556in" height="2.3673611111111112in"}

Classe Java com os endpoint GET e POST.

**8. Conclusão**

Neste artigo, aprendemos a criar ***endpoints*** **GET** e **POST** em Java utilizando **Spring Boot** e **OpenAPI**, além de configurar a autenticação via **token JWT** para proteger nossos ***endpoints***. Com essas ferramentas, podemos criar APIs seguras e bem documentadas.

------------------------------------------------------------------------

Nota:

- ***Spring Boot*** é um *framework* baseado no [*Spring*](https://spring.io/) que simplifica o desenvolvimento de aplicações Java, eliminando a necessidade de configurações extensas. Ele oferece uma abordagem opinativa para a configuração, permitindo que os desenvolvedores criem rapidamente aplicações robustas e prontas para produção com configurações padrão sensatas. Com recursos como inicializadores automáticos, servidores embutidos e uma vasta gama de bibliotecas integradas, o Spring Boot facilita a criação de micros serviços e aplicações web escaláveis e de alta performance.
