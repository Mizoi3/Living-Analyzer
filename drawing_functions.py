import matplotlib.pyplot as plt
from shapely.geometry import LineString
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.lines import Line2D

def draw_linestrings(linestrings, linestring_sub=None):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.set_aspect('equal')
    for line in linestrings:
        if isinstance(line, LineString):
            x, y = line.xy
            ax.plot(x, y, color="black", linewidth=3)
    ax.invert_yaxis()
    if linestring_sub:
        for line in linestring_sub:
            if isinstance(line, LineString):
                x, y = line.xy
                ax.plot(x, y, color="orange", linewidth=10, alpha=0.3)
    plt.show()

def draw_polygons(polygons, linestrings=None):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.invert_yaxis()
    for poly in polygons:
        mpl_poly = MplPolygon(list(poly.exterior.coords), closed=True, color='orange', linewidth=0, alpha=0.5)
        ax.add_patch(mpl_poly)
    if linestrings:
        for line in linestrings:
            mpl_line = Line2D([point[0] for point in line.coords], [point[1] for point in line.coords],
                              color='black', linewidth=2, alpha=1)
            ax.add_line(mpl_line)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
