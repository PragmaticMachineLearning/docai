import base64
from typing import Optional

from byaldi import RAGMultiModalModel
from langchain_core.messages import HumanMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from rich import print

from docai.extractor import Extractor


class Application(BaseModel):
    insured_name: str = Field(description="The insured name")
    insured_address: str | None = Field(description="The insured address. May be None.")
    insured_phone: str | None = Field(
        description="The insured phone number. May be None."
    )
    insured_email: str | None = Field(
        description="The insured email address. May be None."
    )
    effective_date: str = Field(
        description="Start of the policy period. A.K.A. 'Effective Date'"
    )


class Loss(BaseModel):
    loss_date: str = Field(description="The date of the loss")
    loss_amount: float = Field(description="The amount of the loss")
    loss_description: str = Field(description="The description of the loss")
    date_of_claim: str = Field(description="The date the claim was made / reported")


class LossHistory(BaseModel):
    losses: list[Loss] = Field(description="Loss history")


if __name__ == "__main__":
    extractor = Extractor(index_name="application")
    for query, data_model in [
        ("What losses have occurred in the past 5 years?", LossHistory),
        ("What is the basic application information?", Application),
    ]:
        response = extractor.extract(query=query, data_model=data_model)
        print(query, response)
