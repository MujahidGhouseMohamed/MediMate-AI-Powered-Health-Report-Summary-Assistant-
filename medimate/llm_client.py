import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

class LLMClient:
    def __init__(self, model='llama3-8b-8192'):
        self.model = model
        self.client = Groq(api_key=GROQ_API_KEY)

    def ask(self, system, prompt, max_tokens=300):
        if not GROQ_API_KEY:
            return "Groq API key not set. Set GROQ_API_KEY in .env to use LLM features."

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
