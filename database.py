from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime

import pandas as pd
from sqlalchemy import DateTime, Integer, String, Text, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from config import DATABASE_URL


class Base(DeclarativeBase):
    pass


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    curso: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    usuario: Mapped[str] = mapped_column(String(255), nullable=False, default="desconhecido")
    avaliacao: Mapped[str] = mapped_column(Text, nullable=False)
    sentimento: Mapped[str] = mapped_column(String(20), nullable=False)
    sentimento_bin: Mapped[int] = mapped_column(Integer, nullable=False)
    sentimento_predito: Mapped[int] = mapped_column(Integer, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


def criar_tabelas() -> None:
    Base.metadata.create_all(bind=engine)


@contextmanager
def obter_sessao():
    sessao = SessionLocal()
    try:
        yield sessao
        sessao.commit()
    except Exception:
        sessao.rollback()
        raise
    finally:
        sessao.close()


def banco_esta_vazio(sessao: Session) -> bool:
    total = sessao.scalar(select(func.count(Avaliacao.id)))
    return total == 0


def importar_csv(sessao: Session, caminho_csv: str) -> int:
    df = pd.read_csv(caminho_csv)
    df = df.dropna(subset=["curso", "avaliacao"])
    df = df[df["sentimento"].isin(["Positivo", "Negativo"])].copy()

    if "sentimento_bin" not in df.columns:
        df["sentimento_bin"] = df["sentimento"].map({"Positivo": 1, "Negativo": 0})
    if "sentimento_predito" not in df.columns:
        df["sentimento_predito"] = df["sentimento_bin"]

    registros = []
    for row in df.to_dict(orient="records"):
        registros.append(
            Avaliacao(
                curso=str(row["curso"]),
                usuario=str(row.get("usuario") or "desconhecido"),
                avaliacao=str(row["avaliacao"]),
                sentimento=str(row["sentimento"]),
                sentimento_bin=int(row["sentimento_bin"]),
                sentimento_predito=int(row["sentimento_predito"]),
            )
        )

    sessao.add_all(registros)
    sessao.flush()
    return len(registros)
