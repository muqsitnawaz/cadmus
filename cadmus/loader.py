from datetime import datetime
from datetime import timezone
from typing import List
from csv import DictReader
from pydantic import BaseModel
from json import load as json_load


class Email(BaseModel):
    sender: str
    subject: str
    snippet: str
    date: str


class Link(BaseModel):
    title: str
    url: str
    count: int
    date: str


def load_gmail(filename: str) -> List[Email]:
    """Load gmails from file."""

    emails: List[Email] = []
    with open(filename, encoding='utf-8') as csvf:
        csvReader = DictReader(csvf)
        for rows in csvReader:
            emails.append(
                Email(
                    sender=rows['From'],
                    subject=rows['Subject'],
                    snippet=rows['Snippet'],
                    date=rows['Date']
                )
            )

    return emails


def load_chrome(filename: str) -> List[Link]:
    """Load chrome history from file."""

    links: List[Link] = []
    with open(filename, "r") as f:
        data = json_load(f)

        for item in data:
            timestamp_sec = item['visitTime'] / 1000
            date_time = datetime.fromtimestamp(timestamp_sec, tz=timezone.utc)
            date_time.strftime("%a, %d %b %Y %H:%M:%S %z (UTC)")

            links.append(
                Link(
                    title=item['title'],
                    url=item['url'],
                    count=item['visitCount'],
                    date=date_time.strftime("%a, %d %b %Y %H:%M:%S %z (UTC)")
                )
            )

    return links


if __name__ == "__main__":
    emails = load_gmail('../data/gmail.csv')
    print(emails)

    links = load_chrome('../data/chrome.json')

    for link in links:
        link_dict = link.model_dump()
        print(link_dict)