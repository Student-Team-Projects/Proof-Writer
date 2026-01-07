#!/usr/bin/env python3
import subprocess
import json
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# print(CURRENT_DIR)

MODEL_CONFIG_PATH = os.path.join(CURRENT_DIR, "configModels.json")
CONNECTION_CONFIG_PATH = os.path.join(CURRENT_DIR, "configConnection.json")
# print(CONFIG_PATH)

with open(MODEL_CONFIG_PATH) as f:
    models = json.load(f)

with open(CONNECTION_CONFIG_PATH) as f:
    config = json.load(f)

USER = config["user"]
HOST = config["host"]
PASSWORD = config["password"]

class Model:
    def __init__(self, user, host, password, model):
        self.user = user
        self.host = host
        self.password = password
        self.model = models[model]

    def getContext(self):
        """
        Tworzy obiekt kontekstu powiązany z tym modelem.
        """
        return Context(self)


class Context:
    def __init__(self, model: Model):
        self.model = model


    def exec_cmd(self, remote_cmd, stdin=None):
        ssh_cmd = ["sshpass", "-p", self.model.password, "ssh", f"{self.model.user}@{self.model.host}", "curl", "-s", "--data-binary", "@-", "http://localhost:11435/api/generate"]
        proc = subprocess.run(ssh_cmd, input=stdin, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print(ssh_cmd,stdin)
        return proc.stdout or proc.stderr
        # print(ssh_cmd)
        # return input()


    def ask(self, prompt, thinking = True):
        body = {
            "model": self.model.model,
            "prompt": prompt,
            "stream": False,
            "thinking": thinking
        }
        json_body = json.dumps(body)
        raw = self.exec_cmd(None, stdin=json_body)
        return json.loads(raw)['response']


def getModel(name = "phi"):
    return Model(user = USER, host = HOST, password = PASSWORD, model = name)

