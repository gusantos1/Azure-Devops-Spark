from pyspark.sql.types import *


SCHEMA_ITERATIONS = StructType(
    [
        StructField("Iteration_Id", StringType(), True),
        StructField("Iteration_Name", StringType(), True),
        StructField("Iteration_Path", StringType(), True),
        StructField("Iteration_Start_Date", DateType(), True),
        StructField("Iteration_End_Date", DateType(), True),
        StructField("Iteration_State", StringType(), True),
        StructField("Squad", StringType(), True)
    ]
)

SCHEMA_ALL_TEAMS = StructType(
    [
        StructField("Squad", StringType(), True),
        StructField("Id", StringType(), True)
    ]
)

SCHEMA_ALL_MEMBERS = StructType(
    [
        StructField("Name", StringType(), True),
        StructField("Id", StringType(), True),
        StructField("Squad", StringType(), True)
    ]
)

SCHEMA_TAGS = StructType(
    [
        StructField("Id", StringType(), True),
        StructField("Name", StringType(), True)
    ]
)