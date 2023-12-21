### Helper functions, variables for test files###

import psycopg2

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
