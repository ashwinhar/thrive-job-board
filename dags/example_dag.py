from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator

from job_boards.elemental import Elemental

from airflow.decorators import dag, task


elemental = Elemental()
pass
