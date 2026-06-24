import os
import pandas as pd
import string
import nltk

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

# Baixar recursos do NLTK
nltk.download('stopwords')

diretorio_base = os.path.dirname(os.path.abspath(__file__))
diretorio_arquivos = os.path.join(diretorio_base, 'arquivos')

# Carrega o CSV com as avaliações
df = pd.read_csv(os.path.join(diretorio_arquivos, "dataset_avaliacoes_simulado.csv"), sep=',')

df = df.dropna(subset=['avaliacao'])
df = df[df['sentimento'].isin(['Positivo', 'Negativo'])]

def limpar_texto(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('portuguese'))
    palavras = text.split()
    palavras = [p for p in palavras if p not in stop_words]
    return ' '.join(palavras)

# Aplica o pré-processamento
df['avaliacao_processada'] = df['avaliacao'].apply(limpar_texto)

# Vetorização com CountVectorizer
vectorizer_bow = CountVectorizer()
X_bow = vectorizer_bow.fit_transform(df['avaliacao_processada'])

# Vetorização com TF-IDF
vectorizer_tfidf = TfidfVectorizer()
X_tfidf = vectorizer_tfidf.fit_transform(df['avaliacao_processada'])

# Exibe as primeiras 5 linhas da matriz TF-IDF (como DataFrame)
df_tfidf = pd.DataFrame(X_tfidf.toarray(), columns=vectorizer_tfidf.get_feature_names_out())
#print(df_tfidf.head)

#Colunas geradas
print(vectorizer_tfidf.get_feature_names_out())

# Criação de uma coluna binária para o sentimento
df['sentimento_bin'] = df['sentimento'].map({'Positivo': 1, 'Negativo': 0})
y = df['sentimento_bin']

# Divisão dos dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

modelos = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Multinomial NB": MultinomialNB(),
    "Linear SVC": LinearSVC(),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
}

for nome, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    print(f"\n=== {nome} ===")
    print("Acurácia:", accuracy_score(y_test, y_pred))
    print("Matriz de Confusão:\n", confusion_matrix(y_test, y_pred))
    print("Relatório:\n", classification_report(y_test, y_pred))








