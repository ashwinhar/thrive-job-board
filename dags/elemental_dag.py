"""Basic DAG"""
from typing import List, Dict
import pendulum
from airflow.decorators import dag, task

import job_boards.transaction as t
from job_boards.job import Job
from job_boards.job_board import JobBoard
from job_boards.elemental import Elemental


@task()
def extract() -> List[Dict]:
    """
    Extract website HTML

    Creates new Elemental instance and extracts HTML. Originally jobs in the job_list
    are of type Job. XCom doesn't support sending messages with custom objects.
    Therefore, each Job is transformed into a Dict, and then transformed back into a 
    Job object at the source destination

    Returns:
        new_job_list (List[Dict]): List of jobs, in Dict representation
    """
    elemental = Elemental()

    html_response = elemental.get_html_from_file("20231208")
    job_list = elemental.extract_jobs(html_response)

    print([print(str(job)) for job in job_list])

    new_job_list = [job.to_dict() for job in job_list]
    return new_job_list


@task()
def transform(job_list: List[Dict]):
    """
    Clean jobs in job list
    """
    new_job_list = [Job.load_from_dict(job) for job in job_list]
    cleaned_list = JobBoard.clean_job_list(new_job_list)

    return [job.to_dict() for job in cleaned_list]


@task()
def load(job_list: List[Dict]):
    """
    In v0, simply prints all jobs to the command line
    """
    for job in job_list:
        t.publish_to_database("jobs", job)


@task()
def log_table_state(table: str):
    """
    Prints current table state to log file in /my_logs/
    """
    t.get_current_table_state(table)


@dag(
    schedule=None,
    start_date=pendulum.datetime(2019, 12, 13),
    catchup=False,
    tags=["Elemental ETL - Basic"],
)
def elemental_etl_basic():
    """
    This module performs a basic ETL for Elemental based on either a HTML file
    stored in the /data/ directory, or freshly scrapes the website listed in the
    self.website property. 
    """

    e_job_list = extract()

    t_job_list = transform(e_job_list)
    print(t_job_list)
    load(t_job_list)
    log_table_state("jobs")


elemental_etl_basic()
