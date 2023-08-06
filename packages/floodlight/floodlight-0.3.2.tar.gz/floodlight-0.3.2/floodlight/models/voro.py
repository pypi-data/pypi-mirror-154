from typing import Tuple

import numpy as np
from scipy.spatial.distance import cdist
from scipy.spatial import Voronoi

from floodlight import XY
from floodlight.core.property import TeamProperty, PlayerProperty
from floodlight.models.base import BaseModel, requires_fit


class VoronoiModel(BaseModel):
    """
    An incredibly shitty, super-slow voronoi model not intended for publication (!)
    """
    def __init__(self, pitch):
        super().__init__(pitch=pitch)
        # model parameter
        self._space_control_1_ = None
        self._space_control_2_ = None

    @staticmethod
    def _convex_polygon_area(points):
        x = points[:, 0]
        y = points[:, 1]
        area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

        return area

    def voronoi_from_points(self, all_points):
        """hacky voronoi calculation bounding pitch surface by cell reflection"""
        # param
        pitch_area = self._pitch.length * self._pitch.width     # SUPER NOT SAFE
        N = len(all_points)

        # bin
        space_controls = np.zeros((N, 1))

        # add reflected points
        reflected_points = np.concatenate(
            (
                all_points,
                all_points * (-1, 1),
                all_points * (1, -1),
                all_points * (-1, 1) + (80, 0),
                all_points * (1, -1) + (0, 40),
            )
        )

        # create Voronoi diagram and fill bin for both teams
        vor = Voronoi(reflected_points)
        for p in range(N):
            point_region = vor.point_region[p]  # The region of the player
            regions = vor.regions[point_region]  # The vertices indices of that region
            vertices = vor.vertices[regions]  # The coordinates of these vertices (=polygon)
            p_area = round((self._convex_polygon_area(vertices) / pitch_area) * 100, 2)
            space_controls[p, 0] = p_area

        return space_controls

    def fit(self, xy1: XY, xy2: XY):
        """Fit the model to the given data and calculate space controls
        """
        # security
        if len(xy1) != len(xy2):
            raise ValueError("mismatching time dimensions")
        else:
            T = len(xy1)

        # bin
        space_controls1 = np.full((T, xy1.N), np.nan)
        space_controls2 = np.full((T, xy2.N), np.nan)

        # loop
        for t in range(T):
            # get points
            points1 = xy1[t].reshape(-1, 2)
            points2 = xy2[t].reshape(-1, 2)
            # handle nans
            mask1 = ~ np.isnan(points1).all(axis=1)
            mask2 = ~ np.isnan(points2).all(axis=1)
            points1 = points1[mask1]
            points2 = points2[mask2]
            # count & skip if has no players
            N1 = len(points1)
            N2 = len(points2)
            if N1 < 1 or N2 < 1:
                continue
            # join and get space controls
            points_cat = np.concatenate((points1, points2), axis=0)
            spaces = self.voronoi_from_points(points_cat)
            # spaces = np.array(([[4.67], [3.37], [3.54], [2.07], [3.63], [2.9], [41.3],
            # [9.47], [5.25], [3.13], [1.08], [17.84], [1.74]])) # DEBUG
            # re-assign team-specifically
            space_controls1[t, mask1] = spaces[:N1].squeeze()
            space_controls2[t, mask2] = spaces[N1:].squeeze()

        # wrap as property object
        self._space_control_1_ = PlayerProperty(
            property=space_controls1, name="space_control", framerate=xy1.framerate
        )
        self._space_control_2_ = PlayerProperty(
            property=space_controls2, name="space_control", framerate=xy2.framerate
        )

    @requires_fit
    def control(self) -> Tuple[PlayerProperty, PlayerProperty]:
        """Returns the space controllo. """
        return self._space_control_1_, self._space_control_2_
