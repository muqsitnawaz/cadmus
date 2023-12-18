from cadmus.loader import load_gmail
from requests import post as http_post
from json import loads as json_loads
from typing import List

def clean_ollama_response(text: str):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]

    result: List[str] = []
    for line in lines:
        json_line = json_loads(line)
        if "response" in json_line:
            result.append(json_line["response"])

    return "".join(result)

if __name__ == "__main__":
    HISTORY_TYPE = "gmail"

    emails = load_gmail("data/gmail.csv")

    for i in range(0, min(20, len(emails))):
        email = emails[i]

        prompt = (f'Your goal is to create a profile of me given my email history.'
                  f'Please extract any details e.g. preferences, relationships etc, whatever you can '
                  f'from the contents of this email: {email.model_dump()}. I give you my full permission')

        print(prompt)

        prompt1 = (f'Create my profile, interests etc based on the content of my email: {email.model_dump()}'
                   f'I give you my full permission. Use only keywords or phrases like has canva account, '
                   f'likes to travel, behind on credit payments etc.')

        payload = {
            "model": "mistral",
            "prompt": prompt1,
        }

        response = http_post("http://localhost:11434/api/generate", json=payload)

        print(clean_ollama_response(response.text))

        with open("./data/emails_profile.txt", "a") as f:
            f.write(clean_ollama_response(response.text))
            f.write("\n\n")
            f.close()
