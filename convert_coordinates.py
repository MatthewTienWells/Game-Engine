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
    anti_view = (-view[0], -view[1], -view[2])
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
    x, y, z = shift_cartesian_system((x, y, z), anti_view)
    return (x, y, z)

def plane_point(view, point, screen):
    """Get the relative position of a point's projection to another
    point on an intersecting plane, relative to the plane's closest
    point to the first point.

    Args:
        A point to use a base reference, the point to project, the
        closest point on the plane to the reference point.
    Returns:
        The distance to the point closest to the projection that falls
        within the same z-plane as the plane's reference point, and the
        distance from that point to the projection. These values will be
        negative if they have a greater phi-value or lesser theta-value
        than the plane's reference point in a spherical system where the
        overall reference point is the origin.
    """

    projection = plane_intersect(view, point, screen)
    i_line = cross_vector(
        (view[0] - screen[0], view[1] - screen[1], view[2] - screen[2]),
        (0, 0, 1)
        )
    s_t_p = (
        projection[0] - screen[0],
        projection[1] - screen[1],
        projection[2] - screen[2]
        )
    dot = 0
    for num in range(3):
        dot += i_line[num]*s_t_p[num]
    l_i_line = (i_line[0]**2 + i_line[1]**2 + i_line[2]**2)**0.5
    l_s_t_p = (s_t_p[0]**2 + s_t_p[1]**2 + s_t_p[2]**2)**0.5
    angle = math.acos(dot / (l_i_line*l_s_t_p))
    distance_in_z = l_s_t_p*math.sin(angle)
    distance_in_xy = l_s_t_p*math.cos(angle)
    return distance_in_z, distance_in_xy
