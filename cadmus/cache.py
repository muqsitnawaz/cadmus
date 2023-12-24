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
        if latest < 0:
            latest = 1

        latest = self.database.get_latest_messages(limit=latest)

        for item in latest:
            logger.info(item)

        latest_message = latest[0]  # Most recent message
        similar = self.database.get_similar_messages(latest_message, limit=similar)

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

    def get_notes(self, latest=3, similar=3):
        latest = self.database.get_latest_notes(limit=latest)

        for item in latest:
            logger.info(item)

        latest_note = latest[0]
        similar = self.database.get_similar_notes(latest_note, limit=similar)

        for item in similar:
            logger.info(item)

        notes: Dict[str, Note] = {}
        for item in latest + similar:
            notes[item.uuid] = item

        result = list(notes.values())
        result.sort(key=lambda x: x.timestamp, reverse=True)

        for item in result:
            logger.warning(item)

        return result

    def get_functions(self, description: str, limit=3):
        similar = self.database.get_similar_functions(description, limit=limit)

        for item in similar:
            logger.info(item)

        return similar


if __name__ == "__main__":
    cache = Cache()
    cache.add_message(Message(uuid=str(uuid4()), role="User", content="Hello, World!", timestamp=datetime.now()))
    cache.add_message(Message(uuid=str(uuid4()), role="User1", content="Hello, World!", timestamp=datetime.now()))
    cache.add_message(Message(uuid=str(uuid4()), role="User2", content="Hello, World!", timestamp=datetime.now()))
    cache.add_message(Message(uuid=str(uuid4()), role="User3", content="Hello, World!", timestamp=datetime.now()))
    cache.add_message(Message(uuid=str(uuid4()), role="User4", content="Hello, World!", timestamp=datetime.now()))
    cache.add_message(Message(uuid=str(uuid4()), role="User5", content="Hello, World!", timestamp=datetime.now()))

    cache.add_note(Note(uuid=str(uuid4()), content="This is a note.", timestamp=datetime.now()))
    cache.add_note(Note(uuid=str(uuid4()), content="This is a note1.", timestamp=datetime.now()))
    cache.add_note(Note(uuid=str(uuid4()), content="This is a note2.", timestamp=datetime.now()))

    cache.add_function(Function(uuid=str(uuid4()), name="send_email", description="to send an email"))

    messages = cache.get_messages()
    notes = cache.get_notes()
    functions = cache.get_functions(description="to send an email")
