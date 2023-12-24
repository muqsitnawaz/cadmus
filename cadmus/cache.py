from datetime import datetime
from os import path
from typing import Dict
from uuid import uuid4

from loguru import logger

from database import Database
from model import Function
from model import Message
from model import Note


class Cache:
    def __init__(self):
        print(path.dirname(path.realpath(__file__)))
        self.messages = []
        self.notes = []
        self.functions = []

        self.database = Database(refresh=True)

    def add_message(self, message: Message):
        self.database.add_message(message)

    def add_note(self, note: Note):
        self.database.add_note(note)

    def add_function(self, function: Function):
        self.database.add_function(function)

    def get_messages(self, latest=3, similar=3):
        latest = self.database.get_latest_messages(limit=latest)

        for item in latest:
            logger.info(item)

        similar = self.database.get_similar_messages(latest[0], limit=similar)

        for item in similar:
            logger.info(item)

        messages: Dict[str, Message] = {}
        for item in latest + similar:
            messages[item.uuid] = item

        result = list(messages.values())
        result.sort(key=lambda x: x.timestamp, reverse=True)

        for item in result:
            logger.warning(item)

        return result

    def get_all(self):
        return {
            'Messages': self.messages,
            'Notes': self.notes,
            'Functions': self.functions,
        }

    def get_relevant(self, message):
        # TODO: Implement logic to get relevant messages, notes, and functions
        return {
            'Messages': self.messages,
            'Notes': self.notes,
            'Functions': self.functions,
        }


if __name__ == "__main__":
    cache = Cache()
    cache.add_message(Message(uuid=str(uuid4()), role="User", content="Hello, World!", timestamp=datetime.now()))
    cache.add_message(Message(uuid=str(uuid4()), role="User1", content="Hello, World!", timestamp=datetime.now()))
    cache.add_message(Message(uuid=str(uuid4()), role="User2", content="Hello, World!", timestamp=datetime.now()))
    cache.add_message(Message(uuid=str(uuid4()), role="User3", content="Hello, World!", timestamp=datetime.now()))
    cache.add_message(Message(uuid=str(uuid4()), role="User4", content="Hello, World!", timestamp=datetime.now()))
    cache.add_message(Message(uuid=str(uuid4()), role="User5", content="Hello, World!", timestamp=datetime.now()))
    cache.add_note(Note(uuid=str(uuid4()), content="This is a note.", timestamp=datetime.now()))
    cache.add_function(Function(uuid=str(uuid4()), name="print", description="print()"))
    # print(cache.get_all())

    cache.get_messages()
