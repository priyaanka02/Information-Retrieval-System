# main.py (updated with stemming, VSM, and evaluation)

import re
import json
import urllib.request
from my_module import (
    load_collection_from_url,
    linear_boolean_search,
    vector_space_search,
    remove_stop_words,
    remove_stop_words_by_frequency,
    stem_terms,
    precision_recall,
)
from document import Document

collection = []
ground_truth = {}
stemming_enabled = False


def show_menu():
    print("\nWelcome to the IR System!")
    print("1. Load document collection")
    print("2. Remove stop words (from list)")
    print("3. Remove stop words (by frequency)")
    print("4. Search documents")
    print("5. Load ground truth file")
    print("6. Toggle stemming")
    print("7. Exit")


def load_documents():
    global collection
    url = input("Enter the URL of the text file: ").strip()
    start = int(input("Enter start line: "))
    end = int(input("Enter end line (or -1 for till end): "))
    author = input("Enter author name: ").strip()
    origin = input("Enter origin/source title: ").strip()

    import re

    pattern = re.compile('^THE\\s+([A-Z\\s\\-]+)\\n\\n(.*?)(?=\\n\\nTHE\\s+[A-Z\\s\\-]+|\\Z)', re.DOTALL | re.MULTILINE)
    print("Trying pattern on trimmed text...")
    test_url = urllib.request.urlopen(url)
    raw_text = test_url.read().decode('utf-8')
    lines = raw_text.splitlines()
    lines = lines[start:end] if end > 0 else lines[start:]
    trimmed_text = "\n".join(lines)
    matches = pattern.findall(trimmed_text)
    print(f"Matches found: {len(matches)}")

    print("Downloading and processing...")

    collection = load_collection_from_url(url, pattern, start, end, author, origin)
    print(f"Loaded {len(collection)} documents.")


def remove_by_list():
    if not collection:
        print("You must load documents first.")
        return
    path = input("Enter stopwords file path (e.g., public_tests/englishST.txt): ").strip()
    with open(path, "r", encoding="utf-8") as f:
        stopwords = set(f.read().split())
    for doc in collection:
        doc._filtered_terms = remove_stop_words(doc.terms, stopwords)
        doc._filtered_stemmed_terms = stem_terms(doc._filtered_terms)
    print("Stopwords removed using list.")


def remove_by_frequency():
    if not collection:
        print("You must load documents first.")
        return
    for doc in collection:
        doc._filtered_terms = remove_stop_words_by_frequency(doc.terms, collection)
        doc._filtered_stemmed_terms = stem_terms(doc._filtered_terms)
    print("Stopwords removed using frequency.")


def load_ground_truth():
    global ground_truth
    path = input("Enter path to ground truth JSON file: ").strip()
    try:
        with open(path, "r", encoding="utf-8") as f:
            ground_truth = json.load(f)
        print("Ground truth file loaded successfully.")
    except Exception as e:
        print(f"Failed to load ground truth file: {e}")


def toggle_stemming():
    global stemming_enabled
    stemming_enabled = not stemming_enabled
    print(f"Stemming is now {'enabled' if stemming_enabled else 'disabled'}.")


def search_docs():
    if not collection:
        print("You must load documents first.")
        return

    query = input("Enter search query (single or multiple terms): ").strip().lower()
    use_filtered = input("Use filtered terms? (y/n): ").strip().lower() == 'y'
    use_vsm = input("Use Vector Space Model? (y/n): ").strip().lower() == 'y'

    if use_vsm:
        results = vector_space_search(query, collection, stopword_filtered=use_filtered, stemmed=stemming_enabled)
        results = sorted(results, key=lambda x: -x[0])
    else:
        results = linear_boolean_search(query, collection, stopword_filtered=use_filtered, stemmed=stemming_enabled)

    print("\nSearch Results:")
    retrieved_ids = set()
    for score, doc in results:
        if (use_vsm and score > 0) or (not use_vsm and score == 1):
            print(doc)
            retrieved_ids.add(doc.title.lower().strip().replace(" ", "_"))

    if ground_truth:
        query_terms = query.split()
        relevant_ids = set()
        for term in query_terms:
            if term in ground_truth:
                relevant_ids.update(ground_truth[term])
        precision, recall = precision_recall(retrieved_ids, relevant_ids)
        print(f"\nPrecision: {precision:.2f}, Recall: {recall:.2f}")
    else:
        print("\nNo ground truth loaded, skipping evaluation.")


def main():
    while True:
        show_menu()
        choice = input("Select an option (1-7): ").strip()
        if choice == "1":
            load_documents()
        elif choice == "2":
            remove_by_list()
        elif choice == "3":
            remove_by_frequency()
        elif choice == "4":
            search_docs()
        elif choice == "5":
            load_ground_truth()
        elif choice == "6":
            toggle_stemming()
        elif choice == "7":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
