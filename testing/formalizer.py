#!/usr/bin/env python3
from api import *

"""
    FORMALIZER czyta dowód z "results/solver_out.txt", a następnie kreuje i   
    wysyła zapytanie do modelu, by ten przetłumaczył odpowiednie fragmenty na
    język formalny. Wynik zapisuje do "results/formalizer_out.txt"
"""

solver_out_file = open("results/solver_out.txt", "r")
solver_out = solver_out_file.read()

formalizer_prompt_file = open("../resources/prompts/formalizer/prompt1.txt", "r")
formalizer_prompt = formalizer_prompt_file.read()
formalizer_prompt = formalizer_prompt.replace("{PROOF_JSON}", solver_out)

formalizer_out = ask(formalizer_prompt, model="deepseek-r1:14b")
with open("results/formalizer_out.txt", "w") as f:
    f.write(formalizer_out)
print(formalizer_out)