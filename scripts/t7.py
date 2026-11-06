import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
from mpl_toolkits.mplot3d import proj3d

# 1. Command-Line Argument Processing
parser = argparse.ArgumentParser(
    description="Interactive Hyperbolic Triangle: 2D Upper Half-Plane & 3D Hyperbola (Hyperboloid) Models."
)
parser.add_argument('coords', type=float, nargs='*', help='Coordinates as real and imaginary parts.')

parsed_args = parser.parse_args()
input_args = parsed_args.coords

if not input_args:
    input_args = [2.0, 1.0, 3.0, 2.0, 4.0, 7.0]

if len(input_args) == 4:
    r1, i1, r2, i2 = input_args
    z1 = r1 + 1j * i1
    z2 = r2 + 1j * i2
    z3 = z1 * z2
elif len(input_args) == 6:
    r1, i1, r2, i2, r3, i3 = input_args
    z1 = r1 + 1j * i1
    z2 = r2 + 1j * i2
    z3 = r3 + 1j * i3
else:
    print("Error: Provide either 4 args (r1 i1 r2 i2) or 6 args (r1 i1 r2 i2 r3 i3).", file=sys.stderr)
    sys.exit(1)

if z1.imag <= 0 or z2.imag <= 0 or z3.imag <= 0:
    raise ValueError("All imaginary components must be strictly greater than 0.")

current_vertices = [z1, z2, z3]
current_mode = "hyperbolic plane"

# ==========================================
# 2. Mathematical Helper Functions (2D & 3D)
# ==========================================

def get_circle_params(za, zb):
    xa, ya = za.real, za.imag
    xb, yb = zb.real, zb.imag
    if np.isclose(xa, xb):
        return xa, np.inf
    c = (np.abs(zb)**2 - np.abs(za)**2) / (2 * (xb - xa))
    r = np.abs(za - c)
    return c, r

def get_tangent(z, w, c, r):
    if np.isinf(r):
        T = 1j * np.sign(w.imag - z.imag)
    else:
        T = 1j * (z - c)
        vec_to_w = w - z
        if np.real(np.conj(T) * vec_to_w) < 0:
            T = -T
    return T / np.abs(T)

def compute_triangle_data(z_list):
    za, zb, zc = z_list
    c12, r12 = get_circle_params(za, zb)
    c23, r23 = get_circle_params(zb, zc)
    c31, r31 = get_circle_params(zc, za)

    T_13 = get_tangent(za, zc, c31, r31)
    T_12 = get_tangent(za, zb, c12, r12)
    alpha1 = np.arccos(np.clip(np.real(np.conj(T_12) * T_13), -1.0, 1.0))

    T_21 = get_tangent(zb, za, c12, r12)
    T_23 = get_tangent(zb, zc, c23, r23)
    alpha2 = np.arccos(np.clip(np.real(np.conj(T_21) * T_23), -1.0, 1.0))

    T_32 = get_tangent(zc, zb, c23, r23)
    T_31 = get_tangent(zc, za, c31, r31)
    alpha3 = np.arccos(np.clip(np.real(np.conj(T_32) * T_31), -1.0, 1.0))

    area = np.pi - (alpha1 + alpha2 + alpha3)
    return (c12, r12), (c23, r23), (c31, r31), area

def uhp_to_hyperboloid(z):
    """Isometric mapping from Upper Half-Plane (x + iy) to 3D Hyperboloid Z^2 - X^2 - Y^2 = 1."""
    x, y = z.real, z.imag
    X = x / y
    Y = (x**2 + y**2 - 1.0) / (2.0 * y)
    Z = (x**2 + y**2 + 1.0) / (2.0 * y)
    return np.array([X, Y, Z])

def hyperboloid_to_uhp(X, Y):
    """Inverse isometric mapping from (X, Y) on the Hyperboloid back to x + iy in Upper Half-Plane."""
    Z = np.sqrt(1.0 + X**2 + Y**2)
    y = 1.0 / (Z - Y)
    x = X * y
    return x + 1j * max(y, 0.05)

def lorentz_dot(U, V):
    """Minkowski inner product in R^(2,1): Ux*Vx + Uy*Vy - Uz*Vz."""
    return U[0]*V[0] + U[1]*V[1] - U[2]*V[2]

