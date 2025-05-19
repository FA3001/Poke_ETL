from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
from extract_pokemon_api import extract_pokemon_data
from airflow.operators.bash import BashOperator
import psycopg2
import csv

DBT_PROJECT_DIR = "/usr/local/airflow/dags/pok"
DBT_PROFILES_DIR = "/usr/local/airflow/dags"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 10),
    'email_on_failure': False,
    'email_on_retry': False,
    'schedule_interval': '@daily',
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}


def load_csv_to_postgres(file_path):
    # Fetch connection details from Airflow connection
    conn_config = BaseHook.get_connection('postgres_conn')
    pg_conn_params = {
        'host': conn_config.host,
        'port': conn_config.port,
        'user': conn_config.login,
        'password': conn_config.password,
        'dbname': conn_config.schema,  
    }
    
    conn = psycopg2.connect(**pg_conn_params)
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE staging.pokemon_raw;")
    with open(file_path, 'r') as f:
        next(f) 
        cur.copy_expert("""
            COPY staging.pokemon_raw
            FROM STDIN
            WITH CSV HEADER
            DELIMITER ','
            NULL ''
            QUOTE '"'
            ESCAPE '\\'
        """, f)
    
    conn.commit()
    cur.close()
    conn.close()


with DAG(
    dag_id='POK_DAG',
    default_args=default_args,
    description='ETL DAG for Pokémon data',
    catchup=False,
    template_searchpath='/usr/local/airflow',
) as dag:
    extract_task = PythonOperator(
        task_id='extract_pokemon_data',
        python_callable=extract_pokemon_data,
        op_kwargs={'output_dir': '/usr/local/airflow/data', 'limit': 1008},
    )
    create_table = PostgresOperator(
        task_id = "create_table",
        postgres_conn_id = 'postgres_conn',
        sql='sql/pokemon_table.sql',
    )
    load_data = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_csv_to_postgres,
        op_kwargs={
            'file_path': 'data/pokemon_db.csv',
        },
    )
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f"dbt run --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}"
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f"dbt test --project-dir {DBT_PROJECT_DIR} --profiles-dir {DBT_PROFILES_DIR}"
    )

extract_task >> create_table >> load_data >> dbt_run >> dbt_test 