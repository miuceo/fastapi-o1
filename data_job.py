import json
from typing import Any, Dict

def get_all_data() -> Dict[str, Any]:
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
            return data
    except:
        return {"products": [], "categories": []}


def write_data(data: Dict[str, Any]) -> bool:
    try:
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except:
        return False