def get_3d_hyperbola_geodesic(Pa, Pb, z_rim):
    """
    Computes:
    - arc_pts: 3D hyperbola segment between Pa and Pb
    - full_pts: Extended 3D hyperbola across the hyperboloid up to Z = z_rim
    - apex_pt: The minimum-Z vertex of the geodesic hyperbola
    """
    cosh_d = max(-lorentz_dot(Pa, Pb), 1.0 + 1e-9)
    d = np.arccosh(cosh_d)
    sinh_d = np.sinh(d)

    if sinh_d < 1e-7:
        arc_pts = np.column_stack([Pa, Pb])
        return arc_pts, arc_pts, Pa

    # Unit spacelike tangent vector Q at Pa pointing toward Pb
    Q = (Pb - cosh_d * Pa) / sinh_d

    # Segment between Pa (s = 0) and Pb (s = d)
    s_arc = np.linspace(0.0, d, 100)
    arc_pts = np.outer(Pa, np.cosh(s_arc)) + np.outer(Q, np.sinh(s_arc))

    # Find apex of the hyperbola (minimum Z along gamma(s))
    # gamma_z(s) = Pa[2]*cosh(s) + Q[2]*sinh(s) = A * cosh(s + s0)
    A = np.sqrt(max(Pa[2]**2 - Q[2]**2, 1.0))
    s0 = np.arctanh(np.clip(Q[2] / Pa[2], -0.999999, 0.999999))
    s_apex = -s0
    apex_pt = Pa * np.cosh(s_apex) + Q * np.sinh(s_apex)

    # Solve gamma_z(s) = z_rim for full dashed hyperbola bounds
    s_span = np.arccosh(max(z_rim / A, 1.0))
    s_full = np.linspace(-s0 - s_span, -s0 + s_span, 200)
    full_pts = np.outer(Pa, np.cosh(s_full)) + np.outer(Q, np.sinh(s_full))

    return arc_pts, full_pts, apex_pt

# ==========================================
# 3. Setup Figure, 2D Axes, 3D Axes & Toggle
# ==========================================

fig = plt.figure(figsize=(11, 10))

# 2D Upper Half-Plane Axes
ax2d = fig.add_axes([0.08, 0.07, 0.86, 0.85])
ax2d.axhline(0, color='black', linewidth=1.5, label='Real Axis (y = 0)')
ax2d.axvline(0, color='black', linewidth=1.5, linestyle='-.', label='Y-Axis (x = 0)')
ax2d.grid(True, linestyle='--', alpha=0.5)
ax2d.set_aspect('equal')
ax2d.set_xlabel('Re(z)')
ax2d.set_ylabel('Im(z)')
ax2d.set_xlim(-3, 12)
ax2d.set_ylim(-1, 10)

# 2D Plot Elements
vertex_plots_2d, = ax2d.plot([], [], 'ro', markersize=9, label='Vertices')
vertex_texts_2d = [ax2d.text(0, 0, '', fontsize=10, fontweight='bold') for _ in range(3)]
arc_lines_2d = [ax2d.plot([], [], 'b-', lw=2.5, label='Hyperbolic Triangle' if i == 0 else "")[0] for i in range(3)]
dashed_lines_2d = [ax2d.plot([], [], 'g--', alpha=0.5, label='Full Geodesics' if i == 0 else "")[0] for i in range(3)]
center_plots_2d, = ax2d.plot([], [], 'ko', markersize=6, label='Geodesic Centers')
center_texts_2d = [ax2d.text(0, 0, '', fontsize=8, ha='center', color='darkgreen', fontweight='bold') for _ in range(3)]
ax2d.legend(loc='upper left')

# 3D Hyperboloid Axes (Initially Hidden)
ax3d = fig.add_axes([0.05, 0.05, 0.88, 0.87], projection='3d')
ax3d.view_init(elev=15, azim=60)
ax3d.set_visible(False)
ax3d.disable_mouse_rotation()
surf_3d = None

# 3D Plot Elements
vertex_plots_3d, = ax3d.plot([], [], [], 'ro', markersize=8, zorder=10, label='Vertices')
vertex_texts_3d = [ax3d.text(0, 0, 0, '', fontsize=9, fontweight='bold', color='darkred') for _ in range(3)]
arc_lines_3d = [ax3d.plot([], [], [], 'b-', lw=3.0, zorder=8, label='Hyperbola Triangle' if i == 0 else "")[0] for i in range(3)]
dashed_lines_3d = [ax3d.plot([], [], [], 'g--', lw=1.5, alpha=0.75, label='Full Geodesic Hyperbolas' if i == 0 else "")[0] for i in range(3)]
apex_plots_3d, = ax3d.plot([], [], [], 'ko', markersize=5, zorder=9, label='Hyperbola Apexes')
apex_texts_3d = [ax3d.text(0, 0, 0, '', fontsize=8, color='darkgreen', fontweight='bold') for _ in range(3)]

# RadioButtons Toggle Widget
ax_radio = fig.add_axes([0.74, 0.89, 0.22, 0.09], facecolor='#f4f4f4')
radio = RadioButtons(ax_radio, ('hyperbolic plane', 'hyperbola'), active=0)

theta_full = np.linspace(0, np.pi, 300)
u_mesh = np.linspace(0, 1, 35)
phi_mesh = np.linspace(0, 2 * np.pi, 60)
U_grid, PHI_grid = np.meshgrid(u_mesh, phi_mesh)
last_z_rim = None

