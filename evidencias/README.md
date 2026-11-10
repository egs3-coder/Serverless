# Evidências

Coloque aqui os prints (PNG/JPG) de cada etapa. Use estes nomes para o professor achar fácil:

| Arquivo | O que o print precisa mostrar |
|---|---|
| `01-versoes.png` | `sam --version`, `docker --version` e `python --version` |
| `02-sam-build.png` | Saída de `sam build` terminando em **Build Succeeded** |
| `03-invoke-1.png` | 1ª `time sam local invoke -e events/pedido.json` (resposta 201 + tempo `real`) |
| `04-invoke-2.png` | 2ª invocação igual, com o tempo |
| `05-start-api.png` | Terminal com `sam local start-api` mostrando `Mounting GuiaTransporteFunction at http://127.0.0.1:3000/guias [POST]` |
| `06-curl-sem-warm.png` | 3 chamadas curl **sem** `--warm-containers` (`invocacaoNesteAmbiente` sempre 1) |
| `07-curl-warm-lazy.png` | 3 chamadas curl **com** `--warm-containers LAZY` (1, 2, 3) |
| `08-timeout-3s.png` | Chamada com `"demorar":true` e o erro `timed out after 3 seconds` |
| `09-timeout-10s.png` | `template.yaml` com `Timeout: 10`, novo `sam build` e a chamada com `"demorar":true` dando 201 |
| `10-testes.png` (opcional) | `python -m pytest -q` com os 5 testes passando |
