#!/usr/bin/env python3

import MainAgent.MainAgent as ma
import os
import logging

path = "../../statements/statement2.txt"

if not os.path.exists(path):
    raise FileNotFoundError(f"File not found: {path}")

with open(path, "r", encoding="utf-8") as f:
    statement = f.read()

model = ma.MainAgent()

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO)

proof, verification = model.solve(statement)

print(proof)

if verification: 
    print("Verification was successful")
else:
    print("Werification failed")