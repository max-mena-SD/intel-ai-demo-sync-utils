from classfier.mnli_label_model import MnliLabelModel
from database.insert_update import InsertUpdate
from utils.var_global import VarGlobal


class AddLabels:

    def get_one_map(self) -> tuple:

        db_name = VarGlobal.DATABASE_NAME
        first_table_name = VarGlobal.TABLE_METADATA_PREMAP
        second_table_name = VarGlobal.TABLE_METADATA_MAP
        id_key = VarGlobal.METADATA_PREMAP_PK
        where = "a.summary is not NULL AND b.id_name is NULL"

        dict_premap = SelectDB(db_name).select_one_join_where(
            first_table_name, second_table_name, id_key, where
        )

        return dict_premap

    def get_info_label(self) -> dict:

        dict_premap = self.get_one_map()
        dict_classification = MnliLabelModel().insert_label_info(dict_premap)
        return dict_classification

    def save_label_info(self) -> None:
        insert = InsertUpdate(VarGlobal.DATABASE_NAME)
        pass
        # connects to database and save the labels based in the results of the model
