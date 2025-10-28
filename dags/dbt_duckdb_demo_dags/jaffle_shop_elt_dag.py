from airflow import DAG
from airflow.decorators import dag, task
from airflow.providers.standard.operators.python import PythonOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig, ExecutionConfig, ExecutionMode
from datetime import datetime, timedelta
import os
import dlt
from pathlib import Path
from include.dlt_pipeline.load_data import local_csvs # reuse your dlt pipeline

# dbt env variables
DBT_PROFILE_NAME = "dbt_project"
DBT_PROJECT_PATH = Path(f"/usr/local/airflow/dags/{DBT_PROFILE_NAME}/")
DBT_PROFILE_PATH = f"{DBT_PROJECT_PATH}/profiles.yml"
DBT_TARGET_NAME = "dev"

# DuckDB specific configuration
DUCKDB_FILEPATH = os.getenv("DUCKDB_FILEPATH", f"{DBT_PROJECT_PATH}/dev.duckdb")

default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=1),
}

def run_dlt_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="load_data_pipeline",
        dataset_name="raw",
        destination=dlt.destinations.duckdb(
            credentials=DUCKDB_FILEPATH
        )
    )
    pipeline.run(local_csvs())

@dag(
    dag_id="jaffle_shop_elt_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["dbt", "dlt", "duckdb"],
)
def dlt_dbt_duckdb_demo():

    extract_load = PythonOperator(
        task_id="extract_load_dlt",
        python_callable=run_dlt_pipeline,
    )

    transform_with_dbt = DbtTaskGroup(
        group_id="transform_with_dbt",
        project_config=ProjectConfig(dbt_project_path=DBT_PROJECT_PATH),
        profile_config=ProfileConfig(
            profile_name=DBT_PROFILE_NAME, 
            profiles_yml_filepath=DBT_PROFILE_PATH,
            target_name=DBT_TARGET_NAME
        ),
        render_config=RenderConfig(
            select=[
                "staging.stg_customers",
                "staging.stg_orders",
                "staging.stg_payments",
                "marts.marts_customers",
                "marts.marts_orders",
                ]                        # this runs the models one by one and avoids concurrency issues in duckdb
        ),
        execution_config=ExecutionConfig(
            dbt_executable_path="dbt",
            execution_mode=ExecutionMode.LOCAL,
        ),
        operator_args={
            "install_deps": True,
            "full_refresh": False,
            "dbt_cmd_flags": ["--debug"],
            "threads": 1,
        },
    )

    extract_load >> transform_with_dbt


dlt_dbt_duckdb_demo()
