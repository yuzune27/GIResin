import json

def save_token(tokendata):
    with open("tokenData.json", "a", encoding="utf-8") as f:
        json.dumps(tokendata, f, indent=4)

def open_token():
    with open("tokenData.json", "r", encoding="utf-8") as f:
        return json.loads(f)