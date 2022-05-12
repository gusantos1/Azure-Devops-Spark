## Azure Devops Spark:  A productive library to extract data from Azure Devops and apply agility metrics.



## What is it?

Azure Devops Spark is a Python package that provides the Python ecosystem's most productive way to extract data from Azure Devops and build agility metrics.
It runs on Spark, enabling all the features the technology makes available.

## Main Features

- Get authenticated quickly and simply.

- All columns of the project are automatically mapped, just the ones you want to form your dataframes with.
- Keep having the freedom to configure your Sparksession.
- Get all your organization's backlogs with the method **all_backlog**.
- Get all your organization's teams with the method **all_teams**.
- Get all your organization's iterations with the method **all_iterations**.
- Get all your organization's members with the method **all_members**.
- Get all your organization's items with the method **all_items**.
- Get all your organization's tags with the method **all_tags**.
- Explore the simplicity of agile methods to build powerful metrics for your organization.



## How to install?

```bash
pip install Azure-Devops-Spark
```

## Dependencies

- [certifi >= 2021.10.8](https://pypi.org/project/certifi/)

- [charset-normalizer >= 2.0.12](https://pypi.org/project/charset-normalizer/)

- [idna >= 3.3](pip install idna)

- [requests >= 2.27.1](pip install requests)

- [urllib3 >= 1.26.9](pip install urllib3)

- [python-dateutil >= 2.8.2](pip install python-dateutil)

- [pyspark>=3.2.1](pip install pyspark) 



## The Code

The code and issue tracker are hosted on GitHub: https://github.com/gusantos1/Azure-Devops-Spark

## Quick example

```python
from AzureDevopsSpark import Azure, Agile
from pyspark.sql.functions import datediff #use in agile metrics

devops = Azure('ORGANIZATION', 'PROJECT', 'TOKEN')

## Filter columns
devops.filter_columns([
    'IterationPath', 'Id', 'State', 'WorkItemType', 'CreatedDate', 'ClosedDate', 'Iteration_Start_Date', 'Iteration_End_Date'
])

## Basic data structures
df_members = devops.all_members().data
df_backlog = devops.all_backlog().data
df_iterations = devops.all_iterations().data
df_items = devops.all_items().data

## or

## Pyspark Dataframe data structure
df_members = devops.all_members().df
df_backlog = devops.all_backlog().df
df_iterations = devops.all_iterations().df
df_items = devops.all_items().df

## Agile Metrics
agile = Agile()

## A new dataframe
df_agil = df.items.join(df_iterations, 'IterationPath')

## Metrics

## Average time between CreatedDate and ClosedDate of items in the last 90 days.
lead_time = lead_time = agil.avg(
    df=df_agil,
    ref=[datediff, 'ClosedDate', 'CreatedDate'], # The day difference between the CreatedDate and ClosedDate of each item.
    iteration_path='IterationPath', # GroupBy.
    new='LeadTimeDays', # New column name.
    literal_filter=['ClosedDate >= 90'], # Filtering items from the last 90 days.
    filters={'WorkItemType': 'Task', 'State': 'Closed'} # Custom filters for metric.
).df
```



## Author

The Azure-Devops-Spark library was written by Guilherme Santos < gusantos.ok@gmail.com > in 2022.

## License

GNU General Public License v3.0.
