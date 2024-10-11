# # src/keyword_extractor.py
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from rake_nltk import Rake
# from logger import logger
# import spacy

# class KeywordExtractor:
#     def __init__(self):
#         self.stop_words = set(stopwords.words('english'))
#         self.nlp = spacy.load('en_core_web_sm')
#         self.rake = Rake()

#     def extract_keywords(self, text):
#         try:
#             # Using RAKE for initial keyword extraction
#             self.rake.extract_keywords_from_text(text)
#             kw = self.rake.get_ranked_phrases()
#             # Further refining with spaCy for domain-specificity
#             doc = self.nlp(' '.join(kw))
#             refined_keywords = [token.text for token in doc if token.is_alpha and token.text.lower() not in self.stop_words]
#             logger.info("Extracted keywords.")
#             return refined_keywords
#         except Exception as e:
#             logger.error(f"Error extracting keywords: {e}")
#             return []


# src/keyword_extractor.py
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from logger import logger

class KeywordExtractor:
    def extract_keywords(self, text):
        # Extract domain-specific keywords from the text using TF-IDF.
        try:
            vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_array = np.array(vectorizer.get_feature_names_out())
            tfidf_sorting = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]

            top_n = 20  # Number of top keywords
            top_n_ids = tfidf_sorting[:top_n]
            keywords = feature_array[top_n_ids].tolist()
            return keywords
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
