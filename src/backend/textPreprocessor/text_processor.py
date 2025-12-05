import re
from typing import List
import nltk
from nltk.tokenize import word_tokenize
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

STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
    'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her',
    'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs',
    'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
    'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
    'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
    'very', 's', 't', 'can', 'just', 'don', 'should', 'now'
}


class TextPreprocessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = STOPWORDS

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



