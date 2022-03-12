class Query:
    def __init__(self, metric: str):
        self.metric = metric

    def __str__(self) -> str:
        return self.metric
