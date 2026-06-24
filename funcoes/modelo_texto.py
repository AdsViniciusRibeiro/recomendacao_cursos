from sklearn.base import BaseEstimator, TransformerMixin
import string
import nltk
import pandas as pd
from nltk.corpus import stopwords

nltk.download('stopwords')

class TextoPreprocessador(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.stop_words = set(stopwords.words('portuguese'))

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if not isinstance(X, pd.Series):
            X = pd.Series(X)
        return X.apply(self._limpar_texto)

    def _limpar_texto(self, text):
        text = str(text).lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        words = [word for word in words if word not in self.stop_words]
        return ' '.join(words)

