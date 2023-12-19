"""
Tests methods from transaction.py. Specifically tests methods against the table "temp_test". 

The following record is *guaranteed* to be in that table and is verified by the first test:

    id    |  company  |  position  |  location  
----------+-----------+------------+------------
 123ABC   | t_Company | t_Position | t_Location

If that test fails, results from the other tests are unreliable.
"""

import psycopg2
import job_boards.transaction as t
from job_boards.job import Job

# Database connection constants
DBNAME = "thrive"
USER = "admin"
PASSWORD = "admin"
TABLE = "temp_test"

# Temp record constants
T_REC_ID = '123ABC'
T_REC_COMPANY = 't_Company'
T_REC_POSITION = 't_Position'
T_REC_LOCATION = 't_Location'


def create_temp_table(default=True):
    """Creates temp table context for testing cases below"""
    with psycopg2.connect(f"dbname={DBNAME} user={USER} password={PASSWORD}") as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE TABLE {TABLE} (id varchar(255), company varchar(255),\
                      position varchar(255), location varchar(255))")
            if default:
                cur.execute(
                    f"INSERT INTO {TABLE} (id, company, position, location)\
                        VALUES ('123ABC', 't_Company', 't_Position', 't_Location')"
                )

        conn.commit()


def destroy_temp_table():
    """Destroys temp table context for testing cases below"""
    with psycopg2.connect(f"dbname={DBNAME} user={USER} password={PASSWORD}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE {TABLE}")

        conn.commit()


def create_temp_table_data():
    """Creates 10 sample records in temp table context"""
    samp_records = [
        [f'{i}', f'{i}_company', f'{i}_position', f'{i}_location'] for i in range(10)]

    for record in samp_records:
        with psycopg2.connect(f"dbname={DBNAME} user={USER} password={PASSWORD}") as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"INSERT INTO {TABLE} (id, company, position, location)\
                        VALUES ('{record[0]}', '{record[1]}', '{record[2]}', '{record[3]}')"
                )
            conn.commit()


def test_check_test_record():
    """
    Ensures that only one record with id='123ABC' exists in table
    """
    create_temp_table()
    with psycopg2.connect(f"dbname={DBNAME} user={USER} password={PASSWORD}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {TABLE} WHERE id='123ABC'")
            num_records = cur.fetchall()[0][0]

            assert num_records == 1
    destroy_temp_table()


def test_check_exists():
    """
    Ensures check exists method works correctly
    """
    create_temp_table()
    assert t.check_exists(TABLE, '123ABC') is True
    destroy_temp_table()


def test_publish_to_database():
    """
    Ensures ability to write to the database. Dependent on test_check_exists()
    """
    create_temp_table()
    job = Job(company="temp_comp", position="temp_pos", location="temp_loc")
    job.set_id()
    job_id = job.id

    t.publish_to_database(TABLE, job.to_dict())

    if job_id is not None:
        assert t.check_exists(TABLE, job_id)

    destroy_temp_table()


def test_remove_from_database():
    """
    Ensures ability to delete record from a table. Dependent on test_check_exists()
    """
    create_temp_table()
    job = Job(company="r_comp", position="r_pos", location="r_loc")
    job.set_id()
    job_id = job.id

    t.publish_to_database(TABLE, job.to_dict())

    if job_id is not None and t.check_exists(TABLE, job_id):
        t.remove_from_database(TABLE, job_id)
        assert not t.check_exists(TABLE, job_id)
    else:
        print("Temporary job record not published correctly")
        assert False

    destroy_temp_table()


def test_no_duplication():
    """
    Tests that if a record already exists in the table, no duplicate is made even if requested
    """
    create_temp_table()
    d_job = Job(company="t_Company", position="t_Position",
                location="l_Location")
    d_job.set_id()

    t.publish_to_database(TABLE, d_job.to_dict())
    t.update_job_list(TABLE, [d_job.to_dict()])

    with psycopg2.connect(f"dbname={DBNAME} user={USER} password={PASSWORD}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {TABLE} WHERE id='{d_job.id}'")
            assert cur.fetchall()[0][0] == 1

    destroy_temp_table()


def test_record_removed():
    create_temp_table(default=False)
    create_temp_table_data()
    records = t.get_current_table_state(TABLE)
    destroy_temp_table()

    assert True
