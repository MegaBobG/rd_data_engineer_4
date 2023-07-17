import os
import time
import requests
import json
from typing import Iterable
from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.hooks.http import HttpHook
from airflow.operators.branch import BaseBranchOperator
from airflow.utils.context import Context
from airflow.operators.empty import EmptyOperator
from airflow.models.variable import Variable
from ht_template.job1.bll.sales_api import save_sales_to_local_disk


AUTH_TOKEN = Variable.get(key='AUTH_TOKEN')
BASE_DIR = Variable.get(key='BASE_DIR')
RAW_DIR = os.path.join(BASE_DIR, "raw", "sales", "2022-08-09")

dag_path = os.getcwd()

BASE_DIR_2 = os.getcwd()
RAW_DIR_2 = os.path.join(BASE_DIR_2, "processed_data", "raw", "sales", "2022-08-09")
STG_DIR_2 = os.path.join(BASE_DIR_2, "processed_data", "stg", "sales", "2022-08-09")

# input_dir = Path(f'{dag_path}/processed_data/raw/sales/2022-08-09')
# output_dir = Path(f'{dag_path}/processed_data/stg/sales/2022-08-09')

dag = DAG(
    dag_id="process_sales_2",
    schedule=None,
    start_date=datetime.strptime("2023-07-10", "%Y-%m-%d"),
    tags=['lecture']
)

extract_data_from_api = PythonOperator(
    task_id="extract_data_from_api",
    python_callable=save_sales_to_local_disk,
    op_kwargs={"date": "2022-08-09", "raw_dir": RAW_DIR_2},
    dag=dag
)

convert_to_avro = BashOperator(
    task_id="convert_to_avro",
    bash_command='echo "Давай дасвидания"',
    dag=dag
)

extract_data_from_api >> convert_to_avro
