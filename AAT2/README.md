# AAT-2: Information-Retrieval Question Answering (TF-IDF)

Advance NLP (AML23702) · Nideesh V (1GA23AI028) · Dept. of AI & ML, Global Academy of Technology

## Folder layout
```
AAT2/
├── backend/   app.py (Flask, port 5102), core.py (NLP logic), AAT2_IR_Question_Answering.ipynb, requirements.txt
├── frontend/  index.html, style.css, app.js
└── data/      documents.txt
```
Data: data/documents.txt - five short documents on Indian heritage sites (one per line).

## Run
```bash
cd AAT2/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt_tab')"
python app.py          # open http://localhost:5102
```
The notebook `AAT2_IR_Question_Answering.ipynb` (run from the `backend/` folder) shows the same steps cell by cell.
