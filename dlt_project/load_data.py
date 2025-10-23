import os
import dlt
import pandas as pd

@dlt.source
def local_csvs():
    @dlt.resource(name="raw_customers")
    def customers():
        yield pd.read_csv("../dbt_project/seeds/raw_customers.csv")

    @dlt.resource(name="raw_orders")
    def orders():
        yield pd.read_csv("../dbt_project/seeds/raw_orders.csv")

    @dlt.resource(name="raw_payments")
    def payments():
        yield pd.read_csv("../dbt_project/seeds/raw_payments.csv")

    return customers, orders, payments


if __name__ == "__main__":
    print("Loading data into DuckDB...")

    pipeline = dlt.pipeline(
        pipeline_name="load_data_pipeline",
        dataset_name="raw"
    )

    pipeline.run(local_csvs())

    print("Data loaded successfully!")
