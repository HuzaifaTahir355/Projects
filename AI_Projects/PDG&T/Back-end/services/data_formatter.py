
class DataFormatter:
    def db_response_to_list_of_dicts(self, table_column_names: list[tuple], db_response_data: list[tuple]):
        formated_data: list = []
        inner_dict: dict  = {}
        for row in db_response_data:
            if len(row) == len(table_column_names):
                for i, column_name in enumerate(table_column_names):
                    inner_dict[column_name] = row[i]
                formated_data.append(inner_dict)
                inner_dict = {}
            else:
                continue
        
        return formated_data
    
    
    def db_response_with_single_value_to_list_of_strings(self, db_response_data: list[tuple]):
        formated_data: list = []
        for row in db_response_data:
            formated_data.append(row[0])
        return formated_data