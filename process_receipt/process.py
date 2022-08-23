import re
from .read_file import process_text_data

def find_indexes_equal_character(block: list, element: str)-> list:
    return [index for index, text_element in enumerate(block) if  element == text_element]

def find_indexes_that_contain_character(block: list, element: str)-> list:
    return [index for index, text_element in enumerate(block) if  element in text_element]

def index_before_2_and_after_2(index:int)->list:
    return [index - 2, index - 1, index + 1, index + 2]

def get_line_item(text: list, index_x: int)-> list:
    return [text[index] for index in index_before_2_and_after_2(index_x)]

def split_block_by_index(block: list, start: int = None, end: int = None)-> list:
    return block[start:end]

def get_indexes_to_break_down_block(block: list)-> tuple:
    index_invoice = find_indexes_that_contain_character(block,'-INVOICE-')[0]
    index_item = find_indexes_that_contain_character(block, 'ITEM')[0]

    return index_invoice, index_item

def get_main_blocks(reference_block: list, target_block: list )-> list:
    index_invoice, index_item = get_indexes_to_break_down_block(reference_block)

    indexes = [None, index_invoice, index_item, None]
    blocks = []

    for index in range(len(indexes) - 1):
        blocks.append(split_block_by_index(target_block,start=indexes[index], end=indexes[index + 1]))

    return blocks

def get_all_line_items(line_items_block: list)-> list:
    indexes_x = find_indexes_equal_character(line_items_block, 'X')
    result = []

    for index in indexes_x:
        result.append(get_line_item(line_items_block, index))

    return result

def get_company_info(company_info_block: list)-> tuple:
    index_company_registration = find_indexes_that_contain_character(block=company_info_block, element="CO.")[0]

    company_name = split_block_by_index(company_info_block, 1, index_company_registration)
    company_name = process_text_data(company_name, ' ')

    address_lines = split_block_by_index(company_info_block, index_company_registration + 1)
    address_lines = process_text_data(address_lines, ' ')

    return company_name, address_lines

def get_total(totals_block: list)-> str:
    total_rounded_index = find_indexes_that_contain_character(totals_block, 'ROUNDED')[0]
    total = totals_block[total_rounded_index + 1]
    return total.split(' ')[1]

def get_date(date_block: list)-> str:
    pattern = re.compile("[0-9][0-9]-[0-9][0-9]-[0-9][0-9]")

    for i in date_block:
        find = re.search(pattern, i)
        if find:
            return find.group()