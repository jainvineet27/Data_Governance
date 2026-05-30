# Databricks notebook source
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


