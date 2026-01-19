from abc import ABC, abstractmethod

__ALL__ = ['ButtonColor']

class BaseColor(ABC):

    @abstractmethod
    def color_scheme(self) -> dict:  # , primary: str, warning: str, danger: str, success: str
        """
        Args:

        Returns:
            (:dict)

        Raises:
            (:NotImplementedError)

        """
        raise NotImplementedError


class ButtonColor(BaseColor):

    def __init__(self, primary: str, warning: str, danger: str, success: str):
        self.primary = primary
        self.warning = warning
        self.danger = danger
        self.success = success

    def color_scheme(self) -> dict:
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