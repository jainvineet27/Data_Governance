from pyspark import pipelines as dp

@dp.materialized_view()
def load_raw_data():
    df = (
        spark.read.format("csv")
        .option("header", "true")
        .option("inferSchema", "true")
        .load("/Volumes/namaste_catalog/vineetdb/testvolume/source_files/orders_files/customers-100.csv")
    )
    return df.selectExpr(
        "Index AS `index`",
        "`Customer Id` AS customer_id",
        "`First Name` AS first_name",
        "`Last Name` AS last_name",
        "Company AS company",
        "City AS city",
        "Country AS country",
        "`Phone 1` AS phone_1",
        "`Phone 2` AS phone_2",
        "Email AS email",
        "`Subscription Date` AS subscription_date",
        "Website AS website"
    )

# @dp.table()
# def my_transformation():
#     return (
#         spark.readStream.format("cloudFiles")
#         .option("cloudFiles.format", "csv")
#         .option("cloudFiles.inferColumnTypes", "true")
#         .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
#         .option("cloudFiles.maxFilesPerTrigger", "1")
#         .load("/Volumes/namaste_catalog/vineetdb/testvolume/source_files/orders_files/customers-100.csv")
#     )
