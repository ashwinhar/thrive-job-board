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

    At the moment, this method does not include error checking of any kind, and does not look for 
    duplicate records. 

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


def get_current_table_state(table: str, log=False) -> List[dict]:
    """
    Write current table state to timestamped log file

    Parameters:
        dbname (str): Database name for PostgreSQL database connection via psycopg2
        user (str): Username for PostgreSQL database connection via psycopg2
        password (str): Password for PostgreSQL database connection via psycopg2
    Returns
        records (list): List of current records in target table
        TODO untested 
    """

    target_dir = "./my_logs/"
    records = None

    with psycopg2.connect(f"dbname={DBNAME} user={USER} password={PASSWORD}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"select id, company, position, location from {table}")
            records = cur.fetchall()

    if log:
        with open(f'{target_dir}{table}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt',
                  'w', encoding='utf8') as file:
            # Each job board should have its own directory within the "data" directory
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
            for record in records:
                file.write(str(record))
                file.write('\n')

    return [{
        '_id': record[0],
        '_company': record[1],
        '_position': record[2],
        '_location': record[3]
    } for record in records
    ]


def handler_helper(records: List[dict]) -> dict:
    """
    Convert list of dicts into dict of dicts
    """
    edited = {}
    for record in records:
        edited[record.get('_id')] = {
            '_id': record.get('_id'),
            '_company': record.get('_company'),
            '_position': record.get('_position'),
            '_location': record.get('_location')
        }
    return edited


def handler(table_state: List[dict], web_extract: List[dict]) -> List:
    """
    Creates instruction set for changing table state

    Takes in the table_state and web_extract, to update the state in the database. First, it looks 
    for cases where a job id exists in the table_state but does NOT exist in the web_extract. In 
    these cases, the record should be deleted from the table. 
    """
    instructions = []
    web_extract_dict = handler_helper(web_extract)

    for entry in table_state:
        # A job exists in the table but it no longer appears on the website
        if entry.get('_id') not in web_extract_dict:
            instructions.append({'_id': entry.get('_id'), 'instruction': 'R'})
        else:
            del web_extract_dict[entry.get('_id')]

    # Create records that do not currently exist
    for key, value in web_extract_dict.items():
        instructions.append({'_id': key, 'instruction': 'P'})

    return instructions
