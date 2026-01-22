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
            raise FileNotFoundError(f"Brak pliku promptu: {FORMALIZE_PATH}")

        with open(FORMALIZE_PATH, "r", encoding="utf-8") as f:
            prompt = f.read()

        final_prompt = prompt.replace("STATEMENT_HERE", statement).replace("PROOF_HERE", proof).replace("EXAMPLES_HERE", get_examples_string(self.requirements, EXAMPLES_PATH))
        logging.info(final_prompt)
        return self.model.ask(final_prompt, thinking=True)


def get_examples_string(requirements: dict, base_path: str = "examples") -> str:
    """
    Pobiera losowe przykłady z folderów na podstawie mapy wymagań.
    
    Args:
        requirements (dict): Mapa {źródło: ilość}, np. {"historia": 2, "all": 3}
        base_path (str): Ścieżka do głównego folderu z przykładami.
        
    Returns:
        str: Sformatowany ciąg tekstowy z przykładami.
    """
    selected_file_paths = []
    
    # Sprawdzenie czy folder główny istnieje
    if not os.path.exists(base_path):
        return f"Błąd: Folder '{base_path}' nie istnieje."

    # Iteracja po wymaganiach
    for source, count in requirements.items():
        current_pool = []
        
        if source == "all":
            # 1. Pobierz pliki ze WSZYSTKICH podfolderów w 'examples'
            for root, dirs, files in os.walk(base_path):
                # Pomijamy pliki w samym folderze głównym, interesują nas podfoldery
                if root == base_path:
                    continue
                for file in files:
                    current_pool.append(os.path.join(root, file))
        else:
            # 2. Pobierz pliki z KONKRETNEGO folderu
            target_folder = os.path.join(base_path, source)
            if os.path.exists(target_folder) and os.path.isdir(target_folder):
                current_pool = [
                    os.path.join(target_folder, f) 
                    for f in os.listdir(target_folder) 
                    if os.path.isfile(os.path.join(target_folder, f))
                ]
            else:
                print(f"Ostrzeżenie: Źródło '{source}' nie istnieje w {base_path}")
                continue

        # Losowanie plików (zabezpieczenie przed żądaniem większej liczby niż dostępna)
        k = min(count, len(current_pool))
        if k > 0:
            selected_files = random.sample(current_pool, k)
            selected_file_paths.extend(selected_files)

    # Budowanie wynikowego stringa
    output_parts = []
    
    for i, file_path in enumerate(selected_file_paths, 1):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            # Formatowanie pojedynczego bloku
            block = f"Example {i}\n\n{content}"
            output_parts.append(block)
        except Exception as e:
            output_parts.append(f"Example {i}\n\n[Błąd odczytu pliku: {file_path}]")

    # Łączenie bloków podwójną nową linią (lub pojedynczą, zależnie od preferencji odstępów)
    return "\n\n".join(output_parts)