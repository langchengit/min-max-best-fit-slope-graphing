import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# data of the lab
x = [[0.55, 0.75], [0.55, 0.72], [0.55, 0.77], [0.555, 0.88], [0.55, 1.12]]
y = [0.295, 0.355, 0.397, 0.411, 0.462]


#error for x and y
error_x = 0.6
error_y = 0.05

def div(arr):
    return arr[0] / arr[1]

def calc(data):
    return 6 - data * 8.33

x_center = [div(x) for x in x]
y_center = [calc(y) for y in y]

print (x_center)
print (y_center)

boxes = []
for y, x in zip(y, x):
    left   = (x[0] - 0.01) / (x[1] + 0.155)
    right  = (x[0] + 0.01) / (x[1] - 0.155)
    bottom =  6 - (y + 0.005) * 8.33
    top    = 6 - (y - 0.005) * 8.33
    boxes.append({
        "left": left, "right": right,
        "bottom": bottom, "top": top,
        "width": right - left, "height": top - bottom
    })


def box_corners(b):
    return [
        (b["left"],  b["bottom"]),
        (b["left"],  b["top"]),
        (b["right"], b["bottom"]),
        (b["right"], b["top"]),
    ]


def line_intersects_box(m, b_int, box):
    y_left  = m * box["left"]  + b_int
    y_right = m * box["right"] + b_int
    y_lo = min(y_left, y_right)
    y_hi = max(y_left, y_right)
    return y_lo <= box["top"] and y_hi >= box["bottom"]


def count_boxes(m, b_int, boxes):
    return sum(line_intersects_box(m, b_int, box) for box in boxes)


# -------------------------------------------------------
# Generate all candidate lines from corner pairs
# -------------------------------------------------------
candidates = []

n = len(boxes)
for i in range(n):
    for j in range(n):
        if i == j:
            continue
        for c1 in box_corners(boxes[i]):
            for c2 in box_corners(boxes[j]):
                x1, y1 = c1
                x2, y2 = c2
                if x2 == x1:
                    continue
                m = (y2 - y1) / (x2 - x1)
                b_int = y1 - m * x1
                candidates.append((m, b_int))

# -------------------------------------------------------
# Filter to lines passing through the most boxes
# -------------------------------------------------------
max_boxes_hit = max(count_boxes(m, b_int, boxes) for m, b_int in candidates)

best_candidates = [
    (m, b_int)
    for m, b_int in candidates
    if count_boxes(m, b_int, boxes) == max_boxes_hit
]

min_m, min_b = min(best_candidates, key=lambda x: x[0])
max_m, max_b = max(best_candidates, key=lambda x: x[0])

# -------------------------------------------------------
# Best-fit line
# -------------------------------------------------------
best_m, best_b = np.polyfit(x_center, y_center, 1)

# -------------------------------------------------------
# Plot
# -------------------------------------------------------
plt.figure(figsize=(8, 6))
ax = plt.gca()

plt.scatter(x_center, y_center, zorder=3, color="black", label="Data points")

for b in boxes:
    rect = Rectangle(
        (b["left"], b["bottom"]),
        b["width"], b["height"],
        fill=False, linewidth=1.5, zorder=2
    )
    ax.add_patch(rect)

x_min = min(b["left"]   for b in boxes)
x_max = max(b["right"]  for b in boxes)
y_min = min(b["bottom"] for b in boxes)
y_max = max(b["top"]    for b in boxes)

pad_x = (x_max - x_min) * 0.15
pad_y = (y_max - y_min) * 0.15
plt.xlim(x_min - pad_x, x_max + pad_x)
plt.ylim(y_min - pad_y, y_max + pad_y)

x_vals = [x_min - pad_x, x_max + pad_x]

plt.plot(x_vals, [min_m  * x + min_b  for x in x_vals],
         linewidth=2, linestyle="--", color="blue",
         label=f"Min slope = {min_m:.4f}")
plt.plot(x_vals, [max_m  * x + max_b  for x in x_vals],
         linewidth=2, linestyle="--", color="orange",
         label=f"Max slope = {max_m:.4f}")
plt.plot(x_vals, [best_m * x + best_b for x in x_vals],
         linewidth=2, linestyle="-",  color="green",
         label=f"Best fit  = {best_m:.4f}")

plt.title("back emf vs velocity graph - DC Motor lab")
plt.xlabel("velocity (m/s)")
plt.ylabel("back emf (V)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

print(f"Best-fit slope:     {best_m:.6f}")
print(f"Best-fit intercept: {best_b:.6f}")
print(f"Min slope:          {min_m:.6f}")
print(f"Max slope:          {max_m:.6f}")