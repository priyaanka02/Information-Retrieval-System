# 🧠 Information Retrieval System

A powerful and modular **Information Retrieval (IR)** engine that supports Boolean Search, Vector Space Model (TF-IDF + Cosine Similarity), stopword removal, stemming, and performance evaluation using precision & recall. 

> Built as part of MSc AI coursework, this system lets you explore how classic IR concepts are implemented and evaluated.

---

## 👩‍💻 Authors

- **Priyanka Choudhary**  
- **Samyuktha Alfred**  

📅 July 2025 | 🐍 Python 3.10+

---

## 📂 Project Structure

- **IR-system/**
  - `main.py` — CLI interface  
  - `my_module.py` — All core logic  
  - `document.py` — Document class  
  - `porter_stemmer.py` — Custom Porter stemmer  
  - `test_wrapper.py` — Wrapper for tests  
  - `gt_aesop.json` — Ground truth for Aesop dataset  
  - `gt_grimm.json` — Ground truth for Grimm dataset  
  - `stemming_algorithm.txt` — Notes on stemming  
  - **public_tests/** — PR02 tests + stopword list  
    - `englishST.txt`  
  - **pr03_tests_v1.0/** — PR03 unit tests  
  - `README.md` — This fabulous file 💁‍♀️



---
## 🚀 Features

Everything your inner search engine geek dreams of 💭:

- ✅ **Load & parse documents from a URL** — with regex-based splitting  
- ✅ **Tokenization & normalization** — clean text, clean conscience  
- ✅ **Stopword removal** — both list-based & frequency-based  
- ✅ **Boolean Search** — with optional stemming & stopword filtering  
- ✅ **Vector Space Model (TF-IDF + Cosine Similarity)** — fancy math, accurate results  
- ✅ **Precision & Recall Evaluation** — using ground truth JSONs  
- ✅ **Custom Porter Stemmer** — hand-coded, academic paper style 🤓  

---

## 🧪 How to Run

### 👉 CLI Mode

In the same directory as the files, we used the command prompt to run - 
python main.py


### 📋 Menu Options

Once you run the CLI, you’ll be prompted with a little menu to:

- 📂 **Load documents**  
- ✂️ **Remove stopwords**  
- 🌱 **Toggle stemming**  
- 🔍 **Perform Boolean or VSM search**  
- 📊 **Evaluate results with ground truth**

---

### 🧪 Running Tests

Use your fave Python testing tool — whether it’s `pytest`, `unittest`, or whatever you're vibing with — to run tests located in:

- 🧾 `public_tests/`  
- 🧪 `pr03_tests_v1.0/`

---

## 📊 Sample Use Case

Here’s how you can slay the IR game step-by-step:

1. 📚 **Load documents** — Aesop’s Fables or Grimm’s Fairy Tales from Project Gutenberg.  
2. 🐺 **Search for terms** — like `wolf` or `princess` using Boolean or VSM.  
3. 🌱 **Toggle options** — enable/disable stemming and stopword removal as needed.  
4. 📈 **Evaluate performance** — measure precision & recall using the ground truth JSONs.  
5. 👀 **Analyze results** — see how your IR system is serving accuracy.

---

## 💡 Notes

- 🧠 The **custom Porter Stemmer** follows the OG 1980 algorithm paper — old but gold.  
- 🧹 You get **full control** over preprocessing: stemming, stopwords, the whole shebang.  
- 🧩 The design is **super modular**, so you can plug in cool stuff later —  
  like ranking models, better tokenizers, or even *transformers* 👀.

---




