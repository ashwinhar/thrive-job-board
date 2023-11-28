"""
Scrapes target webpages for jobs
"""

import requests
from bs4 import BeautifulSoup


def save_webpage_html(response: BeautifulSoup, website_name: str) -> None:
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

def get_jobs(response: BeautifulSoup) -> None:
    """
    Extract company name and title for each job listed on the Elemental webpage

    Inputs:
        response: BeautifulSoup object that has webpage content
    Outputs:
        jobs: Dictionary that contains jobs and target attributes
    Returns:
        None
    """
    jobs_html = response.find_all(attrs={"data-testid","job-list-item"})

    for job in jobs_html:
        print(job)

def main():
    """
    Main driver
    """
    r = requests.get('https://jobs.elementalexcelerator.com/jobs', timeout=3)
    webpage_content = BeautifulSoup(r.content, 'html.parser')
    save_webpage_html(webpage_content, 'elemental')


if __name__ == "__main__":
    main()
