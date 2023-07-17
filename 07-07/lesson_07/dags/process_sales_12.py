import os
import json
import csv
import fastavro
import requests
from airflow import DAG
from datetime import datetime

from airflow.operators.python import PythonOperator

from airflow.models.variable import Variable
from ht_template.job1.bll.sales_api import save_sales_to_local_disk
from ht_template.job2.bll.transfer_api import transfer_from_raw_to_stg

AUTH_TOKEN = Variable.get(key='AUTH_TOKEN')
BASE_DIR = Variable.get(key='BASE_DIR')
RAW_DIR = os.path.join(BASE_DIR, "raw", "sales", "2022-08-09")

dag_path = os.getcwd()

BASE_DIR_2 = os.getcwd()
RAW_DIR_2 = os.path.join(BASE_DIR_2, "processed_data", "raw", "sales", "2022-08-09")
json_file_path = os.path.join(RAW_DIR_2, "sales_2022-08-09.json")

STG_DIR_2 = os.path.join(BASE_DIR_2, "processed_data", "stg", "sales", "2022-08-09")
csv_file_path = os.path.join(STG_DIR_2, "sales_2022-08-09.csv")
avro_file_path = os.path.join(STG_DIR_2, "sales_2022-08-09.avro")

RAW_DIR_3 = os.path.join(BASE_DIR_2, "processed_data")
STG_DIR_3 = os.path.join(BASE_DIR_2, "raw_data")


dag = DAG(
    dag_id="process_sales_12",
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

convert_to_avro = PythonOperator(
    task_id="convert_to_avro",
    python_callable=transfer_from_raw_to_stg,
    op_kwargs={"raw_dir": RAW_DIR_2, "stg_dir": STG_DIR_2},
    dag=dag
)

extract_data_from_api >> convert_to_avro
