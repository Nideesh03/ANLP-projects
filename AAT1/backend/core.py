"""AAT-1: POS tagging and named entity recognition with spaCy."""
import spacy

nlp = spacy.load("en_core_web_sm")


def analyse(text):
    doc = nlp(text)
    words = [{"word": tok.text, "upos": tok.pos_, "penn": tok.tag_, "lemma": tok.lemma_,
              "dep": tok.dep_, "explain": spacy.explain(tok.pos_) or ""}
             for tok in doc if not tok.is_space and not tok.is_punct]
    entities = [{"text": ent.text, "label": ent.label_, "explain": spacy.explain(ent.label_) or "",
                 "start": ent.start_char, "end": ent.end_char} for ent in doc.ents]
    tag_count = {}
    for w in words:
        tag_count[w["upos"]] = tag_count.get(w["upos"], 0) + 1
    return {"words": words, "entities": entities,
            "tag_count": dict(sorted(tag_count.items(), key=lambda kv: -kv[1])),
            "noun_chunks": [c.text for c in doc.noun_chunks], "sentences": len(list(doc.sents)),
            "model": f"{nlp.meta['lang']}_{nlp.meta['name']} {nlp.meta['version']}"}


def run(payload):
    return analyse(payload.get("text", ""))
