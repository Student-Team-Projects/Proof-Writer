#!/usr/bin/env python3

import ProofWriter.Api.api as api
import os

class StepsCheckAgent:
    def __init__(self, model):
        self.model = model
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    def check(self, statement: str, proof: str):

        CHECK_PATH = os.path.join(self.CURRENT_DIR,"../resources/StepsCheckAgent/check1.txt")

        if not os.path.exists(CHECK_PATH):
            raise FileNotFoundError(f"Brak pliku promptu: {CHECK_PATH}")

        with open(CHECK_PATH, "r", encoding="utf-8") as f:
            prompt = f.read()

        final_prompt = prompt.replace("STATEMENT_HERE", statement).replace("PROOF_HERE", proof)

        return self.model.ask(final_prompt, thinking=True)