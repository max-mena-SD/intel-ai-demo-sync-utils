from classfier.llm_sum_model import LLMSumModel
from database.select_db import SelectDB
from database.insert_update import InsertUpdate
from utils.var_global import VarGlobal

import re


class AddSummary:

    def __init__(self):
        self.summarizar = LLMSumModel()
        self.db_instance = SelectDB(VarGlobal.DATABASE_NAME)

    def eliminate_special_characters(self, text: str) -> str:
        text = re.sub(
            r"(^#{1,6}\s+)|(\*{1,2}|\_{1,2})|(`[^`]+`)|(^[-*+]|\d+\.)|(^\s{4,})",
            " ",
            text,
        )
        return text

    def eliminate_link_info(self, text: str) -> str:
        text = re.sub(r"\[.*?\]\(.*?\)", "", text)
        return text

    def get_one_premap(self, platform: str) -> tuple:
        tup_reg = self.db_instance.select_one_where(
            VarGlobal.TABLE_METADATA_PREMAP,
            f"lower(platform) = '{platform}' AND summary IS NULL",
        )
        return tup_reg

    def summarize_openvino(self, tup_reg: tuple) -> dict:

        dict_reg = {}
        description = self.eliminate_special_characters(tup_reg[3])
        summary = self.summarizar.to_sumarize(description)

        if summary == "":
            other = self.eliminate_link_info(description)
            summary = self.summarizar.to_sumarize(other)

        dict_reg[tup_reg[0]] = summary

        return dict_reg

    def update_premap_summary(self, summary: dict):
        update = InsertUpdate(VarGlobal.DATABASE_NAME)
        table_name = VarGlobal.TABLE_METADATA_PREMAP
        key_name = VarGlobal.METADATA_PREMAP_PK
        field_name = VarGlobal.METADATA_PREMAP_SUMMARY
        key_value = next(iter(summary))
        value_set = summary[key_value]
        update.update_one_where(table_name, key_name, field_name, key_value, value_set)

    def process_all_summary(self, platform: str) -> None:
        tup_reg = self.get_one_premap(platform)
        while tup_reg:
            if not tup_reg:
                break
            dict_summary = self.summarize_openvino(tup_reg)
            self.update_premap_summary(dict_summary)
            tup_reg = self.get_one_premap(platform)
