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
import tests.helpers as h


def test_check_test_record():
    """
    Ensures that only one record with id='123ABC' exists in table
    """
    h.create_temp_table()
    with psycopg2.connect(f"dbname={h.DBNAME} user={h.USER} password={h.PASSWORD}") as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {h.TABLE} WHERE id='123ABC'")
            num_records = cur.fetchall()[0][0]

            assert num_records == 1
    h.destroy_temp_table()


def test_check_exists():
    """
    Ensures check exists method works correctly
    """
    h.create_temp_table()
    assert t.check_exists(h.TABLE, '123ABC') is True
    h.destroy_temp_table()


def test_publish_to_database():
    """
    Ensures ability to write to the database. Dependent on test_check_exists()
    """
    h.create_temp_table()
    job = Job(company="temp_comp", position="temp_pos", location="temp_loc")
    job.set_id()
    job_id = job.id

    t.publish_to_database(h.TABLE, job.to_dict())

    if job_id is not None:
        assert t.check_exists(h.TABLE, job_id)

    h.destroy_temp_table()


def test_remove_from_database():
    """
    Ensures ability to delete record from a table. Dependent on test_check_exists()
    """
    h.create_temp_table()
    job = Job(company="r_comp", position="r_pos", location="r_loc")
    job.set_id()
    job_id = job.id

    t.publish_to_database(h.TABLE, job.to_dict())

    if job_id is not None and t.check_exists(h.TABLE, job_id):
        t.remove_from_database(h.TABLE, job_id)
        assert not t.check_exists(h.TABLE, job_id)
    else:
        print("Temporary job record not published correctly")
        assert False

    h.destroy_temp_table()


def test_no_duplication():
    """
    Tests that if a record already exists in the table, no duplicate is made even if requested
    """
    h.create_temp_table()
    d_job = Job(company="t_Company", position="t_Position",
                location="l_Location")
    d_job.set_id()

    t.publish_to_database(h.TABLE, d_job.to_dict())
    t.update_job_list(h.TABLE, [d_job.to_dict()])

    with psycopg2.connect(f"dbname={h.DBNAME} user={h.USER} password={h.PASSWORD}") as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT COUNT(*) FROM {h.TABLE} WHERE id='{d_job.id}'")
            assert cur.fetchall()[0][0] == 1

    h.destroy_temp_table()


def test_handler():
    """
    Tests if instructions are created correctly to update a table state
    """
    h.create_temp_table(default=False)
    h.create_temp_table_data()
    samp_table_state = t.get_current_table_state(h.TABLE)

    samp_web_extract = [
        {'_id': f'{i}',
         '_company': f'{i}_company',
         '_position': f'{i}_position',
         '_location': f'{i}_location'
         } for i in range(12) if i % 2 == 0]

    samp_web_extract.append({'_id': '3', '_company': '3_company', '_position': '3_position',
                             '_location': '3_location'
                             })

    instructions = t.handler(samp_table_state, samp_web_extract)

    h.destroy_temp_table()

    check_instructions = [
        {'_id': '1', 'instruction': 'R'},
        {'_id': '5', 'instruction': 'R'},
        {'_id': '7', 'instruction': 'R'},
        {'_id': '9', 'instruction': 'R'},
        {'_id': '10', 'instruction': 'C'},
    ]

    assert instructions == check_instructions
