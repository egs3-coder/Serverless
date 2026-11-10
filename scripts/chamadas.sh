#!/usr/bin/env bash
# Faz as chamadas HTTP do Passo 4 (3x) contra o `sam local start-api`.
# Uso (em OUTRO terminal, com o start-api rodando):  bash scripts/chamadas.sh
URL="${URL:-http://127.0.0.1:3000/guias}"

for i in 1 2 3; do
  echo "--- Chamada $i ---"
  curl -s -X POST "$URL" -H "Content-Type: application/json" \
       -d '{"requisicaoId":"R-002","hospital":"H-Caruaru"}' \
       -w "\n(HTTP %{http_code} em %{time_total}s)\n"
done
