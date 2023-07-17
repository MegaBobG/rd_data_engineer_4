import os
import time
import requests
import json
# import fastavro
import pandas as pd
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
from airflow.models import Variable
from pathlib import Path

from ht_template.job1.bll.sales_api import save_sales_to_local_disk

AUTH_TOKEN = Variable.get(key='AUTH_TOKEN')
BASE_DIR = Variable.get(key='BASE_DIR')
RAW_DIR = os.path.join(BASE_DIR, "raw", "sales", "2022-08-09")

dag_path = os.getcwd()

BASE_DIR_2 = os.getcwd()
RAW_DIR_2 = os.path.join(BASE_DIR_2, "processed_data", "raw", "sales", "2022-08-09")
STG_DIR_2 = os.path.join(BASE_DIR_2, "processed_data", "stg", "sales", "2022-08-09")

dag = DAG(
    dag_id="process_sales_6",
    schedule=None,
    start_date=datetime.strptime("2023-07-12", "%Y-%m-%d"),
    tags=['lecture']
)


def transform_data_csv():
    sales = pd.read_csv(f"{dag_path}/raw_data/sales_2022-08-09.csv", low_memory=False)
    file_name = "SALES_2022-08-09"
    output_dir = Path(f'{dag_path}/processed_data')
    sales.to_csv(output_dir / f"{file_name}.csv", index=False)


transform_data = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data_csv,
    dag=dag
)
