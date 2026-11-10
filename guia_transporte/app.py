"""
Rota Vital - Função serverless que gera a GUIA DE TRANSPORTE de uma requisição.

Fluxo: o hospital (ou o sistema do Rota Vital) envia um POST /guias com a
requisição de bolsas de sangue; a função valida o pedido e devolve a guia
que acompanha o transporte.

Baseado no código do enunciado (Atividade individual 1 - Serverless),
com dois ajustes:
  1. Decodifica o body quando ele vem em base64 (isBase64Encoded = true),
     que é o formato gerado pelo `sam local generate-event` nas versões
     recentes do SAM CLI.
  2. Devolve 400 quando o body não é um JSON válido, em vez de estourar erro.
"""
import base64
import json
import time

# Variável GLOBAL: fica fora do handler, então é criada na fase de Init.
# Ela só "sobrevive" entre chamadas se o mesmo ambiente de execução
# (container) for reaproveitado. Não é um lugar confiável para guardar estado.
contador = 0


def _resposta(status, corpo):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(corpo, ensure_ascii=False),
    }


def _ler_body(event):
    body = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")
    return json.loads(body)


def lambda_handler(event, context):
    global contador
    contador += 1

    try:
        pedido = _ler_body(event)
    except (ValueError, TypeError):
        return _resposta(400, {"erro": "body precisa ser um JSON válido"})

    if "requisicaoId" not in pedido:
        return _resposta(400, {"erro": "requisicaoId obrigatório"})

    if pedido.get("demorar"):
        time.sleep(5)  # passa do Timeout de 3 s definido no template.yaml

    guia = {
        "guia": "G-" + pedido["requisicaoId"],
        "hospital": pedido.get("hospital"),
        "bolsas": pedido.get("bolsas", []),
        "invocacaoNesteAmbiente": contador,
    }
    return _resposta(201, guia)
