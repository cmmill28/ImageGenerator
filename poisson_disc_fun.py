def poissonDisc(width, height, r, k, min_overlap_dist=10, max_overlap_dist=150):
    def get_cell_coords(pt):
        """Get the coordinates of the cell that pt = (x,y) falls in."""
        return int(pt[0] // a), int(pt[1] // a)

    def get_neighbours(coords):
        """Return the indexes of points in cells neighbouring cell at coords."""
        dxdy = [(-1, -2), (0, -2), (1, -2), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
                (-2, 0), (-1, 0), (1, 0), (2, 0), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
                (-1, 2), (0, 2), (1, 2), (0, 0)]
        neighbours = []
        for dx, dy in dxdy:
            neighbour_coords = coords[0] + dx, coords[1] + dy
            if not (0 <= neighbour_coords[0] < nx and 0 <= neighbour_coords[1] < ny):
                continue
            neighbour_cell = cells[neighbour_coords]
            if neighbour_cell is not None:
                neighbours.append(neighbour_cell)
        return neighbours

    def point_valid(pt, overlap_radius):
        """Check if the point is valid with respect to the current overlap radius."""
        cell_coords = get_cell_coords(pt)
        for idx in get_neighbours(cell_coords):
            nearby_pt = samples[idx]
            distance2 = (nearby_pt[0] - pt[0]) ** 2 + (nearby_pt[1] - pt[1]) ** 2
            if distance2 < overlap_radius ** 2:
                return False
        return True

    def get_point(k, refpt, overlap_radius):
        """Try to find a candidate point relative to refpt to emit in the sample."""
        i = 0
        while i < k:
            rho, theta = np.random.uniform(r, 2 * r), np.random.uniform(0, 2 * np.pi)
            pt = refpt[0] + rho * np.cos(theta), refpt[1] + rho * np.sin(theta)
            if not (0 <= pt[0] < width and 0 <= pt[1] < height):
                continue
            if point_valid(pt, overlap_radius):
                return pt
            i += 1
        return False

    a = r / np.sqrt(2)
    nx, ny = int(width / a) + 1, int(height / a) + 1
    coords_list = [(ix, iy) for ix in range(nx) for iy in range(ny)]
    cells = {coords: None for coords in coords_list}

    pt = (np.random.uniform(0, width), np.random.uniform(0, height))
    samples = [pt]
    cells[get_cell_coords(pt)] = 0
    active = [0]

    nsamples = 1
    overlapping_points = []
    overlap_radius = min_overlap_dist
    while active:
        idx = np.random.choice(active)
        refpt = samples[idx]
        pt = get_point(k, refpt, overlap_radius)
        if pt:
            samples.append(pt)
            nsamples += 1
            active.append(len(samples) - 1)
            cells[get_cell_coords(pt)] = len(samples) - 1

            if overlap_radius > min_overlap_dist:
                overlapping_points.append(pt)
        else:
            overlap_radius += 5  # Gradually increase the radius by 5 units
            if overlap_radius > max_overlap_dist:
                active.remove(idx)
                overlap_radius = min_overlap_dist  # Reset the overlap radius for the next point

    return samples, overlapping_points