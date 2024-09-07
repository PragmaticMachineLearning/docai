from byaldi import RAGMultiModalModel
from langchain_core.messages import HumanMessage
from langchain_core.pydantic_v1 import BaseModel
from langchain_openai import ChatOpenAI


class Extractor:
    def __init__(
        self,
        index_name: str,
    ):
        self.rag = RAGMultiModalModel.from_index(index_name)

    def extract(self, query: str, data_model: BaseModel, k: int = 3):
        results = self.rag.search(query=query, k=k)
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
                            "text": "Extract structured information from this insurance policy application",
                        },
                    ]
                    + image_content
                )
            ]
        )
        return response
