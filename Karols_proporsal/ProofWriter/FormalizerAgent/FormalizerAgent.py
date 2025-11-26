#!/usr/bin/env python3


import Api.api as api
import os

class FormalizerAgent:
    def __init__(self, model: api.Model):
        self.model = model

    def formalize(self, statement: str, proof: str):

        ctx = self.model.getContext()

        path = "FormalizerAgent/prompts/formalize1.txt"

        if not os.path.exists(path):
            raise FileNotFoundError(f"Brak pliku promptu: {path}")

        with open(path, "r", encoding="utf-8") as f:
            prompt = f.read()

        final_prompt = prompt.replace("STATEMENT_HERE", statement).replace("PROOF_HERE", proof)

        return ctx.ask(final_prompt, thinking=True)
    
    def repair(self, statement: str, proof: str, errors):
        ctx = self.model.getContext()

        path = "SolverAgent/prompts/repair1.txt"

        if not os.path.exists(path):
            raise FileNotFoundError(f"Brak pliku promptu: {path}")

        with open(path, "r", encoding="utf-8") as f:
            prompt = f.read()

        final_prompt = prompt.replace("STATEMENT_HERE", statement).replace("PROOF_HERE", proof).replace("ERRORS_HERE", errors)

        return ctx.ask(final_prompt, thinking=True)
