# CSOnline - Parte III: Segurança JWT, Autorização por Papéis e Testes 100% Verdes

![Evolução da aplicação CSOnline - Gestão de Centro de Distribuição (CDs)](/articles/assets/img/2025_08_09_IMAGE_001.png)

## O que evoluiu nesta fase

Nesta terceira etapa avançamos em segurança, qualidade e preparo para a integração total do ***frontend* Vue** com o ***backend* Jakarta EE**. O sistema agora possui autenticação JWT robusta, autorização por papéis coerente nos endpoints, suíte de testes completa e scripts de desenvolvimento mais amigáveis.

Principais destaques:

- Segurança ponta a ponta com **JWT** (autenticação) e autorização por papéis (@RolesAllowed)
- Matriz de permissões alinhada aos casos de uso reais (**ADMIN, BUSINESS, COURIER, CUSTOMER**)
- Cobertura de **100% dos testes automatizados** com JUnit 5 e configuração para CI
- Scripts PowerShell otimizados para build, testes e execução one-click

---

## Segurança Enterprise com Jakarta Security

### Implementação JWT Robusta

Substituímos a autenticação básica por uma **infraestrutura completa de JWT**:

- **AuthResource.java** - Endpoint /auth/login para criação de tokens
- **JWTAuthenticationMechanism** - Mecanismo padronizado para validação de tokens
- **JWTIdentityStore** - Armazenamento seguro de credenciais
- **Filtros automáticos** para endpoints protegidos (@RolesAllowed)

### Modelo de Autorização por Papéis

Matriz de papéis baseada nos perfis reais do negócio:

- **ADMIN** - Acesso total, configurações, perfis de usuário
- **BUSINESS** - Operação comercial, rotas, monitoramento
- **COURIER** - Entregadores, visualização de rotas e confirmações
- **CUSTOMER** - Clientes com acesso ao tracking e histórico

Cada endpoint protegido agora possui **anotação específica** que valida o papel do usuário:

```java
@Path("/api/deliveries")
@RolesAllowed({"ADMIN", "BUSINESS"})
public class DeliveryResource {
    // Métodos protegidos por autorização de papéis
}
```

## Testes de Segurança: Cobertura Total

### Suite de Testes Ampliada

Adicionamos uma **bateria completa de testes** que validam a segurança:

- **JWT Creation Tests** - Valida geração de tokens
- **Authentication Tests** - Testa fluxo completo de login
- **Authorization Tests** - Verifica acesso por papel
- **Invalid Token Tests** - Confirma rejeição de tokens inválidos
- **Expired Token Tests** - Testa comportamento com tokens expirados

### Status dos Testes: 100% Verdes

Os **20 cenários de teste** implementados estão todos passando, garantindo:

- Criação e validação correta de tokens JWT
- Proteção contra tokens expirados/inválidos
- Autorização apropriada por papel em cada endpoint
- Rejeição de tokens sem permissões adequadas
- Tempo de vida configurável para sessões

## Tooling Aprimorado: DevX em Foco

### Scripts PowerShell Otimizados

Refinamos os scripts de desenvolvimento para melhorar a experiência:

- **build.ps1** - Compilação limpa com opção de testes
- **run.ps1** - Execução rápida com opções de ambiente
- **test.ps1** - Testes unitários com relatório
- **clean.ps1** - Limpeza completa de artefatos

### Documentação Estruturada

Nova estrutura de documentação:

- **doc/INDEX.md** - Guia geral de uso
- **doc/SECURITY.md** - Detalhes da implementação JWT
- **doc/API.md** - Referência para consumo de endpoints
- **doc/TESTING.md** - Guia de testes e validação

## Como Testar a Segurança JWT

Para experimentar a implementação JWT, você pode:

1. Executar o servidor: `./run.ps1`
2. Autenticar via POST: `curl -X POST http://localhost:8080/csonline/api/auth/login -d "{\"username\":\"admin\",\"password\":\"password\"}" -H "Content-Type: application/json"`
3. Usar o token retornado: `curl -H "Authorization: Bearer SEU_TOKEN_JWT" http://localhost:8080/csonline/api/users`

Os testes automatizados também podem ser executados para verificar a segurança:
```
./test.ps1
```

## Próximos Passos: Rumo à Entrega MVP

Com a **segurança** e **qualidade** estabelecidas, os próximos passos incluem:

- **Frontend:** integrar telas ao *backend*, melhorar UX/UI, criar guards por papel, estados vazios e feedbacks.

- **Backend:** refinar validações, paginação/ordenação de listagens, monitoramento e métricas.

- **QA:** cenários E2E (Cypress/Playwright) para fluxos críticos de autenticação e autorização.

- **DevOps:** pipelines de CI/CD e empacotamento para ambientes (**dev/homolog/prod**).

Faça um fork do repositório em [**https://github.com/chmulato/csonline**](https://github.com/chmulato/csonline) e confira a documentação em **doc/INDEX.md**. Pull Requests são bem-vindos!

[![Christian Mulato](/articles/assets/img/foto_chri.jpg)](https://www.linkedin.com/in/chmulato/)
