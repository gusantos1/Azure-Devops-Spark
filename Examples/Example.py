# Databricks notebook source
# MAGIC %md
# MAGIC # azure-devops-pyspark
# MAGIC >  Azure Devops PySpark: A productive library to extract data from Azure Devops and apply agile metrics.
# MAGIC 
# MAGIC Pypi.org: https://pypi.org/project/azure-devops-pyspark/  
# MAGIC github: https://github.com/gusantos1/azure-devops-pyspark/

# COMMAND ----------

# MAGIC %md
# MAGIC ## Import

# COMMAND ----------

from AzureDevopsPySpark import Azure

# COMMAND ----------

# MAGIC %md
# MAGIC ## Azure

# COMMAND ----------

token = dbutils.secrets.get(scope = "main", key = "devops")
devops = Azure('gusantosok', 'GusantosDevops', token)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Members

# COMMAND ----------

members = devops.members()

# COMMAND ----------

display(members)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Squads

# COMMAND ----------

squads = devops.teams()

# COMMAND ----------

display(squads)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Iterations

# COMMAND ----------

iterations = devops.iterations()

# COMMAND ----------

display(iterations)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Tags

# COMMAND ----------

df_tags = devops.tags()

# COMMAND ----------

display(df_tags)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Items

# COMMAND ----------

df_items = devops.items()

# COMMAND ----------

display(df_items)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Select specific columns

# COMMAND ----------

devops.filter_columns(['System.IterationPath', 'System.WorkItemType', 'System.Id', 'System.State', 'System.Title', 'System.AssignedTo'])

# COMMAND ----------

df_select = devops.items()

# COMMAND ----------

display(df_select)
