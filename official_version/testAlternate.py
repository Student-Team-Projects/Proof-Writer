#!/usr/bin/env python3

import ProofWriter as pw
import os
import logging

path = "../statements/statement5.txt"

if not os.path.exists(path):
    raise FileNotFoundError(f"File not found: {path}")

with open(path, "r", encoding="utf-8") as f:
    statement = f.read()
    
DSModel = pw.Api.api.getModel("deepseek-r1")

stepListAgent = pw.AlternateAgents.StepListAgent.StepListAgent(DSModel)

logging.basicConfig(level=logging.DEBUG)

output = stepListAgent.createStepList(statement)

import json

def clean_ai_jsonNew(raw_output: str) -> dict:
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
  
  
import subprocess
import tempfile
import os

#Substitute for your own path
ISABELLE_BIN = "/home/ltrzos/Isabelle2025/bin/isabelle"
  
def VerifyCorrectness(isabelleCode):
    with tempfile.TemporaryDirectory() as tmpdir:
        thy_path = os.path.join(tmpdir, "Scratch.thy")
        with open(thy_path, "w") as f:
            f.write(isabelleCode)
            
        root_path = os.path.join(tmpdir, "ROOT")
        with open(root_path, "w") as f:
            f.write("session TEMP_SESSION = HOL +\n  theories\n    Scratch\n")
            
        try:
            result = subprocess.run(
                [ISABELLE_BIN, "build", "-d", tmpdir, "-b", "TEMP_SESSION"],
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "stdout": result.stdout, "stderr": result.stderr}
        except subprocess.CalledProcessError as e:
            return {"success": False, "stdout": e.stdout, "stderr": e.stderr}

start_tag = "```json"
end_tag = "```"

start_idx = output.find(start_tag)
end_idx = output.find(end_tag, start_idx + len(start_tag))

if start_idx != -1 and end_idx != -1:
    trimmed_output = output[start_idx + len(start_tag):end_idx].strip()
else:
    trimmed_output = output
    
    
output = trimmed_output
    
print(output)

outputCleared = clean_ai_jsonNew(output)

print(outputCleared)

IsabelleString = """
theory Scratch
  imports Main
begin

locale group =
  fixes mul :: "'a ⇒ 'a ⇒ 'a" (infixl "∙" 70)
    and one :: "'a" ("e")
    and inv :: "'a ⇒ 'a"
  assumes assoc: "(x ∙ y) ∙ z = x ∙ (y ∙ z)"
      and left_one: "e ∙ x = x"
      and right_one: "x ∙ e = x"
      and left_inv: "inv x ∙ x = e"

begin

lemma group_axioms:
  "((x ∙ y) ∙ z = x ∙ (y ∙ z)) ∧
   (e ∙ x = x) ∧
   (x ∙ e = x) ∧
   (inv x ∙ x = e)"
  by (metis assoc left_one right_one left_inv)"""
  
IsabelleEnding = """
  
end

end"""

for i in range(len(outputCleared["A"])):
    DSModel = pw.Api.api.getModel("deepseek-r1")
    
    singleStepAgent = pw.AlternateAgents.SingleStepAgent.SingleStepAgent(DSModel)
    
    readyIsabelleCode = """
    locale group =
  fixes mul :: "'a ⇒ 'a ⇒ 'a" (infixl "∙" 70)
    and one :: "'a" ("e")
    and inv :: "'a ⇒ 'a"
  assumes assoc: "(x ∙ y) ∙ z = x ∙ (y ∙ z)"
      and left_one: "e ∙ x = x"
      and right_one: "x ∙ e = x"
      and left_inv: "inv x ∙ x = e"

begin

lemma group_axioms:
  "((x ∙ y) ∙ z = x ∙ (y ∙ z)) ∧
   (e ∙ x = x) ∧
   (x ∙ e = x) ∧
   (inv x ∙ x = e)"
  by (metis assoc left_one right_one left_inv)
    """
    
    output = singleStepAgent.createLemma(outputCleared["A"][i]["statement"], readyIsabelleCode)
    
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
      
    IsabelleString += f"""
    
lemma S{i+1}
{statement}
by (metis {deps})
    
    """
    
    print(IsabelleString)
    
    
IsabelleString += IsabelleEnding

izaVerification = VerifyCorrectness(IsabelleString)

print(izaVerification)

if(izaVerification["success"]):
  print("Success!")