from .base_processor import BaseProcessor

class Translator(BaseProcessor):
    def __init__(self, client, severity, source_lang, target_lang):
        super().__init__(client, severity, source_lang, target_lang)
        self.base_prompt = (
            "You are a translator. Translate the given text from {src} to {tgt}. "
            "Do not add comments, only return the translated text."
        )

def build_prompt(self):
    return self.base_prompt.format(src=self.source_lang, tgt=self.target_lang)