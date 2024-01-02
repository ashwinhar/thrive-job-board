"""Test job board functionality"""

from job_boards.elemental import Elemental
from job_boards.job_board import JobBoard
from job_boards.job import Job


def main():
    job = Job('test', 'test', 'test')
    dict_repr = job.to_dict()

    new_job = Job.load_from_dict(dict_repr)
    print(str(new_job))
    """Driver function"""
    elemental = Elemental()

    # Extract
    html_response = elemental.get_html_from_file("20231208")
    job_list = elemental.extract_jobs(html_response)

    # Transform
    cleaned = JobBoard.clean_job_list(job_list)

    # Load
    for job in cleaned:
        print(str(job))


if __name__ == "__main__":
    main()
