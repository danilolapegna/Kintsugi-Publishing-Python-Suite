import openai
import logging

class OpenAIClient:
    def __init__(self, api_key, model, max_retries=3):
        openai.api_key = api_key
        self.model = model
        self.max_retries = max_retries

    def get_completion(self, system_prompt, user_prompt):
        attempt = 0
        while attempt < self.max_retries:
            try:
                r = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                if r.choices and r.choices[0].message.content:
                    return r.choices[0].message.content.strip()
                return None
            except Exception as e:
                logging.error(e)
                attempt += 1
        return None
