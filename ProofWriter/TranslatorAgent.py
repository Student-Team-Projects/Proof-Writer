#!/usr/bin/env python3


import ProofWriter.Api.api as api
from ProofWriter.Tools.Prompts import fill_prompt
class TranslatorAgent:
    def __init__(self, model: api.Model):
        self.model = model

    def translate(self, statement: str, proof: str):
        prompt = fill_prompt("TranslatorAgent/translate1.txt", STATEMENT=statement, PROOF=proof)
        return self.model.ask(prompt, thinking=True)
