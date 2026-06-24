import pandas as pd

# Carrega o mesmo dataset
df = pd.read_csv(r'C:\Users\Vinicius Ribeiro\Downloads\dataset_avaliacoes_simulado.csv')

# Garante que os sentimentos estejam binarizados
df = df[df['sentimento'].isin(['Positivo', 'Negativo'])]
df['sentimento_bin'] = df['sentimento'].map({'Positivo': 1, 'Negativo': 0})

# Agrupa por curso e calcula média de sentimentos
df_resultado = df.groupby('curso')['sentimento_bin'].mean().reset_index()

# Ordena pelos cursos mais bem avaliados
df_resultado = df_resultado.sort_values(by='sentimento_bin', ascending=False)

# Exibe os 5 melhores cursos
print("Top 5 cursos recomendados com base nos sentimentos das avaliações:")
print(df_resultado.head(5))
