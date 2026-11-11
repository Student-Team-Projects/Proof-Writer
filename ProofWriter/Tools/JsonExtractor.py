import json
import re

def extract_outermost_json(s):
    if '{' not in s or '}' not in s:
        return None
    
    start = s.find('{')
    end = s.rfind('}') + 1
    json_str = s[start:end].strip()
    
    return json_str


def clean_ai_json(raw_output: str) -> dict:
    """
    Cleans up a string returned by the AI and returns it as valid JSON text.
    """
    cleaned = raw_output.replace("```json", "").replace("```", "").strip()

    first_brace = cleaned.find('{')
    last_brace = cleaned.rfind('}') + 1
    if first_brace == -1 or last_brace == -1:
        raise ValueError("No JSON found in the AI response.")
    cleaned = cleaned[first_brace:last_brace]

    cleaned = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', cleaned)

    #cleaned = cleaned.replace('\n', '\\n')

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON after cleanup: {e}")

    return cleaned