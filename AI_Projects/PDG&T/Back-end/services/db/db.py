import psycopg2
from env import Env
import indicators as ind

class DB:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(user=Env.get("USER"),
                                               password=Env.get("PASSWORD"),
                                               host=Env.get("HOST"),
                                               port=Env.get("PORT"),
                                               database=Env.get("DATABASE"))
        except Exception as e:
            # Password authentication
            print(e)


    def __get_list_of_db(self):
        try:
            result = DB().single_command_executer("SELECT datname FROM pg_database;", get_data=True)
            list_of_db = [tup[0] for tup in result]
            return list_of_db
        except Exception as e:
            print(e)
        

    def get_list_of_tables(self):
        try:
            result = DB().single_command_executer('''
                                                    SELECT table_name
                                                    FROM information_schema.tables
                                                    WHERE table_schema = 'public';
                                                    ''', get_data=True)
            if result:
                list_of_table = [tup[0] for tup in result]
                return list_of_table
            else:
                return []
        except Exception as e:
            print(e)


    def get_table_columns(self, table_name: str):
        try:
            result = DB().single_command_executer(f'''
                                                    SELECT column_name, data_type, is_nullable
                                                    FROM information_schema.columns
                                                    WHERE table_name = '{table_name}'
                                                    ORDER BY ordinal_position;
                                                    ''', get_data=True)
            if result:
                list_of_columns = [tup[0] for tup in result]
                return list_of_columns
            else:
                return False
        except Exception as e:
            print(e)


    def create_db(self, db_name: str):
        existing_db = self.__get_list_of_db()
        if db_name in existing_db:
            return "DB already Exist!"
        else:
            return DB().single_command_executer(f"CREATE DATABASE {db_name};", save_data=True)


    def single_command_executer(self, query: str, get_data: bool = False, save_data: bool = False):
        try:
            result = f"{ind.info_indicator} please specify the purpose of calling this function"

            if get_data or save_data:
                self.cursor = self.connection.cursor()
                self.cursor.execute(query)
                if get_data:
                    result = self.cursor.fetchall()
                elif save_data:
                    self.connection.commit()
                    result = f"{ind.success_indicator} Query executed Successfully"
                
                self.cursor.close()
            return result
            
        except Exception as e:
            return f"{ind.error_indicator} Error occur during query execution - {e}"
        

    def insert_multiple_records(self, table_name: str, records: list[tuple]):
        try:
            self.table_columns = self.get_table_columns(table_name)
            
            # Prepare the columns and placeholders
            columns_str = ', '.join(self.table_columns)
            placeholders = ', '.join(['%s'] * len(self.table_columns))

            self.cursor = self.connection.cursor()
            self.sql_insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

            # executemany() to insert multiple rows
            self.cursor.executemany(self.sql_insert_query, records)
            self.connection.commit()
            return f"{ind.success_indicator}  {self.cursor.rowcount} Record inserted successfully into {table_name} table"

        except (Exception, psycopg2.Error) as error:
            return f"{ind.fail_indicator}  Failed inserting record into {table_name} table - {error}"
        

    def delete_table_from_db(self, table_name: str):
        existing_tables = self.get_list_of_tables()
        if table_name in existing_tables:
            return DB().single_command_executer(f"DROP TABLE {table_name};", save_data=True)
        else:
            return f"{ind.fail_indicator}  Table Doesn't Exist!"
        

    def get_data_from_table(self, table_name: str, column_names: bool = False, query_with_filters = False):
        if query_with_filters:
            query: str = query_with_filters
        else:
            query: str = f"SELECT * FROM {table_name};"

        result = self.single_command_executer(query, get_data=True)
        print("data from table -->", result)

        if column_names:
            table_columns = self.get_table_columns(table_name)
            return table_columns, result
        else:
            return result
        
        
    def delete_data_from_table(self, table_name: str, delete_all_data :bool=False):
        if delete_all_data:
            return self.single_command_executer(f"DELETE FROM {table_name};", save_data=True)
        else:
            return "There is nothing to delete"