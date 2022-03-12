from .label import SUPPORTED_MATCH_OPERATORS, Label


class Query:
    def __init__(self, metric: str):
        self.metric = metric
        self.labels = set()
        self.time_duration = ""
        self.time_modifiers = []

    def __str__(self) -> str:
        query = self.metric
        if self.labels:
            # sort labels just because
            query += "{" + ",".join(sorted(str(label) for label in self.labels)) + "}"
        if self.time_duration:
            query += '[' + self.time_duration + ']'
        for m in self.time_modifiers:
            query += f" {m}"
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

    def add_time_duration(self, duration: str):
        self.time_duration = duration

    def remove_time_duration(self):
        self.time_duration = ""

    def add_offset(self, value: str):
        self.time_modifiers.append(f"offset {value}")

    def add_at_modifier(self, value: str):
        self.time_modifiers.append(f"@ {value}")
