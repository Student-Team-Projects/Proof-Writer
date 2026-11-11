import ProofWriter.Api.api as api
from ProofWriter.Tools.Prompts import fill_prompt

class StepListAgent:
    def __init__(self, model: api.Model):
        self.model = model

    def createStepList(self, statement: str):
        prompt = fill_prompt("StepListAgent/stepListPrompt.txt", STATEMENT=statement)
        return self.model.ask(prompt, thinking=True)
            
            