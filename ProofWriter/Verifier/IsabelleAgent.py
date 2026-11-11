#!/usr/bin/env python3

import subprocess
import re
import os
import uuid
import shutil
import json

class IsabelleAgent:
    def __init__(self, workspace="isabelle_workspace"):
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.workspace = os.path.join(self.CURRENT_DIR,workspace)

    def _reset_workspace(self):
        # Remove the old workspace
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)

        # Create an empty one
        os.makedirs(self.workspace)

    def _write_files(self, theory_name, content):
        # Write the .thy file
        with open(f"{self.workspace}/{theory_name}.thy", "w") as f:
            f.write(content)

        # Write the ROOT file
        with open(f"{self.workspace}/ROOT", "w") as f:
            f.write(
                f"session {theory_name} = HOL +\n"
                f"  theories\n"
                f"    {theory_name}\n"
            )

    def _run_isabelle(self):
        result = subprocess.run(
            ["isabelle", "build", "-D", self.workspace],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Extract the error lines
        error_pattern = re.compile(r"\*\*\*|Error|error|FAILED|Undefined|Unknown|Malformed", re.IGNORECASE)
        all_output = result.stdout.splitlines() + result.stderr.splitlines()
        errors = [line for line in all_output if error_pattern.search(line)]


        return (result.returncode == 0, errors)

    def check(self, proof_string: str):
        """
        Returns:
            { "ok": True }
            or
            { "ok": False, "errors": [...] }
        """

        # Clear the workspace before use
        self._reset_workspace()

        # theory_name = f"Auto_{uuid.uuid4().hex[:8]}"
        theory_name = "Scratch"

        self._write_files(theory_name, proof_string)
        ok, errors = self._run_isabelle()

        if ok:
            return { "ok": True }
        else:
            return { "ok": False, "errors": errors }




# example of use
# agent = IsabelleAgent()

# proof = """
# {
# theory Isabelleproof
#   imports Main
# begin

# lemma "1 + 1 = 2"
#    by simp

# end

# }
# """
# odp = agent.check(proof)
# print(odp)
# for e in odp['errors']:
#     print(e)
