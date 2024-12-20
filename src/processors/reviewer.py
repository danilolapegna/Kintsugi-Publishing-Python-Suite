from .base_processor import BaseProcessor

class Reviewer(BaseProcessor):

    def __init__(self, client, severity, source_lang, target_lang):
        super().__init__(client, severity, source_lang, target_lang)
        self.base_prompt = (
            "You are a reviewer. You will receive text and return grammatical "
            "errors and how to fix them. If no such errors, please just"
            "return 'NO SERIOUS ERRORS HERE'."
        )
        
    def output_suffix(self):
        return "reviewed"

    def build_prompt(self):
        sev_map = {
            1: "very lenient",
            2: "lenient",
            3: "normal",
            4: "strict",
            5: "very strict"
        }
        return f"{self.base_prompt}\nDo it with a severity level that's {sev_map.get(self.severity, 'normal')}"

    def postprocess(self, response, section):
        if response.lower() == "no serious errors here":
            return None
        return response