"""This module implements the abstract class JobBoard"""
from abc import ABC, abstractmethod
from datetime import datetime

import os
import requests
from bs4 import BeautifulSoup


class JobBoard(ABC):
    """
    Abstract class that each job board class will inherit. Includes global functionality using 
    BeautifulSoup to extract and parse through website data, and abstract properties/methods 
    that each class must implement
    """

    def __init__(self):
        pass

    # Property Definitions

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Abstract property for the name of the job board website

        Examples:
        - 'Elemental Excelerator'
        """

    @property
    @abstractmethod
    def website(self) -> str:
        """
        Abstract property for the URL targeted by the web scraper

        Examples:
        - 'https://jobs.elementalexcelerator.com/jobs'
        """

    # Abstract Method Definitions

    @abstractmethod
    def get_jobs() -> list[dict]:
        """Returns jobs defined in a certain structure"""

    # Concrete Method Definitions

    def get_website_data(self) -> BeautifulSoup:
        """Extract website HTML using BeautifulSoup and self.website property"""

        r = requests.get(self.website, timeout=3)

        return r.prettify()

    def name_to_snake(self) -> str:
        """Returns JobBoard property self.name in snake case"""

        return self.name.lower().replace(' ', '_')

    def save_webpage_html(self) -> None:
        """Save HTML to a file within a folder for each job board"""

        webpage_html = self.get_website_data()

        # Each job board should have its own directory within the "data" directory
        if not os.path.exists(f'/data/{self.name_to_snake()}/'):
            os.mkdir(f'/data/{self.name_to_snake()}/')

        with open(f'{self.name_to_snake()}_{datetime.now().strftime("%Y%m%d")}.html', 'w', encoding='utf8') as html_file:
            html_file.write(webpage_html)

    def get_html_from_file(self, date: str) -> BeautifulSoup:
        """
        Given a date, return BeautifulSoup object

        Parameters:
        date (str): Date as string in format "%Y%m%d"

        Examples:
        Elemental.get_html_from_file("20231201")
        """

        with open(f'/data/{self.name_to_snake()}/{self.name_to_snake()}_{date}.html', encoding='utf-8') as wp:
            soup = BeautifulSoup(wp, 'html.parser')

        return soup

