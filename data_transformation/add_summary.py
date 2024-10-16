from classfier.llm_sum_model import LLMSumModel
from database.select_db import SelectDB
from utils.var_global import VarGlobal


class AddSummary:

    def __init__(self):
        self.summarizar = LLMSumModel()
        self.db_instance = SelectDB(VarGlobal.DATABASE_NAME)

    def summarize_openvino(self):

        dict_reg = {}

        tup_reg = self.db_instance.select_one_where(
            VarGlobal.TABLE_METADATA_PREMAP, "lower(platform) = 'openvino'"
        )
        summary = self.summarizar.to_sumarize(tup_reg[3])

        dict_reg[tup_reg[0]] = summary

        return dict_reg
