from typing import List, Dict, Optional
import os
from openai import OpenAI

class ChatModel:
    def __init__(self, provider: str = "ollama"):
        self.provider = provider.lower()
        self.client = self._initialize_client()

    def _initialize_client(self):
        if self.provider == "ollama":
            try:
                from ollama import Client as OllamaClient
                return OllamaClient(host=os.getenv('OLLAMA_BASE_URL'))
            except ImportError:
                raise ImportError("Ollama library not found")
        elif self.provider == "openai":
            return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        else:
            raise ValueError(f"Invalid provider: Must be 'ollama' or 'openai'")

    def chat_completion(self, messages: List[Dict[str, str]]) -> Optional[str]:
        try:
            if self.provider == "ollama":
                response = self.client.chat(model=os.getenv('OLLAMA_MODEL'), messages=messages)
                return response['message']['content']
            elif self.provider == "openai":
                response = self.client.chat.completions.create(model=os.getenv('OPENAI_MODEL'), messages=messages)
                return response.choices[0].message.content
            return None
        except Exception as e:
            print(f"Error during chat completion with {self.provider}: {e}")
            return None

# Example Usage (within the same file or after importing)
if __name__ == "__main__":
    # Example with Ollama
    ollama_model = ChatModel(provider="ollama", base_url="http://localhost:11434", model_name="llama3")
    ollama_response = ollama_model.chat_completion(messages=[{"role": "user", "content": "Tell me a short fact about Bhilai."}])
    if ollama_response:
        print(f"Ollama Response: {ollama_response}")

    # Example with OpenAI (replace with your actual API key)
    openai_model = ChatModel(provider="openai", api_key="YOUR_OPENAI_API_KEY", model_name="gpt-3.5-turbo")
    openai_response = openai_model.chat_completion(messages=[{"role": "user", "content": "What is the capital of Chhattisgarh?"}])
    if openai_response:
        print(f"OpenAI Response: {openai_response}")