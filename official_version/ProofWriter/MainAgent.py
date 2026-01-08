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

    def __init__(self):
        self.DSModel = api.getModel("deepseek-r1")
        self.phiModel = api.getModel("phi")
        self.solverAgent = sol.SolverAgent(self.DSModel)
        self.stepsChecker = stc.StepsCheckAgent(self.phiModel)
        self.generatorAgent = gen.ProofGeneratorAgent(self.solverAgent,self.stepsChecker)
        self.translatorAgent = tra.TranslatorAgent(self.DSModel)
        self.formalizerAgent = form.FormalizerAgent(self.DSModel)
        self.isabelleAgent = isa.IsabelleAgent()
        self.verifierAgent = ver.VerifierAgent(self.formalizerAgent,self.isabelleAgent)

    def solve(self,statement, n_atteppts = 5):
        logging.info("start")
        proof = extract_outermost_json(self.generatorAgent.generate(statement))
        logging.info("start")
        if proof == "Neume":
            return "It is too hard"
        
        formal_succes, formal_proof = self.verifierAgent.verify(statement,proof)
        if formal_succes:
            logging.info("formal verification successful")
        else:
            logging.info("formal verification failed")

        if self.translatorAgent != None: 
            logging.info("Translate to natural language")
            translate_proof = self.translatorAgent.translate(statement, proof)
            logging.debug(translate_proof)
            return translate_proof, formal_succes
        return proof, formal_succes

        
