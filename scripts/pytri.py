""" 
result of discussion with Gemini

Gaussian multiplication preserves norm of 1 for pt1
In order to be able to "see" the order of points generated
I asked Gemini to scale the point norms and draw spiral
edges between consecutive points.
"""
import matplotlib.pyplot as plt
import numpy as np

def generate_sequence(m):
    """
    Generates the sequence pt_1, pt_2, ..., pt_m
    pt_1 = 3/5 + 4/5 * I
    pt_i = pt_{i-2} * pt_{i-1} for i >= 3, with pt_2 = pt_1 * pt_1
    """
    # Base point
    pt1 = 3/5 + 4/5*1j

    trpls = [pt1]
    if m >= 2:
        trpls.append(pt1 * pt1)  # pt2 = pt1 * pt1

    # Recurrence: pt_i = pt_{i-2} * pt_{i-1}
    for j in range(2, m):
        trpls.append(triples[j-2] * triples[j-1])

    return trpls

# Parameters
n = 20   # pylint: disable=invalid-name
r = 1.0  # pylint: disable=invalid-name
s = 0.4  # pylint: disable=invalid-name
k = 100

# Generate sequence of n points
triples = generate_sequence(n)

# Calculate scaled points
scaled_points = []
for i, z in enumerate(triples):
    radius = r + i * s
    angle = np.angle(z)
    scaled_z = radius * np.exp(1j * angle)
    scaled_points.append((radius, angle, scaled_z))

# Generate strictly counterclockwise spiral paths
all_x = []
all_y = []

for i in range(len(scaled_points) - 1):
    r1, theta1, _ = scaled_points[i]
    r2, theta2, _ = scaled_points[i+1]

    # Ensure angular displacement is strictly positive (counterclockwise)
    d_theta = (theta2 - theta1) % (2 * np.pi)

    # Linearly interpolate radius and angle across k intermediate steps
    t = np.linspace(0, 1, k)
    r_interp = r1 + t * (r2 - r1)
    theta_interp = theta1 + t * d_theta

    x_interp = r_interp * np.cos(theta_interp)
    y_interp = r_interp * np.sin(theta_interp)

    all_x.extend(x_interp)
    all_y.extend(y_interp)

# Extract scaled point coordinates for scatter plot
pts_x = [z.real for _, _, z in scaled_points]
pts_y = [z.imag for _, _, z in scaled_points]

# Plotting
plt.figure(figsize=(10, 10))
plt.plot(all_x, all_y, color='tab:blue', linewidth=1.2, label='Counterclockwise Spiral Path')
plt.scatter(pts_x, pts_y, color='tab:red', zorder=5, s=30, label='Scaled Triples')

# Annotate points
for i, (x, y) in enumerate(zip(pts_x, pts_y), start=1):
    plt.annotate(f'P{i}', (x, y), textcoords="offset points", xytext=(5, 5), ha='left', fontsize=8)

plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
plt.axvline(0, color='gray', linestyle='--', alpha=0.5)
plt.gca().set_aspect('equal', adjustable='box')
plt.title(f'Scaled Pythagorean Triples Sequence (n={n}) with CCW Interpolation')
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()

plt.show()
