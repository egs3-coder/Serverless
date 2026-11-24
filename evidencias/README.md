# Evidências

Prints das execuções no Google Cloud Shell, em ordem.

| Arquivo | O que mostra |
|---|---|
| `01-versoes.png` | SAM CLI 1.171.0, Docker 29.9.3 e Python 3.12.3 |
| `02-sam-build.png` | `sam build --use-container` terminando em **Build Succeeded** |
| `03-invoke.png` | Duas execuções de `sam local invoke -e events/pedido.json`: 201, guia `G-R-001`, `REPORT` e tempo `real` (3,57 s e 3,97 s) |
| `04-start-api.png` | `sam local start-api` publicando `POST /guias` em `http://127.0.0.1:3000` |
| `05-curl-sem-warm.png` | 3 chamadas sem `--warm-containers`: contador 1, 1, 1 |
| `06-curl-warm-lazy.png` | 3 chamadas com `--warm-containers LAZY`: contador 1, 2, 3 (1,08 s → 0,04 s) |
| `07a-resposta-400-curl.png` | Pedido sem `requisicaoId`: HTTP 400 `requisicaoId obrigatório` |
| `07b-resposta-400-servidor.png` | Log do SAM com `"POST /guias HTTP/1.1" 400` |
| `08a-timeout-3s.png` | `"demorar": true` com `Timeout: 3`: HTTP 502 em 3,14 s |
| `08b-timeout-servidor.png` | Log do SAM: `timed out after 3 seconds`, `Duration: 3000.00 ms` |
| `09-timeout-10s.png` | Com `Timeout: 10`: HTTP 201 em 5,04 s |
