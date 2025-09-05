---
title: "Parte I - Fundamentos Do Apache Kafka"
date: "30/06/2025"
author: "Christian Mulato"
description: "Artigo técnico sobre parte i - fundamentos do apache kafka"
category: "Java & Spring"
tags: ['Java', 'Spring', 'Docker', 'APIs', 'Maven', 'Kafka']
featured_image: "img/2025_06_30_parte_i_fundamentos_do_apache_kafka_featured.jpg"
---

# Parte I - Fundamentos Do Apache Kafka

![Apache Kafka com Java - Gerenciamento de Filas.](img/image_not_found.png)

Apache Kafka com Java \- Gerenciamento de Filas\.

__Parte I: Fundamentos do Apache Kafka__

__[![Christian Mulato, #OPEN_TO_WORK](img/image_not_found.png)](https://www.linkedin.com/in/chmulato/)__

__[Christian Mulato ](https://www.linkedin.com/in/chmulato/)__

Desenvolvedor Java Sênior | Especialista em Back\-end | Jakarta, Spring Boot, REST APIs, Docker | Engenheiro Químico

30 de junho de 2025

__Introdução__

Esta parte apresenta os conceitos essenciais do Apache Kafka, sua arquitetura, principais componentes e comandos básicos para quem está começando\.

__O que é Apache Kafka?__

Apache Kafka é uma plataforma distribuída de streaming de eventos, projetada para alta performance, escalabilidade e tolerância a falhas\. É amplamente utilizada para processamento de dados em tempo real, integração entre sistemas e pipelines de dados\.

__Conceitos Principais__

- Broker: Servidor Kafka responsável por armazenar e entregar mensagens\.
- Topic: Canal lógico onde as mensagens são publicadas e consumidas\.
- Partition: Subdivisão de um tópico para escalabilidade e paralelismo\.
- Producer: Aplicação que envia mensagens para o Kafka\.
- Consumer: Aplicação que lê mensagens do Kafka\.
- Consumer Group: Grupo de consumidores que compartilham a leitura de partições\.
- Offset: Posição sequencial de uma mensagem dentro de uma partição\.

__Arquitetura Básica__

1. Producers publicam mensagens em tópicos\.
2. Brokers armazenam as mensagens\.
3. Consumers leem as mensagens dos tópicos\.
4. O Kafka garante alta disponibilidade e escalabilidade por meio de partições e replicação\.

__Instalação Rápida com Docker__

docker\-compose up \-d

__Comandos Essenciais__

- Criar um tópico:

kafka\-topics \-\-create \-\-topic meu\-topico \-\-bootstrap\-server localhost:9092 \-\-partitions 3 \-\-replication\-factor 1

- Produzir mensagens:

kafka\-console\-producer \-\-topic meu\-topico \-\-bootstrap\-server localhost:9092

- Consumir mensagens:

kafka\-console\-consumer \-\-topic meu\-topico \-\-from\-beginning \-\-bootstrap\-server localhost:9092

__Exercícios Práticos__

1. Suba o ambiente Kafka localmente\.
2. Crie tópicos com diferentes números de partições\.
3. Produza e consuma mensagens usando o terminal\.
4. Experimente criar múltiplos consumidores em um mesmo grupo\.

__Recursos Recomendados__

- [__Documentação Oficial do Apache Kafka__](https://kafka.apache.org/documentation/)
- Livro: Kafka: The Definitive Guide \(O'Reilly\)

__Exemplo Java: Producer e Consumer Simples__

A seguir, você encontra exemplos didáticos de um Producer e um Consumer em Java, ideais para quem está começando a experimentar o Apache Kafka na prática\. Os arquivos completos estão disponíveis em: parte1\-fundamentos/src/main/java/SimpleProducer\.java e parte1\-fundamentos/src/main/java/SimpleConsumer\.java\.

__Como executar os exemplos__

1. __Garanta que o Kafka está rodando em __localhost:9092

Utilize o docker\-compose\.yml fornecido na pasta parte1\-fundamentos/ para subir o ambiente local rapidamente:

docker\-compose up \-d

2\. __Crie o tópico __meu\-topico se necessário

Execute o comando abaixo para criar o tópico no seu cluster Kafka local:

docker exec \-it <nome\_do\_container\_kafka> kafka\-topics \-\-bootstrap\-server localhost:9092 \-\-create \-\-topic meu\-topico \-\-partitions 1 \-\-replication\-factor 1

Substitua <nome\_do\_container\_kafka> pelo nome real do container Kafka em execução \(ex: kafka ou kafka1\)\.

3\. __Compile e execute os exemplos Java usando Maven__

O projeto já possui um pom\.xml pronto na pasta parte1\-fundamentos com todas as dependências necessárias\. Basta rodar:

mvn compile

mvn exec:java \-Dexec\.mainClass=SimpleProducer

mvn exec:java \-Dexec\.mainClass=SimpleConsumer

O __SimpleProducer __envia uma mensagem de exemplo para o tópico, e o __SimpleConsumer __consome e imprime as mensagens recebidas\.

__Producer Java — Enviando uma mensagem__

O Producer é responsável por publicar mensagens em um tópico Kafka\. Veja um exemplo básico:

import org\.apache\.kafka\.clients\.producer\.KafkaProducer;

import org\.apache\.kafka\.clients\.producer\.ProducerRecord;

import java\.util\.Properties;

public class SimpleProducer \{

    public static void main\(String\[\] args\) \{

        Properties props = new Properties\(\);

        props\.put\("bootstrap\.servers", "localhost:9092"\);

        props\.put\("key\.serializer", "org\.apache\.kafka\.common\.serialization\.StringSerializer"\);

        props\.put\("value\.serializer", "org\.apache\.kafka\.common\.serialization\.StringSerializer"\);

        try \(KafkaProducer<String, String> producer = new KafkaProducer<>\(props\)\) \{

            producer\.send\(new ProducerRecord<>\("meu\-topico", "mensagem de exemplo"\)\);

            System\.out\.println\("Mensagem enviada\!"\);

        \}

    \}

\}

__Consumer Java — Lendo mensagens do tópico__

O Consumer é responsável por ler as mensagens publicadas em um tópico\. Veja um exemplo básico:

import org\.apache\.kafka\.clients\.consumer\.ConsumerRecords;

import org\.apache\.kafka\.clients\.consumer\.KafkaConsumer;

import org\.apache\.kafka\.clients\.consumer\.ConsumerRecord;

import java\.util\.Collections;

import java\.util\.Properties;

public class SimpleConsumer \{

    public static void main\(String\[\] args\) \{

        Properties props = new Properties\(\);

        props\.put\("bootstrap\.servers", "localhost:9092"\);

        props\.put\("group\.id", "grupo\-exemplo"\);

        props\.put\("key\.deserializer", "org\.apache\.kafka\.common\.serialization\.StringDeserializer"\);

        props\.put\("value\.deserializer", "org\.apache\.kafka\.common\.serialization\.StringDeserializer"\);

        try \(KafkaConsumer<String, String> consumer = new KafkaConsumer<>\(props\)\) \{

            consumer\.subscribe\(Collections\.singletonList\("meu\-topico"\)\);

            ConsumerRecords<String, String> records = consumer\.poll\(java\.time\.Duration\.ofSeconds\(5\)\);

            for \(ConsumerRecord<String, String> record : records\) \{

                System\.out\.printf\("Recebido: %s%n", record\.value\(\)\);

            \}

        \}

    \}

\}

__Dica:__ Você pode modificar os exemplos para enviar e consumir múltiplas mensagens, testar diferentes tópicos ou experimentar com múltiplos consumidores para entender o funcionamento dos consumer groups\.

Esses exemplos são apenas para fins didáticos e funcionam em ambientes locais com o Kafka rodando no padrão \(localhost:9092\)\.

__Exercícios Práticos__

Para praticar e aprofundar os conceitos desta parte, consulte também o arquivo auxiliar:

- parte1\-fundamentos/exercicios\-parte1\.md — Exercícios de fundamentos, comandos básicos, experimentação inicial e espaço para anotações\.

__Código\-Fonte e Exemplos__

Todo o conteúdo, exemplos práticos e arquivos de configuração deste artigo estão disponíveis no repositório oficial do projeto no GitHub:

[__🔗__](https://github.com/chmulato/kafka-java-mastery) [__github\.com/chmulato/kafka\-java\-mastery__](http://github.com/chmulato/kafka-java-mastery)

__Acesse, explore e contribua\!__

