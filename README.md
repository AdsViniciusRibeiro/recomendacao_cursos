# Sistema de recomendacao de cursos

API Flask para classificar avaliacoes de cursos por sentimento e recomendar cursos com maior proporcao de avaliacoes positivas.

## Instalar dependencias

```bash
pip install -r requirements.txt
```

## Avaliar modelos

Use o arquivo `resultado_modelos.py` para treinar e comparar as metricas de diferentes algoritmos antes de decidir qual usar no sistema.

```bash
python resultado_modelos.py
```

Ele avalia os seguintes modelos:

```python
modelos = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Multinomial NB": MultinomialNB(),
    "Linear SVC": LinearSVC(),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
}
```

O script exibe acuracia, matriz de confusao e relatorio de classificacao para cada modelo. Com esses resultados, a pessoa pode escolher o algoritmo mais adequado para o conjunto de avaliacoes.

## Treinar modelo final

Depois de escolher o melhor modelo, use `treinamento_ml.py` para treinar o pipeline final. Neste projeto, o modelo definido para uso foi `LinearSVC`.

```bash
python treinamento_ml.py
```

Esse script:

- carrega `arquivos/dataset_avaliacoes_simulado.csv`;
- treina o pipeline com preprocessamento de texto, TF-IDF e classificador;
- salva o modelo treinado em `modelos/modelo_sentimento.pkl`;
- gera `arquivos/dataset_com_predicao.csv` com os sentimentos preditos.

## Rodar com SQLite

SQLite e o banco padrao. Na primeira execucao, o arquivo `banco/recomendacoes.db` sera criado e populado a partir de `arquivos/dataset_com_predicao.csv`, caso ainda esteja vazio.

```bash
python app.py
```

Tambem e possivel migrar o CSV manualmente:

```bash
python scripts/migrar_csv_para_db.py
```

## Rodar com Postgres

Configure a variavel `DATABASE_URL` antes de iniciar a API:

```bash
set DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/recomendacoes
python scripts/migrar_csv_para_db.py
python app.py
```

Em PowerShell:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://usuario:senha@localhost:5432/recomendacoes"
python scripts\migrar_csv_para_db.py
python app.py
```

## Endpoints

`GET /health`

Retorna o status da API.

`POST /classificar`

```json
{
  "curso": "Python para Dados",
  "usuario": "Maria",
  "avaliacao": "Excelente curso, conteudo claro e pratico."
}
```

`GET /recomendar?palavra_chave=python&minimo_avaliacoes=5&limite=5`

Retorna os cursos mais recomendados pelo percentual de avaliacoes positivas.
