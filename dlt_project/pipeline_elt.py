import dlt
import pandas as pd
from dlt.helpers.dbt import create_runner

from load_data import local_csvs  # our existing csv-to-dlt code

def main():
    print("🚀 Running full ELT pipeline")

    # Step 1: Load data into DLT pipeline
    pipeline = dlt.pipeline(
        pipeline_name="elt_pipeline",
        dataset_name="raw",
        destination="duckdb"
    )
    pipeline.run(local_csvs())
    print("✅ DLT load complete.")

    # Step 2: Run dbt transformations using dlt’s runner
    pipeline = dlt.pipeline(
        pipeline_name='pipedrive',
        destination='duckdb',
        dataset_name='main'
    )

    # Make or restore venv for dbt, using the latest dbt version
    # NOTE: If you have dbt installed in your current environment, just skip this line
    #       and the `venv` argument to dlt.dbt.package()
    venv = dlt.dbt.get_venv(pipeline)
    print("⚙️ Running dbt via dlt runner...")

    # Get runner, optionally pass the venv
    dbt = dlt.dbt.package(
        pipeline=pipeline,
        package_location="../dbt_project",            # path where your dbt project exists
        venv=venv
    )

    # Run the models and collect any info
    # If running fails, the error will be raised with a full stack trace
    models = dbt.run_all()

    for m in models:
        print(f"Model {m.model_name} -> status {m.status}, time {m.time}")

    print("🎉 ELT via dlt + dbt runner completed.")

if __name__ == "__main__":
    main()
