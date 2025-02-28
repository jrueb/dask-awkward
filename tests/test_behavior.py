from __future__ import annotations

import awkward as ak
import numpy as np
import pytest

import dask_awkward as dak
from dask_awkward.lib.testutils import assert_eq

behaviors: dict = {}


@ak.mixin_class(behaviors)
class Point:
    def distance(self, other):
        return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    @property
    def x2(self):
        return self.x * self.x

    @ak.mixin_class_method(np.abs)
    def point_abs(self):
        return np.sqrt(self.x**2 + self.y**2)

    @property
    def non_dask_property(self, _dask_array_=None):
        return "this is a non-dask property"

    def non_dask_method(self, _dask_array_=None):
        return _dask_array_


def test_distance_behavior(
    daa_p1: dak.Array,
    daa_p2: dak.Array,
    caa_p1: ak.Array,
    caa_p2: ak.Array,
) -> None:
    daa1 = dak.with_name(daa_p1.points, name="Point", behavior=behaviors)
    daa2 = dak.with_name(daa_p2.points, name="Point", behavior=behaviors)
    caa1 = ak.Array(caa_p1.points, with_name="Point", behavior=behaviors)
    caa2 = ak.Array(caa_p2.points)
    assert_eq(daa1.distance(daa2), caa1.distance(caa2))
    assert_eq(np.abs(daa1), np.abs(caa1))


def test_property_behavior(daa_p1: dak.Array, caa_p1: ak.Array) -> None:
    daa = dak.with_name(daa_p1.points, name="Point", behavior=behaviors)
    caa = ak.Array(caa_p1.points, with_name="Point", behavior=behaviors)
    assert_eq(daa.x2, caa.x2)

    assert daa.behavior == caa.behavior

    assert daa.non_dask_property == caa.non_dask_property

    assert repr(daa.non_dask_method()) == repr(daa)


def test_nonexistent_behavior(daa_p1: dak.Array, daa_p2: dak.Array) -> None:
    daa1 = dak.with_name(daa_p1["points"], "Point", behavior=behaviors)
    daa2 = daa_p2

    with pytest.raises(
        AttributeError,
        match="Method doesnotexist is not available to this collection",
    ):
        daa1._call_behavior_method("doesnotexist", daa2)

    with pytest.raises(
        AttributeError,
        match="Property doesnotexist is not available to this collection",
    ):
        daa1._call_behavior_property("doesnotexist")

    # in this case the field check is where we raise
    with pytest.raises(AttributeError, match="distance not in fields"):
        daa2.distance(daa1)
