"""AAT-4: topic modelling with Latent Dirichlet Allocation (scikit-learn)."""
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


def topics(documents, n_topics=3, top_n=5, seed=9, max_iter=50):
    vec = CountVectorizer(stop_words="english", lowercase=True, min_df=1)
    dtm = vec.fit_transform(documents)
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=seed, max_iter=max_iter,
                                    learning_method="batch", doc_topic_prior=0.1, topic_word_prior=0.05)
    doc_topic = lda.fit_transform(dtm)
    vocab = vec.get_feature_names_out()
    result = []
    for k, weights in enumerate(lda.components_):
        dist = weights / weights.sum()
        idx = dist.argsort()[::-1][:top_n]
        result.append({"topic": k + 1, "words": [{"word": vocab[i], "p": round(float(dist[i]), 4)} for i in idx]})
    docs = [{"doc": i + 1, "text": d, "topic": int(row.argmax()) + 1, "share": round(float(row.max()), 3)}
            for i, (d, row) in enumerate(zip(documents, doc_topic))]
    return {"topics": result, "documents": docs, "vocabulary": len(vocab), "n_docs": len(documents),
            "perplexity": round(float(lda.perplexity(dtm)), 2), "seed": seed}


def run(payload):
    docs = [d.strip() for d in payload["documents"] if d.strip()]
    return topics(docs, int(payload.get("n_topics", 3)), int(payload.get("top_n", 5)), int(payload.get("seed", 9)))
