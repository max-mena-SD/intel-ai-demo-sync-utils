from classfier.mnli_label_model import MnliLabelModel
from database.insert_update import InsertUpdate
from database.select_db import SelectDB
from utils.var_global import VarGlobal


class AddLabels:

    def get_one_map(self) -> tuple:

        db_name = VarGlobal.DATABASE_NAME
        first_table_name = VarGlobal.TABLE_METADATA_PREMAP
        second_table_name = VarGlobal.TABLE_METADATA_MAP
        id_key = VarGlobal.METADATA_PREMAP_PK
        where = "a.summary is not NULL AND b.id_name is NULL"

        dict_premap = SelectDB(db_name).select_one_join_where(
            first_table_name, second_table_name, id_key, id_key, where
        )

        return dict_premap

    def get_one_summary(self) -> tuple:

        db_name = VarGlobal.DATABASE_NAME
        first_table_name = VarGlobal.TABLE_METADATA_PREMAP
        first_key = VarGlobal.METADATA_PREMAP_PK

        second_table_name = VarGlobal.TABLE_METADATA_TAGS_MAP
        second_key = VarGlobal.METADATA_TAGS_MAP_PK

        where = "a.summary is not NULL AND b.metadata_id is NULL"

        dict_premap = SelectDB(db_name).select_one_join_where(
            first_table_name, second_table_name, first_key, second_key, where
        )

        return dict_premap

    def get_info_label(self, summary: str) -> dict:
        dict_classification = MnliLabelModel().insert_label_info(summary)
        return dict_classification

    def save_label_database(
        self, foreign_key: str, category: str, tag_list: dict
    ) -> None:
        InsertUpdate(VarGlobal.DATABASE_NAME).insert_tags_map(
            foreign_key, category, tag_list
        )

    def save_label_info(self, summary: dict) -> None:
        dict_premap = summary
        label_info = self.get_info_label(dict_premap[3])
        foreign_key = dict_premap[0]

        for key, value in label_info.items():
            self.save_label_database(foreign_key, key, value)

    def source_all_labels(self) -> None:
        summary = self.get_one_summary()

        while summary:
            self.save_label_info(summary)
            summary = self.get_one_summary()

        # connects to database and save the labels based in the results of the model
