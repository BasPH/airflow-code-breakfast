import pprint

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

print("hello code breakfast")

default_args = {"owner": "godatadriven", "start_date": airflow.utils.dates.days_ago(14)}

dag = DAG(
    dag_id="1_dag_structures",
    default_args=default_args,
    schedule_interval="0 0 * * *",
)

hello = BashOperator(task_id="hello", bash_command="echo hello!", dag=dag)
foobar = BashOperator(task_id="foobar", bash_command="echo foobar", dag=dag)
hello >> foobar


def _print_context(**context):
    pprint.pprint(context)


print_context = PythonOperator(
    task_id="print_context",
    python_callable=_print_context,
    provide_context=True,
    dag=dag,
)


def _print_exec_date(execution_date, **_):
    pprint.pprint(execution_date)


print_exec_date = PythonOperator(
    task_id="print_exec_date",
    python_callable=_print_exec_date,
    provide_context=True,
    dag=dag,
)

foobar >> [print_context, print_exec_date]

theend = DummyOperator(task_id="theend", dag=dag)
[print_context, print_exec_date] >> theend
