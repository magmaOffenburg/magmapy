from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Union, overload

if TYPE_CHECKING:
    from collections.abc import Iterator

from magmapy.common.communication.parser import ParserError


class MalformedSExpressionError(ParserError):
    """
    Error class representing a malformed symbolic expression / tree.
    """

    def __init__(self) -> None:
        """
        Construct a new malformed symbolic expression parser error.
        """

        super().__init__('Node not closed!')


class SExpression(Sequence[Union[str, 'SExpression']]):
    """
    Representation of a symbolic expression.
    """

    def __init__(self) -> None:
        """
        Construct a new symbolic expression.
        """

        super().__init__()

        self._list: list[str | SExpression] = []

    def append_value(self, v: str) -> str:
        self._list.append(v)
        return v

    def append_node(self) -> SExpression:
        node = SExpression()
        self._list.append(node)
        return node

    def __iter__(self) -> Iterator[str | SExpression]:
        return self._list.__iter__()

    @overload
    def __getitem__(self, i: int) -> str | SExpression: ...
    @overload
    def __getitem__(self, s: slice[Any, Any, Any]) -> Sequence[str | SExpression]: ...
    def __getitem__(self, i: int | slice[Any, Any, Any]) -> str | SExpression | Sequence[str | SExpression]:
        return self._list[i]

    def __len__(self) -> int:
        return len(self._list)

    def __str__(self) -> str:
        return str(self._list)


class SExpParser:
    """
    Simple S-Expression parser.
    """

    def __init__(self) -> None:
        """
        Construct a new parser.
        """

    def parse(self, data: str) -> SExpression:
        """
        Parse the given expression string into an symbolic expression.
        """

        node = SExpression()

        SExpParser._parse(node, data)

        return node

    @staticmethod
    def _parse(node: SExpression, data: str, start_idx: int = 0) -> int:
        """
        Internal recursive parser implementation.
        """

        idx: int = start_idx
        data_len = len(data)

        while idx < data_len:
            if data[idx] == '(':
                # found a new sub expression
                if idx > start_idx:
                    node.append_value(data[start_idx:idx])

                start_idx = idx = SExpParser._parse(node.append_node(), data, idx + 1)
            elif data[idx] == ')':
                # found node terminator for the current expression
                if idx > start_idx:
                    node.append_value(data[start_idx:idx])

                return idx + 1
            elif data[idx] == ' ':
                # found value terminator
                if idx > start_idx:
                    node.append_value(data[start_idx:idx])

                idx += 1
                start_idx = idx
            else:
                idx += 1

        if idx == data_len:
            if idx > start_idx:
                node.append_value(data[start_idx:])

            return idx + 1

        raise MalformedSExpressionError
