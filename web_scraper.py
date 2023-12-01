"""
Scrapes target webpages for jobs
"""

import requests
from bs4 import BeautifulSoup


def save_webpage_html(response: BeautifulSoup, website_name: str) -> str:
    """
    Given a response object, save html code to local directory

    Inputs:
        response: HTTP GET request response delivered by requests package, sourced from main method
    Outputs:
        file: File saved to local directory titled f"{website_name}.html"

    TODO: Update docstring
    """

    webpage_html = response.prettify()

    with open(f'{website_name}.html', 'w', encoding='utf8') as html_file:
        html_file.write(webpage_html)

    return webpage_html


def extract_job_property(job: BeautifulSoup, attr: str) -> str:
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
            property_value = job.find(itemprop=attr)['content']
        except TypeError:
            property_value = None
    else:
        try:
            property_value = job.find(
                itemprop=attr).contents[0].replace('\n', '').strip()
        except TypeError:
            property_value = None

    return property_value


def get_jobs(response: BeautifulSoup) -> list[dict]:
    """
    Extract company name and title for each job listed on the Elemental webpage

    Inputs:
        response: BeautifulSoup object that has webpage content
    Returns:
        database: List of dicts, each entry is a different job
    """

    # It's unclear if this class name is actually constant, it might be some kind UID based on date
    # or version. Worth investigating and updating to make this more stable

    jobs = response.find_all(
        'div', attrs={"class", "sc-beqWaB gupdsY job-card"})

    database = []

    for job in jobs:
        job_info = {
            'company': extract_job_property(job, 'name'),
            'location': extract_job_property(job, 'address'),
            'position': extract_job_property(job, 'title')
        }

        database.append(job_info)

    return database


def new_execution() -> BeautifulSoup:
    """
    Used by main method when we want to get the new HTML from a website
    """
    r = requests.get('https://jobs.elementalexcelerator.com/jobs', timeout=3)
    webpage_content = BeautifulSoup(r.content, 'html.parser')

    return webpage_content


def testing(opts: dict) -> BeautifulSoup:
    """
    Used by main method when we want to test an existing HTML file or generate a new one and test
    """
    if opts['new_file'] == 'Y':
        r = requests.get(
            'https://jobs.elementalexcelerator.com/jobs', timeout=3)
        soup = save_webpage_html(r, 'elemental')

    with open(f'{opts["file_name"]}.html', encoding='utf-8') as wp:
        soup = BeautifulSoup(wp, 'html.parser')

    return soup


def main():
    """
    Main driver
    """
    opts = {
        'new_file': 'N',
        'file_name': 'elemental'
    }

    # webpage_content = new_execution()
    webpage_content = testing(opts)
    jobs = get_jobs(webpage_content)

    print(jobs)


if __name__ == "__main__":
    main()
