# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: product.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder # type: ignore
from google.protobuf import descriptor as _descriptor # type: ignore
from google.protobuf import descriptor_pool as _descriptor_pool # type: ignore
from google.protobuf import symbol_database as _symbol_database # type: ignore
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rproduct.proto\"7\n\tSizeModel\x12\x0c\n\x04size\x18\x01 \x01(\x05\x12\r\n\x05price\x18\x02 \x01(\x02\x12\r\n\x05stock\x18\x03 \x01(\x05\"S\n\x14ProductItemFormModel\x12\r\n\x05\x63olor\x18\x01 \x01(\t\x12\x11\n\timage_url\x18\x02 \x01(\t\x12\x19\n\x05sizes\x18\x03 \x03(\x0b\x32\n.SizeModel\"\x93\x01\n\x10ProductFormModel\x12\x14\n\x0cproduct_name\x18\x01 \x01(\t\x12\x14\n\x0cproduct_desc\x18\x02 \x01(\t\x12\x13\n\x0b\x63\x61tegory_id\x18\x03 \x01(\x05\x12\x11\n\tgender_id\x18\x04 \x01(\x05\x12+\n\x0cproduct_item\x18\x05 \x03(\x0b\x32\x15.ProductItemFormModelb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'product_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SIZEMODEL._serialized_start=17
  _SIZEMODEL._serialized_end=72
  _PRODUCTITEMFORMMODEL._serialized_start=74
  _PRODUCTITEMFORMMODEL._serialized_end=157
  _PRODUCTFORMMODEL._serialized_start=160
  _PRODUCTFORMMODEL._serialized_end=307
# @@protoc_insertion_point(module_scope)
