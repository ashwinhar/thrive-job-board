"""Tests DAG"""
import json
from dags import elemental_dag


def extract_value_from_xcom(xcom_obj):
    if hasattr(xcom_obj, 'xcom_push') and callable(xcom_obj.xcom_push):
        return xcom_obj.xcom_push()
    else:
        return xcom_obj


# def test_extract():
#     """Ensures correct functioning of extract function"""
#     extract_xcom = elemental_dag.extract()
#     job_list = extract_value_from_xcom(extract_xcom)
#     print(job_list)

#     example_job_list = None
#     with open('tests/sample_jobs.json', 'r', encoding='utf-8') as file:
#         example_job_list = json.load(file)

#     assert all(example_job == job for example_job,
#                job in zip(example_job_list, job_list))
