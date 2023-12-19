"""Defines class Job"""
from __future__ import annotations
import inspect
import hashlib
from typing import Dict


class Job():
    """
    Each job to be input into the final output job board on the Thrive website is first
    created as an instance of class Job. 
    """

    ### Magic Functions ###

    def __init__(self, company=None, position=None, location=None):
        self._id = None
        self._company = company
        self._position = position
        self._location = location

    def __str__(self):
        return f"Job(id: {self.id}, company: {self.company}, position: {self.position}, location: {self.location})"

    ### Properties ###

    @property
    def id(self):
        """
        returns self._id
        """
        return self._id

    @property
    def company(self):
        """
        Returns self._company.
        """
        return self._company

    @company.setter
    def company(self, company: str) -> None:
        """
        Set self._company
        """
        if not isinstance(company, str) and company is not None:
            raise TypeError("Company must be a string or None")
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
        if not isinstance(position, str) and position is not None:
            raise TypeError("Position must be a string or None")
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
        if not isinstance(location, str) and location is not None:
            raise TypeError("Location must be a string or None")
        self._location = location

    ### Functions ###
    def set_id(self) -> None:
        """
        Set self._id property

        Special setter to set the id property. ID is a hexadecimal hash, and should only be set 
        when all relevant properties have been defined. Currently, the hash is only dependent on
        the company, position, and location properties. Hashing is done using the SHA256 algorithm. 
        The hexadecimal output is artificially truncated to 8 chars. 
        """

        hash_string = f"{self.company}_{self.position}_{self.location}"
        input_bytes = hash_string.encode()
        hasher = hashlib.sha256()
        hasher.update(input_bytes)

        self._id = hasher.hexdigest()[:8]

    def to_dict(self) -> Dict:
        """
        Converts Job instance into dict of attributes
        """

        return {key: value for key, value in self.__dict__.items()}

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

    ### Static Methods ###

    @staticmethod
    def load_from_dict(dict_repr: Dict) -> Job:
        """
        Return job instance from dict representation

        Parameters:
        dict_repr (Dict): The dict representation of a Job object, typically generated by the
                          Job.to_dict() method 

        Returns:
        Job: Job using the values of the dict_repr parameter as initializaiton
        """
        return Job(
            company=dict_repr.get('_company'),
            position=dict_repr.get('_position'),
            location=dict_repr.get('_location')
        )
