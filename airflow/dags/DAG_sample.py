# Imports - Standard
import os
from datetime import datetime, timedelta

# Imports - Third-party
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


# Constants
AIRFLOW_USER_NAME = os.getenv('_AIRFLOW_WWW_USER_USERNAME')
AIRFLOW_USER_EMAIL = os.getenv('_AIRFLOW_WWW_USER_EMAIL')

# Define default arguments
default_args = {
    'owner': AIRFLOW_USER_NAME,
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': [AIRFLOW_USER_EMAIL],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'example_dag',
    default_args=default_args,
    description='A simple example DAG',
    tags=['example'],
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Define tasks
def print_hello():
    return 'Hello from first task! This is a sample DAG!!!'

hello_task = PythonOperator(
    task_id='hello_task',
    python_callable=print_hello,
    dag=dag
)

bash_task = BashOperator(
    task_id='bash_task',
    bash_command='echo "Hello from second task!"',
    dag=dag
)

# Set task dependencies
hello_task >> bash_task
