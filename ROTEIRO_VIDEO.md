# Vídeo da atividade

**Gravação de tela:** https://youtu.be/hXN19j9MliY

Gravado no Google Cloud Shell com dois terminais: um rodando o servidor (`sam local start-api`) e outro
fazendo as chamadas.

## O que o vídeo mostra, em ordem

| # | Terminal | Comando | Resultado |
|---|---|---|---|
| 1 | chamadas | `time sam local invoke -e events/pedido.json` | HTTP 201 com a guia `G-R-001` e a linha `REPORT` |
| 2 | servidor | `sam local start-api` | rota `POST /guias` publicada na porta 3000 |
| 3 | chamadas | `bash scripts/chamadas.sh` | `invocacaoNesteAmbiente` 1, 1, 1 (container novo a cada chamada) |
| 4 | servidor | `sam local start-api --warm-containers LAZY` | servidor reiniciado reaproveitando o container |
| 5 | chamadas | `bash scripts/chamadas.sh` | `invocacaoNesteAmbiente` 1, 2, 3 (container reaproveitado) |
| 6 | chamadas | `curl` sem `requisicaoId` | HTTP 400 `{"erro": "requisicaoId obrigatório"}` |
| 7 | chamadas | `curl` com `"demorar": true` | HTTP 502 em ~3 s |
| 8 | servidor | (log) | `timed out after 3 seconds` |

Os prints de cada etapa estão em [`evidencias/`](evidencias/).
