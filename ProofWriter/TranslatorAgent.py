#!/usr/bin/env python3


import ProofWriter.Api.api as api
import os
class TranslatorAgent:
    def __init__(self, model: api.Model):
        self.model = model
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    def translate(self, statement: str, proof: str):

        TRANSLATE_PATH = os.path.join(self.CURRENT_DIR,"resources/TranslatorAgent/translate1.txt")

        if not os.path.exists(TRANSLATE_PATH):
            raise FileNotFoundError(f"Brak pliku promptu: {TRANSLATE_PATH}")

        with open(TRANSLATE_PATH, "r", encoding="utf-8") as f:
            prompt = f.read()

        final_prompt = prompt.replace("STATEMENT_HERE", statement).replace("PROOF_HERE", proof)

        return self.model.ask(final_prompt, thinking=True)
