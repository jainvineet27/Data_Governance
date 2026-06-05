from pyspark import pipelines as dp
from pyspark.sql.functions import col
# Streaming table from Kafka
@dp.table
def orders():
   return (spark.readStream.format("kafka")
           .option("kafka.bootstrap.servers", "localhost:9092")
           .option("subscribe", "orders")
           .load())
# Materialized view from CSV
@dp.materialized_view
def customers():
   return spark.read.format("csv").option("header", True).load("/datasets/customers")


# Join and aggregate
@dp.materialized_view
def daily_orders_by_state():
   return (spark.table("orders")
           .join(spark.table("customers"), "customer_id")
           .groupBy("state")
           .count().withColumnRenamed("count", "order_count"))