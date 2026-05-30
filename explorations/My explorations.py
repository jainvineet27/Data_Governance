# Databricks notebook source
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
       .option('cloudfiles.schemaEvolutionMode','rescue')
       .option('cloudFiles.maxFilesPerTrigger','1')
       .load("/Volumes/namaste_catalog/vineetdb/testvolume/source_files/orders_files/customers-100.csv")
 )

display(df)


# COMMAND ----------


