#!/usr/bin/env python3

import json
import os
import re
import signal
import subprocess
import uuid

# Axioms every normal (classical) Lean/Mathlib proof is allowed to depend on.
# Anything else (sorryAx, a user-declared `axiom`, ...) means the proof is not trustworthy.
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


class LeanAgent:
    def __init__(self, project="lean_workspace", timeout=120):
        """
        `project` is a persistent Lake project (created once with `lake new <name> math`),
        NOT a throwaway workspace: it holds the Mathlib dependency, which is huge,
        so we must not delete it between checks.
        """
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.project = os.path.join(self.CURRENT_DIR, project)
        self.scratch = os.path.join(self.project, "scratch")
        self.timeout = timeout
        os.makedirs(self.scratch, exist_ok=True)

    def _run_lean(self, path):
        # start_new_session so that on timeout we can kill lake AND the lean process under it
        # (POSIX only; fine on Linux/macOS)
        proc = subprocess.Popen(
            ["lake", "env", "lean", "--json", path],
            cwd=self.project,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        try:
            out, err = proc.communicate(timeout=self.timeout)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.communicate()
            return None, "", f"Timed out after {self.timeout}s"
        return proc.returncode, out, err

    @staticmethod
    def _parse(stdout):
        """Lean with --json prints one JSON message per line."""
        messages, raw = [], []
        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                messages.append(json.loads(line))
            except json.JSONDecodeError:
                raw.append(line)
        return messages, raw

    @staticmethod
    def _fmt(msg):
        pos = msg.get("pos") or {}
        return f"{pos.get('line', '?')}:{pos.get('column', '?')}: {msg.get('data', '').strip()}"

    def check(self, proof_string: str, theorem_name: str = None):
        """
        proof_string: a complete .lean file (including `import Mathlib` etc. at the top).
        theorem_name: if given, also verifies which axioms the theorem depends on,
                      which catches `sorry` hidden in helper lemmas and cheating with `axiom`.

        Returns:
            { "ok": True }
            or
            { "ok": False, "errors": [...] }
        """
        source = proof_string
        if theorem_name:
            source += f"\n\n#print axioms {theorem_name}\n"

        # Lean does not care about the file name, so a unique name is fine
        # (and lets you run several checks in parallel).
        path = os.path.join(self.scratch, f"Auto_{uuid.uuid4().hex[:8]}.lean")
        try:
            with open(path, "w") as f:
                f.write(source)
            returncode, stdout, stderr = self._run_lean(path)
        finally:
            if os.path.exists(path):
                os.remove(path)

        if returncode is None:  # timeout
            return {"ok": False, "errors": [stderr]}

        messages, raw = self._parse(stdout)
        errors = []

        for m in messages:
            sev = m.get("severity")
            data = m.get("data", "")
            if sev == "error":
                errors.append(self._fmt(m))
            # `sorry` is only a WARNING in Lean and the exit code stays 0, so check explicitly
            elif sev == "warning" and "sorry" in data:
                errors.append(self._fmt(m))
            elif sev == "information" and "depends on axioms" in data:
                match = re.search(r"depends on axioms:\s*\[(.*?)\]", data, re.DOTALL)
                axioms = {a.strip() for a in match.group(1).split(",")} if match else set()
                bad = axioms - STANDARD_AXIOMS
                if bad:
                    errors.append(f"non-standard axioms used: {sorted(bad)}")

        # Non-zero exit but nothing structured (e.g. lake/toolchain problems): report raw output
        if returncode != 0 and not errors:
            errors = raw + [l for l in stderr.splitlines() if l.strip()]
            if not errors:
                errors = [f"lean exited with code {returncode}"]

        if errors:
            return {"ok": False, "errors": errors}
        return {"ok": True}


# example of use
# agent = LeanAgent()
#
# proof = """
# import Mathlib
#
# theorem one_add_one : 1 + 1 = 2 := by
#   norm_num
# """
# odp = agent.check(proof, theorem_name="one_add_one")
# print(odp)
# for e in odp.get("errors", []):
#     print(e)