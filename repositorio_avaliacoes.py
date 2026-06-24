from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import Avaliacao


def salvar_avaliacao(
    sessao: Session,
    *,
    curso: str,
    usuario: str,
    avaliacao: str,
    sentimento: str,
    sentimento_bin: int,
) -> Avaliacao:
    registro = Avaliacao(
        curso=curso,
        usuario=usuario,
        avaliacao=avaliacao,
        sentimento=sentimento,
        sentimento_bin=sentimento_bin,
        sentimento_predito=sentimento_bin,
    )
    sessao.add(registro)
    sessao.flush()
    return registro


def recomendar_cursos(
    sessao: Session,
    *,
    palavra_chave: str = "",
    minimo_avaliacoes: int = 5,
    limite: int = 5,
) -> list[dict]:
    sentimento = func.coalesce(Avaliacao.sentimento_predito, Avaliacao.sentimento_bin)
    consulta = (
        select(
            Avaliacao.curso.label("curso"),
            func.count(Avaliacao.id).label("quantidade"),
            func.avg(sentimento).label("proporcao_positiva"),
        )
        .where(sentimento.is_not(None))
        .group_by(Avaliacao.curso)
        .having(func.count(Avaliacao.id) >= minimo_avaliacoes)
        .order_by(func.avg(sentimento).desc(), func.count(Avaliacao.id).desc(), Avaliacao.curso.asc())
        .limit(limite)
    )

    if palavra_chave:
        consulta = consulta.where(func.lower(Avaliacao.curso).contains(palavra_chave.lower()))

    resultados = sessao.execute(consulta).all()
    return [
        {
            "curso": row.curso,
            "quantidade": int(row.quantidade),
            "proporcao_positiva": round(float(row.proporcao_positiva), 4),
        }
        for row in resultados
    ]

