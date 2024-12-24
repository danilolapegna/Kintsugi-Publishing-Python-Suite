from .base_openai_processor import BaseOpenAIProcessor

class Summariser(BaseOpenAIProcessor):
    def __init__(self, client, processor_parameters):
        super().__init__(client, processor_parameters)
        
        self.base_prompt = (
            "You are a summarisation expert. You will receive a piece of text. Your task is to:"
            " 1) Generate a concise summary that captures all the most relevant point of the text."
            " 2) Ensure the summary is accurate, clear, and written in the same language as the input text."
        )

    def output_suffix(self):
        return "summarised"

    def build_prompt(self):
        return self.base_prompt