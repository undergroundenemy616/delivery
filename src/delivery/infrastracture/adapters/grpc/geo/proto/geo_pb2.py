# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: geo.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder


# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\tgeo.proto"\'\n\x15GetGeolocationRequest\x12\x0e\n\x06Street\x18\x01 \x01(\t"2\n\x13GetGeolocationReply\x12\x1b\n\x08Location\x18\x01 \x01(\x0b\x32\t.Location" \n\x08Location\x12\t\n\x01x\x18\x01 \x01(\x05\x12\t\n\x01y\x18\x02 \x01(\x05"\x1d\n\rErrorResponse\x12\x0c\n\x04text\x18\x01 \x01(\t2E\n\x03Geo\x12>\n\x0eGetGeolocation\x12\x16.GetGeolocationRequest\x1a\x14.GetGeolocationReplyb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "geo_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_GETGEOLOCATIONREQUEST"]._serialized_start = 13
    _globals["_GETGEOLOCATIONREQUEST"]._serialized_end = 52
    _globals["_GETGEOLOCATIONREPLY"]._serialized_start = 54
    _globals["_GETGEOLOCATIONREPLY"]._serialized_end = 104
    _globals["_LOCATION"]._serialized_start = 106
    _globals["_LOCATION"]._serialized_end = 138
    _globals["_ERRORRESPONSE"]._serialized_start = 140
    _globals["_ERRORRESPONSE"]._serialized_end = 169
    _globals["_GEO"]._serialized_start = 171
    _globals["_GEO"]._serialized_end = 240
# @@protoc_insertion_point(module_scope)
