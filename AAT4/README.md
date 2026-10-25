# AAT-4: Topic Modelling with LDA

Advance NLP (AML23702) · Nideesh V (1GA23AI028) · Dept. of AI & ML, Global Academy of Technology

## Folder layout
```
AAT4/
├── backend/   app.py (Flask, port 5104), core.py (NLP logic), AAT4_LDA_Topic_Modelling.ipynb, requirements.txt
├── frontend/  index.html, style.css, app.js
└── data/      documents.txt
```
Data: data/documents.txt - twelve short documents on music, farming and finance (one per line).

## Run
```bash
cd AAT4/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python app.py          # open http://localhost:5104
```
The notebook `AAT4_LDA_Topic_Modelling.ipynb` (run from the `backend/` folder) shows the same steps cell by cell.
