#!/usr/bin/env python3

"""
A client wrapper for OpenAI's API to handle chat-based completions.

- Supports retry logic for API calls with configurable maximum retries.
- Allows interaction via system and user prompts.
- Handles errors and logs failures for debugging.
"""

import openai
import logging

class OpenAIClient:
    def __init__(self, api_key, model, max_retries=3):
        openai.api_key = api_key
        self.client = openai
        self.model = model
        self.max_retries = max_retries

    def get_completion(self, system_prompt, user_prompt):
        attempt = 0
        response = None

        while attempt < self.max_retries and response is None:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                if not response.choices:
                    raise ValueError("No valid response")
            except Exception as e:
                logging.error(f"Error in API call at attempt {attempt + 1}: {e}")
                response = None
                attempt += 1

        if response and response.choices and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        return None