# AAT-3: Retrieval-Augmented Generation over the Neo4j Movies Graph

Advance NLP (AML23702) · Nideesh V (1GA23AI028) · Dept. of AI & ML, Global Academy of Technology

## Folder layout
```
AAT3/
├── backend/   app.py (Flask, port 5103), core.py (NLP logic), AAT3_RAG_Neo4j_Movies.ipynb, requirements.txt
├── frontend/  index.html, style.css, app.js
└── data/      movies.cypher
```
Data: data/movies.cypher - official Neo4j Movies script (neo4j-graph-examples/movies); data/movies.json - offline export of the same graph (38 movies, 133 people).

## Run
```bash
cd AAT3/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python app.py          # open http://localhost:5103
```
The notebook `AAT3_RAG_Neo4j_Movies.ipynb` (run from the `backend/` folder) shows the same steps cell by cell.

## Configuration (no secrets in the repo)
Copy `.env.example` and set the values in your shell (do not commit real values):

```bash
export NEO4J_URI=bolt://localhost:7687   # leave unset to use data/movies.json
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=<your password>
export LLM_API_KEY=<optional, any OpenAI-compatible key>
```

To load the graph into a local Neo4j: open Neo4j Browser and run the contents of `data/movies.cypher`
(or `cypher-shell -u neo4j -p <password> -f data/movies.cypher`).
Without `LLM_API_KEY` the app answers with a clearly labelled template built from the retrieved facts.
