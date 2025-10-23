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
    venv = dlt.dbt.get_venv(pipeline)
    print("⚙️ Running dbt via dlt runner...")
    # `create_runner` uses DLT’s config to bootstrap and invoke dbt
    runner = create_runner(
        venv=venv,
        credentials={},  # can be empty if your profiles.yml has the connection info
        working_dir=".",                           # working directory, usually current dir
        package_location="../dbt_project",            # path where your dbt project exists
        package_profiles_dir="../dbt_project",        # where profiles.yml is located
        package_profile_name="dbt_project"    # your profile name, e.g., “my_duckdb_project”
    )
    models = runner.run_all()

    for m in models:
        print(f"Model {m.model_name} -> status {m.status}, time {m.time}")

    print("🎉 ELT via dlt + dbt runner completed.")

if __name__ == "__main__":
    main()
