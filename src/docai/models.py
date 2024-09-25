import json
import re

from langchain.output_parsers import PydanticOutputParser
from langchain_community.chat_models import ChatLiteLLM
from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field
from rich import print

model_kwargs = {"tool_choice": "none"}


class ResponseModel(BaseModel):
    location: str = Field(description="Location of France on the map")
    president: str = Field(description="Current president of France")


def extract_json(text):
    # Remove any leading/trailing whitespace
    text = text.strip()

    # Try to extract JSON from between <json> tags
    json_match = re.search(r"<json>(.*?)</json>", text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # If no tags, look for JSON-like structure
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            # If still no match, assume the entire text is JSON
            json_str = text

    # Remove any markdown code block syntax
    json_str = re.sub(r"^```json\s*|\s*```$", "", json_str, flags=re.MULTILINE)

    # Clean up any remaining markdown backticks
    json_str = json_str.strip("`").strip()

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Problematic JSON string: {json_str}")
        raise


def llm_processor(
    model_name: str, temperature: float, data_model: type[BaseModel], messages: list
):
    # set up a parser
    parser = PydanticOutputParser(pydantic_object=data_model)

    # Create a system message with the parsing instructions
    system_message = SystemMessage(
        content=f"Extract the requested information and format the output as a JSON object.\n{parser.get_format_instructions()}"
    )

    # Combine the system message with the input messages
    full_messages = [system_message] + messages

    model = ChatLiteLLM(model=model_name, temperature=temperature)
    response = model.invoke(full_messages)

    # Extract the content from the response
    response_content = (
        response.content if hasattr(response, "content") else str(response)
    )

    try:
        json_data = extract_json(response_content)
        return data_model(**json_data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response content: {response_content}")
        raise


if __name__ == "__main__":
    data = [
        "What is the location of France on the map? Who is the current president of France?"
    ]
    print(
        llm_processor(
            model_name="claude-3-opus-20240229",
            temperature=0.0,
            data_model=ResponseModel,
            messages=data,
        )
    )
