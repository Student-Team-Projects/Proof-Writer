#!/usr/bin/env python3

import ProofWriter as pw
import os
import logging

path = "../statements/statement2.txt"

if not os.path.exists(path):
    raise FileNotFoundError(f"File not found: {path}")

with open(path, "r", encoding="utf-8") as f:
    statement = f.read()

DSModel = pw.Api.api.getModel("deepseek-r1")
phiModel = pw.Api.api.getModel("phi")
solverAgent = pw.ProofGenerator.SolverAgent.SolverAgent(DSModel)
stepsChecker = pw.ProofGenerator.StepsCheckAgent.StepsCheckAgent(phiModel)
generatorAgent = pw.ProofGenerator.ProofGeneratorAgent.ProofGeneratorAgent(solverAgent,stepsChecker,2)
formalizerAgent = pw.Verifier.FormalizerAgent.FormalizerAgent(DSModel)
isabelleAgent = pw.Verifier.IsabelleAgent.IsabelleAgent()
verifierAgent = pw.Verifier.VerifierAgent.VerifierAgent(formalizerAgent,isabelleAgent,2)
translatorAgent = pw.TranslatorAgent.TranslatorAgent(DSModel)

model = pw.MainAgent.MainAgent(generatorAgent,verifierAgent,translatorAgent,30)

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

proof, verification = model.solve(statement)

print(proof)

if verification: 
    print("Verification was successful")
else:
    print("Werification failed")