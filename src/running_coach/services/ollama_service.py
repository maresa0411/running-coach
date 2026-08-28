from ollama import chat

from running_coach.services.llm_service import LLMService


class OllamaService(LLMService):

    def __init__(self, model: str) -> None:
        self.model = model

    def generate(self, prompt: str) -> str:
        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.message.content