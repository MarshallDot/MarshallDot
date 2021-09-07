from dataclasses import dataclass
import typing


@dataclass
class Basic:
    data: typing.Union[bool, str, int, float]
