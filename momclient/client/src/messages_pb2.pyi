from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectionRequest(_message.Message):
    __slots__ = ["channel_id", "queue_label"]
    CHANNEL_ID_FIELD_NUMBER: _ClassVar[int]
    QUEUE_LABEL_FIELD_NUMBER: _ClassVar[int]
    channel_id: str
    queue_label: str
    def __init__(self, queue_label: _Optional[str] = ..., channel_id: _Optional[str] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ["content", "id", "topic"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    content: bytes
    id: str
    topic: str
    def __init__(self, id: _Optional[str] = ..., content: _Optional[bytes] = ..., topic: _Optional[str] = ...) -> None: ...
