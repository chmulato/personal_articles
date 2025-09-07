# Parte II: Java com Apache Kafka

![Apache Kafka com Java: Producers, Consumers e Integração Prática](/articles/assets/img/2025_07_05_IMAGE_001.png)

## Desenvolvimento de Aplicações Kafka Nativas com o Ecossistema Java

Esta parte mostra como integrar aplicações Java ao Apache Kafka, cobrindo desde a configuração do cliente até exemplos práticos de producers e consumers.

---

## Estrutura de Pastas e Artefatos

Os principais arquivos e diretórios desta parte estão em parte2-java/:

- `docker-compose.yml`: ambiente Kafka para testes locais
- `pom.xml`: dependências Maven do projeto Java
- `src/main/java/com/mulato/`: código-fonte dos Producers e Consumers
- `src/test/java/com/mulato/`: testes automatizados
- `target/`: arquivos compilados e JAR gerado após build

Consulte cada pasta para exemplos completos e adapte conforme seu ambiente.

## Configuração do Ambiente Java

- Java 11+ (recomendado Java 17+)
- Gerenciador de dependências: Maven ou Gradle
- Dependência principal: org.apache.kafka:kafka-clients

**Exemplo de dependência Maven**

```xml
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
    <version>3.5.1</version>
</dependency>
```

## Produtores em Java

### Produtor Simples

```java
import org.apache.kafka.clients.producer.*;
import java.util.Properties;

public class SimpleProducer {
    public static void main(String[] args) {
        // Configurações do produtor
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        
        // Criação do produtor
        Producer<String, String> producer = new KafkaProducer<>(props);
        
        // Envio de mensagem
        producer.send(new ProducerRecord<>("meu-topico", "chave1", "valor1"),
            new Callback() {
                public void onCompletion(RecordMetadata metadata, Exception e) {
                    if (e != null) {
                        e.printStackTrace();
                    } else {
                        System.out.printf("Mensagem enviada para %s, partition %d, offset %d%n",
                            metadata.topic(), metadata.partition(), metadata.offset());
                    }
                }
            });
        
        // Fechamento do produtor
        producer.close();
    }
}
```

### Produtor com Configurações Avançadas

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

// Configurações avançadas
props.put("acks", "all");                     // Confirmação de todos os replicas
props.put("retries", 3);                      // Tentativas de reenvio
props.put("batch.size", 16384);               // Tamanho do lote em bytes
props.put("linger.ms", 10);                   // Tempo de espera para envio do lote
props.put("buffer.memory", 33554432);         // Memória buffer para o produtor
props.put("max.block.ms", 1000);              // Tempo máximo de bloqueio
props.put("compression.type", "snappy");      // Compressão de mensagens

Producer<String, String> producer = new KafkaProducer<>(props);
```

### Serialização Personalizada

```java
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Serializer;

public class JsonSerializer<T> implements Serializer<T> {
    private final ObjectMapper objectMapper = new ObjectMapper();
    
    @Override
    public byte[] serialize(String topic, T data) {
        if (data == null)
            return null;
        try {
            return objectMapper.writeValueAsBytes(data);
        } catch (Exception e) {
            throw new RuntimeException("Erro ao serializar para JSON", e);
        }
    }
}
```

## Consumidores em Java

### Consumidor Simples

```java
import org.apache.kafka.clients.consumer.*;
import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class SimpleConsumer {
    public static void main(String[] args) {
        // Configurações do consumidor
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("group.id", "meu-grupo");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        
        // Criação do consumidor
        Consumer<String, String> consumer = new KafkaConsumer<>(props);
        
        // Inscrição no tópico
        consumer.subscribe(Collections.singletonList("meu-topico"));
        
        // Loop de consumo
        try {
            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                for (ConsumerRecord<String, String> record : records) {
                    System.out.printf("Recebido: tópico = %s, partição = %d, offset = %d, chave = %s, valor = %s%n",
                        record.topic(), record.partition(), record.offset(), record.key(), record.value());
                }
            }
        } finally {
            consumer.close();
        }
    }
}
```

### Consumidor com Commit Manual

```java
Consumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Collections.singletonList("meu-topico"));

while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    
    // Processamento das mensagens
    for (ConsumerRecord<String, String> record : records) {
        System.out.printf("Processando: %s%n", record.value());
        // lógica de processamento
    }
    
    // Commit manual após processamento
    consumer.commitSync();
}
```

### Deserialização Personalizada

```java
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Deserializer;

public class JsonDeserializer<T> implements Deserializer<T> {
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final Class<T> type;
    
    public JsonDeserializer(Class<T> type) {
        this.type = type;
    }
    
    @Override
    public T deserialize(String topic, byte[] data) {
        if (data == null)
            return null;
        try {
            return objectMapper.readValue(data, type);
        } catch (Exception e) {
            throw new RuntimeException("Erro ao deserializar de JSON", e);
        }
    }
}
```

## Avro com Kafka e Schema Registry

### Configuração Maven para Avro

```xml
<dependencies>
    <dependency>
        <groupId>org.apache.avro</groupId>
        <artifactId>avro</artifactId>
        <version>1.11.1</version>
    </dependency>
    <dependency>
        <groupId>io.confluent</groupId>
        <artifactId>kafka-avro-serializer</artifactId>
        <version>7.3.1</version>
    </dependency>
