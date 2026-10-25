# AAT-1: POS Tagging and Named Entity Recognition (spaCy)

Advance NLP (AML23702) · Nideesh V (1GA23AI028) · Dept. of AI & ML, Global Academy of Technology

## Folder layout
```
AAT1/
├── backend/   app.py (Flask, port 5101), core.py (NLP logic), AAT1_POS_NER_spaCy.ipynb, requirements.txt
├── frontend/  index.html, style.css, app.js
└── data/      sample_paragraph.txt
```
Data: data/sample_paragraph.txt - sample paragraph used in the notebook and pre-filled in the UI.

## Run
```bash
cd AAT1/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py          # open http://localhost:5101
```
The notebook `AAT1_POS_NER_spaCy.ipynb` (run from the `backend/` folder) shows the same steps cell by cell.
