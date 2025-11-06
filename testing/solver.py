#!/usr/bin/env python3
from api import *

"""
    SOLVER czyta twierdzenie z "statement.txt", a następnie kreuje i   
    wysyła zapytanie do modelu, by ten dowiódł tezę. Wynik zapisuje
    do "results/solver_out.txt"
"""

statement_file = open("statement.txt", "r")
statement = statement_file.read()

solver_prompt_file = open("../resources/prompts/solver/prompt1.txt", "r")
solver_prompt = solver_prompt_file.read()
solver_prompt = solver_prompt.replace("{STATEMENT_HERE}", statement)

solver_out = ask(solver_prompt, model="deepseek-r1:14b")
print(solver_out)
with open("results/solver_out.txt", "w") as f:
    f.write(solver_out)
