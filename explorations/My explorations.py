# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "1"
# ///
# MAGIC %sql
# MAGIC drop table if exists  namaste_catalog.sdp.orders_silver
# MAGIC

# COMMAND ----------

# MAGIC %sql 
# MAGIC drop table namaste_catalog.sdp.orders_bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from namaste_catalog.sdp.orders_bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC select * 
# MAGIC from namaste_catalog.vineetdb.kafka_streaming

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from namaste_catalog.lakeflowconnect.status_bronze

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from namaste_catalog.lakeflowconnect.orders_silver

# COMMAND ----------

# MAGIC %sql
# MAGIC select  * from  namaste_catalog.lakeflowconnect.orders_silver

# COMMAND ----------

df =spark.read.format('csv').option('header',True).load("/Volumes/namaste_catalog/vineetdb/testvolume/source_files/orders_files/customers-100.csv")
display(df)

# COMMAND ----------

df = (spark.readStream.format('cloudFiles')
       .option('cloudFiles.format','csv')
       .option('cloudFiles.inferSchema',True)
       .option('cloudFiles.schemaLocation',"/Volumes/namaste_catalog/vineetdb/testvolume/schemaLocation")
       .option('cloudfiles.schemaEvolutionMode','rescue') # 4 emtyhod addNewColumns etc
       .option('cloudFiles.maxFilesPerTrigger','1')
       .load("/Volumes/namaste_catalog/vineetdb/testvolume/source_files/orders_files/customers-100.csv")
 )

display(df)


# COMMAND ----------

# MAGIC %md
# MAGIC ## CDC MERGE INTO STYLE
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

# MERGE INTO silver.orders AS t
# USING (
#   SELECT
#     *,
#     _change_type,
#     _commit_version
#   FROM table_changes('bronze.orders', 0)
# ) AS s
# ON t.id = s.id

# WHEN MATCHED AND s._change_type = 'delete' THEN
#   DELETE

# WHEN MATCHED AND s._change_type = 'update_postimage' THEN
#   UPDATE SET
#     t.customer = s.customer,
#     t.amount = s.amount,
#     t.status = s.status

# WHEN NOT MATCHED AND s._change_type = 'insert' THEN
#   INSERT (id, customer, amount, status)
#   VALUES (s.id, s.customer, s.amount, s.status);

