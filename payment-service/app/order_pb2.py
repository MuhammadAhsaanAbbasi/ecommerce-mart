# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: order.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder # type: ignore
from google.protobuf import descriptor as _descriptor # type: ignore
from google.protobuf import descriptor_pool as _descriptor_pool # type: ignore
from google.protobuf import symbol_database as _symbol_database # type: ignore
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0border.proto\x12\x05order\"d\n\tOrderBase\x12\x15\n\rorder_address\x18\x01 \x01(\t\x12\x14\n\x0cphone_number\x18\x02 \x01(\t\x12\x13\n\x0btotal_price\x18\x03 \x01(\x02\x12\x15\n\rorder_payment\x18\x04 \x01(\t\"g\n\rOrderItemForm\x12\x12\n\nproduct_id\x18\x01 \x01(\t\x12\x17\n\x0fproduct_item_id\x18\x02 \x01(\x05\x12\x17\n\x0fproduct_size_id\x18\x03 \x01(\x05\x12\x10\n\x08quantity\x18\x04 \x01(\x05\"t\n\nOrderModel\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x10\n\x08order_id\x18\x02 \x01(\t\x12\x1e\n\x04\x62\x61se\x18\x03 \x01(\x0b\x32\x10.order.OrderBase\x12#\n\x05items\x18\x04 \x03(\x0b\x32\x14.order.OrderItemFormb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ORDERBASE._serialized_start=22
  _ORDERBASE._serialized_end=122
  _ORDERITEMFORM._serialized_start=124
  _ORDERITEMFORM._serialized_end=227
  _ORDERMODEL._serialized_start=229
  _ORDERMODEL._serialized_end=345
# @@protoc_insertion_point(module_scope)
