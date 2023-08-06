from abc import ABC, abstractmethod
from typing import Callable, Optional, Union
from dataclasses import dataclass, field
from openpyxl.styles import Color as oxlColor
from openpyxl.styles.borders import Border as oxlBorder
from openpyxl.styles.borders import Side as oxlSide
from openpyxl.styles.alignment import Alignment as oxlAlignment
from openpyxl.styles.fonts import Font as oxlFont

from openpyxl.cell.read_only import ReadOnlyCell, EmptyCell

ReadOnlyCellTypes = Union[ReadOnlyCell, EmptyCell]


def init_oxlBorder(
    left=None,
    right=None,
    top=None,
    bottom=None,
    diagonal=None,
    diagonal_direction=None,
    vertical=None,
    horizontal=None,
    diagonalUp=False,
    diagonalDown=False,
    outline=True,
    start=None,
    end=None,
) -> oxlBorder:
    if right is None:
        right = oxlSide()
    if left is None:
        left = oxlSide()
    if top is None:
        top = oxlSide()
    if bottom is None:
        bottom = oxlSide()
    return oxlBorder(
        left=left,
        right=right,
        top=top,
        bottom=bottom,
        diagonal=diagonal,
        diagonal_direction=diagonal_direction,  # type: ignore
        vertical=vertical,  # type: ignore
        horizontal=horizontal,  # type: ignore
        diagonalUp=diagonalUp,
        diagonalDown=diagonalDown,
        outline=outline,
        start=start,  # type: ignore
        end=end,  # type: ignore
    )


def init_oxlAlignment(
    horizontal=None,
    vertical=None,
    textRotation=0,
    wrapText=None,
    shrinkToFit=None,
    indent=0,
    relativeIndent=0,
    justifyLastLine=None,
    readingOrder=0,
    text_rotation=None,
    wrap_text=None,
    shrink_to_fit=None,
    mergeCell=None,
):

    return oxlAlignment(
        horizontal=horizontal,
        vertical=vertical,
        textRotation=textRotation,
        wrapText=wrapText,
        shrinkToFit=shrinkToFit,
        indent=indent,
        relativeIndent=relativeIndent,
        justifyLastLine=justifyLastLine,
        readingOrder=readingOrder,
        text_rotation=text_rotation,
        wrap_text=wrap_text,
        shrink_to_fit=shrink_to_fit,
        mergeCell=mergeCell,
    )


def init_oxlFont(
    name=None,
    sz=11.0,
    b=True,
    i=False,
    charset=None,
    u=None,
    strike=None,
    color=None,
    scheme=None,
    family=None,
    size=None,
    bold=None,
    italic=None,
    strikethrough=None,
    underline=None,
    vertAlign=None,
    outline=None,
    shadow=None,
    condense=None,
    extend=None,
):

    return oxlFont(
        name=name,
        sz=sz,  # type: ignore
        b=b,
        i=i,
        charset=charset,
        u=u,
        strike=strike,
        color=color,
        scheme=scheme,
        family=family,
        size=size,
        bold=bold,
        italic=italic,
        strikethrough=strikethrough,
        underline=underline,
        vertAlign=vertAlign,
        outline=outline,
        shadow=shadow,
        condense=condense,
        extend=extend,
    )


@dataclass
class SearchCellDefinition:
    fill_color: Optional[oxlColor] = None
    data_type: str = "s"
    border: Optional[oxlBorder] = field(default_factory=init_oxlBorder)
    value: Optional[Union[str, int, float]] = None
    alignment: Optional[oxlAlignment] = field(default_factory=init_oxlAlignment)
    font: Optional[oxlFont] = field(default_factory=init_oxlFont)


class BaseComparer(ABC):
    def __init__(self, weigth: int):
        self.weigth = weigth

    def compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCellDefinition
    ) -> int:
        return self.weigth * self._compare(cell, search_cell)

    @abstractmethod
    def _compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCellDefinition
    ) -> int:
        pass


class CombinedComparer:
    def __init__(self, *args: BaseComparer):
        self.total_weigth = sum(comparer.weigth for comparer in args)
        self.comparers = list(args)

    def compare(
        self, cell: ReadOnlyCellTypes, search_cell: SearchCellDefinition
    ) -> int:

        res = sum(comparer.compare(cell, search_cell) for comparer in self.comparers)
        res_scaled = int(res / self.total_weigth)

        return res_scaled
