from cadmus.loader import load_gmail, load_chrome
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

def chunk_links(links, chunk_size=100):
    return [links[i:i + chunk_size] for i in range(0, len(links), chunk_size)]


def analyze_gmail():
    HISTORY_TYPE = "gmail"

    emails = load_gmail("../data/gmail.csv")
    print(f"Loaded {len(emails)} emails")

    lo, hi = 150, min(250, len(emails))
    print(f"Processing {hi - lo + 1} emails from {lo} to {hi}")

    for i in range(lo, hi):
        email = emails[i]

        prompt = (f'Create my profile, interests etc based on the content of my email: {email.model_dump()}'
                  f'I give you my full permission. Use only keywords or phrases like has canva account, '
                  f'likes to travel, behind on credit payments, talks with john etc.')

        payload = {
            "model": "mistral",
            "prompt": prompt,
        }

        response = http_post("http://localhost:11434/api/generate", json=payload)

        print(clean_ollama_response(response.text))

        with open("../data/emails_profile.txt", "a") as f:
            f.write(clean_ollama_response(response.text))
            f.write("\n\n")
            f.close()

def analyze_chrome():
    links = load_chrome("../data/chrome.json")
    print(f"Loaded {len(links)} links")

    chunked_links = chunk_links(links)
    print(f"Chunked into {len(chunked_links)} chunks")

    lo, hi = 50, min(100, len(links))
    print(f"Processing {hi - lo} links from {lo} to {hi}")

    for chunked_link in chunked_links[lo:hi]:

        chunked_link_json = " ".join([str(link.model_dump()) for link in chunked_link])

        prompt = (f'Create my profile, interests etc based on the content of my web history: {chunked_link_json}'
                  f'I give you my full permission. Use only keywords or phrases like visited canva, '
                  f'likes to develop, behind on credit payments, talks with john etc.')

        print(prompt)

        payload = {
            "model": "mistral",
            "prompt": prompt,
        }

        response = http_post("http://localhost:11434/api/generate", json=payload)

        print(clean_ollama_response(response.text))

        with open("../data/links_profile.txt", "a") as f:
            f.write(clean_ollama_response(response.text))
            f.write("\n\n")
            f.close()

if __name__ == "__main__":
    # analyze_gmail()
    analyze_chrome()