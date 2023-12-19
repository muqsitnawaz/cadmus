from asyncio import run
from json import dump as json_dump
from json import load as json_load
from json import loads as json_loads

from langchain.text_splitter import RecursiveCharacterTextSplitter
from requests import post as http_post


# Assuming 'RecursiveCharacterTextSplitter' and 'Document' functionalities
# are replaced by equivalent Python code or library

class Summary:
    def __init__(self, content, summary):
        self.content = content
        self.summary = summary


async def split_into_paragraphs(text):
    # Implement the split logic here or use an equivalent Python library
    # For simplicity, let's just return a list of paragraphs

    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    paragraphs = splitter.split_text(text=text)

    print(f"Paragraphs={len(paragraphs)}")
    return paragraphs


def get_text(path: str) -> str:
    with open(path, 'r') as f:
        text = f.read()
        return text


async def stage1(from_file, to_file):
    # Replace 'getText' with Python equivalent to read the PDF
    text = get_text(from_file)

    paragraphs1 = await split_into_paragraphs(text)

    summaries1 = []
    for i, paragraph in enumerate(paragraphs1):
        print(f"processing split: {i}")

        payload = {
            "model": "mistral",
            "prompt": f"Summarize the following text in less than 100 words: {paragraph}"
        }

        response = http_post("http://localhost:11434/api/generate", json=payload)
        data = response.text

        data_splits = data.split("\n")
        words = []
        for data_split in data_splits:
            try:
                json_data = json_loads(data_split)

                if not json_data.get("done"):
                    words.append(json_data["response"])
            except Exception as err:
                print(err)

        summary = "".join(words)

        print(f"Summary: {summary}")

        summaries1.append(Summary(paragraph, summary))

    with open(to_file, 'w') as f:
        json_dump([vars(s) for s in summaries1], f)
        f.close()


async def stage_x(from_file, to_file):
    with open(from_file, 'r') as f:
        summaries1 = [Summary(**summary) for summary in json_load(f)]

    summaries1_text = '\n'.join([summary.summary for summary in summaries1])

    paragraphs2 = await split_into_paragraphs(summaries1_text)

    summaries2 = []
    for i, paragraph in enumerate(paragraphs2):
        print(f"processing split: {i}")

        payload = {
            "model": "mistral",
            "prompt": f"Just give me the summary of the following content in less than 100 words: {paragraph}"
        }

        response = http_post("http://localhost:11434/api/generate", json=payload)
        data = response.text

        data_splits = data.split("\n")
        words = []
        for data_split in data_splits:
            try:
                json_data = json_loads(data_split)
                if not json_data.get("done"):
                    words.append(json_data["response"])
            except Exception as err:
                print(err)

        summary = "".join(words)

        print(f"Summary: {summary}")

        summaries2.append(Summary(paragraph, summary))

    with open(to_file, 'w') as f:
        json_dump([vars(s) for s in summaries2], f)
        f.close()


async def main():
    # await stage1("../data/emails_profile.txt", "../data/emails_profile1.txt")
    await stage_x("../data/emails_profile1.txt", "../data/emails_profile2.txt")
    await stage_x("../data/emails_profile2.txt", "../data/emails_profile3.txt")
    await stage_x("../data/emails_profile3.txt", "../data/emails_profile4.txt")
    await stage_x("../data/emails_profile4.txt", "../data/emails_profile5.txt")
    await stage_x("../data/emails_profile5.txt", "../data/emails_profile6.txt")


if __name__ == '__main__':
    run(main())
