"""Test job board functionality"""
from job_boards.elemental import Elemental


def main():
    """Driver function"""
    elemental = Elemental()
    elemental.save_webpage_html()

    html_response = elemental.get_html_from_file("20231208")
    jobs = elemental.get_jobs(html_response)

    print(jobs)


if __name__ == "__main__":
    main()
