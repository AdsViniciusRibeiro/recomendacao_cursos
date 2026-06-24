import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent 
CSV_PADRAO = BASE_DIR / "arquivos" / "dataset_com_predicao.csv"
MODELO_SENTIMENTO = BASE_DIR / "modelos" / "modelo_sentimento.pkl"
SQLITE_PADRAO = BASE_DIR / "banco" / "recomendacoes.db"

MINIMO_AVALIACOES = int(os.getenv("MINIMO_AVALIACOES", "5"))
QTD_RETORNO = int(os.getenv("QTD_RETORNO", "5"))


def _normalizar_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


DATABASE_URL = _normalizar_database_url(
    os.getenv("DATABASE_URL", f"sqlite:///{SQLITE_PADRAO.as_posix()}")
)

