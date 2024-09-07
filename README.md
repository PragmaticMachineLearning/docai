# Sample usage

Install:
```bash
pyenv virtualenv 3.10.6 docai
pyenv activate docai
poetry install
```

Build the index:
```bash
python scripts/build_index.py --folder "pdfs/" --index_name "application"
```

Extraction structured information from the index (open extract.py to see queries and pydantic models):
```bash
python scripts/extract.py
```