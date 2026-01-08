#!/usr/bin/env python3



from ProofWriter.Tools.JsonExtractor import *
import json
import logging
class VerifierAgent:

    def __init__(self, formalizer, isabelle):
        self.formalizerAgent = formalizer
        self.isabelleAgent = isabelle

    def verify(self,statement, proof, n_attempts = 20):
        # print(proof)
        for attempt in range(n_attempts):
            logging.info(f"{attempt+1} attempt at formalize")
            formal_proof = self.formalizerAgent.formalize(statement,proof)
            logging.debug(formal_proof)
            logging.info(f"check {attempt+1} formal solution")
            verify = self.isabelleAgent.check(formal_proof)
            logging.debug(verify)
            if verify['ok'] == True:
                logging.info("succes")
                return True, formal_proof
            logging.info(f"{attempt+1}formal solution is incorrect")
        logging.info("Neume")
        return False, None





        
