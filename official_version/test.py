#!/usr/bin/env python3

import ProofWriter as pw
import os
import logging

path = "../statements/statement5.txt"

if not os.path.exists(path):
    raise FileNotFoundError(f"File not found: {path}")

with open(path, "r", encoding="utf-8") as f:
    statement = f.read()


GPTModel = pw.Api.api.getModel("gpt-oss-cloud") 
GPTMniejszy = pw.Api.api.getModel("gpt-oss")
DSModel = pw.Api.api.getModel("deepseek-r1")
DSV3Model = pw.Api.api.getModel("deepseek-v3")
phiModel = pw.Api.api.getModel("phi")
solverAgent = pw.ProofGenerator.SolverAgent.SolverAgent(DSV3Model)
stepsChecker = pw.ProofGenerator.StepsCheckAgent.StepsCheckAgent(DSV3Model)
generatorAgent = pw.ProofGenerator.ProofGeneratorAgent.ProofGeneratorAgent(solverAgent,stepsChecker,2)
formalizerAgent = pw.Verifier.FormalizerAgentWithRandomExamples.FormalizerAgentWithRandomExamples(DSV3Model,{"AAA":2, "all" : 2})
# formalizerAgent = pw.Verifier.FormalizerAgent.FormalizerAgent(DSV3Model)
isabelleAgent = pw.Verifier.IsabelleAgent.IsabelleAgent()
verifierAgent = pw.Verifier.VerifierAgent.VerifierAgent(formalizerAgent,isabelleAgent,2)
translatorAgent = pw.TranslatorAgent.TranslatorAgent(DSModel)

model = pw.MainAgent.MainAgent(generatorAgent,verifierAgent,translatorAgent,2)

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

proof, verification = model.solve(statement)

print(proof)

if verification: 
    print("Verification was successful")
else:
    print("Werification failed")
    
#Example AlternativeModel launch    
    
# altModel = pw.AlternateAgents.AlternateMainAgent.AlternateMainAgent(DSModel, "/home/ltrzos/Isabelle2025/bin/isabelle", True)
# 
# IsabelleBeginning = """
# theory Scratch
#   imports Main
# begin
# 
# locale group =
#   fixes mul :: "'a ⇒ 'a ⇒ 'a" (infixl "∙" 70)
#     and one :: "'a" ("e")
#     and inv :: "'a ⇒ 'a"
#   assumes assoc: "(x ∙ y) ∙ z = x ∙ (y ∙ z)"
#       and left_one: "e ∙ x = x"
#       and right_one: "x ∙ e = x"
#       and left_inv: "inv x ∙ x = e"
# 
# begin
# 
# lemma group_axioms:
#   "((x ∙ y) ∙ z = x ∙ (y ∙ z)) ∧
#    (e ∙ x = x) ∧
#    (x ∙ e = x) ∧
#    (inv x ∙ x = e)"
#   by (metis assoc left_one right_one left_inv)"""
# 
# IsabelleEnding = """
#  
# end
# 
# end"""
# 
# altModel.solve(statement, IsabelleBeginning, IsabelleEnding)