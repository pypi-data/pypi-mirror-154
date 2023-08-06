from openpyxl.workbook.workbook import Workbook
from openpyxl.styles.borders import Side as oxlSide
from .base import BaseComparer, ReadOnlyCellTypes, SearchCellDefinition


class BorderExistanceCompare(BaseComparer):
    def __init__(self, weigth: int = 1):
        super().__init__(weigth=weigth)

    def _compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCellDefinition
    ) -> int:

        if cell.border is None and search_cell.border is None:
            return 0
        elif cell.border is not None and search_cell.border is None:
            return 100
        elif cell.border is None and search_cell.border is not None:
            return 100

        res = 100
        num_sides = 4
        decrement_value = int(res / num_sides)

        if self._compare_side(cell.border.top, search_cell.border.top):  # type: ignore
            res -= decrement_value

        if self._compare_side(cell.border.bottom, search_cell.border.bottom):  # type: ignore
            res -= decrement_value

        if self._compare_side(cell.border.left, search_cell.border.left):  # type: ignore
            res -= decrement_value

        if self._compare_side(cell.border.right, search_cell.border.right):  # type: ignore
            res -= decrement_value

        return res

    def _compare_side(self, side: oxlSide, search_side: oxlSide) -> bool:
        if side.style is None and search_side.style is None:  # type: ignore
            return True
        elif side.style is not None and search_side.style is not None:  # type: ignore
            return True
        return False
