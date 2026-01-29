from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
from collections.abc import Sequence

__ALL__ = ['ButtonColor']

#todo implement protocol instead of abc
class BaseColor(Protocol):

    # @abstractmethod
    def make_color_scheme(self) -> dict:
        ...  # , primary: str, warning: str, danger: str, success: str
        """
        Args:

        Returns:
            (:dict)

        Raises:
            (:NotImplementedError)

        """
        # raise NotImplementedError


class ButtonColor(BaseColor):

    def __init__(self, primary: str, warning: str, danger: str, success: str):
        self.primary = primary
        self.warning = warning
        self.danger = danger
        self.success = success

    def make_color_scheme(self) -> dict:
        """ Implement a color scheme using CSS-style naming convention.

            primary (:obj:`str`):
                 Primary color, often blue
            warning (:obj:`str`):
                Color to indicate warning, often yellow
            danger (:obj:`str`):
                Color to indicate danger, often red
            success (:obj:`str`):
                Color to indicate success, often green

        Args:

        Returns:
            (:dict)

        Raises:
            (:type)

        """#primary: str, warning: str, danger: str, success: str

        return {'Primary': self.primary,
                'Warning': self.warning,
                'Danger': self.danger,
                'Success': self.success
                }

from typing import Protocol

@runtime_checkable
class Speaker(Protocol):
    def speak(self) -> str:
        ...

class Dog:
    def speak(self) -> str:
        return "Woof"

class Person:
    def speak(self) -> str:
        return "Hello"

from collections.abc import Sequence

class Dummy(Sequence):

    def __getitem__(self, item):
        ...


# j = Dummy()
#
# print(j[3])  # This will call __getitem__





