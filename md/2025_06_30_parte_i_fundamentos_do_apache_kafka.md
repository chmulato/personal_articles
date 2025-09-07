# Parte I: Fundamentos do Apache Kafka

![Apache Kafka com Java - Gerenciamento de Filas](/articles/assets/img/2025_06_30_IMAGE_001.png)

## Entendendo os Conceitos Essenciais do Message Broker Mais Popular

Esta parte apresenta os conceitos essenciais do Apache Kafka, sua arquitetura, principais componentes e comandos básicos para quem está começando.

---

## O que é Apache Kafka?

Apache Kafka é uma plataforma distribuída de streaming de eventos, projetada para alta performance, escalabilidade e tolerância a falhas. É amplamente utilizada para processamento de dados em tempo real, integração entre sistemas e pipelines de dados.

## Conceitos Principais

- **Broker**: Servidor Kafka responsável por armazenar e entregar mensagens.
- **Topic**: Canal lógico onde as mensagens são publicadas e consumidas.
- **Partition**: Subdivisão de um tópico para escalabilidade e paralelismo.
- **Producer**: Aplicação que envia mensagens para o Kafka.
- **Consumer**: Aplicação que lê mensagens do Kafka.
- **Consumer Group**: Grupo de consumidores que compartilham a leitura de partições.
- **Offset**: Posição sequencial de uma mensagem dentro de uma partição.

## Arquitetura Básica

1. Producers publicam mensagens em tópicos.
2. Brokers armazenam as mensagens.
3. Consumers leem as mensagens dos tópicos.
4. O Kafka garante alta disponibilidade e escalabilidade por meio de partições e replicação.

## Instalação Rápida com Docker

Para começar rapidamente, você pode usar Docker para criar um ambiente Kafka completo:

```bash
# Crie uma rede para os containers
docker network create kafka-net

# Inicie o Zookeeper
docker run -d --name zookeeper --network kafka-net -e ZOOKEEPER_CLIENT_PORT=2181 confluentinc/cp-zookeeper:7.3.0

# Inicie o Kafka
docker run -d --name kafka --network kafka-net -p 9092:9092 \
    -e KAFKA_BROKER_ID=1 \
    -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
    -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092 \
    -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT \
    -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT \
    -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    confluentinc/cp-kafka:7.3.0
```

## Comandos Básicos

### Criando um Tópico

```bash
docker exec -it kafka kafka-topics --create --topic meu-topico --bootstrap-server kafka:29092 --partitions 3 --replication-factor 1
```

### Listando Tópicos

```bash
docker exec -it kafka kafka-topics --list --bootstrap-server kafka:29092
```

### Descrevendo um Tópico

```bash
docker exec -it kafka kafka-topics --describe --topic meu-topico --bootstrap-server kafka:29092
```

### Produzindo Mensagens

```bash
docker exec -it kafka kafka-console-producer --topic meu-topico --bootstrap-server kafka:29092
> Mensagem 1
> Mensagem 2
> Mensagem 3
```

### Consumindo Mensagens

```bash
docker exec -it kafka kafka-console-consumer --topic meu-topico --from-beginning --bootstrap-server kafka:29092
```

## Configurações Importantes

### Retenção de Mensagens

O Kafka mantém as mensagens por um período configurável:

```bash
# Configurar retenção para 7 dias
docker exec -it kafka kafka-configs --alter --entity-type topics --entity-name meu-topico --add-config retention.ms=604800000 --bootstrap-server kafka:29092
```

### Número de Partições

O número ideal de partições depende do paralelismo desejado:

```bash
# Aumentar número de partições
docker exec -it kafka kafka-topics --alter --topic meu-topico --partitions 6 --bootstrap-server kafka:29092
```

## Monitoramento Básico

### Verificando Consumer Groups

```bash
docker exec -it kafka kafka-consumer-groups --list --bootstrap-server kafka:29092
```

### Verificando Offsets de um Consumer Group

```bash
docker exec -it kafka kafka-consumer-groups --describe --group meu-grupo --bootstrap-server kafka:29092
```

## Dicas e Melhores Práticas

1. **Particionamento adequado**: Escolha um número de partições que permita escalabilidade.
2. **Chaves de particionamento**: Use chaves para garantir ordenação de mensagens relacionadas.
3. **Replicação**: Em ambientes de produção, use fator de replicação >= 3.
4. **Monitoramento**: Implemente monitoramento para identificar problemas cedo.
5. **Gerenciamento de esquemas**: Considere usar Avro ou Protobuf com Schema Registry.

## Ferramentas Úteis

- **Conduktor**: Interface gráfica para gerenciamento de clusters Kafka.
- **Kafka Tool**: Ferramenta desktop para visualização e administração.
- **kcat (anteriormente kafkacat)**: Utilitário de linha de comando versátil.

## Exemplos de Código Simples

### Producer em Java

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

Producer<String, String> producer = new KafkaProducer<>(props);
producer.send(new ProducerRecord<>("meu-topico", "chave", "valor"));
producer.close();
```

### Consumer em Java

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "meu-grupo");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

Consumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Collections.singletonList("meu-topico"));

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, String> record : records) {
        System.out.printf("offset = %d, key = %s, value = %s%n", 
                          record.offset(), record.key(), record.value());
    }
}
```

Esses exemplos são apenas para fins didáticos e funcionam em ambientes locais com o Kafka rodando no padrão (localhost:9092).

## Exercícios Práticos

Para praticar e aprofundar os conceitos desta parte, consulte também o arquivo auxiliar:

- `parte1-fundamentos/exercicios-parte1.md` — Exercícios de fundamentos, comandos básicos, experimentação inicial e espaço para anotações.

## Código-Fonte e Exemplos

Todo o conteúdo, exemplos práticos e arquivos de configuração deste artigo estão disponíveis no repositório oficial do projeto no GitHub:

[**🔗 github.com/chmulato/kafka-java-mastery**](https://github.com/chmulato/kafka-java-mastery)

**Acesse, explore e contribua!**

#ApacheKafka #Java #Messaging #EventStreaming #DataStreaming #Microservices #Integration #RealTimeData

[![Christian Mulato](/articles/assets/img/foto_chri.jpg)](https://www.linkedin.com/in/chmulato/)
