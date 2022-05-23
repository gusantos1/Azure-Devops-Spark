from typing import List


class Response:
    def __init__(self, data: List[dict], schema:List[str], spark):
        self.__data = data
        self.__df = spark.createDataFrame(data=[tuple(item.values()) for item in data], schema=schema)

    def show(self, select: List[str] = None, truncate: bool = True):
        """
            Show a spark dataframe.
        """
        if select:
            return self.__df.select(select).show(self.__df.count(), truncate=truncate)
        else:
            return self.__df.show(self.__df.count(), truncate=truncate)

    @property
    def data(self):
        """
            Returns data in its basic structure.
        """
        return self.__data
      
    @property
    def df(self):
        """
            Returns a spark dataframe.
        """
        return self.__df
    
    def table(self, database: str, table: str, format = 'delta', mode = 'overwrite'):
      """
        Creates a table in cluster.
        format default: delta
        mode default: overwrite
        :param database: Database present in the cluster.
        :param table: Name of the table to be created.
        :param format: Format of the table to be created, delta, orc, parquet.
        :param mode: Table creation mode, overwrite, append, ...
      """
      return self.__df.write.format(format).mode(mode).saveAsTable(f'{database}.{table}')
    
    def parquet(self, path: str, mode: str ='overwrite', partitionBy: str =None, compression: str =None):
        """
            Creates parquet files in path.
            mode default: overwrite
        """
        return self.__df.write.mode(mode).parquet(f'{path}', partitionBy=partitionBy, compression=compression)
    
    def view(self, name: str):
        """
            Creates a table view.
        """
        return self.__df.createOrReplaceTempView(name)