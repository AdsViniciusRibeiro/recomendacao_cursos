import pandas as pd
import joblib
from flask import Flask, jsonify, request

from config import CSV_PADRAO, MINIMO_AVALIACOES, MODELO_SENTIMENTO, QTD_RETORNO
from database import banco_esta_vazio, criar_tabelas, importar_csv, obter_sessao
from repositorio_avaliacoes import recomendar_cursos, salvar_avaliacao


app = Flask(__name__)
_modelo = None
_erro_modelo = None


def obter_modelo():
    global _modelo, _erro_modelo
    if _modelo is not None:
        return _modelo
    if _erro_modelo is not None:
        raise RuntimeError(_erro_modelo)

    try:
        _modelo = joblib.load(MODELO_SENTIMENTO)
    except Exception as exc:
        _erro_modelo = f"Nao foi possivel carregar o modelo de sentimento: {exc}"
        raise RuntimeError(_erro_modelo) from exc
    return _modelo


def preparar_banco() -> None:
    criar_tabelas()
    if not CSV_PADRAO.exists():
        return

    with obter_sessao() as sessao:
        if banco_esta_vazio(sessao):
            importar_csv(sessao, str(CSV_PADRAO))


def _inteiro_query(nome: str, padrao: int, minimo: int = 1) -> int:
    valor = request.args.get(nome, padrao)
    try:
        valor = int(valor)
    except (TypeError, ValueError):
        return padrao
    return max(valor, minimo)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/classificar", methods=["POST"])
def classificar():
    data = request.get_json() or {}
    avaliacao = str(data.get("avaliacao") or "").strip()
    curso = str(data.get("curso") or "").strip()
    usuario = str(data.get("usuario") or "desconhecido").strip() or "desconhecido"

    if not avaliacao or not curso:
        return jsonify({"erro": "Campos 'curso' e 'avaliacao' sao obrigatorios."}), 400

    try:
        modelo = obter_modelo()
    except RuntimeError as exc:
        return jsonify({"erro": str(exc)}), 500

    #pred = int(modelo.predict(pd.Series([avaliacao]))[0])
    pred = int(modelo.predict([avaliacao])[0])
    sentimento = "Positivo" if pred == 1 else "Negativo"

    with obter_sessao() as sessao:
        registro = salvar_avaliacao(
            sessao,
            curso=curso,
            usuario=usuario,
            avaliacao=avaliacao,
            sentimento=sentimento,
            sentimento_bin=pred,
        )

    return jsonify(
        {
            "id": registro.id,
            "sentimento_previsto": sentimento,
            "sentimento_bin": pred,
            "registro_salvo": True,
        }
    ), 201


@app.route("/recomendar", methods=["GET"])
def recomendar():
    palavra_chave = request.args.get("palavra_chave", "").strip()
    minimo_avaliacoes = _inteiro_query("minimo_avaliacoes", MINIMO_AVALIACOES)
    limite = _inteiro_query("limite", QTD_RETORNO)

    with obter_sessao() as sessao:
        ranking = recomendar_cursos(
            sessao,
            palavra_chave=palavra_chave,
            minimo_avaliacoes=minimo_avaliacoes,
            limite=limite,
        )

    if not ranking and palavra_chave:
        return jsonify({"mensagem": f'Nenhum curso encontrado com "{palavra_chave}".'}), 404
    if not ranking:
        return jsonify({"mensagem": "Nenhum curso com avaliacoes suficientes."}), 404

    return jsonify(ranking)


preparar_banco()


if __name__ == "__main__":
    app.run(debug=True)
