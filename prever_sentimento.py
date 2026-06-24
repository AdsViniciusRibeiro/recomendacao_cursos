import joblib
import pandas as pd

# Carrega o modelo treinado
modelo = joblib.load('modelo_sentimento.pkl')

# Nova avaliação como pandas.Series
nova_avaliacao = pd.Series(["O curso foi excelente, adorei a explicação."])

# Previsão
pred = modelo.predict(nova_avaliacao)

# Saída
print("Sentimento:", "Positivo" if pred[0] == 1 else "Negativo")
