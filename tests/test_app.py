"""Testes unitários do handler (rodam sem Docker: python -m pytest)."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "guia_transporte"))
import app  # noqa: E402

EVENTS = os.path.join(os.path.dirname(__file__), "..", "events")


def carregar(nome):
    with open(os.path.join(EVENTS, nome), encoding="utf-8") as f:
        return json.load(f)


def test_gera_guia_com_evento_base64():
    resp = app.lambda_handler(carregar("pedido.json"), None)
    corpo = json.loads(resp["body"])
    assert resp["statusCode"] == 201
    assert corpo["guia"] == "G-R-001"
    assert corpo["hospital"] == "H-Recife"
    assert corpo["bolsas"] == ["O-NEG-0142"]


def test_body_texto_puro_como_no_curl():
    evento = {"body": json.dumps({"requisicaoId": "R-002", "hospital": "H-Caruaru"})}
    resp = app.lambda_handler(evento, None)
    assert resp["statusCode"] == 201
    assert json.loads(resp["body"])["bolsas"] == []


def test_sem_requisicao_id_retorna_400():
    resp = app.lambda_handler(carregar("pedido_invalido.json"), None)
    assert resp["statusCode"] == 400


def test_json_invalido_retorna_400():
    resp = app.lambda_handler({"body": "isso não é json"}, None)
    assert resp["statusCode"] == 400


def test_contador_cresce_no_mesmo_ambiente():
    antes = app.contador
    app.lambda_handler({"body": '{"requisicaoId":"X"}'}, None)
    app.lambda_handler({"body": '{"requisicaoId":"Y"}'}, None)
    assert app.contador == antes + 2
