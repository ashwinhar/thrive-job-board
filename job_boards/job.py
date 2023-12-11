"""Defines class Job"""
import inspect


class Job():
    """
    Each job to be input into the final output job board on the Thrive website is first
    created as an instance of class Job. 
    """

    def __init__(self, company=None, position=None, location=None):
        self._company = company
        self._position = position
        self._location = location

    @property
    def company(self):
        """
        Returns self.company.
        """
        return self._company

    @company.setter
    def company(self, company: str) -> None:
        """
        Set self.company
        """
        if not isinstance(company, str):
            raise TypeError("Company must be a string")
        self._company = company

    @property
    def position(self):
        """
        Returns self.position.
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Set self.position
        """
        if not isinstance(position, str):
            raise TypeError("Position must be a string")
        self._position = position

    @property
    def location(self):
        """
        Returns self.location.
        """
        return self._location

    @location.setter
    def location(self, location):
        """
        Set self.location
        """
        if not isinstance(location, str):
            raise TypeError("Position must be a string")
        self._location = location

    def clean_strings(self) -> None:
        """
        Takes all string properties and cleans them:
        - Trims whitespace
        - Removes characters like "\n"
        """

        for name, prop in inspect.getmembers(self.__class__,
                                             lambda member: isinstance(member, property)):
            current_value = getattr(self, name)

            if isinstance(current_value, str):
                setattr(self, name, current_value.strip().replace('\n', ''))
