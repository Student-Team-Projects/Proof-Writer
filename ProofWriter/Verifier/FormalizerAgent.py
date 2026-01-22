#!/usr/bin/env python3


import ProofWriter.Api.api as api
import os

class FormalizerAgent:
    def __init__(self, model: api.Model):
        self.model = model
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    def formalize(self, statement: str, proof: str):

        FORMALIZE_PATH = os.path.join(self.CURRENT_DIR,"../resources/FormalizerAgent/formalize1.txt")

        if not os.path.exists(FORMALIZE_PATH):
            raise FileNotFoundError(f"Brak pliku promptu: {FORMALIZE_PATH}")

        with open(FORMALIZE_PATH, "r", encoding="utf-8") as f:
            prompt = f.read()

        final_prompt = prompt.replace("STATEMENT_HERE", statement).replace("PROOF_HERE", proof)

        return self.model.ask(final_prompt, thinking=True)
