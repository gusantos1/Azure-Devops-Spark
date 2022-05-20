# Databricks notebook source
# MAGIC %md
# MAGIC # Azure-Devops-Spark
# MAGIC > A productive library to extract data from Azure Devops and apply agile metrics.
# MAGIC 
# MAGIC Pypi.org: https://pypi.org/project/Azure-Devops-Spark/  
# MAGIC github: https://github.com/gusantos1/Azure-Devops-Spark

# COMMAND ----------

# MAGIC %md
# MAGIC ## Install Package

# COMMAND ----------

pip install Azure-Devops-Spark

# COMMAND ----------

# MAGIC %md
# MAGIC ## Import

# COMMAND ----------

from AzureDevopsSpark import Azure, Agile
from pyspark.sql.functions import datediff
from operator import truediv

# COMMAND ----------

# MAGIC %md
# MAGIC ## Azure

# COMMAND ----------

devops = Azure('organization', 'project', 'token')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Members

# COMMAND ----------

members = devops.all_members().df

# COMMAND ----------

# MAGIC %md
# MAGIC ## Squads

# COMMAND ----------

squads = devops.all_teams().df

# COMMAND ----------

# MAGIC %md
# MAGIC ## Iterations

# COMMAND ----------

iterations = devops.all_iterations().df

# COMMAND ----------

# MAGIC %md
# MAGIC ## Items

# COMMAND ----------

df_items = devops.all_items().df

# COMMAND ----------

# MAGIC %md
# MAGIC ## Backlog

# COMMAND ----------

df_backlog = devops.all_backlog().df

# COMMAND ----------

# MAGIC %md 
# MAGIC ## Join

# COMMAND ----------

full = df_items.join(iterations, df_items.IterationPath == iterations.Iteration_Path)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Base Agile

# COMMAND ----------

df_agil = full.select(
    'AreaPath', 'IterationPath', 'Iteration_Start_Date', 'Iteration_End_Date', 'WorkItemType', 'Id', 'AssignedTo', 'CreatedDate', 'ClosedDate', 'ChangedDate', 'ActivatedDate', 'State', 'Effort')

# COMMAND ----------

# MAGIC %md
# MAGIC # Agile Metrics
# MAGIC > The Agile class receives any PySpark dataframe, it is formed by aggregation methods and types of filters that make customization flexible to apply agile metrics. Agile doesn't have, for example, a cycle time method, but it is possible to create from the avg method with your customizations.
# MAGIC 
# MAGIC All public methods of this class return a Detail object containing detail and df attributes, detail is the dataframe version before aggregation and df is the dataframe already aggregated.
# MAGIC 
# MAGIC - avg, count, max, min, sum
# MAGIC ###### After filtering a dataframe, it performs the operation on the column passed as an argument in ref.
# MAGIC 
# MAGIC ```avg(self, df, ref: Union[str, list], iteration_path: str, new: str, literal_filter: List[str] = None, between_date: Dict[str, str] = None, group_by: List[str] = None, **filters)```
# MAGIC 
# MAGIC <br/>
# MAGIC 
# MAGIC - custom  
# MAGIC ###### Agile.custom takes two PySpark dataframes and the information needed to merge and apply an operation between two columns. Supported Operators: is_, is_not, add, and_, floordiv, mod, mul, pow, sub e ceil (Pyspark).
# MAGIC 
# MAGIC   ```python custom(self, df_left, def_right, left: str, right: str, how: str, op: operator, left_ref: str, right_ref: str, new: str)```

# COMMAND ----------

agile = Agile()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Lead Time

# COMMAND ----------

df_lead_time = agile.avg(
    df=df_agil,
    ref=[datediff, 'ClosedDate', 'CreatedDate'], # You can pass the signature of the datediff method as a parameter which will result in the ClosedDate - CreatedDate operation.
    iteration_path='IterationPath',
    new='LeadTimePbiDaysIn90Days',
    literal_filter=['ClosedDate >= 90'], # Agile knows that 'ClosedDate' is a DateType instance, so ClosedDate >= (D-90).
    filters={
        'WorkItemType': 'Product Backlog Item',
        'State': 'Done'}
).df

# We could also filter between a time range between 2022-01-01 to 2022-12-31 with between_date.

#     between_date = {
#         'CreatedDate': '2022-01-01',
#         'ClosedDate': '2022-12-31'
#     },    

# COMMAND ----------

# MAGIC %md
# MAGIC ## Backlog

# COMMAND ----------

df_qtd_backlog = agile.count(
  df=df_backlog,
  ref='Id',
  iteration_path='IterationPath',
  new='QtdBacklog',
  filters={
      'WorkItemType': ['Product Backlog Item', 'Improvement', 'Bug', 'Issue', 'Technical Debt', 'Spike', 'Vulnerability'],
      'State': '<>Removed'} # Use <> for negation logical expressions.
).df

# COMMAND ----------

# MAGIC %md
# MAGIC ## Backlog (Bug + Technical Debt) / Count(Backlog)

# COMMAND ----------

df_qtd_bug_debt = agile.count(
    df=df_backlog,
    ref='Id',
    iteration_path='IterationPath',
    new='QtdBugDebt',
    filters={'WorkItemType': ['Bug', 'Technical Debt']}
).df

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Without using the custom method

# COMMAND ----------

temp = df_qtd_bug_debt.join(df_qtd_backlog, df_qtd_bug_debt['IterationPath'] == df_qtd_backlog['IterationPath'])
temp_two = temp.withColumn('BacklogHealthCalc', temp['QtdBugDebt'] / temp['QtdBacklog'])

# df_backlog_bug_tech = temp_two.select('IterationPath', 'BacklogBugTechDebt').df

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Using the custom method
# MAGIC > Agile.custom receives two PySpark dataframes and the information needed to apply the join and the signature of a Python operator that will do the operation between the two columns.

# COMMAND ----------

df_backlog_bug_tech = agile.custom(df_start_diff, df_qtd_itens, 'IterationPath', 'IterationPath', 'left', truediv, 'BacklogBugTechDebt').df

# COMMAND ----------

# MAGIC %md
# MAGIC ## Multiple join

# COMMAND ----------

dataframes = [
    df_lead_time,
    df_qtd_backlog,
    df_backlog_bug_tech,
    df_backlog_bug_tech
]

# COMMAND ----------

df_agile_metrics = agile.multiple_join(dataframes, 'IterationPath')

# COMMAND ----------

# MAGIC %md
# MAGIC ## Author
# MAGIC 
# MAGIC The Azure-Devops-Spark library was written by Guilherme Silva < https://www.linkedin.com/in/gusantosdev/ > in 2022.
