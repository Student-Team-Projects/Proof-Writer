#!/usr/bin/env python3

import ProofWriter as pw
import os
import logging

import sys
import argparse
import json

def main():
    parser = argparse.ArgumentParser(
        description="Run ProofWriter with a provided theorem file"
    )

    parser.add_argument("--input", type=str, help="Path to the file containing a theorem to prove")
    parser.add_argument("--output", type=str, help="Path to the file where the proof will be saved")
    parser.add_argument("--host", type=str, default="http://localhost:11434", help="Ollama server address")
    parser.add_argument("--log", choices=["debug", "info"], type=str, help="Logging level: debug or info")

    models = ["gemma3:270m"]
    default_model = "gemma3:270m"
    parser.add_argument("--steps_checker_model", choices=models, default=default_model, help="Model to use for steps checker agent")
    parser.add_argument("--solver_model", choices=models, default=default_model, help="Model to use for solver agent")
    parser.add_argument("--translator_model", choices=models, default=default_model, help="Model to use for translator agent")
    parser.add_argument("--formalizer_model", choices=models, default=default_model, help="Model to use for formalizer agent")

    parser.add_argument("--generator_attempts", type=int, default=2, help="Number of attempts for the proof generator agent")
    parser.add_argument("--verifier_attempts", type=int, default=2, help="Number of attempts for the verifier agent")
    parser.add_argument("--main_attempts", type=int, default=12, help="Number of attempts for the main agent")

    parser.add_argument(
        "--examples",
        type=str,
        default='{"all" : 7}',
        help="JSON dictionary specifying the number of random examples from each math field to include in the formalizer prompt (e.g. '{\"algebra\": 3, \"number_theory\": 1}' or '{\"all\": 5}')"
    )

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    host = args.host
    log = args.log
    sess = pw.Api.api.Session(host)
    solver_model = pw.Api.api.createModel(args.solver_model, sess)
    steps_checker_model = pw.Api.api.createModel(args.steps_checker_model, sess)
    translator_model = pw.Api.api.createModel(args.translator_model, sess)
    formalizer_model = pw.Api.api.createModel(args.formalizer_model, sess)
    generator_attempts = args.generator_attempts
    verifier_attempts = args.verifier_attempts
    main_attempts = args.main_attempts
    examples = args.examples

    if input_path and not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")
    if output_path and not os.path.exists(output_path):
        raise FileNotFoundError(f"File not found: {output_path}")
    
    if log == "info":
        logging.basicConfig(level=logging.INFO)
    elif log == "debug":
        logging.basicConfig(level=logging.DEBUG)

    if examples:
        try:
            examples = json.loads(examples)
        except json.JSONDecodeError as e:
            print(f"Error parsing examples JSON: {e}")
            sys.exit(1)

    if input_path:
        with open(input_path, "r", encoding="utf-8") as f:
            statement = f.read()
    else:
        statement = input("Enter the theorem to be proved: ").strip()

    # GPTModel = pw.Api.api.getModel("gpt-oss-cloud") 
    # GPTSmall = pw.Api.api.getModel("gpt-oss")
    # DSModel = pw.Api.api.getModel("deepseek-r1")
    # DSV3Model = pw.Api.api.getModel("deepseek-v3")
    # phiModel = pw.Api.api.getModel("phi")

    solverAgent = pw.ProofGenerator.SolverAgent.SolverAgent(solver_model)
    stepsChecker = pw.ProofGenerator.StepsCheckAgent.StepsCheckAgent(steps_checker_model)
    generatorAgent = pw.ProofGenerator.ProofGeneratorAgent.ProofGeneratorAgent(solverAgent,stepsChecker,generator_attempts)
    formalizerAgent = pw.Verifier.FormalizerAgentWithRandomExamples.FormalizerAgentWithRandomExamples(formalizer_model,examples)
    # formalizerAgent = pw.Verifier.FormalizerAgent.FormalizerAgent(formalizer_model)
    isabelleAgent = pw.Verifier.IsabelleAgent.IsabelleAgent()
    verifierAgent = pw.Verifier.VerifierAgent.VerifierAgent(formalizerAgent,isabelleAgent,verifier_attempts)
    translatorAgent = pw.TranslatorAgent.TranslatorAgent(translator_model)

    model = pw.MainAgent.MainAgent(generatorAgent,verifierAgent,translatorAgent,main_attempts)

    proof, verification = model.solve(statement)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(proof)
    else :
        print(proof)

    if verification: 
        print("Verification was successful")
    else:
        print("Verification failed")
        
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
    
if __name__ == "__main__":
    main()