import os

try:
    import openai
except Exception:
    openai = None

class AIEngine:
    """Simple wrapper around OpenAI's ChatCompletion API."""
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.available = openai is not None and self.api_key
        if self.available:
            openai.api_key = self.api_key

    def ask(self, prompt: str) -> str:
        if not self.available:
            raise RuntimeError("OpenAI API key not configured")
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI request failed: {e}")