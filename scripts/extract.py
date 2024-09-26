from pydantic import BaseModel, Field
from rich import print

from docai.extractor import Extractor


class ExplainedField(BaseModel):
    explanation: str = Field(
        description="Explain where the field was found and why it's the correct value for the field."
    )
    text: str = Field(description="Extracted text value")


class Application(BaseModel):
    insured_name: ExplainedField = Field(description="The insured name")
    insured_address: str = Field(description="The insured address")
    insured_phone: str = Field(description="The insured phone number")
    insured_email: str = Field(description="The insured email address")
    effective_date: str = Field(
        description="Proposed start of the policy period. A.K.A. 'Effective Date"
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
        (
            "What is the basic application information for the property section?",
            Application,
        ),
    ]:
        response = extractor.extract(
            model_name="gpt-4o",
            query=query,
            temperature=0.1,
            data_model=data_model,
            k=3,
        )
        print(query, response)
