from __future__ import annotations

from typing import TYPE_CHECKING

from dask_awkward.io import from_json

if TYPE_CHECKING:
    from ..core import DaskAwkwardArray


def load_nested() -> DaskAwkwardArray:
    return from_json(json_data(kind="records"))


def load_array() -> DaskAwkwardArray:
    return from_json(json_data(kind="numbers"))


def json_data(kind: str = "numbers") -> list[str]:
    if kind == "numbers":
        return _numbers()
    elif kind == "records":
        return _records()
    raise ValueError(f"kind ({kind}) must be 'numbers' or 'records'")


def _records() -> list[str]:
    a1 = """
    [
        {
            "analysis": {
                "x1": [1, 2, 3],
                "y1": [2, 3, 4],
                "z1": [2, 6, 6],
                "t1": [7, 8, 9],
                "x2": [],
                "y2": [],
                "z2": [],
                "t2": []
            }
        },
        {
            "analysis": {
                "x1": [1, 2],
                "y1": [2, 3],
                "z1": [3, 4],
                "t1": [4, 5],
                "x2": [2, 9],
                "y2": [2, 8],
                "z2": [2, 7],
                "t2": [0, 6]
            }
        },
        {
            "analysis": {
                "x1": [],
                "y1": [],
                "z1": [],
                "t1": [],
                "x2": [3, 2, 1],
                "y2": [4, 3, 2],
                "z2": [5, 4, 3],
                "t2": [6, 5, 4]
            }
        }
    ]
    """

    a2 = """
    [
        {
            "analysis": {
                "x1": [],
                "y1": [],
                "z1": [],
                "t1": [],
                "x2": [1, 2, 3],
                "y2": [2, 3, 4],
                "z2": [2, 6, 6],
                "t2": [7, 8, 9]
            }
        },
        {
            "analysis": {
                "x1": [3, 2, 1],
                "y1": [4, 3, 2],
                "z1": [5, 4, 3],
                "t1": [6, 5, 4],
                "x2": [],
                "y2": [],
                "z2": [],
                "t2": []
            }
        },
        {
            "analysis": {
                "x1": [2, 9],
                "y1": [2, 8],
                "z1": [2, 7],
                "t1": [0, 6],
                "x2": [1, 2],
                "y2": [2, 3],
                "z2": [3, 4],
                "t2": [4, 5]
            }
        }
    ]
    """

    a3 = """
    [
        {
            "analysis": {
                "x1": [1, 9, 1],
                "y1": [1, 8, 2],
                "z1": [1, 7, 3],
                "t1": [1, 6, 4],
                "x2": [3, 2, 5],
                "y2": [3, 3, 6],
                "z2": [3, 4, 7],
                "t2": [3, 5, 8]
            }
        },
        {
            "analysis": {
                "x1": [],
                "y1": [],
                "z1": [],
                "t1": [],
                "x2": [1, 2],
                "y2": [2, 3],
                "z2": [2, 6],
                "t2": [7, 8]
            }
        },
        {
            "analysis": {
                "x1": [3, 2, 1, 4],
                "y1": [4, 3, 2, 5],
                "z1": [5, 4, 3, 6],
                "t1": [6, 5, 4, 7],
                "x2": [1, 2],
                "y2": [3, 4],
                "z2": [5, 6],
                "t2": [7, 8]
            }
        }
    ]
    """
    return [a1, a2, a3]


def _numbers() -> list[str]:
    a1 = """
    [
      [
        [3, 2],
        [1],
        [5, 4],
        [6]
      ],
      [
        [7]
      ],
      [
        [8, 9],
        []
      ]
    ]
    """

    a2 = """
    [
      [
        [3, 1],
        [],
        [2, 4],
        [5]
      ],
      [
        [6]
      ],
      [
        [7, 8],
        [9]
      ]
    ]
    """

    a3 = """
    [
      [
        [3, 1],
        [],
        [2],
        [4, 5]
      ],
      [
        [6]
      ],
      [
        [7, 8],
        [9]
      ]
    ]
    """

    return [a1, a2, a3]
