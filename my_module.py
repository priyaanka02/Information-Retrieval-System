# my_module.py (updated)

import urllib.request
import re
import math
from collections import Counter, defaultdict
from document import Document

# === TASK 1 + 2 (LOADING + TOKENIZATION) ===

def load_collection_from_url(url, search_pattern, start_line, end_line, author, origin):
    response = urllib.request.urlopen(url)
    raw_text = response.read().decode('utf-8')

    lines = raw_text.splitlines()
    lines = lines[start_line:end_line] if end_line > 0 else lines[start_line:]
    trimmed_text = "\n".join(lines)

    matches = search_pattern.findall(trimmed_text)
    documents = []
    for i, match in enumerate(matches):
        title, story_text = match
        clean_text = story_text.replace('\n', ' ').strip()
        terms = tokenize(clean_text)
        doc = Document(
            document_id=i,
            title=title.strip(),
            raw_text=clean_text,
            terms=terms,
            author=author,
            origin=origin
        )
        documents.append(doc)
    return documents

def tokenize(text):
    text = re.sub(r"[^\w\s']", '', text)
    return text.lower().split()


# === TASK 3: BOOLEAN SEARCH (with stemming support added) ===

def linear_boolean_search(term, collection, stopword_filtered=False, stemmed=False):
    from my_module import stem_term
    term = term.lower()
    if stemmed:
        term = stem_term(term)

    results = []
    for doc in collection:
        if stemmed and stopword_filtered:
            terms_to_check = doc._filtered_stemmed_terms
        elif stemmed:
            terms_to_check = doc._stemmed_terms
        elif stopword_filtered:
            terms_to_check = doc._filtered_terms
        else:
            terms_to_check = doc.terms

        if term in [t.lower() for t in terms_to_check]:
            results.append((1, doc))
        else:
            results.append((0, doc))
    return results


# === TASK 4: STOP WORD REMOVAL ===

def remove_stop_words(terms, stopwords):
    stopwords = {word.lower() for word in stopwords}
    return [term.lower() for term in terms if term.lower() not in stopwords]

def remove_stop_words_by_frequency(terms, collection, low_freq=0.01, high_freq=0.8):
    all_terms = []
    for doc in collection:
        all_terms.extend(term.lower() for term in doc.terms)

    total_docs = len(collection)
    term_doc_freq = Counter()

    for doc in collection:
        seen = set()
        for term in doc.terms:
            norm = term.lower()
            if norm not in seen:
                seen.add(norm)
                term_doc_freq[norm] += 1

    stopwords = set()
    for term, df in term_doc_freq.items():
        freq = df / total_docs
        if freq <= low_freq or freq >= high_freq:
            stopwords.add(term)

    return [term.lower() for term in terms if term.lower() not in stopwords]


# === TASK 3.1: PORTER STEMMER ===

def stem_term(word):
    from porter_stemmer import stem  # We will create this module next
    return stem(word)

def stem_terms(terms):
    return [stem_term(t) for t in terms]


# === TASK 3.2: VECTOR SPACE SEARCH ===

def vector_space_search(query, collection, stopword_filtered=False, stemmed=False):
    query_terms = tokenize(query)
    if stemmed:
        query_terms = stem_terms(query_terms)

    inverted_index = defaultdict(lambda: defaultdict(int))
    doc_lengths = defaultdict(float)
    total_docs = len(collection)

    for doc in collection:
        if stemmed and stopword_filtered:
            terms = doc._filtered_stemmed_terms
        elif stemmed:
            terms = doc._stemmed_terms
        elif stopword_filtered:
            terms = doc._filtered_terms
        else:
            terms = doc.terms

        tf = Counter(terms)
        for term in tf:
            inverted_index[term][doc.document_id] = tf[term]

    scores = defaultdict(float)
    query_tf = Counter(query_terms)
    for term in query_tf:
        df = len(inverted_index.get(term, {}))
        if df == 0:
            continue
        idf = math.log(total_docs / df)
        query_weight = query_tf[term] * idf
        for doc_id, tf in inverted_index[term].items():
            scores[doc_id] += tf * idf * query_weight

    for doc_id in scores:
        doc = collection[doc_id]
        if stemmed and stopword_filtered:
            terms = doc._filtered_stemmed_terms
        elif stemmed:
            terms = doc._stemmed_terms
        elif stopword_filtered:
            terms = doc._filtered_terms
        else:
            terms = doc.terms

        tf = Counter(terms)
        length = math.sqrt(sum((tf[t] * math.log(total_docs / len(inverted_index.get(t, {})))) ** 2 for t in tf))
        doc_lengths[doc_id] = length

    result = []
    for doc_id, score in scores.items():
        if doc_lengths[doc_id] == 0:
            similarity = 0.0
        else:
            similarity = score / doc_lengths[doc_id]
        result.append((similarity, collection[doc_id]))
    return result


# === TASK 3.3: PRECISION + RECALL ===

def precision_recall(retrieved, relevant):
    if not retrieved:
        return (0.0, 0.0)
    if not relevant:
        return (0.0, 0.0)

    tp = len(retrieved & relevant)
    precision = tp / len(retrieved)
    recall = tp / len(relevant)
    return (precision, recall)
