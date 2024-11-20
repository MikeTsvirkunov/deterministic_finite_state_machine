from typing import Any, List, Type


def throw_exception(error_type: Type[Exception], text: str) -> None:
    d = 1
    raise error_type(text)


def insert_value_to_list(source_list: List, object: Any) -> None:
    source_list.append(object)


def empty_action(*args, **kwargs) -> None:
    pass