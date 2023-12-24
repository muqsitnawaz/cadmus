from datetime import datetime
from typing import Dict
from typing import List

from loguru import logger
from openai import OpenAI
from weaviate import Client as WeaviateClient

from model import Function
from model import Message
from model import Note

openai = OpenAI()

schemas: Dict[str, Dict] = {
    "Message": {
        "class": "Message",
        "properties": [
            {
                "name": "uuid",
                "dataType": ["uuid"],
            },
            {
                "name": "role",
                "dataType": ["text"]
            },
            {
                "name": "content",
                "dataType": ["text"],
            },
            {
                "name": "timestamp",
                "dataType": ["date"],
            },
        ]
    },
    "Note": {
        "class": "Note",
        "properties": [
            {
                "name": "uuid",
                "dataType": ["uuid"],
            },
            {
                "name": "content",
                "dataType": ["text"],
            },
            {
                "name": "timestamp",
                "dataType": ["date"],
            },
        ]
    },
    "Function": {
        "class": "Function",
        "properties": [
            {
                "name": "uuid",
                "dataType": ["uuid"],
            },
            {
                "name": "name",
                "dataType": ["text"],
            },
            {
                "name": "schema",
                "dataType": ["text"],
            },
        ]
    },
}


class Database:
    def __init__(self, refresh=False):
        self.client = WeaviateClient("http://localhost:8080")  # Replace with your endpoint

        if refresh:
            self.client.schema.delete_class("Message")
            self.client.schema.delete_class("Note")
            self.client.schema.delete_class("Function")

        if not self.client.schema.exists("Message"):
            self.client.schema.create_class(schemas["Message"])

        if not self.client.schema.exists("Note"):
            self.client.schema.create_class(schemas["Note"])

        if not self.client.schema.exists("Function"):
            self.client.schema.create_class(schemas["Function"])

    def add_message(self, message: Message) -> str:
        embedding = self.__embed__(message.content)
        return self.__create_object__("Message", message, embedding)

    def add_note(self, note: Note):
        embedding = self.__embed__(note.content)
        return self.__create_object__("Note", note, embedding)

    def add_function(self, function: Function):
        # TODO: Use AST tree for better function matching
        embedding = self.__embed__(function.name)
        return self.__create_object__("Function", function, embedding)

    def get_latest_messages(self, limit: int) -> List[Message]:
        response = (
            self.client.query
            .get(
                class_name="Message",
                properties=["uuid", "role", "content", "timestamp"],
            )
            .with_sort({
                'path': ['timestamp'],
                'order': 'desc',
            })
            .with_limit(limit)
            .do()
        )

        logger.debug(response)

        result: List[Message] = []
        for item in response['data']['Get']['Message']:
            result.append(Message(
                uuid=item['uuid'],
                role=item['role'],
                content=item['content'],
                timestamp=item['timestamp'],
            ))
        return result

    def get_similar_messages(self, message: Message, limit: int) -> List[Message]:
        response = (
            self.client.query
            .get(
                class_name="Message",
                properties=["uuid", "role", "content", "timestamp"],
            )
            .with_near_vector(
                {
                    'vector': self.__embed__(message.content),
                    'certainty': 0.8,
                }
            )
            .with_limit(limit)
            .do()
        )

        logger.debug(response)

        result: List[Message] = []
        for item in response['data']['Get']['Message']:
            result.append(Message(
                uuid=item['uuid'],
                role=item['role'],
                content=item['content'],
                timestamp=item['timestamp'],
            ))
        return result

    def get_latest_notes(self, limit: int):
        response = (
            self.client.query
            .get(
                class_name="Note",
                properties=["uuid", "content", "timestamp"],
            )
            .with_sort({
                'path': ['timestamp'],
                'order': 'desc',
            })
            .with_limit(limit)
            .do()
        )

        logger.debug(response)

        result: List[Note] = []
        for item in response['data']['Get']['Note']:
            result.append(Note(
                uuid=item['uuid'],
                content=item['content'],
                timestamp=item['timestamp'],
            ))
        return result

    def get_similar_notes(self, note: Note, limit: int):
        response = (
            self.client.query
            .get(
                class_name="Note",
                properties=["uuid", "content", "timestamp"],
            )
            .with_near_vector(
                {
                    'vector': self.__embed__(note.content),
                    'certainty': 0.8,
                }
            )
            .with_limit(limit)
            .do()
        )

        logger.debug(response)

        result: List[Note] = []
        for item in response['data']['Get']['Note']:
            result.append(Note(
                uuid=item['uuid'],
                content=item['content'],
                timestamp=item['timestamp'],
            ))
        return result

    def get_similar_functions(self, description: str, limit: int):
        response = (
            self.client.query
            .get(
                class_name="Function",
                properties=["uuid", "name", "description"],
            )
            .with_near_vector(
                {
                    'vector': self.__embed__(description),
                    'certainty': 0.8,
                }
            )
            .with_limit(limit)
            .do()
        )

        logger.debug(response)

        result: List[Function] = []
        for item in response['data']['Get']['Function']:
            result.append(Function(
                uuid=item['uuid'],
                name=item['name'],
                description=item['description'],
            ))
        return result

    def __create_object__(self, class_name: str, data_object, embedding) -> str:
        uuid = data_object.uuid
        self.client.data_object.create(
            data_object=data_object.safe_dict(),
            class_name=class_name,
            uuid=uuid,
            vector=embedding
        )
        return uuid

    def __count_objects__(self, class_name: str):
        response = (
            self.client.query
            .aggregate(class_name)
            .with_meta_count()
            .do()
        )
        return response['data']['Aggregate'][class_name][0]['meta']['count']

    def __embed__(self, text: str):
        _ = text
        return [1, 2, 3]
        #
        # response = openai.embeddings.create(
        #     model="text-embedding-ada-002",
        #     input=text
        # )
        # return response['data'][0]['embedding']  # Accessing the embedding


if __name__ == "__main__":
    database = Database(refresh=True)
    message = Message(role="User", content="Hello, World!", timestamp=datetime.now())
    print(message.model_dump_json())
    database.add_message(message)
