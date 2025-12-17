import subprocess
import tempfile
import os

#Sciezka do binarki Izabeli
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