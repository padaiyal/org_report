from abc import ABC, abstractmethod


class Report(ABC):
    def __init__(self, name: str, skip_archived: bool) -> None:
        self.name = name
        self.skip_archived = skip_archived

    # noinspection PyMethodMayBeStatic
    def get_boolean_representation(self, value) -> str:
        if value == '🤷‍':
            return value
        if value == 'None' or not bool(value):
            return '❌'
        return '✅'

    @abstractmethod
    def generate_report(self) -> None:
        pass
