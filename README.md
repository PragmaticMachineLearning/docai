# DocAI

Extract structured data from  unstructured documents using Answer.AI's [Byaldi](https://github.com/AnswerDotAI/byaldi), OpenAI [gpt-4o](https://platform.openai.com/docs/guides/vision), and [Langchain's structured output](https://python.langchain.com/v0.1/docs/modules/model_io/chat/structured_output/).

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
