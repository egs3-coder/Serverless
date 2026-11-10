# Serverless – Guia de Transporte do Rota Vital

Atividade individual 1 (Serverless) · Infraestrutura de Software · ADS · CESAR School · 2026.2

Função HTTP serverless que **recebe uma requisição de bolsas de sangue do Rota Vital e devolve a guia de transporte**.
Rodada localmente com o **AWS SAM CLI** (emulador do AWS Lambda + API Gateway em Docker).

- **Caminho escolhido:** Caminho A (recomendado) – AWS SAM CLI local, sem conta na AWS e sem cartão.
- **Provedor emulado:** AWS (Lambda + API Gateway).
- **Linguagem:** Python 3.12.
- **Vídeo:** `COLE AQUI O LINK DO VÍDEO`

---

## 1. Estrutura do projeto

```
Serverless/
├── template.yaml              # Infra como código (SAM): função, rota POST /guias, Timeout
├── guia_transporte/
│   ├── app.py                 # Handler da função (lambda_handler)
│   └── requirements.txt       # Sem dependências externas
├── events/
│   ├── pedido.json            # Evento API Gateway com uma requisição válida
│   ├── pedido_demorar.json    # Evento com "demorar": true (para estourar o Timeout)
│   └── pedido_invalido.json   # Evento sem requisicaoId (retorna 400)
├── scripts/chamadas.sh        # Faz as 3 chamadas curl do Passo 4
├── tests/test_app.py          # Testes unitários do handler (pytest, sem Docker)
├── evidencias/                # Prints dos comandos e saídas
└── ROTEIRO_VIDEO.md           # Roteiro do vídeo de 3 minutos
```

## 2. O que a função faz

`POST /guias` com um JSON como:

```json
{ "requisicaoId": "R-001", "hospital": "H-Recife", "bolsas": ["O-NEG-0142"] }
```

Resposta **201**:

```json
{ "guia": "G-R-001", "hospital": "H-Recife", "bolsas": ["O-NEG-0142"], "invocacaoNesteAmbiente": 1 }
```

| Situação | Status |
|---|---|
| Pedido válido | `201` com a guia |
| Sem `requisicaoId` | `400` `{"erro": "requisicaoId obrigatório"}` |
| Body que não é JSON | `400` `{"erro": "body precisa ser um JSON válido"}` |
| `"demorar": true` | dorme 5 s → estoura o `Timeout` de 3 s |

O campo `invocacaoNesteAmbiente` vem de uma **variável global** (`contador`) que só cresce se o mesmo
ambiente de execução (container) for reaproveitado — é ele que usamos para observar cold start × warm start.

### Diferença em relação ao código do enunciado

Nas versões atuais do SAM CLI (testei com a **1.171.0**), o `sam local generate-event apigateway aws-proxy`
gera o body **codificado em base64** (`"isBase64Encoded": true`). O código original fazia `json.loads(body)`
direto e quebrava com `JSONDecodeError`. Por isso o `app.py` decodifica o base64 quando esse campo é `true`.
Também tratei o caso de body inválido devolvendo `400` em vez de deixar a função dar erro.

---

## 3. Como rodar (passo a passo)

> **Windows:** rode todos os comandos no **Git Bash** (ou WSL), como pede o enunciado.

### Passo 1 – Instalar as ferramentas

1. **Docker Desktop**: https://docs.docker.com/get-started/get-docker – abra o Docker Desktop e espere ficar "Running".
2. **AWS SAM CLI**: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
   (no Windows é um instalador `.msi`; feche e abra o terminal depois).
3. **Python 3.12**: https://www.python.org/downloads/
4. Conferir:

```bash
sam --version
docker --version
python --version
```

> Não precisa de conta AWS para rodar local. Se o SAM pedir credenciais, rode `aws configure` com valores falsos
> (ex.: `AKIAFAKE` / `fake` / região `us-east-1`) ou apenas ignore o aviso.

### Passo 2 – Baixar o projeto e fazer o build

```bash
git clone https://github.com/egs3-coder/Serverless.git
cd Serverless
sam build
```

Deve terminar com **Build Succeeded**.

*(Como o projeto foi criado: `sam init` → AWS Quick Start Templates → Hello World Example → Python 3.12 → zip.
Depois troquei o caminho `/hello` por `/guias`, o método `get` por `post`, renomeei a pasta `hello_world` para
`guia_transporte` e substituí o `app.py`.)*

