#!/usr/bin/env python3


import ProofWriter.Api.api as api
import os
import logging
class SolverAgent:
    def __init__(self, model: api.Model):
        self.model = model
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    def solve(self, statement: str, proof = None, errors = None):
        """
        Wczytuje prompt solvera, podmienia 'STATEMENT_HERE'
        i wysyła zapytanie przez context.
        """
        if proof != None:

            return self.repair(statement,proof,"")
        
        ctx = self.model.getContext()
        SOLVE_PATH = os.path.join(self.CURRENT_DIR,"../resources/SolverAgent/solve1.txt")
        
        if not os.path.exists(SOLVE_PATH):
            raise FileNotFoundError(f"Brak pliku promptu: {SOLVE_PATH}")

        with open(SOLVE_PATH, "r", encoding="utf-8") as f:
            prompt = f.read()

        final_prompt = prompt.replace("STATEMENT_HERE", statement)

        return ctx.ask(final_prompt, thinking=True)
    
    def repair(self, statement: str, proof: str, errors):
        ctx = self.model.getContext()

        REPAIR_PATH = os.path.join(self.CURRENT_DIR,"../resources/SolverAgent/repair1.txt")

        if not os.path.exists(REPAIR_PATH):
            raise FileNotFoundError(f"Brak pliku promptu: {REPAIR_PATH}")

        with open(REPAIR_PATH, "r", encoding="utf-8") as f:
            prompt = f.read()

        final_prompt = prompt.replace("STATEMENT_HERE", statement).replace("PROOF_HERE", proof).replace("ERRORS_HERE", errors)

        return ctx.ask(final_prompt, thinking=True)
