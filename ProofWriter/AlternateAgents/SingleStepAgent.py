#!/usr/bin/env python3


import ProofWriter.Api.api as api
from ProofWriter.Tools.Prompts import fill_prompt

class SingleStepAgent:
    def __init__(self, model: api.Model):
        self.model = model

    def createLemma(self, statement: str, code: str):
        prompt = fill_prompt("SingleStepAgent/singleStepPrompt.txt", STATEMENT=statement, CODE=code)
        return self.model.ask(prompt, thinking=True)
            
            