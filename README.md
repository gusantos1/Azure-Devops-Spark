## Azure Devops PySpark:  A productive library to extract data from Azure Devops and apply agile metrics.



## What is it?

Azure Devops PySpark is a Python package that provides the most productive way to extract data from Azure Devops and build agile metrics.
It runs on PySpark, enabling all the features the technology makes available.

## Main Features

- Get authenticated quickly and simply.

- All columns of the project are automatically mapped, just the ones you want to form your dataframes with.
- SparkSession already created in spark variable.
- Get all your organization's backlogs with the method **all_backlog**.
- Get all your organization's teams with the method **all_teams**.
- Get all your organization's iterations with the method **all_iterations**.
- Get all your organization's members with the method **all_members**.
- Get all your organization's items with the method **all_items**.
- Get all your organization's tags with the method **all_tags**.
- Explore the simplicity of Agile class to build powerful metrics for your organization.

## How to install?

```bash
pip install azure-devops-pyspark
```

**[For local use it is necessary to install pyspark>=3.2.1 and also configure the necessary environment variables. If you don't know, click here.](https://github.com/gusantos1/como_instalar_spark)**

## The Code

The code and issue tracker are hosted on GitHub: https://github.com/gusantos1/azure-devops-pyspark

## Quick example

```python
from AzureDevopsPySpark import Azure, Agile
from pyspark.sql.functions import datediff #use in agile metrics

devops = Azure('ORGANIZATION', 'PROJECT', 'TOKEN')
```

```python
## Filter columns
devops.filter_columns([
    'IterationPath', 'Id', 'State', 'WorkItemType',
    'CreatedDate', 'ClosedDate', 'Iteration_Start_Date', 'Iteration_End_Date'
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
```

```python
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

[**In this link you will find a notebook with examples of applications using the library's methods.**](https://github.com/gusantos1/azure-devops-pyspark/tree/main/Examples)

## How it works?

<img src="https://github.com/gusantos1/icons/blob/9200dc6c7238fc8f2fac110b015c497786c64354/flow-AzureDevopsSpark.png?raw=true">

## Azure Methods

All public methods of this class return a Response object containing data and df attributes, data is Python basic data structure, and df is PySpark dataframe structure.

- all_backlog

  ###### Returns all backlog work items within a project.

  ```python
  all_backlog(self)
  ```

- filter_columns

  ###### Mapped columns that are not in the list passed as an argument will be excluded.

  ```python
  filter_columns(self, only: List[str])
  ```

- all_iterations

  ###### Returns all iterations in the project.

  ```python
  all_iterations(self, only: List[str] = None, exclude: List[str] = None)
  ```

- all_items

  ###### Returns all work items in the project. `It is possible to filter by SQL in the query parameter set to None`. Ex: Where [System.WorkItemType] = 'Task' AND [System.AssignedTo] = 'Guilherme Silva'. Returns all tasks associated with Guilherme Silva.

  ```python
  all_items(self, query:str = None, params_endpoint:str = None)
  ```

- all_members

  ###### Returns all members in the project.

  ```python
  all_members(self, only: List[str] = None, exclude: List[str] = None, params_endpoint: str = None)
  ```

- all_tags

  ###### Returns all tags registered in the project.

  ```python
  all_tags(self)
  ```

- all_teams

  ###### Returns all teams registered in the project.

  ```python
  all_teams(self, only: List[str] = None, exclude: List[str] = None, params_endpoint:str = None)	
  ```

## Response Methods

- show

  ###### Show a pyspark dataframe.

  ```python
  show(self, select: List[str] = None, truncate: bool = True)
  ```

- data

  ###### Returns data in its basic structure

  ```python
  data(self)
  ```

- df

  ###### Returns a pyspark dataframe

  ```python
  df(self)
  ```

- table

  ###### Creates a table on the cluster with delta format and overwrite mode by default.

  ```python
  table(self, database: str, table: str, format = 'delta', mode = 'overwrite')
  ```

- parquet

  ###### Creates parquet files in path and overwrite mode by default.

  ```python
  parquet(self, path: str, mode: str = 'overwrite', partitionBy: str = None, compression: str = None)
  ```

- view

  Creates a table view.

  ```python
  view(self, name: str)
  ```

  

## Agile Methods

The Agile class receives any PySpark dataframe, it is formed by aggregation methods and types of filters that make customization flexible to apply agile metrics. Agile doesn't have, for example, a cycle time method, but it is possible to create from the avg method with your customizations.

All public methods of this class return a Detail object containing detail and df attributes, detail is the dataframe version before aggregation and df is the dataframe already aggregated.

- avg, count, max, min, sum

  ###### After filtering a dataframe, it performs the operation on the column passed as an argument in ref.

  ```python
  avg(self, df, ref: Union[str, list], iteration_path: str, new: str, literal_filter: List[str] = None, between_date: Dict[str, str] = None, group_by: List[str] = None, **filters)
  ```

- custom

  ###### Agile.custom receives two PySpark dataframes and the information needed to merge and the signature string of a Python operator that will do the operation between the two columns. Supported operators: is_, is_not, add, and_, truediv, floordiv, mod, mul, pow, sub and ceil (Pyspark).

  ```python
  custom(self, df_left, def_right, left: str, right: str, how: str, op: operator, left_ref: str, right_ref: str, new: str)
  ```
  
- multiple_join

  ###### Receives a list of dataframes and merges using the same column name between them.

  ```python
  multiple_join(self, dfs: list, on: List[str], how: str = 'left')
  ```



## Dependencies

[certifi >= 2021.10.8](https://pypi.org/project/certifi/)

[charset-normalizer >= 2.0.12](https://pypi.org/project/charset-normalizer/)

[idna >= 3.3](https://pypi.org/project/idna/)

[requests >= 2.27.1](https://pypi.org/project/requests/)

[urllib3 >= 1.26.9](https://pypi.org/project/urllib3/)

[python-dateutil >= 2.8.2](https://pypi.org/project/python-dateutil/)

## Author

The azure-devops-pyspark library was written by Guilherme Silva < https://www.linkedin.com/in/gusantosdev/ > in 2022.

https://github.com/gusantos1/azure-devops-pyspark

## License

GNU General Public License v3.0.
