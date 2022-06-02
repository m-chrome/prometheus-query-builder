from attr import dataclass, ib
from attr.validators import instance_of, in_

__all__ = (
    "EQUAL",
    "NOT_EQUAL",
    "REGEX_MATCH",
    "NOT_REGEX_MATCH",
    "SUPPORTED_MATCH_OPERATORS",
    "Label",
)

EQUAL = "="
NOT_EQUAL = "!="
REGEX_MATCH = "=~"
NOT_REGEX_MATCH = "!~"

SUPPORTED_MATCH_OPERATORS = (EQUAL, NOT_EQUAL, REGEX_MATCH, NOT_REGEX_MATCH)


@dataclass(slots=True, frozen=True)
class Label:
    name: str = ib(validator=instance_of(str))
    value: str = ib(validator=instance_of(str), eq=False)
    match_operator: str = ib(default=EQUAL, validator=in_(SUPPORTED_MATCH_OPERATORS), eq=False)

    def __str__(self) -> str:
        return f"{self.name}{self.match_operator}\"{self.value}\""
