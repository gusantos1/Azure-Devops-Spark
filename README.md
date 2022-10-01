## Azure Devops PySpark:  A productive library to extract data from Azure Devops and apply agile metrics.



## What is it?

Azure Devops PySpark is a Python package that provides the most productive way to extract data from Azure Devops and build agile metrics.
It runs on PySpark, enabling all the features the technology makes available.

## Main Features

- Get authenticated quickly and simply.

- All columns of the project are automatically mapped, use the filter_columns method to filter only those you want to form your dataframes with..
- SparkSession already created in spark variable.
- Get all your organization's backlogs with the method **backlog**.
- Get all your organization's teams with the method **teams**.
- Get all your organization's iterations with the method **iterations**.
- Get all your organization's members with the method **members**.
- Get all your organization's items with the method **items**.
- Get all your organization's tags with the method **tags**.
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
from AzureDevopsSpark import Azure, Agile
from pyspark.sql.functions import datediff #use in agile metrics

devops = Azure('ORGANIZATION', 'PROJECT', 'TOKEN')
```

```python
## Filter columns
devops.filter_columns([
    'IterationPath', 'Id', 'State', 'WorkItemType',
    'CreatedDate', 'ClosedDate', 'Iteration_Start_Date', 'Iteration_End_Date'
])


## Pyspark Dataframe data structure
df_backlog = devops.backlog()
df_items = devops.items()
df_iterations = devops.iterations()
df_members = devops.members()
df_tags = devops.tags()
df_teams = devops.teams()
```

```python
## Agile Metrics
agile = Agile()

## A new dataframe
df_agil = df.items.join(df_iterations, 'IterationPath')

## Metrics

## Average time between CreatedDate and ClosedDate of items in the last 90 days.
lead_time = lead_time = agile.avg(
    df=df_agil,
    ref=[datediff, 'ClosedDate', 'CreatedDate'], # The day difference between the CreatedDate and ClosedDate of each item.
    iteration_path='IterationPath', # GroupBy.
    new='LeadTimeDays', # New column name.
    literal_filter=['ClosedDate >= 90'], # Filtering items from the last 90 days.
    filters={'WorkItemType': 'Task', 'State': 'Closed'} # Custom filters for metric.
).df
```

#### In this link you will find a notebook with examples of applications using the library's methods.



## How it works?

<img src="https://github.com/gusantos1/icons/blob/9200dc6c7238fc8f2fac110b015c497786c64354/flow-AzureDevopsSpark.png?raw=true">

## Azure Methods

All public methods of this class return an object spark dataframe.

- backlog

  ###### Returns all backlog work items within a project.

  ```python
  backlog(self)
  ```

- filter_columns

  ###### Mapped columns that are not in the list passed as an argument will be excluded.

  ```python
  filter_columns(self, only: List[str])
  ```

- iterations

  ###### Returns all iterations in the project.

  ```python
  iterations(self, only: List[str] = None, exclude: List[str] = None)
  ```

- items

  ###### Returns all work items in the project. `It is possible to filter by SQL in the query parameter set to None`. Ex: Where [System.WorkItemType] = 'Task' AND [System.AssignedTo] = 'Guilherme Silva'. Returns all tasks associated with Guilherme Silva.

  ```python
  items(self, query:str = None, params_endpoint:str = None)
  ```

- members

  ###### Returns all members in the project.

  ```python
  members(self, only: List[str] = None, exclude: List[str] = None, params_endpoint: str = None)
  ```

- tags

  ###### Returns all tags registered in the project.

  ```python
  tags(self)
  ```

- teams

  ###### Returns all teams registered in the project.

  ```python
  teams(self, only: List[str] = None, exclude: List[str] = None, params_endpoint:str = None)	
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

  ###### Agile.custom takes two PySpark dataframes and the information needed to merge and apply an operation between two columns. Supported Operators: is_, is_not, add, and_, floordiv, mod, mul, pow, sub e ceil (Pyspark).

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

The Azure-Devops-PySpark library was written by Guilherme Silva < https://www.linkedin.com/in/gusantosdev/ > in 2022.

https://github.com/gusantos1/Azure-Devops-Spark

## License

GNU General Public License v3.0.