### Passo 3 – Invocar a função com um evento

Os eventos já estão em `events/`. Eles foram gerados assim:

```bash
sam local generate-event apigateway aws-proxy --method POST --path guias \
    --body '{"requisicaoId":"R-001","hospital":"H-Recife","bolsas":["O-NEG-0142"]}' \
    > events/pedido.json
```

Invocar **duas vezes**, medindo o tempo:

```bash
time sam local invoke -e events/pedido.json
time sam local invoke -e events/pedido.json
```

Na saída aparece o `statusCode: 201`, o body com a guia, uma linha `REPORT ... Duration: ... ms` e,
no fim, o tempo `real` do comando.

| Invocação | Tempo `real` | `Duration` (REPORT) | `Init Duration` |
|---|---|---|---|
| 1ª | `___ s` | `___ ms` | `___ ms` |
| 2ª | `___ s` | `___ ms` | `___ ms` |

### Passo 4 – Acionar por HTTP

**Terminal 1:**

```bash
sam local start-api
```

**Terminal 2** (três chamadas):

```bash
bash scripts/chamadas.sh
# ou manualmente, 3 vezes:
curl -X POST http://127.0.0.1:3000/guias -H "Content-Type: application/json" \
    -d '{"requisicaoId":"R-002","hospital":"H-Caruaru"}'
```

Depois pare o servidor (**Ctrl + C**) e suba de novo reaproveitando containers:

```bash
sam local start-api --warm-containers LAZY
```

E repita as três chamadas.

| Modo | `invocacaoNesteAmbiente` nas 3 chamadas |
|---|---|
| `sam local start-api` | `__, __, __` |
| `sam local start-api --warm-containers LAZY` | `__, __, __` |

### Passo 5 – Bater no limite de tempo

Com o `start-api` rodando (Timeout = 3 s no `template.yaml`):

```bash
curl -X POST http://127.0.0.1:3000/guias -H "Content-Type: application/json" \
    -d '{"requisicaoId":"R-003","demorar":true}'
```

Ou por evento: `sam local invoke -e events/pedido_demorar.json`

**Erro registrado:** `COLE AQUI O ERRO` (no terminal do SAM aparece algo como
`Function 'GuiaTransporteFunction' timed out after 3 seconds` e o curl recebe um erro `502`).

Ajuste: no `template.yaml`, em `Globals > Function`, trocar `Timeout: 3` por `Timeout: 10`, e então:

```bash
sam build
sam local start-api
# repetir o curl com "demorar": true  → agora volta 201 depois de ~5 s
```

### Extra – testes unitários (sem Docker)

```bash
pip install pytest
python -m pytest -q
```

---

## 4. Respostas

### 1. Por que a primeira invocação demorou mais que a segunda? O que acontece na fase de Init?

A primeira invocação pega o **cold start**: não existe ainda um ambiente pronto, então a plataforma precisa
criar um. Na fase de **Init** o Lambda baixa o código, sobe o ambiente de execução (na nuvem uma microVM
Firecracker; no SAM local um container Docker), inicializa o runtime do Python e executa tudo o que está
**fora** do handler (imports e variáveis globais, como o `contador = 0`). Só depois disso vem a fase de
**Invoke**, que roda o `lambda_handler`. Na segunda chamada, parte desse trabalho já está feito
(imagem do Docker já baixada/em cache, ambiente quente), então ela é mais rápida.

No meu teste: 1ª = `___ s`, 2ª = `___ s`. *(Observação: com `sam local invoke` cada execução cria um
container novo, então a maior diferença local vem da primeira vez em que o SAM prepara a imagem do runtime.)*

### 2. O que o campo `invocacaoNesteAmbiente` mostrou com e sem `--warm-containers`? O que isso diz sobre guardar estado numa variável global?

- **Sem** `--warm-containers`: deu sempre **1**, porque o SAM cria um container novo a cada requisição,
  então o `contador` sempre recomeça do zero.
- **Com** `--warm-containers LAZY`: deu **1, 2, 3**, porque o mesmo container foi reaproveitado e a
  variável global continuou na memória entre as chamadas.

Conclusão: variável global **não é um lugar confiável para guardar estado**. Ela só sobrevive se a
plataforma decidir reaproveitar o ambiente, o que não é garantido (o ambiente pode ser destruído a qualquer
momento, e com várias requisições simultâneas cada uma pode cair em um ambiente diferente, cada um com seu
próprio contador). Estado de verdade (ex.: número de guias emitidas) tem que ir para um armazenamento
externo, como DynamoDB, um banco relacional ou Redis. A global serve bem para **cache**, por exemplo uma
conexão de banco criada no Init e reaproveitada nas chamadas quentes.

