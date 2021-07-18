import math

import pytest

from progress_pie.algorithm import Point, Circle, ProgressPie
from progress_pie.exceptions import UnexpectedValueException


def test_point():
    p1 = Point(x=10, y=10.5)
    assert p1.x == 10
    assert p1.y == 10.5

    p2 = Point(1, -1)
    dist = p1.distance(p2)
    assert dist == p2.distance(p1)
    assert dist == math.sqrt((10 - 1) ** 2 + (10.5 + 1) ** 2)


def test_circle():
    c = Circle(Point(6, 6.5), 13.6)
    assert c.radius == 13.6
    assert c.centre.x == 6
    assert c.centre.y == 6.5


def test_progress_pie():
    pie = ProgressPie(Circle(Point(50, 50), 50))

    # test in circle area
    assert pie.in_circle(Point(50, 50)) is True
    assert pie.in_circle(Point(0, 0)) is False
    assert pie.in_circle(Point(50, 100)) is True

    # test progress with the given cases
    assert pie.within_progress(0, 55, 55) is False
    assert pie.within_progress(12, 55, 55) is False
    assert pie.within_progress(13, 55, 55) is True
    assert pie.within_progress(99, 99, 99) is False
    assert pie.within_progress(87, 20, 40) is True

    # circle centre is progressed as long progress is not 0
    assert pie.within_progress(0, 50, 50) is False
    assert pie.within_progress(0.00000000001, 50, 50) is True
    assert pie.within_progress(99.9999, 50, 50) is True
    assert pie.within_progress(25, 50, 50) is True
    assert pie.within_progress(50, 50, 50) is True
    assert pie.within_progress(75, 50, 50) is True
    assert pie.within_progress(100, 50, 50) is True

    assert pie.within_progress(12.5, 51.5, 51.5) is True
    # slope diff is smaller than 1e-6, it is considered as within the progressed area
    assert pie.within_progress(12.5-0.0000000001, 51.5, 51.5) is True
    # slope diff is bigger than 1e-6, it is still consider not within the progressed area
    assert pie.within_progress(12.5-0.00001, 51.5, 51.5) is False


def test_progress_pie_error():
    pie = ProgressPie(Circle(Point(50, 50), 50))
    with pytest.raises(UnexpectedValueException):
        pie.within_progress(-1, 50, 50)

    with pytest.raises(UnexpectedValueException):
        pie.within_progress(100.1, 50.5, 50.5)
