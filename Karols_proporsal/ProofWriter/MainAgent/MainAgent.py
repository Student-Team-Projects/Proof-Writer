#!/usr/bin/env python3



import SolverAgent.SolverAgent as sol
import StepsCheckAgent.StepsCheckAgent as stc
import TranslatorAgent.TranslatorAgent as tra
import FormalizerAgent.FormalizerAgent as form
import IsabelleAgent.IsabelleAgent as isa
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
        self.formalizerAgent = form.FormalizerAgent(self.phiModel)
        self.isabelleAgent = isa.IsabelleAgent()

    def solve(self,statement, n_atteppts = 5):
        logging.info("1 attempt at solutions")
        proof = extract_outermost_json(self.solverAgent.solve(statement))
        logging.debug(proof)
        # print(proof)
        step_success = False
        for attempt in range(n_atteppts):
            logging.info(f"check {attempt+1} solution")
            errors = self.stepsChecker.check(statement,proof)
            logging.debug(errors)
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
            proof = extract_outermost_json(self.solverAgent.repair(statement,proof,errorsJson['errors']))
            logging.debug(proof)
            # print(proof)
        if step_success == False:
            return "It is too hard"
        
        logging.info("Formalize proof")
        formal_proof_json = self.formalizerAgent.formalize(statement,proof)
        logging.debug(formal_proof_json)
        formal_proof_json = formal_proof_json[11:-3]
        # logging.debug(formal_proof_json)
        logging.info("Check formal proof")
        verify = self.isabelleAgent.check(formal_proof_json)
        logging.debug(verify)






        logging.info("Translate to natural language")
        translate_proof = self.translatorAgent.translate(statement, proof)
        logging.debug(translate_proof)
        return translate_proof, verify['ok']

        
