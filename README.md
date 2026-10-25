# ANLP-projects

Advance Natural Language Processing (AML23702) lab exercises · Nideesh V (1GA23AI028)
Dept. of AI & ML, Global Academy of Technology

| AAT | Topic | Port |
|-----|-------|------|
| [AAT1](AAT1) | POS tagging and NER with spaCy | 5101 |
| [AAT2](AAT2) | IR-based question answering (TF-IDF) | 5102 |
| [AAT3](AAT3) | RAG over the Neo4j Movies graph | 5103 |
| [AAT4](AAT4) | LDA topic modelling | 5104 |
| [AAT5](AAT5) | WordNet synonyms and word senses | 5105 |

Each folder is self-contained: `backend/` (Flask app + notebook + requirements.txt), `frontend/` and `data/`.
No secrets are stored in this repository; AAT3 reads its settings from environment variables (see `AAT3/.env.example`).
