from datetime import datetime
from json import JSONEncoder

from pydantic import BaseModel


class Message(BaseModel):
    uuid: str
    role: str
    content: str
    timestamp: datetime

    def safe_dict(cls):
        return {
            'uuid': cls.uuid,
            'role': cls.role,
            'content': cls.content,
            'timestamp': cls.timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }


class Note(BaseModel):
    uuid: str
    content: str
    timestamp: datetime

    def safe_dict(cls):
        return {
            'uuid': cls.uuid,
            'content': cls.content,
            'timestamp': cls.timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }


class Function(BaseModel):
    uuid: str
    name: str
    description: str

    def safe_dict(cls):
        return {
            'uuid': cls.uuid,
            'name': cls.name,
            'description': cls.description,
        }


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # Format as a string, e.g., ISO format
            return obj.isoformat()
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)
