import re
from typing import List
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading punkt")
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading punkttab")
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading stopwords")
    nltk.download('stopwords')


class TextPreprocessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess(self, text: str) -> List[str]:
        tokens = word_tokenize(text)

        tokens = [re.sub(r'[^a-z]', '', token.lower()) for token in tokens]
        tokens = [t for t in tokens if t]  # non empty str

        tokens = [self.stemmer.stem(token) for token in tokens]

        tokens = [token for token in tokens if token not in self.stop_words]

        return tokens


def preprocess_documents(documents: List[str]) -> List[List[str]]:
    preprocessor = TextPreprocessor()
    preprocessed = []

    for i,doc in enumerate(documents):
        tokens = preprocessor.preprocess(doc)
        preprocessed.append(tokens)
       

    return preprocessed



