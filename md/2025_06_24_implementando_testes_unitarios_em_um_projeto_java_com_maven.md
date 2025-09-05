---
title: "Implementando Testes Unitários Em Um Projeto Java Com Maven"
date: "24/06/2025"
author: "Christian Mulato"
description: "Artigo técnico sobre implementando testes unitários em um projeto java com maven"
category: "Java & Spring"
tags: ['Java', 'Spring', 'Docker', 'APIs', 'Testes', 'Maven']
featured_image: "img/2025_06_24_implementando_testes_unitarios_em_um_projeto_java_com_maven_featured.jpg"
---

# Implementando Testes Unitários Em Um Projeto Java Com Maven

*Publicado em 24/06/2025 por [Christian Mulato](https://www.linkedin.com/in/chmulato/)*

## Resumo Executivo

Implementando Testes Unitários com JaCoCo

**Categoria:** Java & Spring  
**Nível:** Intermediário/Avançado  
**Tags:** Java, Spring, Docker, APIs, Testes, Maven

# Implementando Testes Unitários Em Um Projeto Java Com Maven

![Implementando Testes Unitários com JaCoCo](img/image_not_found.png)

Implementando Testes Unitários com JaCoCo

__Implementando Testes Unitários em um Projeto Java com Maven__

__[![Christian Mulato, #OPEN_TO_WORK](img/image_not_found.png)](https://www.linkedin.com/in/chmulato/)__

__[Christian Mulato ](https://www.linkedin.com/in/chmulato/)__

Desenvolvedor Java Sênior | Especialista em Back\-end | Jakarta, Spring Boot, REST APIs, Docker | Engenheiro Químico

24 de junho de 2025

Este artigo aborda a implementação de testes unitários em um projeto Java utilizando Maven, com foco na classe __FileBackup __e na geração de relatórios de cobertura de código com __JaCoCo__\. Vamos explorar como estruturar o projeto, escrever testes eficazes e garantir a qualidade do código\.

__Por que Escrever Testes Unitários?__

Testes unitários garantem que cada parte do seu código funciona como esperado, facilitando a manutenção, __*refatoração *__e evolução do projeto\. Eles ajudam a identificar rapidamente bugs e reduzem o custo de correção de erros\.

__Estrutura de Pastas Padrão__

Para projetos Java seguindo o padrão Maven, a estrutura recomendada é:

project\-root/

│

├── src/

│   ├── main/

│   │   └── java/

│   │       └── com/

│   │           └── mulato/

│   │               └── FileBackup\.java

│   └── test/

│       └── java/

│           └── com/

│               └── mulato/

│                   └── FileBackupTest\.java

__Boas Práticas para Testes Unitários__

- __Nomeie os métodos de teste de forma clara__: O nome deve indicar o que está sendo testado e o resultado esperado\.
- __Teste apenas uma lógica por método__: Cada teste deve validar um único comportamento\.
- __Evite dependências externas__: Use mocks para simular recursos externos \(banco de dados, arquivos, etc\)\.
- __Garanta independência dos testes__: Os testes devem poder ser executados em qualquer ordem\.
- __Mantenha os testes rápidos__: Testes lentos dificultam a integração contínua\.

__Configurando Dependências no Maven__

No arquivo pom\.xml, adicione as dependências do __JUnit 5__ para testes e do __JaCoCo __para cobertura de código:

<dependency>

    <groupId>org\.junit\.jupiter</groupId>

    <artifactId>junit\-jupiter</artifactId>

    <version>5\.10\.2</version>

```xml
<scope>test</scope>

</dependency>
```

E o plugin do __JaCoCo__ dentro da seção <build>:

<plugin>

    <groupId>org\.jacoco</groupId>

    <artifactId>jacoco\-maven\-plugin</artifactId>

    <version>0\.8\.11</version>

    <executions>

        <execution>

            <goals>

                <goal>prepare\-agent</goal>

            </goals>

        </execution>

        <execution>

            <id>report</id>

            <phase>test</phase>

            <goals>

                <goal>report</goal>

            </goals>

        </execution>

    </executions>

</plugin>

__Tornando Métodos Testáveis__

Para que os métodos possam ser testados, eles não devem ser private\. Altere para static \(sem modificador\) ou public:

// Antes

```text
private static void copyDirectory\(\.\.\.\);

private static int countFiles\(\.\.\.\);
```

// Depois

static void copyDirectory\(\.\.\.\);

static int countFiles\(\.\.\.\);

__Exemplos de Asserts no JUnit__

Além do __assertEquals __e __assertTrue__, o __JUnit __oferece outros métodos úteis:

assertFalse\(condition\);

assertNull\(object\);

assertNotNull\(object\);

assertThrows\(Exception\.class, \(\) \-> \{ /\* código \*/ \}\);

__Utilizando Mocks em Testes__

Para testar métodos que dependem de recursos externos, utilize bibliotecas como __Mockito__:

<dependency>

    <groupId>org\.mockito</groupId>

    <artifactId>mockito\-core</artifactId>

    <version>5\.2\.0</version>

```xml
<scope>test</scope>

</dependency>
```

Exemplo de uso:

import static org\.mockito\.Mockito\.\*;

MyService service = mock\(MyService\.class\);

when\(service\.doSomething\(\)\)\.thenReturn\("resultado"\);

__Integração Contínua e Testes Automatizados__

Configure pipelines de CI \(como GitHub Actions, GitLab CI, Jenkins\) para rodar os testes automaticamente a cada push\. Isso garante que novas alterações não quebrem funcionalidades existentes\.

__Exemplo de pipeline com GitHub Actions__

name: Java CI

on: \[push, pull\_request\]

jobs:

  build:

    runs\-on: ubuntu\-latest

    steps:

      \- uses: actions/checkout@v4

      \- name: Set up JDK 21

        uses: actions/setup\-java@v4

        with:

          distribution: 'temurin'

          java\-version: '21'

      \- name: Build with Maven

        run: mvn clean test

__Testes Parametrizados com JUnit 5__

```python
import org\.junit\.jupiter\.params\.ParameterizedTest;

import org\.junit\.jupiter\.params\.provider\.ValueSource;
```

@ParameterizedTest

@ValueSource\(strings = \{"file1\.txt", "file2\.txt"\}\)

void testFileNames\(String fileName\) \{

    assertTrue\(fileName\.startsWith\("file"\)\);

\}

__Exemplo de Classe de Teste Unitário__

```python
package com\.mulato;

import org\.junit\.jupiter\.api\.Test;

import java\.io\.\*;

import java\.util\.concurrent\.atomic\.AtomicInteger;

import static org\.junit\.jupiter\.api\.Assertions\.\*;

class FileBackupTest \{
```

    @Test

    void testCountFilesEmptyFolder\(\) throws IOException \{

        File tempDir = new File\("testDirEmpty"\);

        tempDir\.mkdir\(\);

        try \{

            int count = FileBackup\.countFiles\(tempDir\);

            assertEquals\(0, count\);

        \} finally \{

            tempDir\.delete\(\);

        \}

    \}

    @Test

    void testCopyDirectory\(\) throws IOException \{

        File sourceDir = new File\("sourceDir"\);

        File destDir = new File\("destDir"\);

        sourceDir\.mkdir\(\);

        destDir\.mkdir\(\);

        File file = new File\(sourceDir, "file\.txt"\);

        try \(FileWriter fw = new FileWriter\(file\)\) \{

            fw\.write\("test"\);

        \}

        AtomicInteger filesProcessed = new AtomicInteger\(0\);

        try \{

            FileBackup\.copyDirectory\(sourceDir, destDir, filesProcessed\);

            File copiedFile = new File\(destDir, "file\.txt"\);

            assertTrue\(copiedFile\.exists\(\)\);

            assertEquals\(1, filesProcessed\.get\(\)\);

        \} finally \{

            file\.delete\(\);

            sourceDir\.delete\(\);

            for \(File f : destDir\.listFiles\(\)\) f\.delete\(\);

            destDir\.delete\(\);

        \}

```json
\}

\}
```

__Testando o Método Main__

Para garantir que o método main executa sem lançar exceções:

```python
package com\.mulato;

import org\.junit\.jupiter\.api\.Test;

import static org\.junit\.jupiter\.api\.Assertions\.assertDoesNotThrow;

public class MainTest \{
```

    @Test

    void testMainRunsWithoutException\(\) \{

        assertDoesNotThrow\(\(\) \-> Main\.main\(new String\[\]\{\}\)\);

```json
\}

\}
```

__Gerando Relatórios de Cobertura com JaCoCo__

Após configurar o plugin, execute:

mvn clean test

O relatório será gerado em: target/site/jacoco/index\.html

Abra esse arquivo no navegador para visualizar a cobertura dos testes\.

![Conteúdo do artigo](img/image_not_found.png)

Exemplo de relatório JaCoCo

__Recursos e Leituras Complementares__

- [__Documentação Oficial do JUnit 5__](https://junit.org/junit5/docs/current/user-guide/)
- [__Mockito \- Site Oficial__](https://site.mockito.org/)
- [__Guia de Cobertura de Código com JaCoCo__](https://www.jacoco.org/jacoco/trunk/doc/)
-  [__Boas Práticas de Testes Unitários \(Martin Fowler\)__](https://martinfowler.com/bliki/UnitTest.html)

__Resumo:__

- Estruture seu projeto conforme o padrão Maven\.
- Adicione __JUnit __e __JaCoCo __ao pom\.xml\.
- Torne métodos utilitários testáveis \(não privados\)\.
- Escreva testes unitários para métodos de lógica\.
- Gere e consulte o relatório de cobertura com __JaCoCo__\.
- Considere automatizar seus testes com pipelines de CI modernos\.
- Compartilhe suas experiências e dúvidas nos comentários\!

__Adendo: Hospedando o Código no GitHub e Publicando em Ambiente Produtivo__

Além de implementar e testar seu projeto localmente, você pode hospedar o código no GitHub e publicar em ambientes produtivos\. Veja como:

__1\. Hospedando no GitHub__

- Crie um repositório no GitHub\.
- Faça o commit do seu projeto local e envie para o repositório remoto:

```bash
git init

git add \.

git commit \-m "Primeiro commit"

git remote add origin https://github\.com/SEU\_USUARIO/NOME\_DO\_REPOSITORIO\.git

git push \-u origin main
```

__2\. Publicando em Ambiente Produtivo__

O método de publicação depende do tipo de aplicação:

- __Aplicação Desktop Java__
- Gere um JAR executável com Maven:

mvn clean package

- Transfira o arquivo \.jar para o servidor ou máquina onde será executado\.
- Execute com:

java \-jar nome\-do\-arquivo\.jar

- __Aplicação Web Java__
- Gere um arquivo \.war ou \.jar e faça o deploy em um servidor de aplicação \(Tomcat, WildFly, etc\.\) ou em serviços de nuvem \(Azure, AWS, Heroku, etc\.\)\.
- __Automação com CI/CD__
- Use GitHub Actions para automatizar testes, builds e até deploys para ambientes de produção\.

__Resumo:__

- GitHub serve para versionamento, colaboração e integração contínua\.
- O deploy em produção depende do tipo de aplicação e do ambiente escolhido\.
- Você pode automatizar o processo de build e deploy usando pipelines de CI/CD\.

Se quiser um exemplo de workflow de deploy ou dicas para um ambiente específico, deixe sua dúvida nos comentários\!

Código\-fonte no GitHub: [__chmulato/backup\_files__](https://github.com/chmulato/backup_files)



## Conclusão

Este artigo apresentou conceitos importantes sobre implementando testes unitários em um projeto java com maven. A implementação demonstrada oferece uma base sólida para desenvolvimento e pode ser expandida conforme as necessidades específicas do projeto.

### Principais Pontos Abordados:

- Conceitos fundamentais e arquitetura
- Implementação prática com exemplos de código
- Boas práticas e recomendações
- Considerações para produção

### Próximos Passos:

- Explore a documentação oficial das tecnologias mencionadas
- Experimente os exemplos de código em seu ambiente
- Adapte as soluções para suas necessidades específicas
- Considere testes e monitoramento em ambientes de produção

## Sobre o Autor

**Christian Mulato** é Desenvolvedor Java Sênior especializado em arquiteturas escaláveis e microsserviços. Com experiência em Spring Boot, Docker, APIs REST e sistemas distribuídos, atua no desenvolvimento de soluções enterprise robustas.

**Conecte-se:**
- [LinkedIn](https://www.linkedin.com/in/chmulato/)
- [GitHub](https://github.com/chmulato)
