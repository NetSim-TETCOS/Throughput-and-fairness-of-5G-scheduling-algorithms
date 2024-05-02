import math
import matplotlib.pyplot as plt
import random
import pandas as pd

random.seed(38)

def equilateral_triangle_center(p1, p2, p3):
    """Calculates the center of an equilateral triangle given the coordinates of its corners."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return ((x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3)

def hexagon_side_length(radius):
    """Calculates the side length of a regular hexagon given its apothem (radius from center to vertex)."""
    return 2 * radius / math.sqrt(3)

def hexagon_coordinates(center, side_length, rotation_angle=0):
    """Calculates the coordinates of all vertices of a regular hexagon given its center, side length, and optional rotation angle."""
    cx, cy = center
    vertices = []
    for i in range(6):
        angle = 60 * i + rotation_angle
        x = cx + side_length * math.cos(math.radians(angle))
        y = cy + side_length * math.sin(math.radians(angle))
        vertices.append((x, y))
    return vertices

def random_point_in_hexagon(hexagon_vertices, exclude_points=[]):
    x_min = min(p[0] for p in hexagon_vertices) + side_length / 10
    x_max = max(p[0] for p in hexagon_vertices) - side_length / 10
    y_min = min(p[1] for p in hexagon_vertices) + side_length / 10
    y_max = max(p[1] for p in hexagon_vertices) - side_length / 10

    excluded_points_set = set(exclude_points)

    while True:
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)

        if is_point_inside_hexagon(x, y, hexagon_vertices) and all(
            (x - p[0])**2 + (y - p[1])**2 > (side_length / 10)**2 for p in excluded_points_set):
            return x, y

def is_point_inside_hexagon(x, y, vertices):
    c = False
    i = -1
    j = 5
    for i in range(6):
        if ((vertices[i][1] > y) != (vertices[j][1] > y)) and \
                (x < (vertices[j][0] - vertices[i][0]) * (y - vertices[i][1]) / (vertices[j][1] - vertices[i][1]) + vertices[i][0]):
            c = not c
        j = i
    return c

gnb1 = (1000, 1000)
gnb2 = (2000, 2732.1)
gnb3 = (3000, 1000)

center = equilateral_triangle_center(gnb1, gnb2, gnb3)

radius = 1000
side_length = hexagon_side_length(radius)

hexagon1 = hexagon_coordinates(gnb1, side_length, 30)
hexagon2 = hexagon_coordinates(gnb2, side_length, 30)
hexagon3 = hexagon_coordinates(gnb3, side_length, 30)

num_points_per_hexagon = 10
random_points_hexagon1 = [random_point_in_hexagon(hexagon1, [gnb1, gnb2, gnb3]) for _ in range(num_points_per_hexagon)]
random_points_hexagon2 = [random_point_in_hexagon(hexagon2, [gnb1, gnb2, gnb3]) for _ in range(num_points_per_hexagon)]
random_points_hexagon3 = [random_point_in_hexagon(hexagon3, [gnb1, gnb2, gnb3]) for _ in range(num_points_per_hexagon)]

gnb_points = [(f"gNB{i+1}", gnb[0], gnb[1]) for i, gnb in enumerate([gnb1, gnb2, gnb3])]
ue_points = [("UE{}".format(i+1), x, y) for i, (x, y) in enumerate(random_points_hexagon1 + random_points_hexagon2 + random_points_hexagon3)]

ues = random_points_hexagon1 + random_points_hexagon2 + random_points_hexagon3


df = pd.DataFrame(gnb_points + ue_points, columns=["Point_Name", "X", "Y"])

excel_filename = "gnb_ue_points.xlsx"
df.to_excel(excel_filename, index=False)
print(f"Coordinates saved to '{excel_filename}'")

# Concatenate all hexagon points
hexagon_points = [("Hexagon1", *hexagon1), ("Hexagon2", *hexagon2), ("Hexagon3", *hexagon3)]

# Create DataFrame for hexagon points
hexagon_df = pd.DataFrame(hexagon_points, columns=["Hexagon_Name", "X1", "Y1", "X2", "Y2", "X3", "Y3"])

# Save hexagon points to Excel file
hexagon_excel_filename = "hexagon_points.xlsx"
hexagon_df.to_excel(hexagon_excel_filename, index=False)

print(f"Hexagon coordinates saved to '{hexagon_excel_filename}'")

fig, ax = plt.subplots(figsize=(10, 7))

gnb_legend = plt.plot([gnb1[0], gnb2[0], gnb3[0]], [gnb1[1], gnb2[1], gnb3[1]], 'r^', markersize=9, label='gNB')

for hexagon in [hexagon1, hexagon2, hexagon3]:
    for i in range(len(hexagon)):
        plt.plot([hexagon[i][0], hexagon[(i+1)%6][0]], [hexagon[i][1], hexagon[(i+1)%6][1]], 'b-', alpha=0.7, linewidth=1)

ue_legend = plt.scatter(*zip(*ues), color='green', label='UE', s=15)

# Annotate GNBs
for label, x, y in gnb_points:
    plt.annotate(
        f'{label}\n({x}, {y})',
        (x, y),
        textcoords="offset points",
        xytext=(0,-22),
        ha='center',
        fontsize = 7
    )

# Annotate UEs
for label, x, y in ue_points:
    plt.annotate(
        label,
        (x, y),
        textcoords="offset points",
        xytext=(0,5),
        ha='center',
        fontsize = 7
    )

plt.xlim([min(p[0] for p in [gnb1, gnb2, gnb3]) - side_length,
         max(p[0] for p in [gnb1, gnb2, gnb3]) + side_length])
plt.ylim([min(p[1] for p in [gnb1, gnb2, gnb3]) - side_length,
         max(p[1] for p in [gnb1, gnb2, gnb3]) + side_length])

plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
ax.invert_yaxis()
ax.xaxis.set_ticks_position('top')
ax.set_xlabel("Distance (m)")
ax.xaxis.set_label_position('top')

plt.ylabel("Distance (m)")

# Save the plot as an image file
plot_filename = "gnb_ue_plot.png"
plt.savefig(plot_filename, bbox_inches='tight')
print(f"Plot saved as '{plot_filename}'")


plt.show()


