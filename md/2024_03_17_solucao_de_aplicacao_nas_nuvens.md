---
title: "Solução De Aplicação Nas Nuvens"
date: "17/03/2024"
author: "Christian Mulato"
description: "Artigo técnico sobre solução de aplicação nas nuvens"
category: "Java & Spring"
tags: ['Java', 'Docker', 'Kubernetes', 'APIs', 'Testes', 'Kafka']
featured_image: "img/2024_03_17_solucao_de_aplicacao_nas_nuvens_featured.jpg"
---

# Solução De Aplicação Nas Nuvens

![](img/image_not_found.png)

__Solução de aplicação nas nuvens__

[![Christian Mulato](img/image_not_found.png)](https://www.linkedin.com/in/chmulato/)

__[Christian Mulato](https://www.linkedin.com/in/chmulato/)__

Desenvolvedor Java Sênior na Develcode

17 de março de 2024

__Apache OpenWhisk__ é uma plataforma __*serverless*__ de código aberto que executa funções em resposta a eventos em qualquer escala\. Ela gerencia a infraestrutura, servidores e escalabilidade usando __contêineres Docker__, permitindo que você se concentre em construir aplicativos incríveis e eficientes\.

Aqui estão os principais aspectos do __Apache OpenWhisk__:

__1\. Execução de Funções \(fx\)__: O OpenWhisk permite que você escreva __lógica funcional__ \(chamada de __Actions__\) em qualquer linguagem de programação suportada\. Essas ações podem ser agendadas dinamicamente e executadas em resposta a eventos associados \(por meio de __Triggers__\) de fontes externas \(como __Feeds__\) ou de __solicitações HTTP__\.

__2\. Deploys em Qualquer Lugar__: Como o OpenWhisk baseia seus componentes em contêineres, ele oferece suporte a várias opções de implantação, tanto localmente quanto em infraestruturas de nuvem\. Isso inclui estruturas populares de contêineres, como __Kubernetes__, __OpenShift__ e __Compose__\.

__3\. Suporte a Múltiplas Linguagens__: O OpenWhisk suporta várias linguagens, incluindo __Go, Java, NodeJS, \.NET, PHP, Python, Ruby, Rust, Scala__ e __Swift__\. Além disso, há um tempo de execução experimental para __Deno__ em desenvolvimento\.

__4\. Integração com Serviços Populares__: O OpenWhisk facilita a integração de suas ações com muitos serviços populares usando __Packages__\. Esses pacotes oferecem integrações com serviços como filas de mensagens __Kafka__, bancos de dados como __Cloudant__, notificações push de aplicativos móveis, mensagens do __Slack__ e feeds __RSS__\. Você também pode usar o pacote __Alarms__ para agendar a execução de suas ações em horários específicos ou intervalos recorrentes\.

__5\. Composições Ricas__: O OpenWhisk permite combinar suas funções em composições ricas\. Você pode escrever código em diferentes idiomas, como __JavaScript/NodeJS, Swift, Python, Java__ ou executar lógica personalizada empacotando o código com __Docker__\.

Em resumo, o __Apache OpenWhisk__ oferece uma maneira flexível e escalável de criar aplicativos serverless, permitindo que você se concentre na lógica de negócios e na criação de soluções independentes de nuvem\.

Aqui está um exemplo simples de como criar uma ação \(ou função\) usando o __Apache OpenWhisk__\. Vamos supor que queremos criar uma ação que some dois números:

// Javascript \- Arquivo: soma\.js

function main\(params\) \{

    const \{ num1, num2 \} = params;

    if \(\!num1 || \!num2\) \{

        return \{ error: 'Por favor, forneça os números para somar\.' \};

    \}

    const resultado = num1 \+ num2;

    return \{ resultado \};

\}

Neste exemplo:

\- Criamos uma função chamada *main* que recebe um objeto *params*\.

\- Verificamos se os números *num1* e *num2* foram fornecidos\.

\- Se sim, somamos os números e retornamos o resultado\.

Para criar essa ação no OpenWhisk, você pode usar o seguinte comando na linha de comando:

wsk action create minha\-soma soma\.js

Agora, você pode invocar essa ação passando os parâmetros *num1* e *num2*:

wsk action invoke minha\-soma \-\-param num1 10 \-\-param num2 20

Isso retornará um objeto JSON com o resultado da soma:

// Arquivo \- JSON

\{

   "resultado": 30

\}

Lembre\-se de que este é apenas um exemplo básico\. O OpenWhisk oferece muito mais recursos, como gatilhos, regras e composições, para criar soluções *serverless* mais complexas\.

Para usar o __Apache OpenWhisk__ localmente em um sistema operacional Linux, você pode seguir estas etapas:

__1\. Instalação do Docker e Docker Compose:__

 \- Certifique\-se de ter o __Docker__ instalado em sua máquina\. Se ainda não o tiver, instale\-o\.

 \- Em seguida, instale o __Docker Compose__, que é uma ferramenta para definir e executar aplicativos Docker com vários contêineres\.

__2\. Clone o Repositório do OpenWhisk:__

 \- Abra um terminal e execute o seguinte comando para clonar o repositório do OpenWhisk:

 git clone https://github\.com/apache/openwhisk\.git

__3\. Configuração do Ambiente:__

 \- Navegue para o diretório openwhisk/tools/ubuntu\-setup\.

 \- Execute o script de configuração para instalar as dependências necessárias:

 cd openwhisk/tools/ubuntu\-setup

     \./all\.sh

__4\. Inicie o OpenWhisk Localmente:__

 \- Execute o seguinte comando para iniciar o OpenWhisk localmente usando o Docker Compose:

 docker\-compose \-f docker\-compose\.yml \-f docker\-compose\.local\.yml up

__5\. Verifique a Instalação:__

 \- Após a inicialização, você pode verificar se o OpenWhisk está funcionando corretamente\. Abra um navegador e acesse:

 http://localhost:3233

 Você verá a interface da API do OpenWhisk\.

__6\. Use o CLI do OpenWhisk:__

 \- Instale o CLI do OpenWhisk \(wsk\) em sua máquina\. Você pode baixá\-lo a partir do repositório oficial do OpenWhisk\.

 \- Configure o CLI para apontar para o ambiente local:

 wsk property set \-\-apihost localhost \-\-auth <sua\_chave\_de\_autenticação>

__7\. Crie e Execute Ações:__

 \- Agora você pode criar suas próprias ações e invocá\-las localmente usando o CLI do OpenWhisk\.

Lembre\-se de que essa é uma configuração básica para uso local\.

Implantar uma ação do __Apache OpenWhisk__ em um ambiente de produção envolve algumas etapas importantes\. Vou fornecer uma visão geral, mas lembre\-se de que os detalhes específicos podem variar com base na sua infraestrutura e requisitos\.

![](img/image_not_found.png)

Um exemplo esquemático das tecnologias envolvidas\.

__1\. Configuração do Ambiente__:

\- Ambiente OpenWhisk: Primeiro, você precisa ter um ambiente OpenWhisk configurado\. Isso pode ser local \(usando o OpenWhisk em um cluster Kubernetes ou Docker Compose\) ou em uma nuvem pública \(como IBM Cloud, AWS, Google Cloud, etc\.\)\.

\- __Credenciais__: Certifique\-se de ter as credenciais corretas para acessar o ambiente OpenWhisk\.

__2\. Empacotamento da Ação:__

\- Empacote sua ação \(no nosso exemplo, a ação de soma\) em um arquivo ZIP ou contêiner Docker\. Isso inclui o código da ação e quaisquer dependências necessárias\.

__3\. Criação da Ação:__

\- Use o comando wsk action create para criar a ação no OpenWhisk\. Por exemplo:

 wsk action create minha\-soma soma\.js

__4\. Teste da Ação:__

\- Antes de implantar em produção, teste sua ação para garantir que ela funcione conforme o esperado\. Use o comando wsk action invoke para testar a ação com diferentes parâmetros\.

__5\. Gerenciamento de Segurança:__

\- Configure as permissões corretas para a ação\. Defina quem pode invocar a ação e quem pode gerenciá\-la\.

\- Considere usar __chaves de API__ ou __tokens de autenticação__ para proteger o acesso à sua ação\.

__6\. Monitoramento e Logs:__

\- Configure o monitoramento para sua ação\. Isso pode incluir métricas, logs e alertas\.

\- Use ferramentas como __Prometheus__, __Grafana__ ou serviços de monitoramento da nuvem\.

__7\. Escalabilidade e Redundância:__

\- Planeje a escalabilidade da sua ação\. Como ela se comportará sob carga pesada?

\- Considere a redundância para evitar pontos únicos de falha\.

__8\. Implantação em Produção:__

\- Finalmente, implante sua ação no ambiente de produção\. Isso pode ser feito usando o mesmo comando *wsk action update* ou por meio de ferramentas de CI/CD\.

Lembre\-se de que essas etapas são uma visão geral\. Dependendo do seu caso de uso específico, você pode precisar ajustar ou adicionar etapas adicionais\. Consulte a documentação do [__Apache OpenWhisk__](https://openwhisk.apache.org/documentation.html) e as práticas recomendadas para obter mais detalhes sobre a implantação em produção\.

