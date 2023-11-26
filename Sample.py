# Paste this in a Python Generator.

import c4d

doc: c4d.documents.BaseDocument # The document evaluating this python generator
op: c4d.BaseObject # The python generator

def get_connected_points(poly_obj: c4d.PolygonObject, neighbor: c4d.utils.Neighbor, point_index: int):
    polys_indices = neighbor.GetPointPolys(point_index)

    polys = []

    for poly_index in polys_indices:
        polys.append(poly_obj.GetPolygon(poly_index))

    connected_points = []

    for poly in polys:
        if poly.a == point_index:
            connected_points.append(poly.b)
            if poly.IsTriangle():
                connected_points.append(poly.c)
            else:
                connected_points.append(poly.d)

        if poly.b == point_index:
            connected_points.append(poly.a)
            connected_points.append(poly.c)

        if poly.c == point_index:
            connected_points.append(poly.b)

            if poly.IsTriangle():
                connected_points.append(poly.a)
            else:
                connected_points.append(poly.d)

        if not poly.IsTriangle() and poly.d == point_index:
            connected_points.append(poly.c)
            connected_points.append(poly.a)

    return connected_points

def smooth_points(poly_obj: c4d.PolygonObject, steps: int = 1, stiffness: float = 0.5, points_indices_to_smooth: list[int] = None, neighbor: c4d.utils.Neighbor = None):
    if neighbor is None:
        neighbor = c4d.utils.Neighbor()
        neighbor.Init(poly_obj)

    all_points = poly_obj.GetAllPoints()

    # If no points are defined, smooth all points.
    if not points_indices_to_smooth:
        # Create a list of all point indices.
        points_indices_to_smooth = range(len(all_points))

    for _ in range(steps):
        for point_index in points_indices_to_smooth:
            point = all_points[point_index]

            connected_points_indices = get_connected_points(poly_obj, neighbor, point_index)

            # Calculate center of connected points.
            connected_points = c4d.Vector(0)

            for connected_point_index in connected_points_indices:
                connected_points += poly_obj.GetPoint(connected_point_index)

            connected_points /= len(connected_points_indices)
            
            # Apply stiffness.
            new_point = point - (point - connected_points) * (1.0 - stiffness)

            all_points[point_index] = new_point

        for point_index in points_indices_to_smooth:
            poly_obj.SetPoint(point_index, all_points[point_index])


def main() -> c4d.BaseObject:
    # Create points for a cube.
    points = []
    points.append(c4d.Vector(-100, 100, 100))
    points.append(c4d.Vector(100, 100, 100))
    points.append(c4d.Vector(100, -100, 100))
    points.append(c4d.Vector(-100, -100, 100))
    points.append(c4d.Vector(-100, 100, -100))
    points.append(c4d.Vector(100, 100, -100))
    points.append(c4d.Vector(100, -100, -100))
    points.append(c4d.Vector(-100, -100, -100))

    # Create polygons for a cube.
    polys = []
    polys.append(c4d.CPolygon(0, 3, 2, 1))
    polys.append(c4d.CPolygon(0, 1, 5, 4))
    polys.append(c4d.CPolygon(0, 4, 7, 3))
    polys.append(c4d.CPolygon(4, 5, 6, 7))
    polys.append(c4d.CPolygon(5, 1, 2, 6))
    polys.append(c4d.CPolygon(7, 6, 2, 3))

    # Create the cube.
    poly_obj = c4d.BaseObject(c4d.Opolygon)

    poly_obj.ResizeObject(len(points), len(polys))

    for i, point in enumerate(points):
        poly_obj.SetPoint(i, point)

    for i, poly in enumerate(polys):
        poly_obj.SetPolygon(i, poly)

    # Call the Subdivide command for the cube.
    bc = c4d.BaseContainer()
    bc[c4d.MDATA_SUBDIVIDE_SIMPLESUB] = 1

    res = c4d.utils.SendModelingCommand(command=c4d.MCOMMAND_SUBDIVIDE,
                                        list=[poly_obj],
                                        mode=c4d.MODELINGCOMMANDMODE_POLYGONSELECTION,
                                        bc=bc,
                                        doc=doc,
                                        flags=c4d.MODELINGCOMMANDFLAGS_CREATEUNDO)

    c4d.EventAdd()

    # Call smooth_points.
    smooth_points(poly_obj, steps = 1, stiffness = 0.5)

    return poly_obj
