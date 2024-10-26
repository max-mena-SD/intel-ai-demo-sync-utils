import sqlite3
from database.select_db import SelectDB
from utils.var_global import VarGlobal
from utils.util_func import UtilFunc


class JsonElaboration:

    def get_header_json(
        self,
        first_table_name: str,
        second_table_name: str,
        first_key: str,
        second_key: str,
        where: str,
    ) -> tuple:
        db_instance = SelectDB(VarGlobal.DATABASE_NAME)

        metadata = db_instance.select_one_join_where(
            first_table_name, second_table_name, first_key, second_key, where
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
        json_element["imageUrl"] = metadata[3] if metadata[3] else "null"
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

    def json_sql_element(self):
        first_table_name = "metadata_map"
        second_table_name = "processed_demos_control"
        first_key = "id_name"
        second_key = "demo_id"
        where = 'b.demo_id is NULL OR ( b.demo_id is not null AND a.status = "latest")'
        metadata = self.get_header_json(
            first_table_name, second_table_name, first_key, second_key, where
        )

        metadata_tags = self.get_body_json(metadata[0])
        metadata_tags_dict = UtilFunc().list_tuple_to_dict(metadata_tags)

        # print(metadata_tags_dict)

        json_element = self.build_json_element(metadata, metadata_tags_dict)
        print(type(json_element), "\n", json_element)

        """
        At this point the program creates based on the information from the database a dictionary
        with the first element of the table metadata_map, something needs to be implemented to 
        have the the program going over all the elements of the table metadata_map that also have
        information in the table metadata_tags_map.

        After having the way to go over the elements of both table and create a dictionary based off them
        the next step is to create a json file with the information of the dictionary created
        research if the file should be constructed step by step or if is better to create the whole thing
        at once.
        """
