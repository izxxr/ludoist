# MIT License

# Copyright (c) 2024 Izhar Ahmad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from typing import Type, Any, List, Mapping, TypeVar
from enum import IntEnum
from oblate import Schema, fields, LoadContext, DumpContext

import collections.abc

__all__ = (
    "IntEnumField",
    "SchemaList",
)

_S = TypeVar("_S", bound=Schema)


class IntEnumField(fields.Field[int, IntEnum]):
    def __init__(self, enum_cls: Type[IntEnum], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._enum_cls = enum_cls

    def value_load(self, value: Any, context: LoadContext) -> IntEnum:
        if not isinstance(value, int):
            raise ValueError("value must be an integer")

        return self._enum_cls(value)

    def value_dump(self, value: IntEnum, context: DumpContext) -> int:
        return value.value


class SchemaList(fields.Field[List[Mapping[str, Any]], List[_S]]):
    def __init__(self, schema_cls: Type[_S], *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._schema_cls = schema_cls

    def value_load(self, value: Any, context: LoadContext) -> List[_S]:
        if not isinstance(value, list):
            raise ValueError("value must be a list")

        out = []
        for data in value:
            if not isinstance(data, collections.abc.Mapping):
                raise ValueError("list contains an invalid item")

            out.append(self._schema_cls(data))

        return out

    def value_dump(self, value: List[_S], context: DumpContext) -> List[Mapping[str, Any]]:
        return [v.dump() for v in value]
