"""AAT-3: Retrieval-Augmented Generation over the Neo4j Movies graph.

Knowledge source : live Neo4j when NEO4J_URI is set, otherwise data/movies.json (export of the same graph).
Generator        : any OpenAI-compatible chat API when LLM_API_KEY is set, otherwise a labelled template answer.
"""
import json
import os
import re

import requests

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "movies.json")


class GraphStore:
    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        if uri:
            from neo4j import GraphDatabase
            self.driver = GraphDatabase.driver(
                uri, auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "")))
            self.driver.verify_connectivity()
            self.source = f"Neo4j database at {uri}"
            rows = self.cypher("MATCH (m:Movie) RETURN m.title AS title, m.released AS released, m.tagline AS tagline")
            self.movies = {r["title"]: r for r in rows}
            self.people = {r["name"]: r["born"] for r in
                           self.cypher("MATCH (p:Person) RETURN p.name AS name, p.born AS born")}
            self.rels = self.cypher(
                "MATCH (p:Person)-[r]->(m:Movie) RETURN p.name AS person, type(r) AS type, "
                "r.roles AS roles, r.rating AS rating, r.summary AS summary, m.title AS movie")
        else:
            self.driver = None
            d = json.load(open(DATA))
            self.source = "offline JSON export (data/movies.json)"
            self.movies = {m["title"]: m for m in d["movies"]}
            self.people = {p["name"]: p.get("born") for p in d["people"]}
            self.rels = d["relationships"]

    def cypher(self, query, **params):
        return [r.data() for r in self.driver.execute_query(query, **params).records]

    # each helper corresponds to one Cypher pattern
    def about_movie(self, title):
        # MATCH (m:Movie {title:$t}) OPTIONAL MATCH (p:Person)-[r]->(m) RETURN m, p, r
        m = self.movies[title]
        rs = [r for r in self.rels if r["movie"] == title]
        out = [f"'{title}' came out in {m['released']}" +
               (f" with the tagline \"{m['tagline']}\"." if m.get("tagline") else ".")]
        for rel, word in (("DIRECTED", "director(s)"), ("WROTE", "writer(s)"), ("PRODUCED", "producer(s)")):
            names = sorted(r["person"] for r in rs if r["type"] == rel)
            if names:
                out.append(f"The {word} of '{title}': {', '.join(names)}.")
        cast = sorted(f"{r['person']} ({'/'.join(r.get('roles') or [])})" for r in rs if r["type"] == "ACTED_IN")
        if cast:
            out.append(f"Actors in '{title}': " + ", ".join(cast) + ".")
        for r in rs:
            if r["type"] == "REVIEWED":
                out.append(f"{r['person']} rated '{title}' {r.get('rating')}/100: \"{r.get('summary')}\".")
        return out

    def about_person(self, name):
        # MATCH (p:Person {name:$n})-[r]->(m:Movie) RETURN type(r), m.title, m.released
        rs = [r for r in self.rels if r["person"] == name]
        born = self.people.get(name)
        out = [f"{name} was born in {born}." if born else f"The graph has no birth year for {name}."]
        for rel, verb in (("ACTED_IN", "acted in"), ("DIRECTED", "directed"), ("WROTE", "wrote"),
                          ("PRODUCED", "produced"), ("REVIEWED", "reviewed")):
            films = sorted({(self.movies[r["movie"]]["released"], r["movie"]) for r in rs if r["type"] == rel})
            if films:
                out.append(f"{name} {verb}: " + ", ".join(f"{t} ({y})" for y, t in films) + ".")
        return out

    def released_in(self, year):
        # MATCH (m:Movie {released:$year}) RETURN m.title
        films = sorted(t for t, m in self.movies.items() if m["released"] == year)
        return [f"Movies from {year} in the graph: {', '.join(films) if films else 'none'}."]


_store = None


def get_store():
    global _store
    if _store is None:
        _store = GraphStore()
    return _store


def retrieve(question):
    g, q = get_store(), question.lower()
    facts, found = [], []
    for title in sorted(g.movies, key=len, reverse=True):          # longest title first
        if title.lower() in q:
            found.append(("Movie", title))
            facts += g.about_movie(title)
            q = q.replace(title.lower(), " ")
    for name in g.people:
        if name.lower() in q:
            found.append(("Person", name))
            facts += g.about_person(name)
    for y in re.findall(r"\b(?:19|20)\d{2}\b", question):
        found.append(("Year", y))
        facts += g.released_in(int(y))
    return found, facts


INTENTS = {"acted": ["Actors in", "acted in:"], "cast": ["Actors in"], "star": ["Actors in", "acted in:"],
           "direct": ["director", "directed:"], "wrote": ["writer", "wrote:"], "writ": ["writer", "wrote:"],
           "produc": ["producer", "produced:"], "releas": ["Movies from"], "review": ["rated"]}


def template_answer(question, facts):
    """Fallback used when no LLM is configured: put the facts matching the question's intent first."""
    if not facts:
        return "The Movies graph has nothing on that. Try naming a movie, a person or a release year."
    q = question.lower()
    keys = [k for word, ks in INTENTS.items() if word in q for k in ks]
    focus = [f for f in facts if any(k in f for k in keys)]
    return "Based on the Neo4j Movies graph: " + " ".join((focus or facts)[:3])


def generate(question, facts):
    key = os.getenv("LLM_API_KEY")
    if not key or not facts:
        return template_answer(question, facts), "Template fallback (LLM_API_KEY not set)"
    base = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")
    model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    prompt = ("You answer questions about movies. Use only the facts given. If they are not enough, reply that "
              "the graph does not contain the answer.\n\nFacts:\n" + "\n".join("* " + f for f in facts) +
              f"\n\nQuestion: {question}\nAnswer in 1-3 sentences:")
    resp = requests.post(f"{base}/chat/completions", timeout=60, headers={"Authorization": f"Bearer {key}"},
                         json={"model": model, "temperature": 0.2,
                               "messages": [{"role": "user", "content": prompt}]})
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip(), f"LLM: {model}"


def run(payload):
    question = payload["question"]
    found, facts = retrieve(question)
    try:
        text, gen = generate(question, facts)
    except Exception as exc:  # network / quota problem -> still answer from the graph
        text, gen = template_answer(question, facts), f"Template fallback (LLM call failed: {type(exc).__name__})"
    return {"question": question, "answer": text, "generator": gen, "source": get_store().source,
            "matched": [{"type": t, "value": v} for t, v in found], "facts": facts}
