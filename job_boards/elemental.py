"""Instance of Job Board class for Elemental Excelerator"""

from bs4 import BeautifulSoup
from airflow.decorators import task
from .job_board import JobBoard


class Elemental(JobBoard):
    """Implementation of class Elemental"""

    def __init__(self):
        pass

    @property
    def name(self) -> str:
        return 'Elemental'

    @name.setter
    def name(self, value):
        raise ValueError("Cannot change name of the JobBoard")

    @property
    def website(self) -> str:
        return 'https://jobs.elementalexcelerator.com/jobs'

    @website.setter
    def website(self, value):
        raise ValueError('Cannot change website of the JobBoard')

    def get_job_property(self, job: BeautifulSoup, attr: str) -> str:
        """
        Uses BeautifulSoup library to extract each relevant property for a job. Different flows 
        are necessary for different properties

        Inputs:
            job: A single job from a group of jobs stored in a BeautifulSoup.element.tag object
            property: The name of the property to be passed into the .find() method
        Return:
            property_value: Corresponding value for the target property as a string
        """

        if attr != 'title':
            try:
                search_job = job.find(itemprop=attr)
                property_value = search_job['content']  # type: ignore
            except TypeError:
                property_value = None
        else:
            try:
                property_value = job.find(
                    itemprop=attr).contents[0]  # type: ignore
            except TypeError:
                property_value = None

        return property_value  # type: ignore

    @task
    def extract_jobs(self, response: BeautifulSoup) -> list[dict]:
        """
        Extract company name and title for each job listed on the Elemental webpage

        Inputs:
            response: BeautifulSoup object that has webpage content
        Returns:
            database: List of dicts, each entry is a different job
        """

        # It's unclear if this class name is actually constant, it might be some kind UID based on
        # date or version. Worth investigating and updating to make this more stable

        jobs = response.find_all(
            'div', attrs={"class", "sc-beqWaB gupdsY job-card"})

        database = []

        for job in jobs:
            job_info = {
                'company': self.get_job_property(job, 'name'),
                'location': self.get_job_property(job, 'address'),
                'position': self.get_job_property(job, 'title')
            }

            database.append(job_info)

        return database
