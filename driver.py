"""Test job board functionality"""

from job_boards.elemental import Elemental


def main():
    """Driver function"""
    elemental = Elemental()

    # Extract
    elemental.save_webpage_html()
    html_response = elemental.get_html_from_file("20231208")
    elemental.job_list = elemental.extract_jobs(html_response)

    # Transform
    elemental.clean_job_list()

    # Load
    print(elemental.job_list)


if __name__ == "__main__":
    main()
