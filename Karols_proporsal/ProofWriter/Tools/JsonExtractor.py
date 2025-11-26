import json

def extract_outermost_json(s):
    start = None
    brace_count = 0
    
    for i, char in enumerate(s):
        if char == '{':
            if start is None:
                start = i
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0 and start is not None:
                json_str = s[start:i+1]
                try:
                    json.loads(json_str)
                    return json_str
                except json.JSONDecodeError:
                    return None
    return None