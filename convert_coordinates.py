"""This module provides functions for determining the proper mapping of
objects in a three dimensional cartesian coordinate system to their
projections to a second point on a two-dimensional plane."""

import math


def cartesian_to_spherical(x, y, z):
    """Convert a cartesian point to a spherical point.

    Args:
        x-coordinate of the point, y-coordinate of the point,
        z-coordinate of the point.
    Returns:
        r-value of the point, phi-value of the point, theta-value of the
        point.
    """

    r = (x**2 + y**2 + z**2)**0.5
    phi = math.atan(y/x)
    theta = math.asin(z/r)

    return r, phi, theta


def spherical_to_cartesian(r, phi, theta):
    """Convert a spherical point to a cartesian point.

    Args:
        r-value of the point, phi-value of the point, theta-value of the
        point,
    Returns:
        x-coordinate of the point, y-coordinate of the point,
        z-coordinate of the point.
    """

    z = math.sin(theta)*r
    hypxy = (r**2 - z**2)**0.5
    x = math.cos(phi)*hypxy
    y = math.sin(phi)*hypxy
    return x, y, z


def shift_cartesian_system(points, new_origin, invert_type=False):
    """Shift a cartesian coordinate system into a new cartesian
    coordinate system.

    Args:
        A list of tuples representing the points of interest in the
        previous system, of form (x,y,z), a tuple
        representing the new system's origin in the current system,
        also of form (x,y,z), and a boolean representing whether
        or not to return only the first point as a tuple if a list
        is provided or to place a point in a list if a point is
        provided.
    Returns:
        A tuple representing the point in the new system.
    """

    new_points = []
    if type(points) == list:
        for point in points:
            if type(point) != tuple:
                raise TypeError("Point provided is not a tuple.")
            if len(point) != 3:
                raise ValueError("Point provided is not three-dimensional.")
            new_point = (
                point[0]-new_origin[0],
                point[1]-new_origin[1],
                point[3]-new_origin[2]
                )
            new_points.append(new_point)
        if not invert_type:
            return new_points
        else:
            return new_points[0]
    elif type(points) == tuple:
        new_point = (
            points[0]-new_origin[0],
            points[1]-new_origin[1],
            points[2]-new_origin[2]
            )
        if not invert_type:
            return new_point
        else:
            return [new_point]
    else:
        raise TypeError("Provided value is not a recognized argument type.")


def cross_vector(index, middle):
    """Get the cross product of two vectors.

    Args:
        The two vectors to cross.
    Returns:
        The cross product of the vectors.
    """

    i = index[1]*middle[2] - index[2]*middle[1]
    j = index[2]*middle[0] - index[0]*middle[2]
    k = index[0]*middle[1] - index[1]*middle[0]

    return (i,j,k)


def plane_intersect(view, point, screen):
    """Find the point where the segment from point to view intersects
    a plane.
    Points should be a tuple of the form (x,y,z).

    Args:
        A tuple representing the reference point, a tuple representing
        the point of interest, and a tuple defining the closest point in
        the plane to the reference point.
    Returns:
        The intersection point on the plane.
    """

    point = shift_cartesian_system(point, view)
    screen = shift_cartesian_system(screen, view)
    view = (0.0,0.0,0.0)
    point_s = cartesian_to_spherical(*point)
    screen_s = cartesian_to_spherical(*screen)
    if abs(point_s[1]-screen_s[1]) >= math.pi:
        return False
    if abs(point_s[2]-screen_s[2]) >= math.pi:
        return False
    intersect_distance = (
        screen_s[0]**2
        + (screen_s[0]*math.cos(screen_s[1]))**2
        + (screen_s[0]*math.cos(screen_s[2]))**2
        )**0.5
    x, y, z = spherical_to_cartesian(
        intersect_distance,
        point_s[1],
        point_s[2]
        )
    return (x, y, z)
