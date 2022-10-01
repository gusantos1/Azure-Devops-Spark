from datetime import datetime, date
from typing import List
from pyspark.sql.types import (
    BooleanType,
    DateType,
    DoubleType,
    IntegerType,
    StringType,
    StructField,
)


class Process:
    @classmethod
    def columns(cls, data: dict, fields_column: dict, fields_display: dict) -> dict:
        """
        Receives a dictionary with the data of a work item and returns the data with the selected fields.
        """
        fields = [
            {column.name: data[tag]["displayName"]}
            if tag in fields_display and tag in data
            else ({column.name: data[tag]} if tag in data else {column.name: None})
            for tag, column in fields_column.items()
        ]

        date_type_fields = [
            schema.name
            for name, schema in fields_column.items()
            if schema.dataType == DateType()
        ]
        schema_convert_date = [
            {name: cls.datetime_to_date(schema)}
            if name in date_type_fields and schema != None
            else {name: schema}
            for item in fields
            for name, schema in item.items()
        ]
        item = {}
        for value in schema_convert_date:
            for column, tag in value.items():
                item[column] = tag
        return item

    @classmethod
    def teams(cls, response: dict) -> List[dict]:
        """
        Receives data from all squads and returns `name and id`.
        """
        comprehension = [
            {
                "Squad": values["name"],
                "Id": values["id"],
            }
            for values in response["value"]
        ]
        return comprehension

    @classmethod
    def team_backlog(cls, response: dict) -> List[int]:
        """
        Receives a dictionary and returns a list of ids.
        """
        ids = []
        for list_value in response.values():
            for value in list_value:
                id = str(value["target"]["id"])
                ids.append(id)
        return ids

    @classmethod
    def team_interation(cls, response: dict, squad: str) -> List[dict]:
        """
        Receives a dictionary and returns a list of iteration information.
        """
        comprehension = [
            {
                "Iteration_Id": values["id"],
                "Iteration_Name": values["name"],
                "Iteration_Path": values["path"],
                "Iteration_Start_Date": cls.datetime_to_date(
                    values["attributes"]["startDate"]
                )
                if values["attributes"]["startDate"]
                else None,
                "Iteration_End_Date": cls.datetime_to_date(
                    values["attributes"]["finishDate"]
                )
                if values["attributes"]["finishDate"]
                else None,
                "Iteration_State": values["attributes"]["timeFrame"],
                "Squad": squad,
            }
            for values in response["value"]
        ]
        return comprehension

    @classmethod
    def members(cls, response: dict, squad: str) -> List[dict]:
        """
        Receives a dictionary and the name of a squad and returns a list of all squad members.
        """
        members = []
        for value in response["value"]:
            info = value["identity"]
            member = {"Name": info["displayName"], "Id": info["id"], "squad": squad}
            members.append(member)
        return members

    @staticmethod
    def datetime_to_date(str_datetime: str) -> date:
        """
        Receives a datetime in string and turns it into a date object.
        """
        date = str_datetime[: str_datetime.find("T")]
        return datetime.fromisoformat(date).date()

    @classmethod
    def tags(cls, response: dict) -> List[dict]:
        """
        Receives a dictionary and returns a list comprehension of all tags and their ids.
        """
        return [{"Id": item["id"], "Name": item["name"]} for item in response["value"]]

    @classmethod
    def all_process(cls, response: dict) -> List[dict]:
        """
        Receives a dictionary and returns a list of dict with process id and value.
        [{'id':...,'name': Basic}]
        """
        return [
            {"id": values["typeId"], "name": values["name"]}
            for values in response["value"]
        ]

    @classmethod
    def all_work_items(cls, response: dict) -> List[dict]:
        """
        Receives a dictionary and returns only the item id.
        """
        return [values["id"] for values in response["value"]]

    @classmethod
    def clean_fields(cls, response: dict) -> List[dict]:
        """
        Receives a dictionary with the process fields and returns only the referenceName, name and type.
        [ {'referenceName':'System.Tag', 'name':'Tag', 'type': 'string'},... ]
        """
        return [
            {
                "referenceName": values["referenceName"],
                "name": values["name"],
                "type": values["type"],
            }
            for values in response["value"]
        ]

    @classmethod
    def spark_equivalent(cls, fields: list) -> List[dict]:
        schema = {}
        spark_types = {
            "string": StringType(),
            "integer": IntegerType(),
            "double": DoubleType(),
            "boolean": BooleanType(),
            "html": StringType(),
            "dateTime": DateType(),
        }
        for item in fields:
            ref_name = item["referenceName"]
            name = item["referenceName"].split(".")[-1]
            type_field = spark_types.get(item["type"])
            field = StructField(name, type_field)
            schema[ref_name] = field
        return schema
