# Databricks notebook source
from pyspark.sql.functions import explode_outer, col, expr
df  =spark.sql('select * from namastecatalog.vineetdb.orders_on')

df = df.withColumn('i', explode_outer(col("items"))) \
       .selectExpr("customer.*", "i.*", "order_id", "payment_mode", "cast(order_timestamp as date) as order_date")
display(df)

# COMMAND ----------

# DBTITLE 1,transformation on online orders
# MAGIC %sql
# MAGIC select customer.*  , i.* , order_id , date(order_timestamp), payment_mode 
# MAGIC  from namastecatalog.vineetdb.orders_on
# MAGIC lateral view explode_outer(items) it as i 

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Step 1: Table ko sahi schema ya select query ke sath create karein
# MAGIC CREATE TABLE IF NOT EXISTS namastecatalog.vineetdb.orders_silver
# MAGIC TBLPROPERTIES (delta.enableChangeDataFeed = true)
# MAGIC AS 
# MAGIC SELECT *, CURRENT_TIMESTAMP() AS ingestion_timestamp, _metadata.file_name AS file_name
# MAGIC FROM table_changes('namastecatalog.vineetdb.orders_bronze', 0)
# MAGIC WHERE 1=0; -- Yeh trick khali table structure create karne ke liye hai (bina data ke)

# COMMAND ----------

# DBTITLE 1,Nice
-- To migrate a table from one catalog to another, use CREATE TABLE AS SELECT with fully qualified names.
CREATE TABLE namaste_catalog.schema_name.table_name AS
SELECT * FROM old_catalog.schema_name.table_name;

-- To migrate a schema, recreate the schema in the new catalog and then migrate each table.
CREATE SCHEMA namaste_catalog.schema_name;

-- Example for a single table:
CREATE TABLE namaste_catalog.sales_schema.orders AS
SELECT * FROM old_catalog.sales_schema.orders;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * 
# MAGIC from  namastecatalog.vineetdb.orders_off

# COMMAND ----------

# MAGIC %sql
# MAGIC select * 
# MAGIC from namastecatalog.vineetdb.products_off

# COMMAND ----------

# MAGIC %sql
# MAGIC select p.category , p.product_name  , sum( o.quantity * cast (o.unit_price as int )   ) as total_price
# MAGIC from namastecatalog.vineetdb.orders_off  o inner join  namastecatalog.vineetdb.products_off p on 
# MAGIC  o.product_id = p.product_id 
# MAGIC  group by p.category , p.product_name 
# MAGIC order by total_price desc
