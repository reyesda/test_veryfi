from .read_file import check_and_read
from .process import get_main_blocks, get_all_line_items, get_company_info, get_total, get_date

class Item:
    def __init__(self, properties: list) -> None:
        self.sku: str = properties[0]
        self.quantity: str = properties[1]
        self.price: str = properties[2]
        self.total: str = properties[3]

    def __repr__(self) -> str:
        return str(vars(self))
    
    def result(self)-> dict:
        return vars(self)


class Receipt:
    _list_only_text: list = []
    _list_all_data: list = []
    _main_blocks: list = []

    company: str = ''
    date: str = ''
    address: str = ''
    line_items: list = []
    total: str = []

    def __init__(self, file_path: str) -> None:
        self._list_all_data, self._list_only_text = check_and_read(file_path)
        self._main_blocks = get_main_blocks(self._list_only_text, self._list_only_text)
        self.company, self.address = get_company_info(self._main_blocks[0])
        self.total = get_total(self._main_blocks[2])
        self.date = get_date(self._main_blocks[2])
        self.line_items = self._fill_out_line_items(get_all_line_items(self._main_blocks[1]))

    @staticmethod
    def _fill_out_line_items(list_items: list)-> list:
        items = []
        for item in list_items:
            items.append(Item(item))

        return items

    def __repr__(self) -> str:
        final = {}
        for key, value in vars(self).items():
            if not '__' in key:
                final[key] = value

        return str(final)

    def __getitem__(self, index)-> str:
        return self.line_items[index]

    def get_all_list_info_blocks(self)-> list:
        return get_main_blocks(self._list_only_text, self._list_all_data)
    
    def get_max(self)-> tuple:
        max_pixel_y = 0
        max_pixel_x = 0

        for list_elements in self._list_all_data:
            max_pixel_x = max([list_elements[4], max_pixel_x])
            max_pixel_y = max([list_elements[5], max_pixel_y])

        return (max_pixel_x, max_pixel_y)