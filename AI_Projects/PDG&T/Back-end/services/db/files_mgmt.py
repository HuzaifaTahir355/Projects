from services.db.db import DB
from services.db.settings import DBHandlerSettings
import indicators as ind

class DBHandlerFM:
    def __init__(self):
        self.table_name = "files"
        

    def get_files_from_db(self):
        return DB().get_data_from_table(self.table_name,
                                        query_with_filters="SELECT key,name,type,path FROM files;")


    def create_files_table(self):
        existing_tables = DB().get_list_of_tables()
        if "files" not in existing_tables:
            create_table_query = f'''
            CREATE TABLE {self.table_name} ( 
            key VARCHAR(255) PRIMARY KEY,  
            name VARCHAR(100) NOT NULL,
            type VARCHAR(50) NOT NULL,
            size VARCHAR(50) NOT NULL,
            path VARCHAR(500) NOT NULL,
            updation_date DATE NOT NULL,
            vector_store_name VARCHAR(50) NOT NULL
            ); '''
            result = DB().single_command_executer(create_table_query, save_data=True)
            return result
        else:
            return f"{ind.fail_indicator} Table already exists!"
    
    
    def delete_all_data(self):
        return DB().delete_data_from_table(self.table_name, delete_all_data=True)
    

    def store_data_in_db(self, data: list):
        try:
            columns_of_table = DB().get_table_columns(self.table_name)
            if columns_of_table:
                return DB().insert_multiple_records(self.table_name, data)
            else:
                return f"{ind.fail_indicator} Columns of {self.table_name} are not found"
        except Exception as e:
            print(e)


    def get_data_from_table(self, column_names=True):
        vector_store    :str  = DBHandlerSettings().get_setted_vector_store_name()
        query: str = f"SELECT * FROM {self.table_name} WHERE vector_store_name = '{vector_store}';"
        table_columns, db_data = DB().get_data_from_table('files', column_names=column_names, query_with_filters=query)
        return table_columns, db_data