# src/summarizer.py
import nltk
from nltk.tokenize import sent_tokenize
from logger import logger

class Summarizer:
    def __init__(self):
        pass

    def summarize(self, text, doc_length):
        try:
            sentences = sent_tokenize(text)
            if doc_length <= 10:
                summary = ' '.join(sentences[:10])  # Concise for short docs
            elif 10 < doc_length <= 30:
                summary = ' '.join(sentences[:15])  # Moderate for medium docs
            else:
                summary = ' '.join(sentences[:25])  # Detailed for long docs
            logger.info("Generated summary.")
            return summary
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return ""
