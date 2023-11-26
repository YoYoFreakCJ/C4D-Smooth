import c4d

##############################
# IMPORTANT: READ THE README #
##############################

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

def smooth_points(poly_obj: c4d.PolygonObject, steps: int = 1, stiffness: float = 0.5, points_indices_to_smooth: list[int] = [], neighbor: c4d.utils.Neighbor = None):
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
