# Databricks notebook source
# MAGIC %md
# MAGIC # Zerobus Ingest Python
# MAGIC
# MAGIC Zerobus Ingest is the foundational layer of our data platform, designed to handle high-frequency data streams with ultra-low latency. It serves as the bridge between external data producers and your Lakehouse.
# MAGIC
# MAGIC ### Documentation
# MAGIC - [AWS Docs](https://docs.databricks.com/aws/en/ingestion/zerobus-overview)
# MAGIC - [Azure Docs](https://learn.microsoft.com/en-us/azure/databricks/ingestion/zerobus-overview)
# MAGIC - [Python SDK Repo](https://github.com/databricks/zerobus-sdk-py)
# MAGIC - [Databricks Workspace URL](https://docs.databricks.com/aws/en/ingestion/zerobus-ingest#get-your-workspace-url)
# MAGIC - [Zerobus Ingest Regions](https://docs.databricks.com/aws/en/ingestion/zerobus-limits#workspace)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 1: Prepare the Environment

# COMMAND ----------

# Install SDK - https://github.com/databricks/zerobus-sdk-py
%pip install databricks-zerobus-ingest-sdk

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 2: Configuration

# COMMAND ----------

# Databricks Workspace Information
DATABRICKS_WORKSPACE_ID = "7405614604176320"
DATABRICKS_WORKSPACE_URL = "https://adb-7405614604176320.0.azuredatabricks.net/"
DATABRICKS_REGION = "eu-west-europe"

# Zerobus Ingest URL
ZEROBUS_INGEST_URL = f"{DATABRICKS_WORKSPACE_ID}.zerobus.{DATABRICKS_REGION}.cloud.databricks.com"
print(ZEROBUS_INGEST_URL)
# # Service Princple Authentication
# CLIENT_ID = "your-service-principal-application-id"
# CLIENT_SECRET = "your-service-principal-secret"

# # Table Information
# CATALOG =  "main"
# SCHEMA = "default"
# TABLE = "zerobus_ingest_test"

# COMMAND ----------


# Service Princple Authentication
CLIENT_ID = "your-service-principal-application-id"
CLIENT_SECRET = "your-service-principal-secret"

# Table Information
CATALOG =  "namastecatalog"
SCHEMA = "vineetdb"
TABLE = "zerobus_ingest_test"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 3: Create your target table

# COMMAND ----------

spark.sql(f"CREATE TABLE IF NOT EXISTS {CATALOG}.{SCHEMA}.{TABLE} (id INT,device STRING,payload VARIANT)")

# COMMAND ----------

# Grant your service principal required permissions to the table.
spark.sql(f"GRANT USE CATALOG ON CATALOG {CATALOG} TO " + "`" + CLIENT_ID + "`;").collect()
spark.sql(f"GRANT USE SCHEMA ON SCHEMA {CATALOG}.{SCHEMA} TO " + "`" + CLIENT_ID + "`;").collect()
spark.sql(f"GRANT MODIFY, SELECT ON TABLE {CATALOG}.{SCHEMA}.{TABLE} TO " + "`" + CLIENT_ID + "`;").collect()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 4.a: Implement Sync Client

# COMMAND ----------

# Init SDK
import json
import logging
from zerobus.sdk.sync import ZerobusSdk
from zerobus.sdk.shared import RecordType, StreamConfigurationOptions, TableProperties

# Configure logging (optional but recommended)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Configuration
server_endpoint = ZEROBUS_INGEST_URL
workspace_url = DATABRICKS_WORKSPACE_URL

table_name = f"{CATALOG}.{SCHEMA}.{TABLE}"
client_id = CLIENT_ID
client_secret = CLIENT_SECRET

# Initialize SDK
sdk = ZerobusSdk(server_endpoint, unity_catalog_url=workspace_url)

# Configure table properties
table_properties = TableProperties(table_name)

# Configure stream with JSON record type
options = StreamConfigurationOptions(record_type=RecordType.JSON)

# COMMAND ----------

# Create stream and start writing data

stream = sdk.create_stream(client_id, client_secret, table_properties, options)

try:
    # Ingest records
    for i in range(100):
        # Create JSON record
        record_dict = {
            "id": i,
            "device": f"sensor-{i % 10}",
            "payload": json.dumps({"temp": 20 + (i % 15), "humidity": 50 + (i % 40)}),
        }
    
        stream.ingest_record(record_dict)

        print(f"Ingested record {i + 1}")
    stream.flush()
    print("Successfully ingested 100 records!")
finally:
    stream.close()

# COMMAND ----------

display(spark.sql(f"SELECT * FROM {CATALOG}.{SCHEMA}.{TABLE}"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Step 4.b: Implement AsyncIO Client

# COMMAND ----------

import asyncio
from zerobus.sdk.aio import ZerobusSdk as ZerobusSdkAsync

async def main():
    # Configuration
    server_endpoint = ZEROBUS_INGEST_URL
    workspace_url = DATABRICKS_WORKSPACE_URL

    table_name = f"{os.environ["CATALOG"]}.{os.environ["SCHEMA"]}.{os.environ["TABLE"]}"
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET

    # Initialize SDK
    sdk = ZerobusSdkAsync(server_endpoint, workspace_url)

    # Configure table properties
    table_properties = TableProperties(table_name)

    # Configure stream with JSON record type
    options = StreamConfigurationOptions(record_type=RecordType.JSON)

    # Create stream
    stream = await sdk.create_stream(client_id, client_secret, table_properties, options)

    try:
        # Ingest records
        for i in range(100_000):
            # Create JSON record
            record_dict = {
                "id": i,
                "device": f"sensor-async-{i % 10}",
                "payload": json.dumps({"temp": 20 + (i % 15), "humidity": 50 + (i % 40)}),
            }

            future = stream.ingest_record(record_dict)
            await future  # Optional: Wait for durability confirmation

            if i % 100 == 0:
              print(f"Ingested record {i + 1}")

        print("Successfully ingested 100_000 records!")
    finally:
        await stream.close()

await main()

# COMMAND ----------

display(spark.sql(f"SELECT * FROM {CATALOG}.{SCHEMA}.{TABLE} WHERE startswith(device, 'sensor-async-')"))
