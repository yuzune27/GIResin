import json

x = {845733927: {"ltuid": 174808526, "ltoken": "ggetQDnMHo4Mt25qoeJi5pkdtWRkm4nHm8F3IZNx"}}

def save_token(tokendata):
    with open("tokenData.json", "w", encoding="utf-8") as f:
        json.dump(tokendata, f, indent=4)

def open_token():
    with open("tokenData.json", "r", encoding="utf-8") as f:
        return json.load(f)
    

if __name__ == "__main__":
    jsonData = open_token()
    for jsonUID in jsonData["gi"]:
        print(jsonUID)
        print(type(jsonUID))