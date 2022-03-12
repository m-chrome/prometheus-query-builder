from .label import SUPPORTED_MATCH_OPERATORS, Label


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

    def add_label(self, name: str, value: str, match_operator: str = "="):
        if match_operator not in SUPPORTED_MATCH_OPERATORS:
            raise ValueError("Wrong match operator")

        # replace old label value if exists
        self.remove_label(name)

        self.labels.add(Label(name, value, match_operator))

    def remove_label(self, name: str):
        for label in list(filter(lambda x: x.name == name, self.labels)):
            self.labels.remove(label)
