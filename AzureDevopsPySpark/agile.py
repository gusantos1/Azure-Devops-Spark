import pyspark.sql.functions as f
from ast import operator
from collections import namedtuple
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import eq, gt, lt, ge, le, ne
from typing import Union, List, Dict


class Agile:
    def avg(
        self,
        df,
        ref: Union[str, list],
        iteration_path: str,
        new: str,
        literal_filter: List[str] = None,
        between_date: Dict[str, str] = None,
        group_by: List[str] = None,
        **filters,
    ):
        """
        After filtering a dataframe performs the arithmetic average of the column as a reference.
        """

        agg_column, df_callable = self.__filters(
            df, ref, literal_filter, between_date, **filters
        )
        df_result = (
            df_callable.groupby(iteration_path if not group_by else group_by)
            .agg(f.avg(agg_column).alias(new))
            .orderBy(new)
        )
        return Detail(df_result, df_callable)

    def count(
        self,
        df,
        ref: Union[str, list],
        iteration_path: str,
        new: str,
        literal_filter: List[str] = None,
        between_date: Dict[str, str] = None,
        group_by: List[str] = None,
        **filters,
    ):
        """
        After filtering a dataframe perform the column count as a reference.
        """
        agg_column, df_callable = self.__filters(
            df, ref, literal_filter, between_date, **filters
        )
        df_result = (
            df_callable.groupby(iteration_path if not group_by else group_by)
            .agg(f.countDistinct(agg_column).alias(new))
            .orderBy(new)
        )
        return Detail(df_result, df_callable)

    def custom(
        self,
        df_left,
        df_right,
        left: str,
        right: str,
        how: str,
        op: operator,
        left_ref: str,
        right_ref: str,
        new: str,
    ):
        """
        Agile.custom receives two PySpark dataframes and the information needed to apply the join and the signature of a Python operator that will do the operation between the two columns.
        Supported Operators: is_, is_not, add, and_, floordiv, mod, mul, pow, sub and ceil(pyspark).
        """
        temp_join = df_left.join(df_right, df_left[left] == df_right[right], how)
        df_temp = self.__interpreter_operator(
            temp_join, op, left_ref, right_ref, new
        ).drop(df_right[right])
        df_result = df_temp.select(left, new)
        return Detail(df_result, df_temp)

    def max(
        self,
        df,
        ref: Union[str, list],
        iteration_path: str,
        new: str,
        literal_filter: List[str] = None,
        between_date: Dict[str, str] = None,
        group_by: List[str] = None,
        **filters,
    ):
        """
        After filtering a dataframe perform the column max as a reference.
        """
        agg_column, df_callable = self.__filters(
            df, ref, literal_filter, between_date, **filters
        )
        df_result = (
            df_callable.groupby(iteration_path if not group_by else group_by)
            .agg(f.max(agg_column).alias(new))
            .orderBy(new)
        )
        return Detail(df_result, df_callable)

    def min(
        self,
        df,
        ref: Union[str, list],
        iteration_path: str,
        new: str,
        literal_filter: List[str] = None,
        between_date: Dict[str, str] = None,
        group_by: List[str] = None,
        **filters,
    ):
        """
        After filtering a dataframe perform the column min as a reference.
        """
        agg_column, df_callable = self.__filters(
            df, ref, literal_filter, between_date, **filters
        )
        df_result = (
            df_callable.groupby(iteration_path if not group_by else group_by)
            .agg(f.min(agg_column).alias(new))
            .orderBy(new)
        )
        return Detail(df_result, df_callable)

    def multiple_join(self, dfs: list, on: List[str], how: str = "left"):
        """
        Receives a list of dataframes and merges using the same column name between them.
        """
        previous = dfs[0]
        for df in dfs[1:]:
            merge = previous.join(df, on, how)
            previous = merge
        return merge

    def sum(
        self,
        df,
        ref: Union[str, list],
        iteration_path: str,
        new: str,
        literal_filter: List[str] = None,
        between_date: Dict[str, str] = None,
        group_by: List[str] = None,
        **filters,
    ):
        """
        After filtering a dataframe, perform the sum of the column as a reference.
        """
        agg_column, df_callable = self.__filters(
            df, ref, literal_filter, between_date, **filters
        )
        df_result = (
            df_callable.groupby(iteration_path if not group_by else group_by)
            .agg(f.sum(agg_column).alias(new))
            .orderBy(new)
        )
        return Detail(df_result, df_callable)

    def __filters(
        self,
        df,
        ref: Union[str, list],
        literal_filter: List[str] = None,
        between_date: Dict[str, str] = None,
        **filters,
    ):
        df_filter = self.__wrapper_filter(df, **filters)
        filter_between = self.__wrapper_between(between_date, df_filter)
        df_days = (
            self.__interpreter_literal_filter(filter_between, literal_filter)
            if literal_filter
            else filter_between
        )

        func, col1, col2 = ref if isinstance(ref, list) else [None, None, None]
        df_callable = (
            df_days.withColumn("temp", func(df_days[col1], df_days[col2]))
            if not isinstance(ref, str)
            else df_days
        )
        agg_column = ref if isinstance(ref, str) else "temp"
        return agg_column, df_callable

    def __interpreter_operator(self, temp_join, op: operator, left_ref, right_ref, new):
        accept = (
            "is_",
            "is_not",
            "add",
            "and_",
            "truediv",
            "floordiv",
            "mod",
            "mul",
            "pow",
            "sub",
            "ceil",
        )
        if op in accept:
            operators = {
                "is_": temp_join.withColumn(
                    new, temp_join[left_ref] == temp_join[right_ref]
                )
                if op == "is_"
                else None,
                "is_not": temp_join.withColumn(
                    new, temp_join[left_ref] != temp_join[right_ref]
                )
                if op == "is_not"
                else None,
                "add": temp_join.withColumn(
                    new, temp_join[left_ref] + temp_join[right_ref]
                )
                if op == "add"
                else None,
                "and_": temp_join.withColumn(
                    new, temp_join[left_ref] & temp_join[right_ref]
                )
                if op == "and_"
                else None,
                "truediv": temp_join.withColumn(
                    new, temp_join[left_ref] / temp_join[right_ref]
                )
                if op == "truediv"
                else None,
                "floordiv": temp_join.withColumn(
                    new, f.floor(temp_join[left_ref] / temp_join[right_ref])
                )
                if op == "floordiv"
                else None,
                "mod": temp_join.withColumn(
                    new, temp_join[left_ref] % temp_join[right_ref]
                )
                if op == "mod"
                else None,
                "mul": temp_join.withColumn(
                    new, temp_join[left_ref] * temp_join[right_ref]
                )
                if op == "mul"
                else None,
                "pow": temp_join.withColumn(
                    new, temp_join[left_ref] ** temp_join[right_ref]
                )
                if op == "pow"
                else None,
                "sub": temp_join.withColumn(
                    new, temp_join[left_ref] - temp_join[right_ref]
                )
                if op == "sub"
                else None,
                "ceil": temp_join.withColumn(
                    new, f.ceil(temp_join[left_ref] / temp_join[right_ref])
                )
                if op == "ceil"
                else None,
            }
            return operators.get(op)
        else:
            raise Exception(f"Operator {op} is not supported.")

    def __interpreter_literal_filter(self, df, expression: List[str]):
        accept = ("<", ">", ">=", "==", "<=", "!=")
        if expression:
            for exp in expression:
                expression_split = exp.split()
                col1, col2 = expression_split[0], expression_split[-1]
                validate = self.__validate_operator_dates(df, col1, col2)
                sig = [sig for sig in accept if sig in expression_split][0]
                operators = {
                    "<": df.filter(lt(df[col1], df[col2]))
                    if not validate
                    else df.filter(
                        lt(df[col1], (datetime.now() - relativedelta(days=int(col2))))
                    ),
                    ">": df.filter(gt(df[col1], df[col2]))
                    if not validate
                    else df.filter(
                        gt(df[col1], (datetime.now() - relativedelta(days=int(col2))))
                    ),
                    ">=": df.filter(ge(df[col1], df[col2]))
                    if not validate
                    else df.filter(
                        ge(df[col1], (datetime.now() - relativedelta(days=int(col2))))
                    ),
                    "==": df.filter(eq(df[col1], df[col2]))
                    if not validate
                    else df.filter(
                        eq(df[col1], (datetime.now() - relativedelta(days=int(col2))))
                    ),
                    "<=": df.filter(le(df[col1], df[col2]))
                    if not validate
                    else df.filter(
                        le(df[col1], (datetime.now() - relativedelta(days=int(col2))))
                    ),
                    "!=": df.filter(ne(df[col1], df[col2]))
                    if not validate
                    else df.filter(
                        ne(df[col1], (datetime.now() - relativedelta(days=int(col2))))
                    ),
                }
                df = operators.get(sig)
            return df

    def __validate_operator_dates(self, df, col1: str, col2: str):
        df_types = df.dtypes  # [('AreaPath', 'string'), ('CreatedDate', 'date'),...]
        is_numeric = True if col2.isnumeric() else False
        eq_col = [True for col in df_types if col[0] == col1][0]
        validate = True if is_numeric and eq_col else False
        return validate

    def __wrapper_between(self, between_date, df):
        be_created, be_closed = (
            self.__between_date(between_date) if between_date else [None, None]
        )
        filter_between = (
            df.where(
                (df[be_created.name] >= be_created.date)
                & (df[be_closed.name] <= be_closed.date)
            )
            if between_date
            else df
        )
        return filter_between

    @staticmethod
    def __isdifferent(items: List[str]):
        verify = [True if item[0:2] == "<>" else False for item in items]
        return verify

    @staticmethod
    def __clear_value(items: List[str]):
        return [item.replace("<>", "") for item in items]

    def __wrapper_filter(self, df, **filters):
        if filters:
            for key, value in filters["filters"].items():
                if isinstance(value, list):
                    hasdiff = self.__isdifferent(value)
                    if all(hasdiff):
                        df = df.where(~df[key].isin(self.__clear_value(value)))
                    elif True in hasdiff and False in hasdiff:
                        raise Exception(
                            "<> can only be used for all elements in the list."
                        )
                    else:
                        df = df.where(df[key].isin(value))
                else:
                    hasdiff = self.__isdifferent([value])
                    value = value.replace("<>", "")
                    if all(hasdiff):
                        df = df.filter(df[key] != value)
                    else:
                        if value == "null":
                            df = df.filter(df[key].isNull())
                        else:
                            df = df.filter(df[key] == value)
        return df

    @staticmethod
    def __between_date(between_date):
        if between_date:
            Bedate = namedtuple("BeDate", ["name", "date"])
            between = [item for item in between_date.items()]
            be_created = Bedate(between[0][0], f.lit(between[0][1]))
            be_closed = Bedate(between[1][0], f.lit(between[1][1]))
            return be_created, be_closed
        return [None, None]


class Detail:
    def __init__(self, df, detail):
        self.__dataframe = df
        self.__detail = detail

    @property
    def detail(self):
        """
        Returns the dataframe version before aggregation.
        """
        return self.__detail

    @property
    def df(self):
        """
        Returns the already aggregated dataframe.
        """
        return self.__dataframe
