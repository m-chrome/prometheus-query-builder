from typing import Optional, overload, Union, Mapping, Tuple, Set, Iterable, List

from attr import dataclass, ib, setters
from attr.validators import instance_of

from .label import *


def str_attr_setter(instance, attribute, new_value):
    attribute.validator(instance, attribute, new_value)
    return new_value


@dataclass(slots=True, on_setattr=str_attr_setter)
class Query:

    metric: str = ib(validator=instance_of(str))
    labels: Set[Label] = ib(factory=set, converter=set, on_setattr=setters.frozen)
    offset: Optional[str] = ib(validator=instance_of(str), default="")
    time_duration: Optional[str] = ib(validator=instance_of(str), default="")
    time_modifier: Optional[str] = ib(validator=instance_of(str), default="")
    func: Optional[str] = ib(validator=instance_of(str), default="")

    def __str__(self) -> str:
        query = self.metric
        if self.labels:
            # sort labels just because
            query += "{" + ",".join(sorted(str(label) for label in self.labels)) + "}"
        if self.time_duration:
            query += '[' + self.time_duration + ']'
        if self.offset:
            query += f" offset {self.offset}"
        if self.time_modifier:
            query += f" @ {self.time_modifier}"
        if self.func:
            query = f"{self.func}({query})"
        return query

    @overload
    def add_label(self, label: Label) -> None:
        ...

    @overload
    def add_label(self, label: str, value: str, match_operator: Optional[str] = None) -> None:
        ...

    def add_label(self, label: str, value: Optional[str] = None, match_operator: Optional[str] = None) -> None:
        if isinstance(label, Label):
            pass
        elif isinstance(label, str):
            label = Label(name=label, value=value, match_operator=match_operator or EQUAL)
        else:
            raise TypeError(f"Invalid type: {type(label)}")

        # replace old label value if exists
        self.labels.discard(label)
        self.labels.add(label)

    @overload
    def add_labels(self, labels: Union[List[Label], Set[Label], Tuple[Label]]):
        ...

    @overload
    def add_labels(self, labels: Mapping[str, Union[str, Tuple[str, str]]]):
        ...

    def add_labels(self, labels: Union[Iterable[Label], Mapping[str, Union[str, Tuple[str, str]]]]):
        if isinstance(labels, Mapping):
            for label, item in dict(labels).items():
                if isinstance(item, str):
                    self.add_label(label=label, value=item)
                else:
                    value, operator = item
                    self.add_label(label=label, value=value, match_operator=operator)
        elif isinstance(labels, Iterable):
            for label in labels:
                self.add_label(label=label)
        else:
            raise TypeError(f"Invalid type: {type(labels)}")

    def remove_label(self, name: str) -> None:
        for label in list(filter(lambda x: x.name == name, self.labels)):
            self.labels.remove(label)
