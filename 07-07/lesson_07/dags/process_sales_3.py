import os
import time
import requests
import json
import fastavro
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
from ht_template.job2.bll.transfer_api import transfer_from_raw_to_stg

AUTH_TOKEN = Variable.get(key='AUTH_TOKEN')
BASE_DIR = Variable.get(key='BASE_DIR')
RAW_DIR = os.path.join(BASE_DIR, "raw", "sales", "2022-08-09")
STG_DIR = os.path.join(BASE_DIR, "stg", "sales", "2022-08-09")

dag_path = os.getcwd()
RAW_DIR_2 = os.path.join(dag_path, "raw", "sales", "2022-08-09")
STG_DIR_2 = os.path.join(dag_path, "stg", "sales", "2022-08-09")

dag = DAG(
    dag_id="process_sales_3",
    schedule=None,
    start_date=datetime.strptime("2023-07-11", "%Y-%m-%d"),
    tags=['lecture']
)

extract_data_from_api = PythonOperator(
    task_id="extract_data_from_api",
    python_callable=save_sales_to_local_disk,
    op_kwargs={"date": "2022-08-09", "raw_dir": RAW_DIR},
    dag=dag
)

# convert_to_avro = PythonOperator(
#     task_id="convert_to_avro",
#     python_callable=transfer_from_raw_to_stg,
#     op_kwargs={"raw_dir": RAW_DIR_2, "stg_dir:": STG_DIR},
#     dag=dag
# )
#
# extract_data_from_api >> convert_to_avro

convert_to_avro = BashOperator(
    task_id="convert_to_avro",
    bash_command='echo "Давай дасвидания"',
    dag=dag
)

extract_data_from_api >> convert_to_avro
