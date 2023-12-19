"""
Tests methods from transaction.py. Specifically tests methods against the table "test". 

The following record is *guaranteed* to be in that table and is verified by the first test:

    id    |  company  |  position  |  location  
----------+-----------+------------+------------
 123ABC   | t_Company | t_Position | t_Location

If that test fails, results from the other tests are unreliable.
"""

import pytest
import psycopg2
import job_boards.transaction as t
from job_boards.job import Job

DBNAME = "thrive"
USER = "admin"
PASSWORD = "admin"


def test_check_test_record():
    """
    Ensures that only one record with id='123ABC' exists in table
    """
    with psycopg2.connect(f"dbname={DBNAME} user={USER} password={PASSWORD}") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM test WHERE id='123ABC'")
            num_records = cur.fetchall()[0][0]

            assert num_records == 1


def test_check_exists():
    """
    Ensures check exists method works correctly
    """
    assert t.check_exists('test', '123ABC') is True


def test_publish_to_database():
    """
    Ensures ability to write to the database. Dependent on test_check_exists()
    """
    job = Job(company="temp_comp", position="temp_pos", location="temp_loc")
    job.set_id()
    job_id = job.id

    t.publish_to_database('test', job.to_dict())

    if job_id is not None:
        assert t.check_exists('test', job_id)


def test_remove_from_database():
    """
    Ensures ability to delete record from a table. Dependent on test_check_exists()
    """
    job = Job(company="r_comp", position="r_pos", location="r_loc")
    job.set_id()
    job_id = job.id

    t.publish_to_database('test', job.to_dict())

    if job_id is not None and t.check_exists('test', job_id):
        t.remove_from_database('test', job_id)
        assert not t.check_exists('test', job_id)
    else:
        print("Temporary job record not published correctly")
        assert False


def test_no_duplication():
    """
    Tests that if a record already exists in the table, no duplicate is made even if requested
    """
    d_job = Job(company="t_Company", position="t_Position",
                location="l_Location")
    d_job.set_id()

    t.publish_to_database('test', d_job.to_dict())
    t.update_job_list('test', [d_job.to_dict()])

    with psycopg2.connect(f"dbname={DBNAME} user={USER} password={PASSWORD}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM test WHERE id='{d_job.id}'")
            assert cur.fetchall()[0][0] == 1


def test_record_not_exists():
    pass


def test_record_removed():
    pass
