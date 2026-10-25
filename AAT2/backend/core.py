"""AAT-2: information-retrieval question answering (TF-IDF over unigrams + bigrams)."""
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)


def build_index(documents):
    sentences, owner = [], []
    for d, text in enumerate(documents, start=1):
        for s in nltk.sent_tokenize(text):
            sentences.append(s)
            owner.append(d)
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
    return sentences, owner, vec, vec.fit_transform(sentences)


def answer(question, documents, k=3):
    sentences, owner, vec, matrix = build_index(documents)
    scores = cosine_similarity(vec.transform([question]), matrix)[0]
    order = scores.argsort()[::-1][:k]
    hits = [{"rank": r + 1, "sentence": sentences[i], "doc": owner[i], "score": round(float(scores[i]), 4)}
            for r, i in enumerate(order)]
    found = bool(hits) and hits[0]["score"] > 0
    best = int(order[0])
    # answer window: if the next/previous sentence of the SAME document also matches, include it
    # (resolves answers that sit behind a pronoun, e.g. "It was commissioned by ...")
    window = [best]
    for j in (best - 1, best + 1):
        if 0 <= j < len(sentences) and owner[j] == owner[best] and scores[j] > 0:
            window.append(j)
    passage = " ".join(sentences[i] for i in sorted(window))
    return {"question": question,
            "answer": passage if found else "Sorry, no sentence in the documents matches this question.",
            "top_sentence": sentences[best] if found else "",
            "hits": hits, "sentences": len(sentences), "documents": len(documents),
            "vocabulary": len(vec.vocabulary_)}


def run(payload):
    return answer(payload["question"], payload["documents"])
