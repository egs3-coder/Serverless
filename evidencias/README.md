# Evidências

Prints das execuções no Google Cloud Shell, com o AWS SAM CLI emulando o Lambda e o API Gateway.

| Arquivo | O que mostra |
|---|---|
| `01-versoes.png` | Versões instaladas: SAM CLI 1.171.0, Docker 29.9.3 e Python 3.12.3 |
| `02-sam-build.png` | `sam build --use-container` terminando em **Build Succeeded** |
| `03-04-invoke.png` | Duas execuções de `time sam local invoke -e events/pedido.json`: `statusCode 201`, guia `G-R-001`, linha `REPORT` e tempo `real` (3,57 s e 3,97 s) |
| `05-start-api.png` | `sam local start-api` publicando a rota `POST /guias` em `http://127.0.0.1:3000` |
| `06-curl-sem-warm.png` | 3 chamadas curl sem `--warm-containers`: `invocacaoNesteAmbiente` 1, 1, 1 |
| `07-curl-warm-lazy.png` | 3 chamadas curl com `--warm-containers LAZY`: `invocacaoNesteAmbiente` 1, 2, 3 (1,08 s → 0,04 s) |
| `08a-timeout-3s.png` | curl com `"demorar": true` e `Timeout: 3`: HTTP 502 em 3,14 s |
| `08b-timeout-servidor.png` | Log do SAM: `timed out after 3 seconds`, `Duration: 3000.00 ms` |
| `09-timeout-10s.png` | `Timeout: 10` no template e a mesma chamada respondendo HTTP 201 em 5,04 s |
| `10a-resposta-400-curl.png` | curl sem `requisicaoId`: HTTP 400 com `{"erro": "requisicaoId obrigatório"}` |
| `10b-resposta-400-servidor.png` | Log do SAM com as chamadas registradas como `"POST /guias HTTP/1.1" 400` |
