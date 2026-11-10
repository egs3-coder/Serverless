# Roteiro do vídeo (até 3 minutos)

Grave a tela (Windows: **Win + Alt + R** com a Xbox Game Bar, ou OBS Studio). Deixe o terminal com fonte grande.
Antes de gravar: Docker Desktop aberto, `sam build` já rodado uma vez (para não perder tempo baixando imagem).

| Tempo | O que mostrar | O que falar (sugestão) |
|---|---|---|
| 0:00–0:20 | Repositório no GitHub e o `app.py` | "Essa é a função que gera a guia de transporte do Rota Vital. Ela lê o body, valida o `requisicaoId` e devolve a guia." |
| 0:20–1:00 | `time sam local invoke -e events/pedido.json` **duas vezes** | "Aqui invoco com o evento no formato do API Gateway. Volta 201 com a guia G-R-001. Notem o tempo de cada execução." |
| 1:00–1:50 | Terminal 1: `sam local start-api`. Terminal 2: `bash scripts/chamadas.sh` | "Agora por HTTP. Sem warm containers, `invocacaoNesteAmbiente` fica sempre 1." Pare, suba com `--warm-containers LAZY`, rode de novo: "Agora sobe 1, 2, 3, porque o container foi reaproveitado." |
| 1:50–2:40 | curl com `"demorar":true` → erro. Muda `Timeout: 10`, `sam build`, sobe de novo, repete → 201 | "A função dorme 5 s e o limite é 3 s: estourou o tempo. Aumentando para 10 s, a mesma chamada funciona." |
| 2:40–3:00 | README com as respostas | "No README estão o passo a passo, as evidências e as respostas. Obrigado." |

Suba o vídeo no YouTube como **Não listado** (ou no Google Drive com acesso "qualquer pessoa com o link") e cole o link no README.
