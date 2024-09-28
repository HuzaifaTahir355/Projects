from services.db.db import DB
import indicators as ind

class DBHandlerSettings:
    def __init__(self):
        self.table_name = "settings"

    # output_format = [(800, 'BAAI/bge-large-en-v1.5', 1024, 'Milvus', False, 'meta-llama/Llama-3-70b-chat-hf')]
    def get_setted_chunk_size(self):
        all_settings = self.get_settings_data_from_db()
        if all_settings:
            return all_settings[0][0]
        return 0


    def get_setted_embedding_model(self):
        all_settings = self.get_settings_data_from_db()
        if all_settings:
            return all_settings[0][1]
        return ""
    

    def get_embedding_model_dimension(self):
        all_settings = self.get_settings_data_from_db()
        if all_settings:
            return all_settings[0][2]
        return 0


    def get_setted_vector_store_name(self):
        all_settings = self.get_settings_data_from_db()
        if all_settings:
            return all_settings[0][3]
        return ""


    def get_setted_llm(self):
        all_settings = self.get_settings_data_from_db()
        if all_settings:
            return all_settings[0][5]
        return ""


    def get_settings_data_from_db(self, is_column_name_required: bool = False):
        return DB().get_data_from_table(self.table_name, column_names=is_column_name_required)


    def create_settings_table(self):
        existing_tables = DB().get_list_of_tables()
        if self.table_name not in existing_tables:
            create_table_query = f'''
            CREATE TABLE {self.table_name} (
            chunk_size INT,
            embedding_model VARCHAR,
            embedding_model_dimensions INT,
            vector_store VARCHAR,
            is_image_required Boolean,
            selected_llm VARCHAR
            ); '''
            result = DB().single_command_executer(create_table_query, save_data=True)
            return result
        else:
            return f"{ind.fail_indicator} Table already exists!"
        

    def save_settings_in_db(self, data: list):
        try:
            columns_of_table = DB().get_table_columns(self.table_name)
            if columns_of_table:
                # First delete the previous data to store only one record
                self.delete_all_data()
                return DB().insert_multiple_records(self.table_name, data)
            else:
                return f"{ind.fail_indicator} Columns of {self.table_name} are not found"
        except Exception as e:
            print(e)


    def delete_all_data(self):
        return DB().delete_data_from_table(self.table_name, delete_all_data=True)
    

    def delete_table_from_db(self):
        return DB().delete_table_from_db(self.table_name)