# ==========================================
# 4. Visualization Update Logic
# ==========================================

def update_visualization():
    global surf_3d, last_z_rim
    (c12, r12), (c23, r23), (c31, r31), area = compute_triangle_data(current_vertices)

    if current_mode == "hyperbolic plane":
        # --- Update 2D Upper Half-Plane View ---
        vertex_plots_2d.set_data([z.real for z in current_vertices], [z.imag for z in current_vertices])
        for i, z in enumerate(current_vertices):
            vertex_texts_2d[i].set_position((z.real + 0.15, z.imag))
            vertex_texts_2d[i].set_text(f'Z{i+1} ({z.real:.2f}+{z.imag:.2f}i)')

        def get_arc_coords(za, zb, c, r):
            if np.isinf(r):
                return [za.real, zb.real], [za.imag, zb.imag]
            ta, tb = np.angle(za - c), np.angle(zb - c)
            if ta < 0: ta += 2 * np.pi
            if tb < 0: tb += 2 * np.pi
            t_space = np.linspace(min(ta, tb), max(ta, tb), 100)
            if np.abs(ta - tb) > np.pi:
                t_space = np.linspace(max(ta, tb), min(ta, tb) + 2 * np.pi, 100)
            arc = c + r * np.exp(1j * t_space)
            return arc.real, arc.imag

        edges = [
            (current_vertices[0], current_vertices[1], c12, r12),
            (current_vertices[1], current_vertices[2], c23, r23),
            (current_vertices[2], current_vertices[0], c31, r31)
        ]
        for idx, (za, zb, c, r) in enumerate(edges):
            x_arc, y_arc = get_arc_coords(za, zb, c, r)
            arc_lines_2d[idx].set_data(x_arc, y_arc)

        centers_data = [(c12, r12), (c23, r23), (c31, r31)]
        cx_list, cy_list = [], []
        for idx, (c, r) in enumerate(centers_data):
            if not np.isinf(r):
                hc = c + r * np.exp(1j * theta_full)
                dashed_lines_2d[idx].set_data(hc.real, hc.imag)
                cx_list.append(c)
                cy_list.append(0.0)
                center_texts_2d[idx].set_position((c, -0.4))
                center_texts_2d[idx].set_text(f'C{idx}\n({c:.1f})')
            else:
                dashed_lines_2d[idx].set_data([], [])
                center_texts_2d[idx].set_text('')

        center_plots_2d.set_data(cx_list, cy_list)
        ax2d.set_title(f'Hyperbolic Plane Model (Upper Half-Plane)\nArea = {area:.4f}', fontsize=14, loc='left')

    else:
        # --- Update 3D Hyperbola (Hyperboloid) View ---
        pts_3d = [uhp_to_hyperboloid(z) for z in current_vertices]
        max_z = max(p[2] for p in pts_3d)
        z_rim = max(max_z * 1.25, 3.5)

        # Redraw semi-transparent 3D hyperboloid sheet if rim height changed significantly
        if surf_3d is None or last_z_rim is None or abs(z_rim - last_z_rim) > 0.4:
            if surf_3d is not None:
                surf_3d.remove()
            last_z_rim = z_rim
            r_max = np.sqrt(z_rim**2 - 1.0)
            R_grid = U_grid * r_max
            X_surf = R_grid * np.cos(PHI_grid)
            Y_surf = R_grid * np.sin(PHI_grid)
            Z_surf = np.sqrt(1.0 + R_grid**2)
            surf_3d = ax3d.plot_surface(
                X_surf, Y_surf, Z_surf,
                cmap='winter', alpha=0.22, edgecolor='teal', linewidth=0.25, antialiased=True
            )
            ax3d.set_xlim(-r_max, r_max)
            ax3d.set_ylim(-r_max, r_max)
            ax3d.set_zlim(0, z_rim)
            ax3d.set_xlabel('X')
            ax3d.set_ylabel('Y')
            ax3d.set_zlabel('Z')

        # Update 3D vertices & labels
        vx = [p[0] for p in pts_3d]
        vy = [p[1] for p in pts_3d]
        vz = [p[2] for p in pts_3d]
        vertex_plots_3d.set_data_3d(vx, vy, vz)

        for i, (p, z) in enumerate(zip(pts_3d, current_vertices)):
            vertex_texts_3d[i].set_position_3d((p[0], p[1], p[2] + 0.18))
            vertex_texts_3d[i].set_text(f'Z{i+1} ({z.real:.1f}+{z.imag:.1f}i)')

        # Update 3D hyperbola geodesics (solid edges + dashed extended hyperbolas + apexes)
        pairs = [(0, 1), (1, 2), (2, 0)]
        apex_x, apex_y, apex_z = [], [], []
        for idx, (ia, ib) in enumerate(pairs):
            arc_pts, full_pts, apex_pt = get_3d_hyperbola_geodesic(pts_3d[ia], pts_3d[ib], last_z_rim)
            arc_lines_3d[idx].set_data_3d(arc_pts[0], arc_pts[1], arc_pts[2])
            dashed_lines_3d[idx].set_data_3d(full_pts[0], full_pts[1], full_pts[2])

            apex_x.append(apex_pt[0])
            apex_y.append(apex_pt[1])
            apex_z.append(apex_pt[2])
            apex_texts_3d[idx].set_position_3d((apex_pt[0], apex_pt[1], apex_pt[2] - 0.25))
            apex_texts_3d[idx].set_text(f'C{idx}')

        apex_plots_3d.set_data_3d(apex_x, apex_y, apex_z)
        ax3d.set_title(
            f'3D Hyperbola Model (Hyperboloid Z² - X² - Y² = 1)\n'
            f'Area = {area:.4f}  |  Drag vertex to move, drag space to rotate',
            fontsize=13, loc='left'
        )
        ax3d.legend(loc='upper left')

    fig.canvas.draw_idle()

