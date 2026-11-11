#!/usr/bin/env python3



from ProofWriter.Tools.JsonExtractor import *
import json
import logging
class ProofGeneratorAgent:

    def __init__(self, solver, checker, n_attempts = 5):
        self.solverAgent = solver
        self.stepsChecker = checker
        self.n_attempts = n_attempts

    def generate(self,statement):
        logging.info("1 attempt at solutions")
        proof = self.solverAgent.solve(statement)
        logging.debug(proof)
        # print(proof)
        for attempt in range(self.n_attempts):
            logging.info(f"check {attempt+1} solution")
            errors = self.stepsChecker.check(statement,proof)
            logging.debug(errors)
            # print(errors)
            # print(errors)
            errorsJson = json.loads(extract_outermost_json(errors))
            # print(errorsJson)
            if errorsJson['correct'] == True:
                logging.info("succes")
                return proof
            logging.info(f"{attempt+1} solution is incorrect")
            logging.info(f"{2+attempt} attempt at solutions")
            proof = self.solverAgent.solve(statement,proof,errorsJson['errors'])
            logging.debug(proof)
        return None





        
