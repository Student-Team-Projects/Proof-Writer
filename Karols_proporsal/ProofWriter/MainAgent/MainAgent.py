#!/usr/bin/env python3



import SolverAgent.SolverAgent as sol
import StepsCheckAgent.StepsCheckAgent as stc
import TranslatorAgent.TranslatorAgent as tra
import Api.api as api 
import json
import logging
import re
from Tools.JsonExtractor import *
class MainAgent:

    def __init__(self):
        self.phiModel = api.getModel("phi")
        self.solverAgent = sol.SolverAgent(self.phiModel)
        self.stepsChecker = stc.StepsCheckAgent(self.phiModel)
        self.translatorAgent = tra.TranslatorAgent(self.phiModel)
        
    def solve(self,statement, n_atteppts = 5):
        logging.info("1 attempt at solutions")
        proof = self.solverAgent.solve(statement)
        # print(proof)
        step_success = False
        for attempt in range(n_atteppts):
            logging.info(f"check {attempt+1} solution")
            errors = self.stepsChecker.check(statement,proof)
            # print(errors)
            # print(errors)
            errorsJson = json.loads(extract_outermost_json(errors))
            # print(errorsJson)
            if errorsJson['correct'] == True:
                step_success = True
                logging.info("succes in steps")
                break
            logging.info(f"{attempt+1} solution is incorrect")
            logging.info(f"{2+attempt} attempt at solutions")
            proof = self.solverAgent.repair(statement,proof,errorsJson['errors'])
            # print(proof)
        if step_success == False:
            return "It is too hard"
        logging.info("Translate to natural language")
        translate_proof = self.translatorAgent.translate(statement, proof)
        return translate_proof

        
