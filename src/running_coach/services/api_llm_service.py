import os

from dotenv import load_dotenv
from openai import OpenAI

from running_coach.services.llm_service import LLMService


class ApiLLMService(LLMService):

    def __init__(self, model: str) -> None:
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(
            model = self.model,
            input = prompt
        )

        return response.output_text