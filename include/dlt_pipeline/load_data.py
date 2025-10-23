import os
import dlt
import pandas as pd

# Define seed path with environment override
SEED_PATH = os.getenv("SEED_PATH", "/usr/local/airflow/include/dlt_pipeline/data/")

@dlt.source
def local_csvs():
    @dlt.resource(name="raw_customers")
    def customers():
        yield pd.read_csv(os.path.join(SEED_PATH, "raw_customers.csv"))

    @dlt.resource(name="raw_orders")
    def orders():
        yield pd.read_csv(os.path.join(SEED_PATH, "raw_orders.csv"))

    @dlt.resource(name="raw_payments")
    def payments():
        yield pd.read_csv(os.path.join(SEED_PATH, "raw_payments.csv"))

    return customers, orders, payments
