#!/usr/bin/env python3


import ProofWriter.Api.api as api
from ProofWriter.Tools.Prompts import fill_prompt

class FormalizerAgent:
    def __init__(self, model: api.Model):
        self.model = model

    def formalize(self, statement: str, proof: str):
        prompt = fill_prompt("FormalizerAgent/formalize1.txt", STATEMENT=statement, PROOF=proof)
        return self.model.ask(prompt, thinking=True)
