from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FilesReply(_message.Message):
    __slots__ = ["file_list"]
    FILE_LIST_FIELD_NUMBER: _ClassVar[int]
    file_list: str
    def __init__(self, file_list: _Optional[str] = ...) -> None: ...

class ListFilesRequest(_message.Message):
    __slots__ = ["limit"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    limit: int
    def __init__(self, limit: _Optional[int] = ...) -> None: ...

class SearchFilesRequest(_message.Message):
    __slots__ = ["limit", "pattern"]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    limit: int
    pattern: str
    def __init__(self, pattern: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...
