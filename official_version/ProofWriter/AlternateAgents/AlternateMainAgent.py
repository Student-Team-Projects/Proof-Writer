#!/usr/bin/env python3


import ProofWriter.Api.api as api
import ProofWriter as pw
import os
import logging
import subprocess
import tempfile
import json

class AlternateMainAgent:
    def __init__(self, model: api.Model, isabelleBinPath, verbose: bool):
        self.model = model
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ISABELLE_BIN = isabelleBinPath
        self.verbose = verbose
        
    # Utility method used for extracting a JSON from 
    def clean_ai_jsonNew(self, raw_output: str) -> dict:
        
        start_tag = "```json"
        end_tag = "```"
        
        start_idx = raw_output.find(start_tag)
        end_idx = raw_output.find(end_tag, start_idx + len(start_tag))
        
        if start_idx != -1 and end_idx != -1:
            trimmed_output = raw_output[start_idx + len(start_tag):end_idx].strip()
        else:
            trimmed_output = raw_output
            
        raw_output = trimmed_output
        
        cleaned = raw_output.replace("```json", "").replace("```", "").strip()

        first_brace = cleaned.find('{')
        last_brace = cleaned.rfind('}') + 1
        if first_brace == -1 or last_brace == -1:
            raise ValueError("Nie znaleziono JSON-a w odpowiedzi AI.")

        cleaned = cleaned[first_brace:last_brace]

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"Niepoprawny JSON po czyszczeniu: {e}")

        return data
    
    def VerifyCorrectness(self, isabelleCode):
        with tempfile.TemporaryDirectory() as tmpdir:
            thy_path = os.path.join(tmpdir, "Scratch.thy")
            with open(thy_path, "w") as f:
                f.write(isabelleCode)
                
            root_path = os.path.join(tmpdir, "ROOT")
            with open(root_path, "w") as f:
                f.write("session TEMP_SESSION = HOL +\n  theories\n    Scratch\n")
                
            try:
                result = subprocess.run(
                    [self.ISABELLE_BIN, "build", "-d", tmpdir, "-b", "TEMP_SESSION"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return {"success": True, "stdout": result.stdout, "stderr": result.stderr}
            except subprocess.CalledProcessError as e:
                return {"success": False, "stdout": e.stdout, "stderr": e.stderr}
        
    def solve(self, statement: str, isabelleBeginning: str, isabelleEnding: str):
        
        if statement is None or isabelleBeginning is None or isabelleEnding is None:
            raise ValueError(f"Invalid args")
        
        stepListAgent = pw.AlternateAgents.StepListAgent.StepListAgent(self.model)
        
        logging.basicConfig(level=logging.DEBUG)

        output = stepListAgent.createStepList(statement)
        
        outputCleared = self.clean_ai_jsonNew(output)

        if self.verbose:
            print(outputCleared)  
            
            
        isabelleString = "" + isabelleBeginning
            
        for i in range(len(outputCleared["A"])):
            
            singleStepAgent = pw.AlternateAgents.SingleStepAgent.SingleStepAgent(self.model)
            
            output = singleStepAgent.createLemma(outputCleared["A"][i]["statement"], isabelleBeginning)
            
            raw = output.strip()

            if '"' not in raw:
                statement = f"\"{raw}\""
            else:
                first = raw.find('"')
                last = raw.find('"', first+1)
                statement = raw[first:last+1]
            
            if i == 0:
                deps = "group_axioms"
            else:
                deps = "group_axioms " + " ".join(f"S{j}" for j in range(1, i+1))
            
            isabelleString += f"""
            
            lemma S{i+1}
            {statement}
            by (metis {deps})
                
            """
            
            if self.verbose:
                print(isabelleString)
            
        isabelleString += isabelleEnding
        
        print(f"FINAL PROOF:\n {isabelleString}")
        
        izaVerification = self.VerifyCorrectness(isabelleString)
        
        if self.verbose:
            print(izaVerification)
            
        if izaVerification["success"]:
            print("Success!")
        else:
            print("Fail")
            
          
        
        