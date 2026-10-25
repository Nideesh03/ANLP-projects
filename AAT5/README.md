# AAT-5: WordNet Synonyms, Definitions and Word Senses (NLTK)

Advance NLP (AML23702) · Nideesh V (1GA23AI028) · Dept. of AI & ML, Global Academy of Technology

## Folder layout
```
AAT5/
├── backend/   app.py (Flask, port 5105), core.py (NLP logic), AAT5_WordNet_Senses.ipynb, requirements.txt
├── frontend/  index.html, style.css, app.js
└── data/      contexts.json
```
Data: data/contexts.json - context sentences (bat, crane, light) with a POS hint.

## Run
```bash
cd AAT5/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; [nltk.download(r) for r in ('wordnet','omw-1.4','punkt_tab')]"
python app.py          # open http://localhost:5105
```
The notebook `AAT5_WordNet_Senses.ipynb` (run from the `backend/` folder) shows the same steps cell by cell.
