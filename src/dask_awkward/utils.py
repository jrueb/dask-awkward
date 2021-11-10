from __future__ import annotations

from typing import Any

import numpy as np
from dask.base import is_dask_collection


def assert_eq(a: Any, b: Any) -> None:
    if is_dask_collection(a) and not is_dask_collection(b):
        assert a.compute().to_list() == b.to_list()
    elif is_dask_collection(b) and not is_dask_collection(a):
        assert a.to_list() == b.compute().to_list()
    else:
        assert a.compute().to_list() == b.compute().to_list()


def normalize_single_outer_inner_index(
    divisions: tuple[int, ...], index: int
) -> tuple[int, int]:
    """Determine partition index and inner index for some divisions.

    Parameters
    ----------
    divisions : tuple[int, ...]
        The divisions of a Dask awkward collection.
    index : int
        The overall index (for the complete collection).

    Returns
    -------
    int
        Which partition in the collection.
    int
        Which inner index in the determined partition.

    Examples
    --------
    >>> from dask_awkward.utils import normalize_single_outer_inner_index
    >>> divisions = (0, 3, 6, 8)
    >>> normalize_single_outer_inner_index(divisions, 0)
    (0, 0)
    >>> normalize_single_outer_inner_index(divisions, 5)
    (1, 2)
    >>> normalize_single_outer_inner_index(divisions, 8)
    (2, -1)

    """
    if len(divisions) == 2:
        return (0, index)
    partition_index = int(np.digitize(index, divisions)) - 1
    new_index = index - divisions[partition_index]
    # if last
    if partition_index == (len(divisions) - 1) and new_index == 0:
        return (partition_index - 1, -1)
    return (partition_index, new_index)
