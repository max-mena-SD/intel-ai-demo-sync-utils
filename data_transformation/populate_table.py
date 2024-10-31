from database import InsertUpdate
from utils.var_global import VarGlobal


class PopulateTable:
    def __init__(self):
        self.connection = VarGlobal.DATABASE_NAME
        self.origin_table = VarGlobal.TABLE_METADATA_PREMAP
        self.destination_table = VarGlobal.TABLE_METADATA_MAP

    def populate_map_with_premap(self):
        db = InsertUpdate(self.connection)
        db.update_map_with_premap(self.destination_table, self.origin_table)

    def populate_map_with_youtube(self):
        origin_table = VarGlobal.# Define if there is going to be a table specific to youtube
        db = InsertUpdate(self.connection)
        db.update_map_with_table(self.destination_table, origin_table)
        pass
