---
title: "Explorando O Java Http Client Uma Ferramenta Moderna Para Chamadas Http"
date: "21/07/2024"
author: "Christian Mulato"
description: "Artigo técnico sobre explorando o java http client uma ferramenta moderna para chamadas http"
category: "Java & Spring"
tags: ['Java', 'APIs', 'Testes', 'Maven', 'DevOps', 'IA']
featured_image: "img/2024_07_21_explorando_o_java_http_client_uma_ferramenta_moderna_para_chamadas_http_featured.jpg"
---

# Explorando O Java Http Client Uma Ferramenta Moderna Para Chamadas Http

![Explorando o Java HTTP Client do Java 11+.](img/image_not_found.png)

Explorando o Java HTTP Client do Java 11\+\.

__Explorando o Java HTTP Client: Uma Ferramenta Moderna para Chamadas HTTP__

[![Christian Mulato](img/image_not_found.png)](https://www.linkedin.com/in/chmulato/)

__[Christian Mulato](https://www.linkedin.com/in/chmulato/)__

Desenvolvedor Java Sênior na Develcode

21 de julho de 2024

Olá, desenvolvedores Java\! Hoje, vamos mergulhar em um recurso poderoso introduzido no __Java 11__ \- o __Java HTTP Client__\. Esta API moderna e versátil supera as limitações da antiga __HttpURLConnection__, oferecendo uma interface mais intuitiva e fácil de usar\.

O Java HTTP Client suporta __HTTP/2__ e __WebSocket__, além de permitir o envio de requisições síncronas e assíncronas\. Ele pode lidar com diferentes tipos de corpo de requisição e resposta, como String, InputStream, File e diretamente para um Subscriber do __java\.util\.concurrent\.Flow__\. Além disso, ele também suporta a configuração de tempo limite de requisição, autenticação automática e redirecionamento\.

Neste artigo, vamos explorar como usar o Java HTTP Client, desde a criação de uma instância até a configuração de várias opções, como timeout, proxy e autenticação\. Também vamos aprender a fazer solicitações __GET__ e __POST__, a analisar respostas e a lidar com diferentes códigos de status HTTP\. Além disso, vamos discutir como testar suas chamadas HTTP e comparar o Java HTTP Client com outras bibliotecas populares\.

Então, se você está procurando uma alternativa moderna e poderosa para fazer chamadas HTTP em comparação com a __HttpURLConnection__, continue lendo\!

Aqui estão os tópicos mencionados no documento em ordem de apresentação:

- Introdução ao Java HTTP Client\.
- Configuração do HttpClient\.
- Envio de Requisições GET\.
- Análise da Resposta\.
- Envio de Requisições POST\.
- Tratamento de Respostas\.
- Trabalhando com Headers\.
- Tratamento de Erros e Exceções\.
- AsyncHttpClient e Chamadas Assíncronas\.
- Testes Unitários para Clientes HTTP\.
- Comparação com Outras Bibliotecas\.

Cada tópico aborda diferentes aspectos do __Java HTTP Client__, desde a introdução e configuração até o tratamento de erros e comparações com outras bibliotecas\. Isso deve fornecer uma visão abrangente do Java HTTP Client para vocês\.

__Introdução ao Java HTTP Client:__

 O __Java HTTP Client__ é uma API moderna e versátil introduzida no __Java 11__ para lidar com requisições HTTP\. Ele supera as limitações da antiga __HttpURLConnection__ ao oferecer uma API mais intuitiva e fácil de usar, com suporte para HTTP/2 e WebSocket, além de permitir o envio de requisições síncronas e assíncronas\. A capacidade de lidar com diferentes tipos de corpo de requisição e resposta, como String, InputStream, File e diretamente para um Subscriber do java\.util\.concurrent\.Flow, torna o Java HTTP Client uma escolha superior\. Além disso, ele também suporta a configuração de tempo limite de requisição, autenticação automática e redirecionamento, o que o torna uma alternativa moderna e poderosa para fazer chamadas HTTP em comparação com a HttpURLConnection\.

 Para usar o Java HTTP Client, você precisa seguir alguns passos\. Aqui está um exemplo simples de como fazer uma requisição GET:

![Texto

Descrição gerada automaticamente](img/image_not_found.png)

Exemplo simples de como fazer uma requisição GET com Java HTTP Client\.

Neste exemplo, primeiro criamos um __HttpClient__ usando o método __newHttpClient\(\)__\. 

Em seguida, construímos uma requisição HTTP GET para “http://example\.com” usando __HttpRequest\.newBuilder\(\)__\. 

Finalmente, enviamos a requisição e obtemos a resposta como uma String usando client\.send\(\)\.

Este é um exemplo básico\. O Java HTTP Client é muito mais poderoso e flexível, permitindo que você faça requisições POST, lidar com redirecionamentos, autenticação e muito mais\. 

__Configuração do HttpClient:__

 Vamos abordar aqui um exemplo de como você pode criar uma instância de __HttpClient__ e configurá\-la com opções como __timeout__, __proxy__ e __autenticação__ em Java:

![Texto

Descrição gerada automaticamente](img/image_not_found.png)

Exemplo de como criar uma instância de HttpClient\.

Este código cria um __HttpClient__ com as seguintes configurações:

- Versão HTTP: HTTP/2
- Redirecionamento: Normal
- Timeout de conexão: 20 segundos
- Proxy: proxy\.example\.com na porta 8080
- Autenticação: Usuário “username” com senha “password”

Em seguida, ele cria uma __HttpRequest__ para “http://example\.com”, envia a solicitação e imprime a resposta\. 

Por favor, substitua “proxy\.example\.com”, “username”, “password” e “http://example\.com” pelos valores reais que você deseja usar\. 

Você pode configurar o __timeout__ de leitura usando o método __ofSeconds__ da classe __Duration__ no __HttpClient__\. 

Aqui está um exemplo:

![Texto

Descrição gerada automaticamente com confiança baixa](img/image_not_found.png)

Exemplo de como criar uma instância de HttpClient com timeout\.

Neste exemplo, o timeout de conexão é configurado para 10 segundos\. Se a conexão não for estabelecida dentro deste período, uma exceção será lançada\.

No entanto, a partir do Java 11, o HttpClient não fornece um método direto para configurar o timeout de leitura\. 

O timeout de leitura é geralmente manipulado no lado do servidor\. 

Se o servidor não enviar uma resposta dentro de um determinado período de tempo, ele fechará a conexão\. Nesse caso, o HttpClient lançará uma exceção\.

Se você precisar de um controle mais granular sobre o timeout de leitura, pode ser necessário usar uma biblioteca de terceiros que ofereça esse recurso, como o__ Apache HttpClient__ ou o __OkHttp__\.

__Envio de Requisições GET:__

 Como podemos fazer uma requisição HTTP GET usando o Java HTTP Client:

![Interface gráfica do usuário, Texto, Aplicativo

Descrição gerada automaticamente](img/image_not_found.png)

Exemplo de requisição HTTP GET em código Java com a biblioteca Java HTTP Client\.

Este exemplo, estamos criando um novo __HttpClient__ e construindo uma solicitação __HTTP GET __para “http://example\.com”\. 

Em seguida, enviamos a solicitação e imprimimos o código de status e o corpo da resposta\.

Lembre\-se de substituir “http://example\.com” pelo URL do seu destino\. 

Além disso, este é um exemplo simples e não inclui o tratamento de erros adequado que você deve incluir no código de produção\. 

Por exemplo, você pode querer adicionar um bloco try\-catch para lidar com possíveis exceções\.

Para analisar a resposta JSON e converter em objetos Java, você pode usar a biblioteca Jackson\. Aqui está um exemplo de como você pode fazer isso:

![Interface gráfica do usuário

Descrição gerada automaticamente com confiança baixa](img/image_not_found.png)

Exemplo de uma requisição passando um objeto JSON com a bilbioteca Java HTTP Client\.

Neste exemplo, estamos usando a biblioteca Jackson para converter a resposta JSON em um __Map<String, Object>__\. Primeiro, criamos um novo __ObjectMapper__, que é a classe principal da biblioteca Jackson\. Em seguida, usamos o método __readValue__ para converter a resposta JSON em um mapa\.

Lembre\-se de adicionar a dependência da biblioteca __Jackson__ ao seu projeto\. 

Além disso, este é um exemplo simples e não inclui o tratamento de erros adequado que você deve incluir no código de produção\. 

Por exemplo, você pode querer adicionar um bloco try\-catch para lidar com possíveis exceções\. 

Além disso, você pode querer criar classes de modelo para representar a estrutura do seu JSON, em vez de usar um mapa genérico\.

Isso tornará seu código mais legível e seguro\.

__Como faço para converter JSON em objetos Java usando outras bibliotecas, como o Gson?__

Você pode usar a __biblioteca Java Gson__, do Google, para converter JSON em objetos Java\. 

Aqui está um exemplo de como você pode fazer isso:

![Texto

Descrição gerada automaticamente com confiança média](img/image_not_found.png)

Exemplo de código Java para conversão de JSON para um objeto Java\.

Neste exemplo, estamos usando a biblioteca Gson para converter a resposta JSON em um __Map<String, Object>__\. Primeiro, criamos um novo objeto Gson\. Em seguida, usamos o método fromJson para converter a resposta JSON em um mapa\.

Lembre\-se de adicionar a dependência da biblioteca Gson ao seu projeto\. 

Além disso, este é um exemplo simples e não inclui o tratamento de erros adequado que você deve incluir no código de produção\. Por exemplo, você pode querer adicionar um bloco try\-catch para lidar com possíveis exceções\. Além disso, você pode querer criar classes de modelo para representar a estrutura do seu JSON, em vez de usar um mapa genérico\. Isso tornará seu código mais legível e seguro\.

__Envio de Requisições POST:__

 Vamos demostrar um outro exemplo de como você pode preparar e enviar uma solicitação HTTP POST usando o Java HTTP Client:

![](img/image_not_found.png)

Exemplo de requisição HTTP POST em código Java com a biblioteca Java HTTP Client\.

Neste exemplo, estamos criando um novo __HttpClient__ e construindo uma solicitação __HTTP POST__ para “http://example\.com”\. Estamos enviando um JSON como corpo da solicitação\. Em seguida, enviamos a solicitação e imprimimos o código de status e o corpo da resposta\.

Lembre\-se de substituir “http://example\.com” pelo URL do seu destino e "\{\\"key\\":\\"value\\"\}" pelo seu JSON\. Além disso, este é um exemplo simples e não inclui o tratamento de erros adequado que você deve incluir no código de produção\. 

Por exemplo, você pode querer adicionar um bloco try\-catch para lidar com possíveis exceções\. Além disso, você pode querer adicionar mais cabeçalhos conforme necessário para a sua solicitação\. Por exemplo, alguns servidores podem exigir um cabeçalho de autenticação\.

Aqui está um exemplo de como você pode enviar dados no corpo de uma solicitação HTTP POST usando o Java HTTP Client\. Vamos mostrar dois exemplos, um para enviar dados JSON e outro para enviar dados de formulário\. 

__Exemplo 1: Enviando dados JSON__

![Linha do tempo

Descrição gerada automaticamente com confiança média](img/image_not_found.png)

Exemplo de requisição HTTP POST em código Java com envio de dados JSON\.

__Exemplo 2: Enviando dados de formulário__

![Interface gráfica do usuário, Texto, Aplicativo

Descrição gerada automaticamente](img/image_not_found.png)

Exemplo de requisição HTTP POST em código Java com envio de dados do formulário\.

No primeiro exemplo, estamos enviando um JSON como corpo da solicitação\. 

No segundo exemplo, estamos enviando dados de formulário\. 

Para isso, codificamos cada par de chave\-valor como chave=valor e juntamos todos os pares com & para formar a string do corpo da solicitação\. 

Lembre\-se de substituir “http://exemplo\.com” pelo URL do seu destino e os dados do formulário ou JSON pelos seus próprios dados\. Além disso, estes são exemplos simples e não incluem o tratamento de erros adequado que você deve incluir no código de produção\. 

Por exemplo, você pode querer adicionar um bloco try\-catch para lidar com possíveis exceções\. Além disso, você pode querer adicionar mais cabeçalhos conforme necessário para a sua solicitação\. Por exemplo, alguns servidores podem exigir um cabeçalho de autenticação\.

__Tratamento de Respostas, como lidar com diferentes códigos de status HTTP \(200, 404, 500\):__

Aqui está um exemplo de como você pode lidar com diferentes códigos de status HTTP usando o Java HTTP Client:

![Uma imagem contendo Texto

Descrição gerada automaticamente](img/image_not_found.png)

Exemplo de código de requisição com Java HTTP Client com tratamento do status de resposta\.

Neste exemplo, estamos verificando o código de status da resposta HTTP e lidando com diferentes códigos de status\. 

Se o código de status for entre 200 e 299, isso significa que a solicitação foi bem\-sucedida e podemos ler o corpo da resposta\. 

Se o código de status for 404, isso significa que o recurso solicitado não foi encontrado\. 

Se o código de status for entre 500 e 599, isso significa que houve um erro no servidor\.

Lembre\-se de substituir “http://exemplo\.com” pelo URL do seu destino\. 

Além disso, este é um exemplo simples e não inclui o tratamento de erros adequado que você deve incluir no código de produção\. 

Por exemplo, você pode querer adicionar um bloco try\-catch para lidar com possíveis exceções\. Além disso, você pode querer lidar com outros códigos de status HTTP conforme necessário para a sua aplicação\. Em alguns servidores podem retornar um código de status 401 para solicitações não autenticadas\. Nesse caso, você pode querer adicionar um caso para lidar com o código de status 401\.Ao receber uma resposta HTTP, você pode processar a resposta de várias maneiras\. 

Se a resposta for bem\-sucedida \(código de status HTTP 200\), você pode extrair informações do corpo da resposta\. O corpo da resposta pode ser um JSON, XML ou outro formato de dados\. Para extrair informações, você pode usar bibliotecas como Jackson ou Gson para converter a resposta em objetos Java\. Por exemplo, se a resposta for um JSON, você pode converter o JSON em um Map<String, Object> ou em uma classe de modelo Java que corresponda à estrutura do JSON\. Isso permite que você acesse facilmente as informações na resposta\.

__Trabalhando com Headers:__

Vamos mostrar aqui como adicionar, modificar e ler cabeçalhos HTTP em solicitações e respostas\. Um exemplo de como você pode adicionar, modificar e ler cabeçalhos HTTP usando o HttpClient do Java\.

![](img/image_not_found.png)

Exemplo de código de requisição com Java HTTP Client com modificação do cabeçalho HTTP\.

Neste exemplo, primeiro criamos um __HttpClient__ e uma __HttpRequest__\. Adicionamos um cabeçalho personalizado à solicitação com o método __\.header\(\)__\. Em seguida, enviamos a solicitação e obtemos a resposta\. Para ler os cabeçalhos da resposta, usamos o método \.headers\(\) na resposta, que retorna um __HttpHeaders__\. Em seguida, imprimimos todos os cabeçalhos\. Para modificar um cabeçalho, criamos uma nova solicitação com o mesmo URI que a solicitação original, mas com um valor de cabeçalho diferente\. Em seguida, enviamos a nova solicitação e lemos os cabeçalhos da nova resposta da mesma maneira\.

__Tratamento de Erros e Exceções:__

Para o tratamento de erros e exceções, poderia explicar como tratar exceções relacionadas a conexões, timeouts e erros de servidor\. Aqui está um exemplo de como você pode tratar exceções usando o HttpClient do Java\.

![Uma imagem contendo Tabela

Descrição gerada automaticamente](img/image_not_found.png)

Exemplo de código de requisição com Java HTTP Client tratamento de erro try\-catch\.

Neste exemplo, primeiro criamos um __HttpClient__ e uma __HttpRequest__\. Em seguida, enviamos a solicitação dentro de um bloco __try\-catch__\.

Se a solicitação for bem\-sucedida, verificamos o código de status da resposta\. Se o código de status for entre 200 e 299, a solicitação foi bem\-sucedida\. Se o código de status for 300 ou superior, houve um erro no servidor\.

Se ocorrer uma exceção durante o envio da solicitação, ela será capturada e tratada no bloco catch\. Tratamos três tipos de exceções neste exemplo:

- __HttpTimeoutException: __Esta exceção é lançada quando a solicitação excede o tempo limite\.
- __IOException:__ Esta exceção é lançada quando ocorre um erro de conexão\.
- __ InterruptedException:__ Esta exceção é lançada quando a solicitação é interrompida\.

Cada tipo de exceção é tratado de maneira diferente, imprimindo uma mensagem de erro apropriada\. Você pode personalizar o tratamento de exceções para atender às suas necessidades específicas\. Por exemplo, você pode tentar enviar a solicitação novamente se ela exceder o tempo limite, ou você pode registrar o erro de conexão para análise posterior\.

__AsyncHttpClient e Chamadas Assíncronas:__

O __Java HTTP Client__ suporta tanto chamadas síncronas quanto assíncronas\. As chamadas síncronas são bloqueantes, o que significa que o thread que faz a chamada é bloqueado até que a resposta seja recebida\. As chamadas assíncronas, por outro lado, são não bloqueantes\. Elas retornam imediatamente com um __CompletableFuture__, que pode ser usado para processar a resposta quando ela estiver disponível\.

Aqui está um exemplo de como você pode fazer uma chamada assíncrona com o __HttpClient__:

![Uma imagem contendo Linha do tempo

Descrição gerada automaticamente](img/image_not_found.png)

Exemplo de código de requisição com Java HTTP Client com chamada assíncrona\.

Neste exemplo, usamos o método __sendAsync\(\)__ para enviar a solicitação, que retorna um __CompletableFuture__\. Usamos o método __thenAccept\(\)__ no __CompletableFuture__ para processar a resposta quando ela estiver disponível\. 

Se ocorrer um erro ao enviar a solicitação, ele será tratado no bloco __exceptionally\(\)__\.

Os benefícios das chamadas assíncronas incluem:

- __Não bloqueantes:__ As chamadas assíncronas são não bloqueantes, o que significa que seu aplicativo pode continuar fazendo outras coisas enquanto espera pela resposta\.
- __Eficiência de recursos:__ As chamadas assíncronas podem ser mais eficientes em termos de recursos, especialmente se seu aplicativo precisa fazer muitas solicitações de rede, pois elas podem ser feitas em paralelo\.
- __Melhor desempenho:__ Em muitos casos, as chamadas assíncronas podem melhorar o desempenho do seu aplicativo, pois elas permitem que seu aplicativo faça um melhor uso dos recursos do sistema\.

No entanto, as chamadas assíncronas também podem ser mais complexas de implementar e depurar do que as chamadas síncronas, pois você precisa lidar com chamadas assíncronas "futures" e possivelmente com concorrência\. Portanto, é importante entender bem esses conceitos antes de decidir usar chamadas assíncronas\.

__Testes Unitários para Clientes HTTP:__

Vamos abordar como testar suas chamadas HTTP usando bibliotecas como __JUnit__ e __Mockito__\. Aqui está um exemplo de como você pode testar suas chamadas HTTP usando JUnit e Mockito\.

Primeiro, você precisará adicionar as dependências do JUnit e Mockito ao seu arquivo pom\.xml se estiver usando Maven:

![Texto, Linha do tempo

Descrição gerada automaticamente](img/image_not_found.png)

Dependências do JUnit e Mockito no Maven\.

Aqui está um exemplo de teste unitário para uma classe que faz uma chamada HTTP:

![Uma imagem contendo Tabela

Descrição gerada automaticamente](img/image_not_found.png)

Exemplo de teste unitário com código aplicando a biblioteca Java HTTP Client\.

Neste exemplo, criamos um __HttpClient__ e __HttpResponse__ falsos usando__ Mockito\.mock\(\)\.__ Em seguida, definimos o comportamento do HttpClient falso para retornar a HttpResponse falsa quando o método __send\(\)__ é chamado\. Definimos o comportamento da HttpResponse falsa para retornar uma string fixa quando o método __body\(\)__ é chamado\.

Em seguida, criamos uma __HttpRequest__ e usamos o __HttpClient__ falso para enviá\-la\. Verificamos se a resposta é a esperada usando __assertEquals\(\)\.__

Este é um exemplo simples, mas você pode criar testes mais complexos dependendo das suas necessidades\. Por exemplo, você pode verificar se o método __send\(\)__ foi chamado com os parâmetros corretos, ou você pode testar como seu código lida com diferentes códigos de status de resposta\.

__Comparação com Outras Bibliotecas:__

Em comparação do Java HTTP Client com outras bibliotecas populares como Apache HttpClient, OkHttp e Retrofit:

- __Java HTTP Client:__ A partir do Java 11, o Java HTTP Client tornou\-se parte da biblioteca padrão do Java \(java\.net\.http\)\. Ele suporta HTTP/1\.1 e HTTP/2, bem como comunicação WebSocket\. Ele também suporta chamadas síncronas e assíncronas, o que é uma grande vantagem\. Além disso, por ser parte da biblioteca padrão do Java, não requer dependências adicionais, o que pode simplificar o gerenciamento de dependências\.
- __Apache HttpClient: __O Apache HttpClient existe há muito tempo e é uma biblioteca madura e rica em recursos\. Ele suporta HTTP/1\.1, mas não suporta HTTP/2 ou WebSocket\. Ele também não suporta chamadas assíncronas fora da caixa, embora exista uma biblioteca separada \(HttpAsyncClient\) que adiciona esse suporte\. Uma vantagem do Apache HttpClient é que ele oferece um controle muito granular sobre a configuração da conexão e do protocolo\.
- __OkHttp: __O OkHttp é uma biblioteca moderna que suporta HTTP/2 e WebSocket, além de HTTP/1\.1\. Ele também suporta chamadas síncronas e assíncronas\. Uma característica notável do OkHttp é que ele possui uma API muito limpa e fácil de usar\. Ele também tem um bom suporte para interceptadores, que podem ser usados para adicionar comportamentos personalizados às solicitações e respostas\.
- __Retrofit: __O Retrofit é na verdade um tipo diferente de biblioteca em comparação com as outras mencionadas aqui\. Em vez de ser uma biblioteca de cliente HTTP de baixo nível, o Retrofit é um “conversor de tipo seguro para HTTP”\. Ele usa anotações em interfaces para gerar um cliente HTTP\. Isso pode tornar o código muito mais limpo e fácil de entender, especialmente para APIs REST grandes e complexas\. No entanto, o Retrofit não é uma biblioteca de cliente HTTP completa por si só \- ele precisa ser emparelhado com uma biblioteca de cliente HTTP de baixo nível, como OkHttp\.

Em resumo, o Java HTTP Client é uma escolha sólida para muitos casos de uso, especialmente se você estiver usando o Java 11 ou posterior e quiser manter suas dependências ao mínimo\. Ele pode não ter todos os recursos avançados de bibliotecas como Apache HttpClient ou OkHttp, mas para muitos casos de uso, os recursos que ele oferece serão mais do que suficientes\. Além disso, o suporte para HTTP/2 e WebSocket, bem como chamadas assíncronas, são vantajosas\.

__Conclusão__

Neste artigo, exploramos o poder e a versatilidade do__ Java HTTP Client__, uma adição bem\-vinda ao Java 11 que supera as limitações da antiga __HttpURLConnection__\. Com suporte para HTTP/2 e WebSocket, além de uma variedade de opções de configuração, o __Java HTTP Client __é uma ferramenta indispensável para qualquer desenvolvedor Java que trabalhe com chamadas HTTP\.

Aprendemos como fazer solicitações GET e POST, configurar várias opções e analisar respostas\. Também discutimos como testar suas chamadas HTTP e comparamos o Java HTTP Client com outras bibliotecas populares\.

Esperamos que este artigo tenha sido útil para você entender melhor o Java HTTP Client e como ele pode ser usado para melhorar suas aplicações\. Lembre\-se, a prática leva à perfeição\. Portanto, incentive\-se a experimentar o Java HTTP Client em seus projetos e descubra por si mesmo o quão poderoso ele pode ser\.

Obrigado por ler e feliz codificação\!

