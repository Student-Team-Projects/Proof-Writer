#!/usr/bin/env python3



import SolverAgent.SolverAgent as sol
import StepsCheckAgent.StepsCheckAgent as stc
import Api.api as api 
import json
from Tools.JsonExtractor import extract_outermost_json
class MainAgent:

    def __init__(self):
        self.phiModel = api.getModel("phi")
        self.solverAgent = sol.SolverAgent(self.phiModel)
        self.stepsChecker = stc.StepsCheckAgent(self.phiModel)
    def solve(self,statement, n_atteppts = 5):
        proof = self.solverAgent.solve(statement)
        print(proof)
        nlsuccess = False
        for _ in range(n_atteppts):
            errors = self.stepsChecker.check(statement,proof)
            print(errors)
            errorsJson = json.loads(extract_outermost_json(errors))
            print(errorsJson)
            if errorsJson['correct'] == True:
                nlsuccess = True
                break
            proof = self.solverAgent.repair(statement,proof,errorsJson['errors'])
            print(proof)
        return proof

        
