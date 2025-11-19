#!/usr/bin/env python3
from api import *
from collections import OrderedDict

"""
    PROOF_CHECKER skleja fragmenty dowodu wygenerowanego przez FORMALIZER 
    w jeden, kompletny dowód.
"""

formalizer_out_file = open("results/formalizer_out.txt", "r")
formalizer_out = formalizer_out_file.read()

data = json.loads(formalizer_out)
nodes = data.get("formal_proof", [])

unique = OrderedDict()
for n in nodes:
    nid = int(n['id'])
    if nid not in unique:
        unique[nid] = n

def lemma_header(n): return f"-- lemma_{n['id']} :\n"
def lemma_footer(n): return "\n-- end lemma\n"

out_chunks = []
for node in unique.values():
    code = node.get('formal_code', '').rstrip()
    if not code:
        continue
    if node.get('type') == 'lemma':
        out_chunks.append(lemma_header(node) + code + lemma_footer(node))
    else:
        out_chunks.append(code)
final_proof = "\n\n".join(out_chunks)

with open("results/proofchecker_out.txt", "w") as f:
    f.write(final_proof)
print(final_proof)
