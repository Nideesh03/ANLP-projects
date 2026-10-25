"""AAT-5: synonyms, definitions and context senses with NLTK WordNet + simplified Lesk."""
import nltk
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk

for res, path in (("wordnet", "corpora/wordnet"), ("omw-1.4", "corpora/omw-1.4"), ("punkt_tab", "tokenizers/punkt_tab")):
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(res, quiet=True)

POS_NAME = {"n": "noun", "v": "verb", "a": "adjective", "s": "adjective (satellite)", "r": "adverb"}


def lookup(word, limit=8):
    senses = []
    for s in wn.synsets(word)[:limit]:
        senses.append({"synset": s.name(), "pos": POS_NAME.get(s.pos(), s.pos()), "definition": s.definition(),
                       "examples": s.examples()[:1],
                       "synonyms": sorted({l.name().replace("_", " ") for l in s.lemmas()} - {word})})
    all_syn = sorted({l.name().replace("_", " ") for s in wn.synsets(word) for l in s.lemmas()} - {word})
    return {"word": word, "sense_count": len(wn.synsets(word)), "senses": senses, "all_synonyms": all_syn}


def sense_in_context(word, sentence, pos=None):
    tokens = nltk.word_tokenize(sentence.lower())
    s = lesk(tokens, word, pos=pos or None)
    if s is None:
        return {"word": word, "sentence": sentence, "synset": None, "definition": "No sense found"}
    return {"word": word, "sentence": sentence, "pos_hint": pos or "-", "synset": s.name(),
            "definition": s.definition()}


# ---- extended Lesk: overlap with gloss + examples + lemma names of the sense, its hypernyms and hyponyms ----
STOP = set("a an the of to in on at for by and or is are was were be been it its this that with as from "
           "because too so very enough please his her he she they them their than into out over".split())


_stem = nltk.PorterStemmer().stem


def _bag(text):
    words = {w.strip(".,;:()'\"").lower() for w in text.split()} - STOP - {""}
    return {_stem(w) for w in words}


def _signature(s):
    parts = [s.definition()] + s.examples() + [l.name().replace("_", " ") for l in s.lemmas()]
    for rel in s.hypernyms() + s.hyponyms()[:10]:
        parts += [rel.definition()] + [l.name().replace("_", " ") for l in rel.lemmas()]
    return _bag(" ".join(parts))


def extended_lesk(word, sentence, pos=None):
    ctx = _bag(sentence) - {_stem(word)}
    best, best_score, best_overlap = None, -1, []
    for s in wn.synsets(word, pos=pos or None):
        overlap = sorted(ctx & _signature(s))
        if len(overlap) > best_score:
            best, best_score, best_overlap = s, len(overlap), overlap
    if best is None:
        return {"synset": None, "definition": "No sense found", "overlap": []}
    return {"synset": best.name(), "definition": best.definition(), "overlap": best_overlap}


def run(payload):
    word = payload["word"].strip().lower()
    out = lookup(word)
    out["contexts"] = []
    for c in payload.get("contexts", []):
        if not c.get("sentence", "").strip():
            continue
        row = sense_in_context(word, c["sentence"], c.get("pos"))
        ext = extended_lesk(word, c["sentence"], c.get("pos"))
        row.update({"ext_synset": ext["synset"], "ext_definition": ext["definition"], "overlap": ext["overlap"]})
        out["contexts"].append(row)
    return out
