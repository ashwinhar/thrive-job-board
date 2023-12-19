"""Defines PostgreSQL database interaction methods"""

from datetime import datetime
from typing import List
import os
import psycopg2

DBNAME = "thrive"
USER = "admin"
PASSWORD = "admin"


def check_exists(table: str, identity) -> bool:
    """
    Check if a particular job record already exists in the target table.

    Does not guarantee uniqueness. Table is designed for "id" to be the primary key, but this
    method will work irrespective of whether or not the particular id value passed is repeated.

    Parameters
        table (str): Search for record within this table in the database
        identity (str, None): Id of record to search for. Id is primary key in the table  
    """
    with psycopg2.connect(f"dbname={DBNAME} user={USER} password={PASSWORD}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {table} WHERE id='{identity}'")
            return cur.fetchall()[0][0] > 0


def update_job_list(table: str, job_list: List[dict]):
    """
    Update table with new list of jobs

    This is a driver function that handles the logic of updating a job list. The following cases
    are captured: 
        1. A record already exists in the table -> Table is unchanged [in dev]
        2. A record doesn't exist in the table -> Add record to table [in dev]
        3. A record has been removed from orig. job board -> Record is removed from table [in dev]

    Parameters:
        table (str): Target table to update
        job_list (List[dict]): List of jobs in dict representation 
    """

    for job in job_list:
        if not check_exists(table, job.get('_id')):
            publish_to_database(table, job)


def publish_to_database(table: str, job: dict) -> None:
    """
    Publish a single job to PostgreSQL database

    At the moment, this method does not include error checking of any kind, and does not look
    for duplicate records. 

    Parameters:
        table (str): Target table for publishing
        job (str): Job to be published
    """
    with psycopg2.connect(f"dbname={DBNAME} user={USER} password={PASSWORD}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO {table} (Id, Company, Position, Location) VALUES \
                        ('{job.get('_id')}','{job.get('_company')}', '{job.get('_position')}', \
                         '{job.get('_location')}')")
        conn.commit()


def remove_from_database(table: str, identity: str) -> None:
    """
    Remove record from target table in database

    Parameters:
        table (str): Target table for publishing
        job (str): Job to be published
    """
    with psycopg2.connect(f"dbname={DBNAME} user={USER} password={PASSWORD}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM {table} where id='{identity}'")
        conn.commit()


def get_current_table_state(table: str) -> None:
    """
    Write current table state to timestamped log file

    Parameters:
        dbname (str): Database name for PostgreSQL database connection via psycopg2
        user (str): Username for PostgreSQL database connection via psycopg2
        password (str): Password for PostgreSQL database connection via psycopg2
    """

    target_dir = "./my_logs/"

    # Each job board should have its own directory within the "data" directory
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    conn = psycopg2.connect(
        f"dbname={DBNAME} user={USER} password={PASSWORD}")
    with conn.cursor() as cur:
        cur.execute("select * from jobs")
        rows = cur.fetchall()

        with open(f'{target_dir}{table}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt',
                  'w', encoding='utf8') as file:

            for row in rows:
                file.write(str(row))
                file.write('\n')
