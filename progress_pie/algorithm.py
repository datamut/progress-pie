import math
from dataclasses import dataclass

from progress_pie.exceptions import UnexpectedValueException


@dataclass
class Point:
    x: float
    y: float

    def distance(self, other: 'Point') -> float:
        """
        Calculate the distance of two points in 2d-euclidean space.

        :param other: The other Point
        :return: The euclidean distance of the two points
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


@dataclass
class Circle:
    centre: Point
    radius: float


class ProgressPie:
    def __init__(self, circle: Circle, tolerance: float = 1e-6):
        """
        A general use progress bar/pie calculation algorithm.

        By giving the circle centre and radius, and a minimal error tolerance
        because of float point calculation (default is 1e-6), we can calculate
        whether any given point if withn the progressed area.

        Note the progress bar/pie starts from 90 (PI/2) in Cartesian coordinates, and the progress move clockwise.

        :param circle: The given circle
        :param tolerance: The given error tolerance value, default is 1e-6
        """
        self.circle = circle
        self.round_to = abs(int(math.log10(tolerance)))

    def in_circle(self, p: Point) -> bool:
        """
        Check whether a point is inside a circle.

        :param p: The given point
        :return: whether the given point is inside the circle
        """

        # TODO: discuss if a tolerance should be used here, for now no tolerance used
        return p.distance(self.circle.centre) <= self.circle.radius

    def within_progress(self, pct: float, x: float, y: float):
        """
        Check whether a given point is in the progressed area of a given progressed percentage.

        Note that the pct is a value in range [0, 100]

        :param pct:
        :param x:
        :param y:
        :return:
        """

        if pct > 100 or pct < 0:
            raise UnexpectedValueException('The given pct (progressed percentage) is out of range [0, 100]')

        # as percentage value of [0, 1]
        pct = 0.01 * pct

        if pct == 0:
            # if pct is 0, no any points are progressed
            return False

        if not self.in_circle(Point(x=x, y=y)):
            return False

        if y == self.circle.centre.y:
            # no slope, check separately
            return ((x == self.circle.centre.x)                     # circle centre, any pct > 0 progressed it
                    or (x > self.circle.centre.x and pct >= 0.25)   # pct must be passed the first Quadrant
                    or (x < self.circle.centre.x and pct >= 0.75))  # pct must be passed the third Quadrant

        # progress slope, as it starts from 90 (PI/2), there is a 0.25 pct to be considered
        progress_slope = math.tan(2 * math.pi * (0.25 - pct))

        # given point slope against the centre of circle
        point_slope = (x - self.circle.centre.x) / (y - self.circle.centre.y)

        # round difference to given tolerance and compare difference
        # TODO: discussion - is it diff then round or round then diff, will end up with different result
        return round(point_slope - progress_slope, self.round_to) >= 0
