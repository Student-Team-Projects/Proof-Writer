#!/usr/bin/env python3
import subprocess
import json

USER = ""
HOST = ""
PASSWORD = ""

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
    return json.loads(raw)['response']

passwd_file = open("/home/username/.passwd.txt", "r")
PASSWORD = passwd_file.read()