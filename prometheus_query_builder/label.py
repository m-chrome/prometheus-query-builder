from dataclasses import dataclass


EQUAL = "="
NOT_EQUAL = "!="
REGEX_MATCH = "=~"
NOT_REGEX_MATCH = "!~"

SUPPORTED_MATCH_OPERATORS = (EQUAL, NOT_EQUAL, REGEX_MATCH, NOT_REGEX_MATCH)


@dataclass(frozen=True)
class Label:
    name: str
    value: str
    match_operator: str = "="

    def __str__(self) -> str:
        return self.name + self.match_operator + f'"{self.value}"'
