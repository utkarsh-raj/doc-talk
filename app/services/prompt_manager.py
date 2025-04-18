from typing import Dict, List
from app.constants.prompts import LLM_PROMPTS

class PromptManager:
    def __init__(self):
        llm_prompts = LLM_PROMPTS
        self.prompts: Dict[str, str] = llm_prompts

    def add_prompt(self, prompt_name: str, prompt_text: str) -> None:
        if prompt_name in self.prompts:
            raise ValueError(f"Prompt '{prompt_name}' already exists.")
        self.prompts[prompt_name] = prompt_text

    def get_prompt(self, prompt_name: str) -> str:
        return self.prompts.get(prompt_name, None)

    def list_prompts(self) -> List[str]:
        return list(self.prompts.keys())