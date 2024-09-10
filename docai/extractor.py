from byaldi import RAGMultiModalModel
from docai import extract_text_from_doc
from langchain_core.messages import HumanMessage
from langchain_core.pydantic_v1 import BaseModel
from langchain_openai import ChatOpenAI
from docai.extract_text_from_doc import extract_text_from_pdfs
from rich import print
class Extractor:
    def __init__(
        self,
        index_name: str,
        folder: str
    ):
        self.rag = RAGMultiModalModel.from_index(index_name)
        self.folder = folder

    def extract(self, query: str, data_model: BaseModel, k: int = 3):
        results = self.rag.search(query=query, k=k)

        extract_texts = extract_text_from_pdfs(self.folder)

        combined_text = "\n\n".join([result["text"] for result in extract_texts])
        print(combined_text)
        image_content = [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{result.base64}",
                },
            }
            for result in results
        ]

        model = ChatOpenAI(
            model="gpt-4o",
            temperature=0.0,
        ).with_structured_output(data_model)
        response = model.invoke(
            [
                HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": f"Extract structured information from this insurance policy application. Here's the extracted_text from the PDFs: \n\n {combined_text}",
                        },
                    ]
                    + image_content
                )
            ]
        )
        return response
