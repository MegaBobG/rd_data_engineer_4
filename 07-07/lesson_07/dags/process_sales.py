import os
import pandas as pd
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.models.variable import Variable
from ht_template.job1.bll.sales_api import save_sales_to_local_disk
from ht_template.job2.bll.transfer_api import transfer_from_raw_to_stg

AUTH_TOKEN = Variable.get(key='AUTH_TOKEN')
BASE_DIR = Variable.get(key='BASE_DIR')

start_date = pd.to_datetime("2022-08-09")
end_date = pd.to_datetime("2022-08-11")

BASE_DIR_2 = os.getcwd()
RAW_DIR_2 = os.path.join(BASE_DIR_2, "processed_data", "raw", "sales")
STG_DIR_2 = os.path.join(BASE_DIR_2, "processed_data", "stg", "sales")

dag = DAG(
    dag_id="process_sales",
    schedule_interval="0 1 * * *",
    start_date=datetime.strptime("2023-07-10", "%Y-%m-%d"),
    tags=["lecture"],
    max_active_runs=1,
    catchup=True
)

date_range = pd.date_range(start=start_date, end=end_date)
date_str_list = date_range.strftime("%Y-%m-%d").tolist()

def extract_data_from_api_task(*date_str_list, **kwargs):
    for date_str in date_str_list:
        file_name = f"sales_{date_str}.json"
        file_path = os.path.join(RAW_DIR_2, file_name)
        save_sales_to_local_disk(date=date_str, file_path=file_path)

extract_data_from_api = PythonOperator(
    task_id="extract_data_from_api",
    python_callable=extract_data_from_api_task,
    op_args=date_str_list,
    provide_context=True,
    dag=dag
)

convert_to_avro = PythonOperator(
    task_id="convert_to_avro",
    python_callable=transfer_from_raw_to_stg,
    op_kwargs={"raw_dir": RAW_DIR_2, "stg_dir": STG_DIR_2},
    dag=dag
)

extract_data_from_api >> convert_to_avro
