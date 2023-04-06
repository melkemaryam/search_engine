import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Load English language model in Spacy
nlp = spacy.load('en_core_web_sm')

# Load NLTK stop words
nltk.download('stopwords')
stopwords = set(nltk.corpus.stopwords.words('english'))
# go one directory pack and add to path
import sys
sys.path.append('../')

# Define function for text pre-processing
def preprocess_text(text):
    # Tokenize sentences using Spacy
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    # Tokenize words using NLTK and remove stop words, punctuations, and numbers
    words = [word.lower() for sent in sentences for word in word_tokenize(sent)
             if word.lower() not in stopwords and word.isalpha() or word.isnumeric()]


    return ' '.join(words)