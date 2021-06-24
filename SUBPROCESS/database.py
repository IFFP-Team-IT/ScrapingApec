from pymongo import MongoClient
from SUBPROCESS import scr_hlp

mg_db = "IFFP-EXTRAPEC"
conn = MongoClient("mongodb://127.0.0.1:27017")
database = conn[mg_db]


class DB:
    SAVE_ON = True
    @staticmethod
    def does_id_exists_in_DB(id_profil):
        if not DB.SAVE_ON:
            scr_hlp.scr_hlp.print_if_DEBUG("DB.SAVE_ON is False. So program is not fetching data")
            return
        nb_profile_id = database.main.find({'_id': id_profil}).count()
        nb_other_docId = database.main.find({'id': id_profil}).count()
        scr_hlp.scr_hlp.pause_if_EXTRADEBUG(f"I fund {nb_profile_id}")
        if nb_profile_id != 0 or nb_other_docId != 0:
            scr_hlp.scr_hlp.pause_if_EXTRADEBUG("profile" + id_profil + " exists.")
            return True
        scr_hlp.scr_hlp.pause_if_EXTRADEBUG("profile" + id_profil + " not exists")
        return False
    @staticmethod
    def replaceq(string):
        return string.replace("'", "''")


    # def create_table_in_json(file, list_sheets, table):
    #     for sheet in list_sheets:
    #         data = pd.read_excel(file, sheet_name=table)
    #         json_str = data.to_json(orient='records')
    #     return json_str

    @staticmethod
    def addtoDB(columns_lst, values_lst, dtable):
        if not DB.SAVE_ON:
            scr_hlp.scr_hlp.print_if_DEBUG("DB.SAVE_ON is False. So program is not saving data")
            return
        #database[dtable].initializeUnorderedBulkOp()
        dict_element = dict(zip(columns_lst, values_lst))
        result = database[dtable].insert(dict_element)
        
        #count = len(dict_element)
        scr_hlp.scr_hlp.pause_if_EXTRADEBUG(f"{result}Record inserted successfully into mobile table in {database}")
        conn.close()


