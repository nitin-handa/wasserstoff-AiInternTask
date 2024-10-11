import nltk
import spacy

def setup():
    nltk.download('punkt')
    nltk.download('stopwords')
    spacy.cli.download('en_core_web_sm')

if __name__ == "__main__":
    setup()
