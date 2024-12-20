from .base_processor import BaseProcessor

class ScientificReviewer(BaseProcessor):
    def __init__(self, client, severity, source_lang, target_lang):
        super().__init__(client, severity, source_lang, target_lang)
        self.base_prompt = (
            "You are a scientific reviewer. You will receive text and return only serious factual "
            "or scientific errors, and what's correc there. If there are none, return 'NO FACTUAL ERRORS HERE'."
        )
        
    def output_suffix(self):
        return "scientifically_reviewed"
    
    def build_prompt(self):
        sev_map = {
            1: "very lenient",
            2: "lenient",
            3: "normal",
            4: "strict",
            5: "very strict"
        }
        return f"{self.base_prompt}\nDo this scientific check with a severity: {sev_map.get(self.severity, 'normal')}"

    def postprocess(self, response, section):
        if response.lower() == "no factual errors here":
            return None
        return response
