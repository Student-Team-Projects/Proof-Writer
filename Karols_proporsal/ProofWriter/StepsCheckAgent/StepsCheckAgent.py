#!/usr/bin/env python3

import Api.api as api
import os

class StepsCheckAgent:
    def __init__(self, model: api.Model):
        self.model = model

    def check(self, statement: str, proof: str):

        ctx = self.model.getContext()

        path = "StepsCheckAgent/prompts/check1.txt"

        if not os.path.exists(path):
            raise FileNotFoundError(f"Brak pliku promptu: {path}")

        with open(path, "r", encoding="utf-8") as f:
            prompt = f.read()

        final_prompt = prompt.replace("STATEMENT_HERE", statement).replace("PROOF_HERE", proof)

        return ctx.ask(final_prompt, thinking=True)