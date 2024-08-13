import numpy as np

def poissonDisc(width, height, r, k):
    def get_cell_coords(pt):
        """Get the coordinates of the cell that pt = (x,y) falls in."""
        return int(pt[0] // a), int(pt[1] // a)

    def get_neighbours(coords):
        """Return the indexes of points in cells neighboring cell at coords."""
        dxdy = [(-1, -2), (0, -2), (1, -2), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
                (-2, 0), (-1, 0), (1, 0), (2, 0), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
                (-1, 2), (0, 2), (1, 2), (0, 0)]
        neighbours = []
        for dx, dy in dxdy:
            neighbour_coords = coords[0] + dx, coords[1] + dy
            if not (0 <= neighbour_coords[0] < nx and
                    0 <= neighbour_coords[1] < ny):
                # We're off the grid: no neighbors here.
                continue
            neighbour_cell = cells[neighbour_coords]
            if neighbour_cell is not None:
                # This cell is occupied: store this index of the contained point.
                neighbours.append(neighbour_cell)
        return neighbours

    def point_valid(pt):
        """Is pt a valid point to emit as a sample?"""
        cell_coords = get_cell_coords(pt)
        for idx in get_neighbours(cell_coords):
            nearby_pt = samples[idx]
            # Squared distance between our candidate point, pt, and this nearby_pt.
            distance2 = (nearby_pt[0] - pt[0]) ** 2 + (nearby_pt[1] - pt[1]) ** 2
            if distance2 < r ** 2:
                # The points are too close, so pt is not a candidate.
                return False
        # All points tested: if we're here, pt is valid
        return True

    def get_point(k, refpt):
        """Try to find a candidate point relative to refpt to emit in the sample."""
        i = 0
        while i < k:
            rho, theta = np.random.uniform(r, 2 * r), np.random.uniform(0, 2 * np.pi)
            pt = refpt[0] + rho * np.cos(theta), refpt[1] + rho * np.sin(theta)
            if not (0 <= pt[0] < width and 0 <= pt[1] < height):
                # This point falls outside the domain, so try again.
                continue
            if point_valid(pt):
                return pt
            i += 1
        # We failed to find a suitable point in the vicinity of refpt.
        return False

    # Cell side length
    a = r / np.sqrt(2)
    # Number of cells in the x- and y-directions of the grid
    nx, ny = int(width / a) + 1, int(height / a) + 1

    # A list of coordinates in the grid of cells
    coords_list = [(ix, iy) for ix in range(nx) for iy in range(ny)]
    # Initialize the dictionary of cells
    cells = {coords: None for coords in coords_list}

    # Pick a random point to start with.
    pt = (np.random.uniform(0, width), np.random.uniform(0, height))
    samples = [pt]
    edge_points = []  # To store points near the edges
    overlapping_points = []  # To store points that might overlap with others
    cells[get_cell_coords(pt)] = 0
    active = [0]

    # Check if the first point is near an edge
    edge_threshold = min(width, height) * 0.1  # 10% of the image dimensions
    if pt[0] < edge_threshold or pt[0] > (width - edge_threshold) or pt[1] < edge_threshold or pt[1] > (height - edge_threshold):
        edge_points.append(pt)

    # As long as there are points in the active list, keep trying to find samples.
    while active:
        idx = np.random.choice(active)
        refpt = samples[idx]
        pt = get_point(k, refpt)
        if pt:
            samples.append(pt)
            cells[get_cell_coords(pt)] = len(samples) - 1
            active.append(len(samples) - 1)

            # Check if the point is near an edge
            if pt[0] < edge_threshold or pt[0] > (width - edge_threshold) or pt[1] < edge_threshold or pt[1] > (height - edge_threshold):
                edge_points.append(pt)

            # Check if the point is near other points (potential overlap)
            if any(np.sqrt((pt[0] - s[0]) ** 2 + (pt[1] - s[1]) ** 2) < r * 1.5 for s in samples if s != pt):
                overlapping_points.append(pt)
        else:
            active.remove(idx)

    return samples, edge_points, overlapping_points
