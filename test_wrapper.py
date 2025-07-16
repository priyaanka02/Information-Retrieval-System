# test_wrapper.py (updated for PR03)

from document import Document
from re import Pattern

# === Task 2 ===
def remove_stopwords_by_list(doc: Document, stopwords: set[str]):
    from my_module import remove_stop_words
    doc._filtered_terms = remove_stop_words(doc.terms, stopwords)

def remove_stopwords_by_frequency(doc: Document, collection: list[Document], common_frequency: float, rare_frequency: float):
    from my_module import remove_stop_words_by_frequency
    doc._filtered_terms = remove_stop_words_by_frequency(doc.terms, collection, low_freq=rare_frequency, high_freq=common_frequency)

def load_documents_from_url(url: str, author: str, origin: str, start_line: int, end_line: int, search_pattern: Pattern[str]) -> list[Document]:
    from my_module import load_collection_from_url
    return load_collection_from_url(url, search_pattern, start_line, end_line, author, origin)

def linear_boolean_search(term, collection, stopword_filtered=False, stemmed=False):
    from my_module import linear_boolean_search
    return linear_boolean_search(term, collection, stopword_filtered, stemmed)

# === Task 3 ===
def stem_term(word: str) -> str:
    from my_module import stem_term
    return stem_term(word)

def vector_space_search(query: str, collection: list[Document], stopword_filtered=False, stemmed=False):
    from my_module import vector_space_search
    return vector_space_search(query, collection, stopword_filtered, stemmed)

def precision_recall(retrieved: set[str], relevant: set[str]) -> tuple[float, float]:
    from my_module import precision_recall
    return precision_recall(retrieved, relevant)
