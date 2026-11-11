#!/usr/bin/env python3

import ProofWriter.Api.api as api
from ProofWriter.Tools.Prompts import fill_prompt

# Shape of the checker's answer; Ollama enforces it on the model's output.
CHECK_SCHEMA = {
    "type": "object",
    "properties": {
        "correct": {"type": "boolean"},
        "errors": {"type": "string"},
    },
    "required": ["correct", "errors"],
}

class StepsCheckAgent:
    def __init__(self, model):
        self.model = model

    def check(self, statement: str, proof: str):
        prompt = fill_prompt("StepsCheckAgent/check1.txt", STATEMENT=statement, PROOF=proof)
        return self.model.ask(prompt, thinking=True, schema=CHECK_SCHEMA)