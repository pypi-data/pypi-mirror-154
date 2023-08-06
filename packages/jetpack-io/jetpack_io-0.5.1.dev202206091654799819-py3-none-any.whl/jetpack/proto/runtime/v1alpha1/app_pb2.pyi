from jetpack.proto.runtime.v1alpha1 import remote_pb2 as _remote_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserApp(_message.Message):
    __slots__ = ["revision_to_manifest"]
    class RevisionToManifestEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    REVISION_TO_MANIFEST_FIELD_NUMBER: _ClassVar[int]
    revision_to_manifest: _containers.ScalarMap[int, str]
    def __init__(self, revision_to_manifest: _Optional[_Mapping[int, str]] = ...) -> None: ...
