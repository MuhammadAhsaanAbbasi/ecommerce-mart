# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: user.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nuser.proto\"\x88\x01\n\x04User\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x17\n\x0fhashed_password\x18\x03 \x01(\t\x12\x10\n\x08imageUrl\x18\x04 \x01(\t\x12\x15\n\rdate_of_birth\x18\x06 \x01(\t\x12\x0e\n\x06gender\x18\x07 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\"t\n\tEmailUser\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x10\n\x08imageUrl\x18\x03 \x01(\t\x12\x11\n\tis_active\x18\x04 \x01(\x08\x12\x13\n\x0bis_verified\x18\x05 \x01(\x08\x12\x0c\n\x04role\x18\x06 \x01(\t\"0\n\x03Otp\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\x12\x0b\n\x03otp\x18\x03 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USER._serialized_start=15
  _USER._serialized_end=151
  _EMAILUSER._serialized_start=153
  _EMAILUSER._serialized_end=269
  _OTP._serialized_start=271
  _OTP._serialized_end=319
# @@protoc_insertion_point(module_scope)
