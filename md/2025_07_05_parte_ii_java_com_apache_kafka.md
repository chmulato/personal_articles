---
title: "Parte Ii - Java Com Apache Kafka"
date: "05/07/2025"
author: "Christian Mulato"
description: "Artigo técnico sobre parte ii - java com apache kafka"
category: "Java & Spring"
tags: ['Java', 'Spring', 'Docker', 'APIs', 'Testes', 'Maven']
featured_image: "img/2025_07_05_parte_ii_java_com_apache_kafka_featured.jpg"
---

# Parte Ii - Java Com Apache Kafka

![Apache Kafka com Java: Producers, Consumers e Integração Prática.](img/image_not_found.png)

Apache Kafka com Java: Producers, Consumers e Integração Prática\.

__Parte II: Java com Apache Kafka__

__[![Christian Mulato, #OPEN_TO_WORK](img/image_not_found.png)](https://www.linkedin.com/in/chmulato/)__

__[Christian Mulato ](https://www.linkedin.com/in/chmulato/)__

Desenvolvedor Java Sênior | Especialista em Back\-end | Jakarta, Spring Boot, REST APIs, Docker | Engenheiro Químico

5 de julho de 2025

__Visão Geral__

Esta parte mostra como integrar aplicações Java ao Apache Kafka, cobrindo desde a configuração do cliente até exemplos práticos de producers e consumers\.

__Estrutura de Pastas e Artefatos__

Os principais arquivos e diretórios desta parte estão em parte2\-java/:

- docker\-compose\.yml: ambiente Kafka para testes locais
- pom\.xml: dependências Maven do projeto Java
- src/main/java/com/mulato/: código\-fonte dos Producers e Consumers
- src/test/java/com/mulato/: testes automatizados
- target/: arquivos compilados e JAR gerado após build

Consulte cada pasta para exemplos completos e adapte conforme seu ambiente\.

__Configuração do Ambiente Java__

- Java 11\+ \(recomendado Java 17\+\)
- Gerenciador de dependências: Maven ou Gradle
- Dependência principal: org\.apache\.kafka:kafka\-clients

__Exemplo de dependência Maven__

<dependency>

  <groupId>org\.apache\.kafka</groupId>

  <artifactId>kafka\-clients</artifactId>

  <version>3\.7\.0</version>

</dependency>

__Producer em Java__

Exemplo básico de envio de mensagens para um tópico Kafka:

Properties props = new Properties\(\);

props\.put\("bootstrap\.servers", "localhost:9092"\);

props\.put\("key\.serializer", "org\.apache\.kafka\.common\.serialization\.StringSerializer"\);

props\.put\("value\.serializer", "org\.apache\.kafka\.common\.serialization\.StringSerializer"\);

KafkaProducer<String, String> producer = new KafkaProducer<>\(props\);

ProducerRecord<String, String> record = new ProducerRecord<>\("meu\-topico", "chave", "mensagem"\);

producer\.send\(record\);

producer\.close\(\);

__Consumer em Java__

Exemplo básico de leitura de mensagens de um tópico:

Properties props = new Properties\(\);

props\.put\("bootstrap\.servers", "localhost:9092"\);

props\.put\("group\.id", "meu\-grupo"\);

props\.put\("key\.deserializer", "org\.apache\.kafka\.common\.serialization\.StringDeserializer"\);

props\.put\("value\.deserializer", "org\.apache\.kafka\.common\.serialization\.StringDeserializer"\);

KafkaConsumer<String, String> consumer = new KafkaConsumer<>\(props\);

consumer\.subscribe\(Collections\.singletonList\("meu\-topico"\)\);

while \(true\) \{

    ConsumerRecords<String, String> records = consumer\.poll\(Duration\.ofMillis\(100\)\);

    for \(ConsumerRecord<String, String> record : records\) \{

        System\.out\.printf\("offset = %d, key = %s, value = %s%n", record\.offset\(\), record\.key\(\), record\.value\(\)\);

    \}

\}

__Exemplo Prático: Producer e Consumer em Java__

A seguir, você encontra exemplos didáticos de Producer e Consumer em Java, ideais para quem está começando a integrar aplicações com o Apache Kafka\. Os arquivos completos estão em: 

 parte2\-java/src/main/java/com/mulato/PedidoProducer\.java

e

parte2\-java/src/main/java/com/mulato/PedidoConsumer\.java

__Como executar os exemplos__

1\.__Garanta que o Kafka está rodando em __localhost:9092

Utilize o__* *__docker\-compose\.yml fornecido na pasta parte2\-java/ para subir o ambiente local rapidamente:

docker\-compose up \-d

2\.__Compile o projeto Java com Maven__

O projeto já possui um pom\.xml pronto com todas as dependências necessárias\. Basta rodar:

mvn clean compile

3\.__Execute o Producer para enviar mensagens__

mvn exec:java \-Dexec\.mainClass="com\.mulato\.PedidoProducer"

O Producer simula o envio de pedidos para o tópico Kafka\.

4\.__Execute o Consumer para ler as mensagens__

mvn exec:java \-Dexec\.mainClass="com\.mulato\.PedidoConsumer"

O Consumer consome e imprime os pedidos recebidos\.

__Producer Java — Enviando pedidos__

O Producer é responsável por publicar mensagens \(pedidos\) em um tópico Kafka\. Veja um exemplo básico:

Properties props = new Properties\(\);

props\.put\("bootstrap\.servers", "localhost:9092"\);

props\.put\("key\.serializer", "org\.apache\.kafka\.common\.serialization\.StringSerializer"\);

props\.put\("value\.serializer", "org\.apache\.kafka\.common\.serialization\.StringSerializer"\);

KafkaProducer<String, String> producer = new KafkaProducer<>\(props\);

ProducerRecord<String, String> record = new ProducerRecord<>\("meu\-topico", "chave", "mensagem"\);

producer\.send\(record\);

producer\.close\(\);

__Consumer Java — Lendo pedidos do tópico__

O Consumer é responsável por ler as mensagens publicadas no tópico\. Veja um exemplo básico:

Properties props = new Properties\(\);

props\.put\("bootstrap\.servers", "localhost:9092"\);

props\.put\("group\.id", "meu\-grupo"\);

props\.put\("key\.deserializer", "org\.apache\.kafka\.common\.serialization\.StringDeserializer"\);

props\.put\("value\.deserializer", "org\.apache\.kafka\.common\.serialization\.StringDeserializer"\);

KafkaConsumer<String, String> consumer = new KafkaConsumer<>\(props\);

consumer\.subscribe\(Collections\.singletonList\("meu\-topico"\)\);

while \(true\) \{

    ConsumerRecords<String, String> records = consumer\.poll\(Duration\.ofMillis\(100\)\);

    for \(ConsumerRecord<String, String> record : records\) \{

        System\.out\.printf\("offset = %d, key = %s, value = %s%n", record\.offset\(\), record\.key\(\), record\.value\(\)\);

    \}

\}

__Dica:__ Experimente rodar múltiplos consumers no mesmo grupo para ver como o Kafka distribui as mensagens entre eles\.

Esses exemplos são apenas para fins didáticos e funcionam em ambientes locais com o Kafka rodando no padrão \(localhost:9092\)\.

__Teste Integrado: Producer e Consumer na Prática__

Para garantir que sua aplicação Java está realmente se comunicando com o Kafka, é fundamental realizar testes de integração\. O projeto já inclui um exemplo realista em 

parte2\-java/src/test/java/com/mulato/KafkaIntegrationTest\.java

Esse teste automatizado:

- Sobe o ambiente Kafka local \(use docker\-compose up \-d na pasta parte2\-java/\)\.
- Envia uma mensagem para o tópico pedidos usando um Producer\.
- Consome a mensagem usando um Consumer e valida se ela foi recebida corretamente\.

__Como executar o teste integrado__

1\.__Suba o ambiente Kafka e Zookeeper__

No terminal, dentro da pasta parte2\-java/

docker\-compose up \-d

2\.__Garanta que o tópico __pedidos existe

Se necessário, crie o tópico executando dentro do container Kafka:

docker exec \-it <nome\_do\_container\_kafka> kafka\-topics \-\-bootstrap\-server localhost:9092 \-\-create \-\-topic pedidos \-\-partitions 1 \-\-replication\-factor 1

Use docker ps para descobrir o nome do container Kafka\.

3\.__Execute o teste com Maven__

mvn test

O teste irá:

- Enviar uma mensagem para o tópico pedidos\.
- Consumir a mensagem e validar se ela foi recebida corretamente\.

4\.__Finalize o ambiente__

Após os testes, pare os containers:

docker\-compose down

O teste é didático e pode ser adaptado para outros tópicos, mensagens ou cenários de integração\.

__Exercícios Práticos__

Para praticar e aprofundar os conceitos desta parte, consulte também o arquivo auxiliar:

- exercicios\-parte2\.md — Exercícios práticos de integração Java \+ Kafka, implementação de Producer/Consumer, testes e espaço para anotações\.

__Boas Práticas__

- Use consumer groups para escalabilidade
- Gerencie offsets de forma adequada \(automático/manual\)
- Implemente tratamento de exceções e retries
- Utilize serialização adequada \(String, JSON, Avro\)

__Exercícios Sugeridos__

1. Crie um projeto Java com __*Maven *__ou __*Gradle*__
2. Implemente um producer que envia mensagens simulando pedidos
3. Implemente um consumer que lê e imprime esses pedidos
4. Experimente usar consumer groups e múltiplas partições

__Recursos Recomendados__

- [__Kafka Java Client API__](https://kafka.apache.org/documentation/#producerapi)
- Exemplos oficiais: [__https://kafka\.apache\.org/quickstart__](https://kafka.apache.org/quickstart)

__Código\-Fonte e Exemplos__

Todo o conteúdo, exemplos práticos e arquivos de configuração desta parte estão disponíveis no repositório oficial do projeto no GitHub:

[__🔗__](https://github.com/chmulato/kafka-java-mastery) [__github\.com/chmulato/kafka\-java\-mastery__](http://github.com/chmulato/kafka-java-mastery)

Acesse, explore e contribua\!

