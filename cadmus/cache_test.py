from datetime import datetime
from unittest import TestCase
from uuid import uuid4

from cache import Cache
from model import Message
from model import Note


class TestMemory(TestCase):

    def test_get_all_from_cache(self):
        cache = Cache()
        cache.add_message(
            Message(
                uuid=str(uuid4()),
                role="role",
                content="content",
                timestamp=datetime.now(),
            )
        )
        cache.add_note(
            Note(
                uuid=str(uuid4()),
                content="content",
                timestamp=datetime.now(),
            )
        )
