# coding=utf-8


def convert_to_utf8(value):
    if isinstance(value, str):
        value = value.encode("utf-8")
    return value
