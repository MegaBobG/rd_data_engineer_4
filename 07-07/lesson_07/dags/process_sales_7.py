import os
import time
import requests
import json
import pandas as pd
import fastavro
from pathlib import Path
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
# from ht_template.job2.bll.transfer_api import transfer_from_raw_to_stg

AUTH_TOKEN = Variable.get(key='AUTH_TOKEN')
BASE_DIR = Variable.get(key='BASE_DIR')
RAW_DIR = os.path.join(BASE_DIR, "raw", "sales", "2022-08-09")
STG_DIR = os.path.join(BASE_DIR, "stg", "sales", "2022-08-09")

dag_path = os.getcwd()

BASE_DIR_2 = os.getcwd()
RAW_DIR_2 = os.path.join(BASE_DIR_2, "processed_data", "raw", "sales", "2022-08-09")
STG_DIR_2 = os.path.join(BASE_DIR_2, "processed_data", "stg", "sales", "2022-08-09")

input_dir = Path(f'{dag_path}/processed_data/raw/sales/2022-08-09')
output_dir = Path(f'{dag_path}/processed_data/stg/sales/2022-08-09')

# def transform_data_csv():
#     sales = pd.read_csv(f"{dag_path}/raw_data/sales_2022-08-09.csv", low_memory=False)
#     file_name = "SALES_2022-08-09"
#     output_dir = Path(f'{dag_path}/processed_data')
#     sales.to_csv(output_dir / f"{file_name}.csv", index=False)


# def convert_json_to_avro(json_file_path, avro_file_path, schema):
#     # Загрузка данных из файла JSON
#     with open(json_file_path, 'r') as json_file:
#         data = json.load(json_file)
#
#     # Создание файла Avro и запись данных в него
#     with open(avro_file_path, 'wb') as avro_file:
#         fastavro.writer(avro_file, schema, data)


dag = DAG(
    dag_id="process_sales_7",
    schedule=None,
    start_date=datetime.strptime("2023-07-12", "%Y-%m-%d"),
    tags=['lecture']
)

extract_data_from_api = PythonOperator(
    task_id="extract_data_from_api",
    python_callable=save_sales_to_local_disk,
    op_kwargs={"date": "2022-08-09", "raw_dir": RAW_DIR_2},
    dag=dag
)

# AVRO_SCHEMA = {
#     'name': 'Sales',
#     'type': 'record',
#     'fields': [
#         {'name': 'client', 'type': 'string'},
#         {'name': 'purchase_date', 'type': 'string'},
#         {'name': 'product', 'type': 'string'},
#         {'name': 'price', 'type': 'int'}
#     ]
# }
#
# convert_to_avro = PythonOperator(
#     task_id="convert_to_avro",
#     python_callable=convert_json_to_avro,
#     op_kwargs={"json_file_path": os.path.join(input_dir, "2022-08-09.json"),
#                "avro_file_path": os.path.join(output_dir, "2022-08-09.avro"), "schema": AVRO_SCHEMA},
#     dag=dag
# )

# extract_data_from_api
# convert_to_avro
