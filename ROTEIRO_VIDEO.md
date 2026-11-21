# Vídeo da atividade

**Gravação de tela:** https://youtu.be/dx7wEBCqURE

Gravado no Google Cloud Shell com dois terminais: um rodando o servidor (`sam local start-api`) e outro
fazendo as chamadas.

## O que o vídeo mostra, em ordem

| # | Terminal | Comando | Resultado |
|---|---|---|---|
| 1 | comandos | `time sam local invoke -e events/pedido.json` | HTTP 201 com a guia `G-R-001` e a linha `REPORT` |
| 2 | servidor | `sam local start-api` | rota `POST /guias` publicada na porta 3000 |
| 3 | comandos | `bash scripts/chamadas.sh` | `invocacaoNesteAmbiente` 1, 1, 1 (container novo a cada chamada) |
| 4 | servidor | `sam local start-api --warm-containers LAZY` | servidor reiniciado reaproveitando o container |
| 5 | comandos | `bash scripts/chamadas.sh` | `invocacaoNesteAmbiente` 1, 2, 3 (container reaproveitado) |
| 6 | comandos | `curl` sem `requisicaoId` | HTTP 400 `requisicaoId obrigatório` |
| 7 | comandos | `curl` com `"demorar": true` | HTTP 502 em ~3 s |
| 8 | servidor | (log) | `timed out after 3 seconds` |

## Vídeo complementar

[`video/Serverless_RotaVital_video_legendado.mp4`](video/Serverless_RotaVital_video_legendado.mp4): resumo
de 2min55s, sem áudio e com legendas, montado a partir dos prints de `evidencias/`. Cobre também o código, o
template, o evento, o gráfico de tempos, o ajuste para `Timeout: 10`, a conta de custo e o uso no Rota Vital.