### 3. O que aconteceu com `demorar = true`? Qual o tempo máximo de uma execução no Lambda, e o que fazer com um trabalho mais longo?

Com `Timeout: 3`, a função dormiu 5 s e foi **interrompida pela plataforma aos 3 s**
(`timed out after 3 seconds`); a guia não foi devolvida e o cliente recebeu erro. Depois de subir o
`Timeout` para 10 e refazer o `sam build`, a mesma chamada respondeu 201 depois de uns 5 s.

O tempo máximo de uma execução no AWS Lambda é **900 segundos (15 minutos)**. Para trabalhos mais longos:
dividir em etapas menores e orquestrar com **AWS Step Functions**; processar de forma assíncrona com uma
fila (**SQS**) em vários pedaços; ou levar o trabalho para um serviço sem esse limite, como um container
no **ECS/Fargate** ou o **AWS Batch**.

### 4. Quanto custam 1 milhão de execuções com 128 MB e 100 ms?

Preços de us-east-1: US$ 0,20 por milhão de requisições e US$ 0,0000166667 por GB-s.

**Requisições:**
1.000.000 × (US$ 0,20 / 1.000.000) = **US$ 0,20**

**Computação (GB-s):**
- Memória: 128 MB = 128 / 1024 = **0,125 GB**
- Duração: 100 ms = **0,1 s**
- Por execução: 0,125 GB × 0,1 s = **0,0125 GB-s**
- 1 milhão de execuções: 0,0125 × 1.000.000 = **12.500 GB-s**
- Custo: 12.500 × US$ 0,0000166667 = **≈ US$ 0,2083**

**Total ≈ US$ 0,20 + US$ 0,21 = US$ 0,41** por milhão de execuções.

(Dentro da faixa sempre gratuita — 1 milhão de requisições e 400 mil GB-s por mês — esse volume sairia
de graça.)

### 5. Em que parte do Rota Vital uma função assim faria sentido, e em qual não faria?

**Faz sentido:** em tarefas curtas, sem estado e disparadas por evento, que acontecem de forma irregular:
- gerar a **guia de transporte** quando um hospital faz uma requisição (este exemplo);
- enviar **notificação** (e-mail/SMS/push) quando o status da entrega muda;
- gerar o **PDF/QR Code** da guia;
- receber **webhooks** de parceiros ou validar um pedido antes de gravá-lo.
Nessas partes o volume varia muito ao longo do dia, e pagar só por execução sai mais barato que manter um
servidor ligado.

**Não faz sentido:**
- **rastreamento em tempo real** do veículo com conexão aberta contínua (WebSocket/GPS mandando posição a
  cada segundo) — é carga constante e conexão longa;
- **otimização de rotas** pesada ou relatórios que podem passar de 15 minutos;
- algo que precisa de **estado em memória** entre chamadas (ex.: controle de estoque de bolsas em memória);
- fluxos críticos que não toleram a latência extra de um **cold start** (uma emergência), a não ser com
  concorrência provisionada.

---

## 5. Evidências

Os prints estão na pasta [`evidencias/`](evidencias/) (a lista do que cada print mostra está em
[`evidencias/README.md`](evidencias/README.md)).

## 6. Uso de IA

Declaração conforme a PO-CESAR-021.

- **Ferramenta:** Claude (Anthropic).
- **Finalidade:** ajudar a montar a estrutura do projeto SAM, ajustar o handler para ler o body em base64
  (gerado pelo `sam local generate-event` nas versões novas do SAM CLI), escrever os testes unitários e
  organizar o README e o roteiro do vídeo.
- **Como validei:** rodei eu mesmo todos os comandos dos Passos 2 a 5 na minha máquina (prints em
  `evidencias/`), conferi as respostas da função e os tempos, rodei `python -m pytest` (5 testes passando)
  e `sam validate --lint`, refiz a conta de custo à mão e revisei/reescrevi as respostas com as minhas
  palavras com base no material da Aula 007 e na documentação da AWS.

## 7. Referências

- Ciclo de vida do ambiente de execução do Lambda: https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html
- Cotas do Lambda: https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
- Preços do Lambda: https://aws.amazon.com/lambda/pricing
- SAM CLI – instalação: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
