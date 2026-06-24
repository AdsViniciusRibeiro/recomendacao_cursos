from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from config import CSV_PADRAO
from database import banco_esta_vazio, criar_tabelas, importar_csv, obter_sessao


def main() -> None:
    caminho_csv = Path(sys.argv[1]) if len(sys.argv) > 1 else CSV_PADRAO
    if not caminho_csv.exists():
        raise FileNotFoundError(f"CSV nao encontrado: {caminho_csv}")

    criar_tabelas()
    with obter_sessao() as sessao:
        if not banco_esta_vazio(sessao):
            print("Banco ja possui avaliacoes. Migracao cancelada para evitar duplicidade.")
            return
        total = importar_csv(sessao, str(caminho_csv))

    print(f"Migracao concluida: {total} avaliacoes importadas.")


if __name__ == "__main__":
    main()

