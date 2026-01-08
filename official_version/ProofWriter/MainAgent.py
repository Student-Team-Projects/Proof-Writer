#!/usr/bin/env python3



import ProofWriter.ProofGenerator.SolverAgent as sol
import ProofWriter.ProofGenerator.StepsCheckAgent as stc
import ProofWriter.ProofGenerator.ProofGeneratorAgent as gen
import ProofWriter.TranslatorAgent as tra
import ProofWriter.Verifier.FormalizerAgent as form
import ProofWriter.Verifier.IsabelleAgent as isa
import ProofWriter.Verifier.VerifierAgent as ver
import ProofWriter.Api.api as api 
from ProofWriter.Tools.JsonExtractor import *
import json
import logging
import re
class MainAgent:

    def __init__(self,generator, verifier, translator, n_attempts = 5):
        self.generatorAgent = generator
        self.verifierAgent = verifier
        self.translatorAgent = translator
        self.n_attempts = n_attempts

    def solve(self,statement):
        best_proof = ""
        for na in range(self.n_attempts):
            logging.info("start")
            proof = extract_outermost_json(self.generatorAgent.generate(statement))
            logging.info("start")
            if proof == "Neume":
                continue
            best_proof = proof
            if self.verifierAgent == None:
                break
            formal_succes, formal_proof = self.verifierAgent.verify(statement,proof)
            if formal_succes:
                logging.info("formal verification successful")
                break
            else:
                logging.info("formal verification failed")
        if best_proof == "":
            return "It's too hard", False
        if self.translatorAgent != None: 
            logging.info("Translate to natural language")
            translate_proof = self.translatorAgent.translate(statement, proof)
            logging.debug(translate_proof)
            return translate_proof, formal_succes
        return proof, formal_succes

        
