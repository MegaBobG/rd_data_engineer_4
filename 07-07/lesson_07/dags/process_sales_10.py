import os
import json
import csv
from airflow import DAG
from datetime import datetime

from airflow.operators.python import PythonOperator

from airflow.models.variable import Variable
from ht_template.job1.bll.sales_api import save_sales_to_local_disk

AUTH_TOKEN = Variable.get(key='AUTH_TOKEN')
BASE_DIR = Variable.get(key='BASE_DIR')
RAW_DIR = os.path.join(BASE_DIR, "raw", "sales", "2022-08-09")

dag_path = os.getcwd()

BASE_DIR_2 = os.getcwd()
RAW_DIR_2 = os.path.join(BASE_DIR_2, "processed_data", "raw", "sales", "2022-08-09")
json_file_path = os.path.join(RAW_DIR_2, "sales_2022-08-09.json")

STG_DIR_2 = os.path.join(BASE_DIR_2, "processed_data", "stg", "sales", "2022-08-09")
csv_file_path = os.path.join(STG_DIR_2, "sales_2022-08-09.csv")

RAW_DIR_3 = os.path.join(BASE_DIR_2, "processed_data")
STG_DIR_3 = os.path.join(BASE_DIR_2, "raw_data")


def json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(data[0].keys())  # Записываем заголовки столбцов

        for row in data:
            writer.writerow(row.values())  # Записываем значения строк

    print("Конвертация завершена!")



dag = DAG(
    dag_id="process_sales_10",
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

extract_data_from_api_2 = PythonOperator(
    task_id="extract_data_from_api_2",
    python_callable=json_to_csv,
    op_kwargs={"json_file_path": json_file_path, "csv_file_path": csv_file_path},
    dag=dag
)

extract_data_from_api >> extract_data_from_api_2
