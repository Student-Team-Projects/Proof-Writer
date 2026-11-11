#!/usr/bin/env python3


import ProofWriter.Api.api as api
import os
import random
import logging

class FormalizerAgentWithRandomExamples:
    def __init__(self, model: api.Model, requirements: dict):
        self.model = model
        self.CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.requirements = requirements

    def formalize(self, statement: str, proof: str):
        x = "FormalizerAgentWithRandomExamples"

        FORMALIZE_PATH = os.path.join(self.CURRENT_DIR,"../resources/FormalizerAgentWithRandomExamples/formalize1.txt")
        EXAMPLES_PATH = os.path.join(self.CURRENT_DIR,"../resources/FormalizerAgentWithRandomExamples/Examples")

        if not os.path.exists(FORMALIZE_PATH):
            raise FileNotFoundError(f"Prompt file not found: {FORMALIZE_PATH}")

        with open(FORMALIZE_PATH, "r", encoding="utf-8") as f:
            prompt = f.read()

        final_prompt = prompt.replace("STATEMENT_HERE", statement).replace("PROOF_HERE", proof).replace("EXAMPLES_HERE", get_examples_string(self.requirements, EXAMPLES_PATH))
        logging.info(final_prompt)
        return self.model.ask(final_prompt, thinking=True)


def get_examples_string(requirements: dict, base_path: str = "examples") -> str:
    """
    Picks random examples from folders based on a requirements map.

    Args:
        requirements (dict): Map {source: count}, e.g. {"domain_specific/algebra": 2, "all": 3}
        base_path (str): Path to the main examples folder.

    Returns:
        str: Formatted string containing the examples.
    """
    selected_file_paths = []

    # Check that the main folder exists
    if not os.path.exists(base_path):
        return f"Error: Folder '{base_path}' does not exist."

    # Iterate over the requirements
    for source, count in requirements.items():
        current_pool = []
        
        if source == "all":
            # 1. Collect files from ALL subfolders of 'examples'
            for root, dirs, files in os.walk(base_path):
                # Skip files in the main folder itself; we only want subfolders
                if root == base_path:
                    continue
                for file in files:
                    current_pool.append(os.path.join(root, file))
        else:
            # 2. Collect files from ONE specific folder
            target_folder = os.path.join(base_path, source)
            if os.path.exists(target_folder) and os.path.isdir(target_folder):
                current_pool = [
                    os.path.join(target_folder, f) 
                    for f in os.listdir(target_folder) 
                    if os.path.isfile(os.path.join(target_folder, f))
                ]
            else:
                print(f"Warning: Source '{source}' does not exist in {base_path}")
                continue

        # Sample files at random (capped so we never request more than are available)
        k = min(count, len(current_pool))
        if k > 0:
            selected_files = random.sample(current_pool, k)
            selected_file_paths.extend(selected_files)

    # Build the output string
    output_parts = []
    
    for i, file_path in enumerate(selected_file_paths, 1):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            # Format a single block
            block = f"Example {i}\n\n{content}"
            output_parts.append(block)
        except Exception as e:
            output_parts.append(f"Example {i}\n\n[Error reading file: {file_path}]")

    # Join the blocks with a blank line (or a single newline, depending on spacing preference)
    return "\n\n".join(output_parts)