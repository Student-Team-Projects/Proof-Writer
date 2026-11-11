#!/usr/bin/env python3


import ProofWriter.Api.api as api
import logging
from ProofWriter.Tools.Prompts import fill_prompt
class SolverAgent:
    def __init__(self, model):
        self.model = model

    def solve(self, statement: str, proof = None, errors = None):
        """
        Loads the solver prompt, substitutes 'STATEMENT_HERE'
        and sends the request.
        """
        if proof != None:

            return self.repair(statement,proof,errors)
        
        prompt = fill_prompt("SolverAgent/solve1.txt", STATEMENT=statement)
        return self.model.ask(prompt, thinking=True)

    def repair(self, statement: str, proof: str, errors):
        prompt = fill_prompt("SolverAgent/repair1.txt", STATEMENT=statement, PROOF=proof, ERRORS=errors)
        return self.model.ask(prompt, thinking=True)