</dependencies>

<repositories>
    <repository>
        <id>confluent</id>
        <url>https://packages.confluent.io/maven/</url>
    </repository>
</repositories>
```

### Exemplo de Schema Avro

```json
{
  "namespace": "com.mulato.model",
  "type": "record",
  "name": "Customer",
  "fields": [
    {"name": "id", "type": "int"},
    {"name": "name", "type": "string"},
    {"name": "email", "type": ["null", "string"], "default": null}
  ]
}
```

### Produtor com Avro e Schema Registry

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "io.confluent.kafka.serializers.KafkaAvroSerializer");
props.put("schema.registry.url", "http://localhost:8081");

Producer<String, Customer> producer = new KafkaProducer<>(props);

Customer customer = new Customer(1, "João Silva", "joao@example.com");
producer.send(new ProducerRecord<>("customers", customer.getId().toString(), customer));
producer.close();
```

### Consumidor com Avro e Schema Registry

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "customer-group");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "io.confluent.kafka.serializers.KafkaAvroDeserializer");
props.put("schema.registry.url", "http://localhost:8081");
props.put("specific.avro.reader", "true");

Consumer<String, Customer> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Collections.singletonList("customers"));

while (true) {
    ConsumerRecords<String, Customer> records = consumer.poll(Duration.ofMillis(100));
    for (ConsumerRecord<String, Customer> record : records) {
        Customer customer = record.value();
        System.out.printf("ID: %d, Nome: %s, Email: %s%n", 
                         customer.getId(), customer.getName(), customer.getEmail());
    }
}
```

## Spring Boot com Kafka

### Dependências Spring Boot

```xml
<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
</dependency>
```

### Configuração do Producer

```java
@Configuration
public class KafkaProducerConfig {
    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;
    
    @Bean
    public ProducerFactory<String, String> producerFactory() {
        Map<String, Object> configProps = new HashMap<>();
        configProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        configProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        configProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
        return new DefaultKafkaProducerFactory<>(configProps);
    }
    
    @Bean
    public KafkaTemplate<String, String> kafkaTemplate() {
        return new KafkaTemplate<>(producerFactory());
    }
}
```

### Envio de Mensagens com Spring

```java
@Service
public class KafkaProducerService {
    private final KafkaTemplate<String, String> kafkaTemplate;
    
    public KafkaProducerService(KafkaTemplate<String, String> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }
    
    public void sendMessage(String topic, String message) {
        kafkaTemplate.send(topic, message);
    }
}
```

### Configuração do Consumer

```java
@Configuration
public class KafkaConsumerConfig {
    @Value("${spring.kafka.bootstrap-servers}")
    private String bootstrapServers;
    
    @Bean
    public ConsumerFactory<String, String> consumerFactory() {
        Map<String, Object> props = new HashMap<>();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "spring-group");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        return new DefaultKafkaConsumerFactory<>(props);
    }
    
    @Bean
    public ConcurrentKafkaListenerContainerFactory<String, String> kafkaListenerContainerFactory() {
        ConcurrentKafkaListenerContainerFactory<String, String> factory = 
            new ConcurrentKafkaListenerContainerFactory<>();
        factory.setConsumerFactory(consumerFactory());
        return factory;
    }
}
```

### Consumo de Mensagens com Spring

```java
@Service
public class KafkaConsumerService {
    private static final Logger logger = LoggerFactory.getLogger(KafkaConsumerService.class);
    
    @KafkaListener(topics = "meu-topico", groupId = "spring-group")
    public void listen(String message) {
        logger.info("Mensagem recebida: {}", message);
        // lógica de processamento
    }
}
```

## Recursos Adicionais

- Documentação oficial: [**https://kafka.apache.org/documentation/**](https://kafka.apache.org/documentation/)
- Spring for Apache Kafka: [**https://spring.io/projects/spring-kafka**](https://spring.io/projects/spring-kafka)
- Confluent Kafka Clients: [**https://docs.confluent.io/platform/current/clients/index.html**](https://docs.confluent.io/platform/current/clients/index.html)
- Exemplos oficiais: [**https://kafka.apache.org/quickstart**](https://kafka.apache.org/quickstart)

## Código-Fonte e Exemplos

Todo o conteúdo, exemplos práticos e arquivos de configuração desta parte estão disponíveis no repositório oficial do projeto no GitHub:

[**🔗 github.com/chmulato/kafka-java-mastery**](https://github.com/chmulato/kafka-java-mastery)

Acesse, explore e contribua!

#ApacheKafka #Java #Messaging #EventStreaming #SpringBoot #Avro #KafkaProducer #KafkaConsumer #Integration

[![Christian Mulato](/articles/assets/img/foto_chri.jpg)](https://www.linkedin.com/in/chmulato/)
