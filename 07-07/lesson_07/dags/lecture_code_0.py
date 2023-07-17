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


class RateBranchOperator(BaseBranchOperator):

    def choose_branch(self, context: Context):
        ti = context['ti']
        rate = ti.xcom_pull(task_ids='python_task', key='rate')
        previous_rate = Variable.get(key='previous_rate')
        Variable.set(key='previous_rate', value=rate)
        if rate > float(previous_rate):
            return 'go_up'
        else:
            return 'go_down'


with DAG(
        dag_id="Lecture_DAG",
        schedule=None,
        start_date=datetime.strptime("2023-06-21", "%Y-%m-%d"),
        tags=['lecture']
) as dag:
    def get_rate(**kwargs):
        ti = kwargs['ti']
        hook = HttpHook(
            method='GET',
            http_conn_id='bitcoin_http'
        )
        response = hook.run('v1/bpi/currentprice.json')
        rate = float(json.loads(response.content)['bpi']['USD']['rate_float'])
        print(f"Rate: {rate}")
        ti.xcom_push('rate', rate)


    # 29898

    task = BashOperator(
        task_id="bash_task",
        bash_command="echo \"Hello World!\"",
    )

    python_task = PythonOperator(
        task_id="python_task",
        python_callable=get_rate,
    )

    branch = RateBranchOperator(
        task_id='branch'
    )

    go_up = EmptyOperator(
        task_id='go_up'
    )

    go_down = EmptyOperator(
        task_id='go_down'
    )

    task >> python_task >> branch >> [go_up, go_down]

