from database import InsertUpdate
from utils.var_global import VarGlobal


class PopulateTable:
    def __init__(self):
        self.connection = VarGlobal.DATABASE_NAME
        self.origin_table = VarGlobal.TABLE_METADATA_PREMAP
        self.destination_table = VarGlobal.TABLE_METADATA_MAP

    def populate_premap_with_map(self):
        db = InsertUpdate(self.connection)
        db.update_premap_with_map(self.destination_table, self.origin_table)
