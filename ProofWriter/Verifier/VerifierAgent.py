#!/usr/bin/env python3



from ProofWriter.Tools.JsonExtractor import *
import json
import logging
class VerifierAgent:

    def __init__(self, formalizer, lean, n_attempts = 5):
        self.formalizerAgent = formalizer
        self.leanAgent = lean
        self.n_attempts = n_attempts

    def verify(self,statement, proof):
        logging.debug(proof)
        for attempt in range(self.n_attempts):
            logging.info(f"{attempt+1} attempt at formalize")
            formal_proof = self.formalizerAgent.formalize(statement,proof)
            logging.debug(formal_proof)
            logging.info(f"check {attempt+1} formal solution")
            verify = self.leanAgent.check(formal_proof)
            logging.debug(verify)
            if verify['ok'] == True:
                logging.info("succes")
                return True, formal_proof
            logging.info(f"{attempt+1}formal solution is incorrect")
        logging.info("formal verification failed in all attempts")
        return False, None





        
