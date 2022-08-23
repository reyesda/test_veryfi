# ==============================================
# Marcos Reyes
# Medellín-Colombia
# 23/08/2022
# ==============================================

import os


def is_there_a_file(path: str) -> bool:
    return os.path.exists(path)

def check_file_extension(path: str, extension: str) -> bool:
    return os.path.splitext(path)[1] == extension

def valid_path_file(path: str)-> bool:
    return is_there_a_file(path) and check_file_extension(path, '.txt')

def turn_all_elements_into_int(list_str: list)-> list:
    return list(map(lambda number: int(number), list_str))

def process_text_data(list_text: list, join_string: str)-> str:
    if len(list_text) > 1:
        list_text = join_string.join(list_text)
    else:
        list_text = list_text[0]
        
    return list_text

def read_file(path: str):
    all_data = []
    text = []
    with open(path, 'r') as file:
        for line in file:
            line = line.rstrip('\n').split(',')

            xn_and_yn = turn_all_elements_into_int(line[:8].copy())
            text_data = process_text_data(line[8:].copy(), ',')

            
            xn_and_yn.append(text_data)
            
            text.append(text_data)
            all_data.append(xn_and_yn)
        
        return all_data, text

def check_and_read(path: str):
    if valid_path_file(path):
        return read_file(path)

def get_all_files_by_extension(path: str, extension: str)-> list:
    return {file_name: path+"/"+file_name for file_name in os.listdir(path) if extension in file_name}