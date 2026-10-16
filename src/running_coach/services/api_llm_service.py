import os

from dotenv import load_dotenv
from openai import OpenAI

from running_coach.services.llm_service import LLMService


class ApiLLMService(LLMService):

    def __init__(self, model: str) -> None:
        self.model = model

    def generate(self, prompt: str) -> str:
        load_dotenv()

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.responses.create(
            model = self.model,
            input = prompt
        )

        return response.output_text