# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: connect.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='connect.proto',
  package='com',
  syntax='proto3',
  serialized_options=b'Z\024../Protobuf;Protobuf',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rconnect.proto\x12\x03\x63om\"Z\n\rCommunication\x12\x0c\n\x04Type\x18\x01 \x01(\t\x12\x0b\n\x03Msg\x18\x02 \x01(\t\x12\x10\n\x08Username\x18\x03 \x01(\t\x12\x10\n\x08Userlist\x18\x04 \x03(\t\x12\n\n\x02IP\x18\x05 \x01(\tB\x16Z\x14../Protobuf;Protobufb\x06proto3'
)




_COMMUNICATION = _descriptor.Descriptor(
  name='Communication',
  full_name='com.Communication',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Type', full_name='com.Communication.Type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Msg', full_name='com.Communication.Msg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Username', full_name='com.Communication.Username', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Userlist', full_name='com.Communication.Userlist', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='IP', full_name='com.Communication.IP', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=112,
)

DESCRIPTOR.message_types_by_name['Communication'] = _COMMUNICATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Communication = _reflection.GeneratedProtocolMessageType('Communication', (_message.Message,), {
  'DESCRIPTOR' : _COMMUNICATION,
  '__module__' : 'connect_pb2'
  # @@protoc_insertion_point(class_scope:com.Communication)
  })
_sym_db.RegisterMessage(Communication)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
