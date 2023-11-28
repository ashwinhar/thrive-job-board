import requests
from bs4 import BeautifulSoup


def save_webpage_html(response: requests.models.Response, website_name: str) -> None:
    """
    Given a response object, save html code to local directory

    Inputs:
        response: HTTP GET request response delivered by requests package, sourced from main method
    Returns:
        None
    """

    webpage_content = BeautifulSoup(response.content, 'html.parser')
    webpage_html = webpage_content.prettify()

    with open(f'{website_name}.html', 'w', encoding='utf8') as html_file:
        html_file.write(webpage_html)


def main():
    """
    Main driver
    """
    r = requests.get('https://jobs.elementalexcelerator.com/jobs', timeout=3)
    save_webpage_html(r, 'elemental')


if __name__ == "__main__":
    main()
