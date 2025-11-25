#!/usr/bin/env python3

import subprocess
import re
import os
import uuid
import shutil

class IsabelleAgent:
    def __init__(self, workspace="isabelle_workspace"):
        self.workspace = workspace

    def _reset_workspace(self):
        # Usuwamy stary workspace
        if os.path.exists(self.workspace):
            shutil.rmtree(self.workspace)

        # Tworzymy pusty
        os.makedirs(self.workspace)

    def _write_files(self, theory_name, content):
        # Zapis .thy
        with open(f"{self.workspace}/{theory_name}.thy", "w") as f:
            f.write(content)

        # Zapis ROOT
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

        # Wyłuskanie błędów
        error_pattern = re.compile(r"\*\*\*|Error|error|FAILED|Undefined|Unknown|Malformed", re.IGNORECASE)
        errors = [line for line in result.stderr.splitlines() if error_pattern.search(line)]

        return (result.returncode == 0, errors)

    def check(self, proof_string: str):
        """
        Zwraca:
            { "ok": True }
            lub
            { "ok": False, "errors": [...] }
        """

        # Czyścimy workspace przed użyciem
        self._reset_workspace()

        theory_name = f"Auto_{uuid.uuid4().hex[:8]}"

        if not proof_string.strip().startswith("theory"):
            proof_string = f"""
theory {theory_name}
imports Main
begin

{proof_string}

end
"""

        self._write_files(theory_name, proof_string)
        ok, errors = self._run_isabelle()

        if ok:
            return { "ok": True }
        else:
            return { "ok": False, "errors": errors }




# example of use
# agent = IsabelleAgent()

# proof = """
# lemma "1 + 1 = 2"
#   by simp
# """

# print(agent.check(proof))
