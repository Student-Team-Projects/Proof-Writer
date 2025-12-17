#!/usr/bin/env python3
import subprocess
import json

# DO NOT SHARE !!!!!!!!!!!!!

# DO NOT SHARE !!!!!!!!!!!!!

# DO NOT SHARE !!!!!!!!!!!!!

# DO NOT SHARE !!!!!!!!!!!!!

# DO NOT SHARE !!!!!!!!!!!!!

USER = ""
HOST = ""
PASSWORD = ""

# DO NOT SHARE !!!!!!!!!!!!!

# DO NOT SHARE !!!!!!!!!!!!!

# DO NOT SHARE !!!!!!!!!!!!!

# DO NOT SHARE !!!!!!!!!!!!!

# DO NOT SHARE !!!!!!!!!!!!!

def exec_cmd(remote_cmd, stdin=None):

    ssh_cmd = ["sshpass", "-p", PASSWORD, "ssh", f"{USER}@{HOST}", "curl", "-s", "--data-binary", "@-", "http://localhost:11435/api/generate"]
    proc = subprocess.run(ssh_cmd, input=stdin, text=True,
    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout or proc.stderr

def ask(prompt, model="phi4:14b", thinking=True):
    body = {
    "model": model,
    "prompt": prompt,
    "stream": False,
    "thinking": thinking
    }
    json_body = json.dumps(body)
    raw = exec_cmd(None, stdin=json_body)
    #print(raw, "ala ma kota")
    return json.loads(raw)['response']

# passwd_file = open("/home/username/.passwd.txt", "r")
# PASSWORD = passwd_file.read()

with open("config.json") as f:
    config = json.load(f)

USER = config["user"]
HOST = config["host"]
PASSWORD = config["password"]




##-------------------------BOOSTING----------------------------


def ModelBoost(prompt, models, thinking=False, election_thinking=False):

    # -------------------------------
    # 1. Generation phase
    # -------------------------------
    responses = {}

    for model in models:
        try:
            responses[model] = ask(
                prompt,
                model=model,
                thinking=thinking
            )
        except Exception as e:
            responses[model] = f"[ERROR] {e}"

    # -------------------------------
    # 2. Election phase
    # -------------------------------
    votes = {model: 0 for model in models}

    answers_blob = "\n\n".join(
        f"[{model}]\n{resp}"
        for model, resp in responses.items()
    )

    election_prompt = f"""
You are an impartial evaluator.

Several models answered the SAME prompt.
Choose the BEST answer based on:
- correctness
- logical soundness
- adherence to the task

Rules:
- Do NOT vote for your own answer automatically.
- Do NOT explain your choice.
- Output EXACTLY one line.

Format:
WINNER = <model_name>

Answers:
{answers_blob}
"""

    for voter in models:
        try:
            decision = ask(
                election_prompt,
                model=voter,
                thinking=election_thinking
            ).strip()

            if decision.startswith("WINNER ="):
                chosen = decision.split("=", 1)[1].strip()
                if chosen in votes:
                    votes[chosen] += 1

        except Exception:
            pass

    # -------------------------------
    # 3. Select winner
    # -------------------------------
    winning_model = max(votes, key=votes.get)
    best_answer = responses[winning_model]

    return {
        "best_answer": best_answer,
        "winning_model": winning_model,
        "votes": votes,
        "responses": responses
    }