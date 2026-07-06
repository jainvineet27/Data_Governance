from pyspark import pipelines as dp 

file_path = spark.conf.get("ingestion_path")
print(file_path)

@dp.table(name="orders_off")
def read_orders():
    return spark.read.format("csv").option("header",True).load(f"{file_path}/orders")

@dp.table(name="products_off")
def read_products():
    return spark.read.format("csv").option("header",True).load(f"{file_path}/products")

@dp.table(name="customers_off")
def read_customers():
    return spark.read.format("csv").option("header",True).load(f"{file_path}/customers")

@dp.table(name="orders_on")
def read_orders():
    return spark.read.format("json").option("multiLine",True).load(f"{file_path}/orders/online")
