import pandas as pd
import joblib
import os

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from funcoes.modelo_texto import TextoPreprocessador


diretorio_base = os.path.dirname(os.path.abspath(__file__))
diretorio_arquivos = os.path.join(diretorio_base, 'arquivos')

# Carrega dataset
df = pd.read_csv(os.path.join(diretorio_arquivos, "dataset_avaliacoes_simulado.csv"), sep=',')
df = df.dropna(subset=['avaliacao'])
df = df[df['sentimento'].isin(['Positivo', 'Negativo'])]

# Mapeia sentimentos para binário
df['sentimento_bin'] = df['sentimento'].map({'Positivo': 1, 'Negativo': 0})

# Divide dados
X = df['avaliacao']
y = df['sentimento_bin']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Cria pipeline
pipeline = Pipeline([
    ('limpeza', TextoPreprocessador()),
    ('vetorizador', TfidfVectorizer()),
    ('classificador', LinearSVC())
])

# Treina modelo
pipeline.fit(X_train, y_train)

# Avaliação
y_pred = pipeline.predict(X_test)
print("Acurácia:", accuracy_score(y_test, y_pred))
print("Matriz de Confusão:\n", confusion_matrix(y_test, y_pred))
print("Relatório de Classificação:\n", classification_report(y_test, y_pred))

# Salva o pipeline treinado
joblib.dump(pipeline, os.path.join(diretorio_base, 'modelos', 'modelo_sentimento.pkl'))
print("Modelo salvo como 'modelo_sentimento.pkl'")

# Faz a predição dos sentimentos nas avaliações
df['sentimento_predito'] = pipeline.predict(df['avaliacao'])

# (Opcional) Salva o dataset atualizado
df.to_csv(os.path.join(diretorio_arquivos, 'dataset_com_predicao.csv') , index=False)
