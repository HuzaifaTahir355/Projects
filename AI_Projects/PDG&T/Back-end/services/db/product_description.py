from services.db.db import DB
import indicators as ind

class DBHandlerPD:
    def __init__(self):
        self.table_name = "product_description"


    def get_product_description_data_from_db(self):
        return DB().get_data_from_table(self.table_name)


    def create_product_description_table(self):
        existing_tables = DB().get_list_of_tables()
        if self.table_name not in existing_tables:
            create_table_query = f'''
            CREATE TABLE {self.table_name} ( 
            raw_data VARCHAR NOT NULL
            ); '''
            result = DB().single_command_executer(create_table_query, save_data=True)
            return result
        else:
            return f"{ind.fail_indicator} Table already exists!"
        

    def store_data_in_db(self, data: list):
        try:
            columns_of_table = DB().get_table_columns(self.table_name)
            if columns_of_table:
                return DB().insert_multiple_records(self.table_name, data)
            else:
                return f"{ind.fail_indicator} Columns of {self.table_name} are not found"
        except Exception as e:
            print(e)


    def delete_all_data(self):
        return DB().delete_data_from_table(self.table_name, delete_all_data=True)