# ==========================================
# 5. Toggle Callback & Mouse Event Handlers
# ==========================================

def on_mode_change(label):
    global current_mode, dragging_index
    current_mode = label
    dragging_index = None

    if current_mode == "hyperbolic plane":
        ax3d.disable_mouse_rotation()
        ax3d.set_visible(False)
        ax2d.set_visible(True)
    else:
        ax2d.set_visible(False)
        ax3d.set_visible(True)
        ax3d.mouse_init()

    update_visualization()

radio.on_clicked(on_mode_change)

dragging_index = None

def get_3d_screen_pixels(pt3d):
    """Projects a 3D point (X, Y, Z) to 2D display pixel coordinates."""
    x2, y2, _ = proj3d.proj_transform(pt3d[0], pt3d[1], pt3d[2], ax3d.get_proj())
    return ax3d.transData.transform((x2, y2))

def on_press(event):
    global dragging_index
    if event.button != 1:
        return

    if current_mode == "hyperbolic plane" and event.inaxes == ax2d:
        click_z = event.xdata + 1j * event.ydata
        distances = [np.abs(click_z - z) for z in current_vertices]
        min_idx = int(np.argmin(distances))
        if distances[min_idx] < 0.8:
            dragging_index = min_idx

    elif current_mode == "hyperbola" and event.inaxes == ax3d:
        pts_3d = [uhp_to_hyperboloid(z) for z in current_vertices]
        click_px = np.array([event.x, event.y])
        pixel_dists = [np.linalg.norm(get_3d_screen_pixels(p) - click_px) for p in pts_3d]
        min_idx = int(np.argmin(pixel_dists))
        # If clicked within 15 pixels of a 3D vertex, grab it and pause 3D camera rotation
        if pixel_dists[min_idx] < 15.0:
            dragging_index = min_idx
            ax3d.disable_mouse_rotation()

def on_motion(event):
    global dragging_index
    if dragging_index is None:
        return

    if current_mode == "hyperbolic plane" and event.inaxes == ax2d:
        if event.xdata is None or event.ydata is None:
            return
        new_imag = max(event.ydata, 0.05)
        current_vertices[dragging_index] = event.xdata + 1j * new_imag
        update_visualization()

    elif current_mode == "hyperbola" and event.inaxes == ax3d:
        # Slide the grabbed vertex along the 3D hyperboloid using local screen Jacobian
        p_cur = uhp_to_hyperboloid(current_vertices[dragging_index])
        X, Y = p_cur[0], p_cur[1]
        px_cur = get_3d_screen_pixels(p_cur)
        delta_px = np.array([event.x, event.y]) - px_cur

        eps = 1e-2
        p_dx = np.array([X + eps, Y, np.sqrt(1.0 + (X + eps)**2 + Y**2)])
        p_dy = np.array([X, Y + eps, np.sqrt(1.0 + X**2 + (Y + eps)**2)])
        J = np.column_stack([
            (get_3d_screen_pixels(p_dx) - px_cur) / eps,
            (get_3d_screen_pixels(p_dy) - px_cur) / eps
        ])
        # Regularized least-squares step on (X, Y)
        dXY = np.linalg.lstsq(J.T @ J + 1e-3 * np.eye(2), J.T @ delta_px, rcond=None)[0]
        X_new, Y_new = X + dXY[0], Y + dXY[1]
        current_vertices[dragging_index] = hyperboloid_to_uhp(X_new, Y_new)
        update_visualization()

def on_release(event):
    global dragging_index
    if dragging_index is not None and current_mode == "hyperbola":
        ax3d.mouse_init()  # Re-enable 3D rotation after releasing vertex
    dragging_index = None

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# Initial render
update_visualization()
plt.show()
