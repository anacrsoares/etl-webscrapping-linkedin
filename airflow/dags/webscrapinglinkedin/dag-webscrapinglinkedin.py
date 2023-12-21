# Airflow imports
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

with DAG("scraping-jobs", # Dag id
  start_date=datetime(2023, 1 ,1), # start date, the 1st of January 2023 
  schedule='@daily', # Cron expression, here @daily means once every day.
  catchup=False
) as dag:
    
    # This operator does nothing. 
    start_task = EmptyOperator(
        task_id='starting-task', # The name of the sub-task in the workflow.
        dag=dag # When using the "with Dag(...)" syntax you could leave this out
    )


    t1 = BashOperator(
        task_id='testairflow',
        bash_command='python /opt/airflow/dags/webscrapinglinkedin/crawler.py',
        dag=dag)
    
    # t2 = BashOperator(
    # task_id='testairflow',
    # bash_command='python /opt/airflow/dags/apps/.py',
    # dag=dag)
    
    start_task >> t1