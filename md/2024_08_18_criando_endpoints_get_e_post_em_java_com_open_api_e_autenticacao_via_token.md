# Criando Endpoints GET e POST em Java com OpenAPI e Autenticação via Token

![Criando Endpoints GET e POST em Java](/articles/assets/img/2024_08_18_IMAGE_001.png)

## Introdução

Neste artigo, vamos aprender a criar ***endpoints*** **GET** e **POST** em uma aplicação Java utilizando Spring Boot e OpenAPI. Além disso, vamos configurar a autenticação via **token JWT** para proteger nossos ***endpoints***.

## Configuração do Projeto

Primeiro, vamos configurar nosso projeto ***Spring Boot***. No pom.xml, adicione as seguintes dependências:

```xml
<dependencies>
    <!-- Spring Boot Starter Web -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    
    <!-- Spring Security -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
    
    <!-- JWT -->
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt</artifactId>
        <version>0.9.1</version>
```java
@RestController
@RequestMapping("/api/items")
public class ItemController {

    private List<Item> items = new ArrayList<>();

    @GetMapping
    @Operation(summary = "Obter todos os itens", description = "Retorna uma lista de todos os itens disponíveis")
    public ResponseEntity<List<Item>> getAllItems() {
        return ResponseEntity.ok(items);
    }
}
```

## Criando o Endpoint POST

Agora, vamos criar um ***endpoint*** **POST** que adiciona um novo item:

```java
@RestController
@RequestMapping("/api/items")
public class ItemController {

    private List<Item> items = new ArrayList<>();

    // Método GET anterior...

    @PostMapping
    @Operation(summary = "Adicionar um novo item", description = "Adiciona um novo item à lista")
```java
@RestController
@RequestMapping("/api/items")
public class ItemController {

    private List<Item> items = new ArrayList<>();

    // Método GET anterior...

    @PostMapping
    @Operation(summary = "Adicionar um novo item", description = "Adiciona um novo item à lista")
    public ResponseEntity<Item> addItem(@RequestBody Item item) {
        items.add(item);
        return ResponseEntity.status(HttpStatus.CREATED).body(item);
    }
}
```

## Configurando a Autenticação via Token JWT

Para proteger nossos ***endpoints***, vamos configurar a autenticação via **token JWT**. Primeiro, crie uma classe para gerar e validar tokens JWT:

```java
@Component
public class JwtTokenUtil {

    private static final long EXPIRATION_TIME = 864_000_000; // 10 dias
    private final String SECRET = "minhaChaveSecreta";

    public String generateToken(String username) {
        return Jwts.builder()
                .setSubject(username)
                .setExpiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME))
                .signWith(SignatureAlgorithm.HS512, SECRET)
                .compact();
    }

    public String getUsernameFromToken(String token) {
        return Jwts.parser()
                .setSigningKey(SECRET)
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(SECRET).parseClaimsJws(token);
            return true;
        } catch (Exception e) {
            return false;
        }
    }
}
```

## Configurando o Spring Security

Agora, configure o **Spring Security** para usar o JWT:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Autowired
    private JwtTokenUtil jwtTokenUtil;

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable()
            .authorizeRequests()
            .antMatchers("/api/auth/**").permitAll()
            .antMatchers("/v3/api-docs/**", "/swagger-ui/**", "/swagger-ui.html").permitAll()
            .anyRequest().authenticated()
            .and()
            .addFilterBefore(new JwtAuthenticationFilter(jwtTokenUtil), 
                             UsernamePasswordAuthenticationFilter.class);
    }
}
```

```java
@Configuration
public class OpenApiConfig {
    
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("API de Itens")
                        .version("1.0")
                        .description("API para gerenciamento de itens com autenticação JWT")
                        .contact(new Contact().name("Seu Nome").email("seu.email@exemplo.com")))
                .components(new Components()
                        .addSecuritySchemes("bearerAuth", 
                                new SecurityScheme()
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")));
    }
}
```

Agora, adicione as anotações de segurança em seus endpoints:

```java
@RestController
@RequestMapping("/api/items")
@Tag(name = "Itens", description = "Operações relacionadas a itens")
@SecurityRequirement(name = "bearerAuth")
public class ItemController {
    
    private List<Item> items = new ArrayList<>();
    
    @GetMapping
    @Operation(summary = "Obter todos os itens", 
               description = "Retorna uma lista de todos os itens disponíveis")
    public ResponseEntity<List<Item>> getAllItems() {
        return ResponseEntity.ok(items);
    }
    
    @PostMapping
    @Operation(summary = "Adicionar um novo item", 
               description = "Adiciona um novo item à lista")
    public ResponseEntity<Item> addItem(@RequestBody Item item) {
        items.add(item);
        return ResponseEntity.status(HttpStatus.CREATED).body(item);
    }
}
```

## Conclusão

Neste artigo, aprendemos a criar ***endpoints*** **GET** e **POST** em Java utilizando **Spring Boot** e **OpenAPI**, além de configurar a autenticação via **token JWT** para proteger nossos ***endpoints***. Com essas ferramentas, podemos criar APIs seguras e bem documentadas.

> **Nota:** ***Spring Boot*** é um *framework* baseado no [*Spring*](https://spring.io/) que simplifica o desenvolvimento de aplicações Java, eliminando a necessidade de configurações extensas. Ele oferece uma abordagem opinativa para a configuração, permitindo que os desenvolvedores criem rapidamente aplicações robustas e prontas para produção com configurações padrão sensatas. Com recursos como inicializadores automáticos, servidores embutidos e uma vasta gama de bibliotecas integradas, o Spring Boot facilita a criação de micros serviços e aplicações web escaláveis e de alta performance.

[![Christian Mulato](/articles/assets/img/foto_chri.jpg)](https://www.linkedin.com/in/chmulato/)
