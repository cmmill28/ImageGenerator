import numpy as np
from sklearn.cluster import KMeans

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
                continue
            neighbour_cell = cells[neighbour_coords]
            if neighbour_cell is not None:
                neighbours.append(neighbour_cell)
        return neighbours

    def point_valid(pt):
        """Is pt a valid point to emit as a sample?"""
        cell_coords = get_cell_coords(pt)
        for idx in get_neighbours(cell_coords):
            nearby_pt = samples[idx]
            distance2 = (nearby_pt[0] - pt[0]) ** 2 + (nearby_pt[1] - pt[1]) ** 2
            if distance2 < r ** 2:
                return False
        return True

    def get_point(k, refpt):
        """Try to find a candidate point relative to refpt to emit in the sample."""
        i = 0
        while i < k:
            rho, theta = np.random.uniform(r, 2 * r), np.random.uniform(0, 2 * np.pi)
            pt = refpt[0] + rho * np.cos(theta), refpt[1] + rho * np.sin(theta)
            if not (0 <= pt[0] < width and 0 <= pt[1] < height):
                continue
            if point_valid(pt):
                return pt
            i += 1
        return False

    def is_near_border(pt):
        """Check if the point is near the border."""
        edge_threshold = min(width, height) * 0.1  # 10% of image dimensions
        return pt[0] < edge_threshold or pt[0] > (width - edge_threshold) or pt[1] < edge_threshold or pt[1] > (height - edge_threshold)

    a = r / np.sqrt(2)
    nx, ny = int(width / a) + 1, int(height / a) + 1
    coords_list = [(ix, iy) for ix in range(nx) for iy in range(ny)]
    cells = {coords: None for coords in coords_list}

    pt = (np.random.uniform(0, width), np.random.uniform(0, height))
    samples = [pt]
    edge_points = []  # Points near edges
    cells[get_cell_coords(pt)] = 0
    active = [0]

    if is_near_border(pt):
        edge_points.append(pt)

    while active:
        idx = np.random.choice(active)
        refpt = samples[idx]
        pt = get_point(k, refpt)
        if pt:
            samples.append(pt)
            cells[get_cell_coords(pt)] = len(samples) - 1
            active.append(len(samples) - 1)

            if is_near_border(pt):
                edge_points.append(pt)
        else:
            active.remove(idx)

    # Apply k-means clustering to find clusters
    kmeans = KMeans(n_clusters=min(5, len(samples)), random_state=0).fit(samples)
    cluster_centers = kmeans.cluster_centers_

    return samples, edge_points, cluster_centers
