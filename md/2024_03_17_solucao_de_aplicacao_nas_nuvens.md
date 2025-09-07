![Computação em nuvem](/articles/assets/img/2024_03_17_IMAGE_001.png)

# Solução de aplicação nas nuvens

*17 de março de 2024*

**Apache OpenWhisk** é uma plataforma *serverless* de código aberto que executa funções em resposta a eventos em qualquer escala. Ela gerencia a infraestrutura, servidores e escalabilidade usando **contêineres Docker**, permitindo que você se concentre em construir aplicativos incríveis e eficientes.

## Principais características do Apache OpenWhisk

**1. Execução de Funções (fx)**  
O OpenWhisk permite escrever **lógica funcional** (chamada de **Actions**) em qualquer linguagem suportada. Essas ações são executadas em resposta a eventos (via **Triggers**) de fontes externas (**Feeds**) ou de **solicitações HTTP**.

**2. Deploys em Qualquer Lugar**  
Como o OpenWhisk utiliza contêineres, ele suporta várias opções de implantação: localmente ou em infraestruturas de nuvem, incluindo **Kubernetes**, **OpenShift** e **Compose**.

**3. Suporte a Múltiplas Linguagens**  
O OpenWhisk trabalha com diversas linguagens: **Go, Java, NodeJS, .NET, PHP, Python, Ruby, Rust, Scala** e **Swift**. Existe também um runtime experimental para **Deno** em desenvolvimento.

**4. Integração com Serviços Populares**  
O OpenWhisk facilita a integração com serviços populares através de **Packages**: filas **Kafka**, bancos **Cloudant**, notificações push, mensagens do **Slack** e feeds **RSS**. O pacote **Alarms** permite agendar execuções em horários específicos ou intervalos recorrentes.

**5. Composições Avançadas**  
Você pode combinar funções em composições poderosas, usando código em diferentes linguagens (**JavaScript/NodeJS, Swift, Python, Java**) ou executar lógica personalizada via **Docker**.

Em resumo, o **Apache OpenWhisk** oferece uma maneira flexível e escalável de criar aplicativos serverless, permitindo que você se concentre na lógica de negócios e na criação de soluções independentes de nuvem.

---

## Exemplo prático: criando uma ação no OpenWhisk

Veja como criar uma ação simples que soma dois números:

```javascript
// Javascript - Arquivo: soma.js
function main(params) {
  const { num1, num2 } = params;
  
  if (!num1 || !num2) {
    return { error: 'Por favor, forneça os números para somar.' };
  }
  
  const resultado = num1 + num2;
  return { resultado };
}
```

Neste exemplo:
- Criamos uma função `main` que recebe parâmetros
- Verificamos se ambos os números foram fornecidos
- Retornamos o resultado da soma em formato JSON

Para criar esta ação no OpenWhisk, use o comando:

```bash
wsk action create minha-soma soma.js
```

Para invocar a ação com parâmetros:

```bash
wsk action invoke minha-soma --param num1 10 --param num2 20
```

O resultado será um objeto JSON com a soma:

```json
{
  "resultado": 30
}
```

Este é apenas um exemplo básico. O OpenWhisk oferece recursos mais avançados como gatilhos, regras e composições para criar soluções serverless complexas.

---

## Instalação local do OpenWhisk (Linux)

Para usar o **Apache OpenWhisk** localmente em um sistema Linux, siga estas etapas:

**1. Instale o Docker e Docker Compose**
- Certifique-se de ter o **Docker** instalado
- Instale o **Docker Compose** para gerenciar múltiplos contêineres

**2. Clone o repositório**
```bash
git clone https://github.com/apache/openwhisk.git
```

**3. Configure o ambiente**
```bash
cd openwhisk/tools/ubuntu-setup
./all.sh
```

**4. Inicie o OpenWhisk**
```bash
docker-compose -f docker-compose.yml -f docker-compose.local.yml up
```

**5. Verifique a instalação**
- Acesse http://localhost:3233 para ver a interface da API

**6. Configure o CLI**
- Instale o CLI do OpenWhisk (wsk)
- Configure-o para o ambiente local:
```bash
wsk property set --apihost localhost --auth <sua_chave_de_autenticação>
```

**7. Crie e execute ações**
- Comece a criar suas próprias ações usando o CLI

Essa é uma configuração básica para uso local.

---

## Implantação em ambiente de produção

Implantar uma ação do **Apache OpenWhisk** em produção envolve algumas etapas importantes:

![Um exemplo esquemático das tecnologias envolvidas.](/articles/assets/img/2024_03_17_IMAGE_003.png)

**1. Configuração do Ambiente**
- Configure um ambiente OpenWhisk: local (Kubernetes ou Docker Compose) ou em nuvem pública (IBM Cloud, AWS, Google Cloud)
- Obtenha as credenciais corretas para acesso

**2. Empacotamento da Ação**
- Empacote sua ação em um arquivo ZIP ou contêiner Docker
- Inclua o código e todas as dependências necessárias

**3. Criação da Ação**
```bash
wsk action create minha-soma soma.js
```

**4. Teste da Ação**
- Teste sua ação antes da implantação em produção
- Use `wsk action invoke` com diferentes parâmetros

**5. Gerenciamento de Segurança**
- Configure as permissões adequadas para cada ação
- Utilize **chaves de API** ou **tokens de autenticação**

**6. Monitoramento e Logs**
- Implemente monitoramento com métricas, logs e alertas
- Considere ferramentas como **Prometheus**, **Grafana** ou serviços de nuvem

**7. Escalabilidade e Redundância**
- Planeje como sua ação se comportará sob carga
- Implemente redundância para evitar pontos únicos de falha

**8. Implantação Final**
- Utilize `wsk action update` ou ferramentas de CI/CD
- Monitore o comportamento após a implantação

Consulte a [documentação oficial do Apache OpenWhisk](https://openwhisk.apache.org/documentation.html) para práticas recomendadas e detalhes específicos sobre implantação em produção.

---

[![Christian Mulato](/articles/assets/img/fo)](https://www.linkedin.com/in/chmulato/)

[**Christian Mulato**](https://www.linkedin.com/in/chmulato/)

Desenvolvedor Java Sênior na Develcode
