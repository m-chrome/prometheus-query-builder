from dataclasses import dataclass


SUPPORTED_MATCH_OPERATORS = ("=", "!=", "=~", "!~")


@dataclass(frozen=True)
class Label:
    key: str
    value: str
    match_operator: str = "="

    def __str__(self) -> str:
        return self.key + self.match_operator + f'"{self.value}"'


class Query:
    def __init__(self, metric: str):
        self.metric = metric
        self.labels = set()

    def __str__(self) -> str:
        query = self.metric
        if self.labels:
            # sort labels just because
            query += "{" + ",".join(sorted(str(label) for label in self.labels)) + "}"
        return query

    def add_label(self, key: str, value: str, match_operator: str = "="):
        if match_operator not in SUPPORTED_MATCH_OPERATORS:
            raise ValueError("Wrong match operator")
        self.labels.add(Label(key, value, match_operator))
