from openpyxl.workbook.workbook import Workbook
from .base import BaseComparer, ReadOnlyCellTypes, SearchCellDefinition


class DataTypeCompare(BaseComparer):
    def __init__(self, weigth: int = 1):
        super().__init__(weigth=weigth)

    def _compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCellDefinition
    ) -> int:
        return 0 if cell.data_type == search_cell.data_type else 100
