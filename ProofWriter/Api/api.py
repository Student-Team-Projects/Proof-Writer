#!/usr/bin/env python3
import subprocess
import json
import requests

import logging

def createModel(model_name, session):
    """
    Create model associated with a session.
    """
    return Model(model_name, session)

class Session:
    def __init__(self, host = "http://127.0.0.1:11434"):
        self.host = host
    
    def list_models(self):
        """
        Prints the available model names.
        """
        url = self.host.rstrip("/") + "/api/tags"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return [m.get("name") for m in data.get("models", []) if "name" in m]

class Model:
    def __init__(self, model_name, session):
        self.model_name = model_name
        self.session = session

    def ask(self, prompt, thinking = True, timeout = 60):
        """
        Sends prompt to the model and waits for the response.
        """
        url = self.session.host.rstrip("/") + "/api/generate"
        body = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "thinking": thinking
        }
        resp = requests.post(url, json=body, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()

        return data.get("response", "")
    
    def getSession(self):
        return self.session