from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'ashwinh',
    'retries': 2,
}

def greet():
    print('hello')

with DAG(
    default_args=default_args,
    dag_id='firstdag',
    description='loremipsum',
    start_date=datetime(2023,12,1),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet
    )