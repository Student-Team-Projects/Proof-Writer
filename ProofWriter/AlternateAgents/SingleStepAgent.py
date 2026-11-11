#!/usr/bin/env python3


import ProofWriter.Api.api as api
import os

class SingleStepAgent:
    def __init__(self, model: api.Model):
        self.model = model
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        
    def createLemma(self, statement: str, code: str):
        
        PROMPT_PATH = os.path.join(self.CURRENT_DIR,"../resources/SingleStepAgent/singleStepPrompt.txt")
        
        if not os.path.exists(PROMPT_PATH):
            raise FileNotFoundError(f"Prompt file not found: {PROMPT_PATH}")
        
        with open(PROMPT_PATH, "r", encoding="utf-8") as f:
            prompt = f.read()
            
        final_prompt = prompt.replace("STATEMENT_HERE", statement).replace("CODE_HERE", code)
        
        return self.model.ask(final_prompt, thinking=True)
            
            