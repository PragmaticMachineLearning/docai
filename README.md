# DocAI

Extract structured data from  unstructured documents using Byaldi, Langchain, and OpenAI gpt-4o

### Installation
```bash
pyenv virtualenv 3.10.6 docai
pyenv activate docai
poetry install
```

### Environment vars
Ensure you have an OPENAI_API_KEY and HF_TOKEN set in your environment variables.

```bash
export OPENAI_API_KEY=<your key>
export HF_TOKEN=<your token>
```

### Sample usage

Build the index from the pdfs/ folder:
```bash
python scripts/build_index.py --folder "pdfs/" --index_name "application"
```

Extraction structured information from the index (open extract.py to see queries and pydantic models):
```bash
python scripts/extract.py
```