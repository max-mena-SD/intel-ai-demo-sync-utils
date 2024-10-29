# standard libraries
import ast
import json
import os

# local modules
from database.select_db import SelectDB
from database.insert_update import InsertUpdate
from utils.var_global import VarGlobal
from utils.util_func import UtilFunc


class JsonElaboration:

    def __init__(self) -> None:
        # self.header_query_map_ERASE = {
        #     "first_table_name": "metadata_map",
        #     "second_table_name": "processed_demos_control",
        #     "first_key": "id_name",
        #     "second_key": "demo_id",
        #     "where": 'b.demo_id is NULL OR ( b.demo_id is not null AND a.status = "latest")',
        # }
        self.header_query_map = {
            "first_table_name": "metadata_map",
            "second_table_name": "json_formatted_data",
            "first_key": "id_name",
            "second_key": "id_name",
            "where": 'b.id_name is NULL OR ( b.id_name is not null AND b.status = "completed")',
        }

    def get_header_json(self, header_query_map: dict) -> tuple:
        db_instance = SelectDB(VarGlobal.DATABASE_NAME)

        metadata = db_instance.select_one_join_where(
            header_query_map["first_table_name"],
            header_query_map["second_table_name"],
            header_query_map["first_key"],
            header_query_map["second_key"],
            header_query_map["where"],
        )

        return metadata

    def build_json_element(self, metadata: tuple, metadata_tags: list) -> dict:
        json_element = {
            "title": None,
            "path": None,
            "imageUrl": None,
            "createdDate": None,
            "modifiedDate": None,
            "links": {
                "github": None,
                "docs": None,
                "colab": None,
                "binder": None,
            },
            "tags": {"categories": [], "tasks": [], "libraries": [], "other": []},
        }
        # header information
        json_element["title"] = metadata[1]
        json_element["path"] = metadata[2]
        json_element["imageUrl"] = metadata[3] if metadata[3] else None
        json_element["createdDate"] = metadata[4]
        json_element["modifiedDate"] = metadata[5]
        json_element["links"]["github"] = metadata[6]

        # Process tags
        for category_name, tag_name in metadata_tags.items():

            if category_name == "industry":
                json_element["tags"]["categories"] = tag_name
            elif category_name == "type":
                json_element["tags"]["tasks"] = tag_name
            elif category_name == "platform_tools":
                json_element["tags"]["libraries"] = tag_name
            elif category_name == "technology":
                json_element["tags"]["other"] = tag_name
            elif category_name == "use_case_functionality":
                json_element["tags"]["other"].extend(tag_name)

        json_element["tags"]["libraries"].append(metadata_tags["complexity_level"][0])

        return json_element

    # metadata[0]
    def get_body_json(self, id_name: str) -> list:
        db_instance = SelectDB(VarGlobal.DATABASE_NAME)

        metadata_tags = db_instance.select_tags_demo(id_name)

        return metadata_tags

    def json_sql_element(self) -> dict:
        metadata = self.get_header_json(self.header_query_map)
        metadata_tags = self.get_body_json(metadata[0])
        metadata_tags_dict = UtilFunc().list_tuple_to_dict(metadata_tags)

        json_element = self.build_json_element(metadata, metadata_tags_dict)
        return json_element

    def save_json_to_db(self, id_name: str, sql_result: dict) -> bool:

        db_instance = InsertUpdate(VarGlobal.DATABASE_NAME)
        inserted = db_instance.insert_dict_json(id_name, sql_result)

        return inserted

    def save_to_file_json(self, dict_json: list):

        json_file = os.path.join(VarGlobal.DATA_JSON_FOLDER, VarGlobal.DATA_JSON_NAME)
        with open(json_file, "w") as f:

            f.write("[\n")
            first_registry = True

            for tuple_info in dict_json:
                if not first_registry:
                    f.write(",\n")
                else:
                    first_registry = False

                dict_info = ast.literal_eval(tuple_info[1])
                line = f"{json.dumps(dict_info, indent=4)}"
                f.write(line)
            f.write("\n]")

    def sql_to_json_builder(self):

        inserted = True
        metadata = self.get_header_json(self.header_query_map)

        while metadata and inserted:
            id_name = metadata[0]
            dict_sql = self.json_sql_element()
            inserted = self.save_json_to_db(id_name, dict_sql)
            metadata = self.get_header_json(self.header_query_map)

        db = SelectDB(VarGlobal.DATABASE_NAME)
        dict_json = db.select_all(VarGlobal.TABLE_JSON_FORMATTED_DATA)
        self.save_to_file_json(dict_json)

        db = InsertUpdate(VarGlobal.DATABASE_NAME)
        db.update_json_formatted_data()
        # necesito consultar lo que tiene json_formatted_data para nviarlo a
        # self.add_to_json()
        # self.insert_processed_demos_control(id_name, )
