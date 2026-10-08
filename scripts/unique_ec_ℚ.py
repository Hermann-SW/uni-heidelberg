from fractions import Fraction
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.widgets import Button, CheckButtons, TextBox
import numpy as np

# Check if cypari2 is available
CYPARI_AVAILABLE = False
try:
  import cypari2

  CYPARI_AVAILABLE = True
except ImportError:
  pass


def format_frac_tex(f):
  if f.denominator == 1:
    return str(f.numerator)
  else:
    return f"\\frac{{{f.numerator}}}{{{f.denominator}}}"


def format_term_frac(f, variable_str):
  if f == 0:
    return ""
  val = abs(f)
  num_str = (
      str(val.numerator)
      if val.denominator == 1
      else f"\\frac{{{val.numerator}}}{{{val.denominator}}}"
  )
  if f > 0:
    return f" + {num_str}{variable_str}"
  else:
    return f" - {num_str}{variable_str}"


def format_constant_frac(f):
  if f == 0:
    return ""
  val = abs(f)
  num_str = (
      str(val.numerator)
      if val.denominator == 1
      else f"\\frac{{{val.numerator}}}{{{val.denominator}}}"
  )
  if f > 0:
    return f" + {num_str}"
  else:
    return f" - {num_str}"


def print_usage():
  print("Usage options:")
  print(
      "  1) python unique_ec_ℚ.py x1 y1 x2 y2   (Specify via two rational"
      " points)"
  )
  print(
      "  2) python unique_ec_ℚ.py a b          (Specify via curve parameters a"
      " and b)"
  )
  print("Example 1: python unique_ec_ℚ.py 9/2 1 7/6 1")
  print("Example 2: python unique_ec_ℚ.py -209 1156")


def plot_elliptic_curve(f_a, f_b, input_points=None):
  a, b = float(f_a), float(f_b)
  eq_str = (
      f"$y^2 = x^3{format_term_frac(f_a, 'x')}{format_constant_frac(f_b)}$"
  )

  # Adjust layout to make room for widgets at the bottom
  fig, ax = plt.subplots(figsize=(10, 8))
  fig.subplots_adjust(bottom=0.25)

  ax.set_aspect("equal", adjustable="datalim")

  if input_points:
    fx1, fy1 = input_points[0]
    fx2, fy2 = input_points[1]
    x1, y1 = float(fx1), float(fy1)
    x2, y2 = float(fx2), float(fy2)
    x_span = max(abs(x1 - x2) * 2, 8)
    y_span = max(abs(y1 - y2) * 2, 12)
    ax.set_xlim(min(x1, x2) - x_span, max(x1, x2) + x_span)
    ax.set_ylim(
        -max(abs(y1), abs(y2)) - y_span, max(abs(y1), abs(y2)) + y_span
    )
  else:
    ax.set_xlim(-10, 10)
    ax.set_ylim(-12, 12)

  contour_holder = [None]
  rat_scatter_holder = [None]
  input_scatter_holder = [None]

  state = {
      "active": False,
      "integral": False,
      "scale45": False,
      "height": 1000,
  }

  point_labels = {}

  def transform_point(px, py):
    """Maps curve-space point (px, py) to plot-space with y-axis scaling y / sqrt(x)."""
    if state["scale45"] and px > 0:
      return px, py / np.sqrt(px)
    return px, py

  def get_pari_points():
    if not CYPARI_AVAILABLE or not state["active"]:
      return []
    try:
      pari = cypari2.Pari()
      pa = pari(str(f_a))
      pb = pari(str(f_b))
      E = pari.ellinit([0, 0, 0, pa, pb])
      if state["integral"]:
        pts = pari.ellratpoints(E, [state["height"], 1])
      else:
        pts = pari.ellratpoints(E, state["height"])
      parsed = []
      for pt in pts:
        if len(pt) >= 2:
          try:
            rx_str = str(pt[0])
            ry_str = str(pt[1])
            px = float(pt[0])
            py = float(pt[1])
            if py != 0:
              parsed.append((px, py, rx_str, ry_str))
          except Exception:
            pass
      return parsed
    except Exception as e:
      print(f"Error fetching ellratpoints: {e}")
      return []

  def y_tick_formatter(val, pos):
    if not state["scale45"] or val == 0:
      return f"{val:.0f}" if isinstance(val, int) or val == int(val) else f"{val}"
    try:
      roots = np.roots([1.0, 0.0, a - val**2, b])
      real_roots = [r.real for r in roots if np.isreal(r) and r.real > 0]
      if real_roots:
        x_val = min(real_roots)
        y_val = val * np.sqrt(x_val)
        if val < 0:
          y_val = -y_val
        if abs(y_val - round(y_val)) < 1e-3:
          return str(int(round(y_val)))
        return f"{y_val:.1f}"
    except Exception:
      pass
    return f"{val}"

  ax.yaxis.set_major_formatter(FuncFormatter(y_tick_formatter))

  def format_coord(x, y):
    true_y = y
    if state["scale45"] and x > 0:
      try:
        roots = np.roots([1.0, 0.0, a - y**2, b])
        real_roots = [r.real for r in roots if np.isreal(r) and r.real > 0]
        if real_roots:
          x_approx = min(real_roots)
          true_y = y * np.sqrt(x_approx)
          if y < 0:
            true_y = -true_y
      except Exception:
        pass
    return f"x={x:.3f}, y={true_y:.3f} (plot_y={y:.3f})"

  ax.format_coord = format_coord

  def update_plot_elements():
    if contour_holder[0] is not None:
      for coll in contour_holder[0].collections:
        coll.remove()

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    gx = np.linspace(xmin, xmax, 800)
    gy = np.linspace(ymin, ymax, 800)
    X, Y = np.meshgrid(gx, gy)

    if state["scale45"]:
      safe_sqrt_x = np.sqrt(np.maximum(0, X))
      F = np.where(
          X > 0,
          (Y * safe_sqrt_x) ** 2 - (X**3 + a * X + b),
          Y**2 - (X**3 + a * X + b),
      )
    else:
      F = Y**2 - (X**3 + a * X + b)

    contour_holder[0] = ax.contour(
        X, Y, F, levels=[0], colors="royalblue", linewidths=2.5
    )

    point_labels.clear()

    if input_points:
      for p in input_points:
        orig_px, orig_py = float(p[0]), float(p[1])
        if orig_py != 0:
          plot_px, plot_py = transform_point(orig_px, orig_py)
          point_labels[(plot_px, plot_py)] = f"({p[0]}, {p[1]})"

      if input_scatter_holder[0] is not None:
        input_scatter_holder[0].remove()

      ix = [k[0] for k in point_labels.keys()]
      iy = [k[1] for k in point_labels.keys()]
      if ix:
        p1_str = f"({format_frac_tex(input_points[0][0])}, {format_frac_tex(input_points[0][1])})"
        p2_str = f"({format_frac_tex(input_points[1][0])}, {format_frac_tex(input_points[1][1])})"
        input_scatter_holder[0] = ax.scatter(
            ix,
            iy,
            color="crimson",
            s=90,
            zorder=6,
            label=f"Input Points: $P_1{p1_str}$, $P_2{p2_str}$",
        )

    if rat_scatter_holder[0] is not None:
      rat_scatter_holder[0].remove()
      rat_scatter_holder[0] = None

    if state["active"] and CYPARI_AVAILABLE:
      r_pts = get_pari_points()
      if r_pts:
        rx, ry = [], []
        for p in r_pts:
          plot_px, plot_py = transform_point(p[0], p[1])
          point_labels[(plot_px, plot_py)] = f"({p[2]}, {p[3]})"
          rx.append(plot_px)
          ry.append(plot_py)

        rat_scatter_holder[0] = ax.scatter(
            rx,
            ry,
            color="darkorange",
            s=40,
            zorder=4,
            label="ellratpoints",
            alpha=0.8,
        )

    # Only show legend if there are labeled artists
    handles, labels = ax.get_legend_handles_labels()
    if handles:
      ax.legend(loc="upper left")

    fig.canvas.draw_idle()

  is_updating = [False]

  def on_lims_changed(ax_obj):
    if is_updating[0]:
      return
    is_updating[0] = True
    update_plot_elements()
    is_updating[0] = False

  ax.callbacks.connect("xlim_changed", on_lims_changed)
  ax.callbacks.connect("ylim_changed", on_lims_changed)

  update_plot_elements()

  ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
  ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
  ax.set_title(f"Elliptic Curve: {eq_str}", fontsize=13, pad=12)
  ax.set_xlabel("$x$", fontsize=11)
  ax.set_ylabel("$y$", fontsize=11)
  ax.grid(True, linestyle=":", alpha=0.5)

  handles, labels = ax.get_legend_handles_labels()
  if handles:
    ax.legend(loc="upper left")

  # --- Hover Tooltip Setup ---
  annot = ax.annotate(
      "",
      xy=(0, 0),
      xytext=(15, 15),
      textcoords="offset points",
      bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8, ec="black"),
      arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
  )
  annot.set_visible(False)

  def on_hover(event):
    if event.inaxes != ax:
      if annot.get_visible():
        annot.set_visible(False)
        fig.canvas.draw_idle()
      return

    found = False
    if point_labels:
      xmin, xmax = ax.get_xlim()
      ymin, ymax = ax.get_ylim()
      data_w = xmax - xmin
      data_h = ymax - ymin

      for (px, py), label_text in point_labels.items():
        dx = (event.xdata - px) / data_w
        dy = (event.ydata - py) / data_h
        dist = np.sqrt(dx**2 + dy**2)
        if dist < 0.03:
          annot.xy = (px, py)
          annot.set_text(label_text)
          annot.set_visible(True)
          found = True
          fig.canvas.draw_idle()
          break

    if not found and annot.get_visible():
      annot.set_visible(False)
      fig.canvas.draw_idle()

  fig.canvas.mpl_connect("motion_notify_event", on_hover)

  # --- UI Widgets Setup ---
  ax_check = fig.add_axes([0.08, 0.05, 0.28, 0.15])
  ax_box = fig.add_axes([0.42, 0.09, 0.12, 0.06])
  ax_btn = fig.add_axes([0.57, 0.09, 0.22, 0.06])

  if CYPARI_AVAILABLE:
    chk = CheckButtons(
        ax_check,
        ["Find ellratpoints", "Integral only", "±45° Scale"],
        [False, False, False],
    )
    txt_box = TextBox(ax_box, "Height: ", initial="1000")
    btn_zoom = Button(ax_btn, "Zoom to All Points")

    chk.rectangles[1].set_facecolor("#e0e0e0")
    chk.rectangles[1].set_edgecolor("#aaaaaa")
    for text in chk.labels[1:2]:
      text.set_color("#888888")

    def on_check(label):
      if label == "Find ellratpoints":
        state["active"] = not state["active"]
        txt_box.ax.set_visible(state["active"])
        btn_zoom.ax.set_visible(state["active"])

        if state["active"]:
          chk.rectangles[1].set_facecolor("#ffffff")
          chk.rectangles[1].set_edgecolor("black")
          chk.labels[1].set_color("black")
        else:
          state["integral"] = False
          if chk.get_status()[1]:
            chk.set_active(1)
          chk.rectangles[1].set_facecolor("#e0e0e0")
          chk.rectangles[1].set_edgecolor("#aaaaaa")
          chk.labels[1].set_color("#888888")

      elif label == "Integral only":
        if state["active"]:
          state["integral"] = not state["integral"]
        else:
          if chk.get_status()[1]:
            chk.set_active(1)
          return

      elif label == "±45° Scale":
        state["scale45"] = not state["scale45"]

      update_plot_elements()

    chk.on_clicked(on_check)

    def submit_height(text):
      try:
        val = int(text)
        state["height"] = val
        update_plot_elements()
      except ValueError:
        print("Invalid height integer value.")

    txt_box.on_submit(submit_height)

    def zoom_to_all(event):
      if not state["active"]:
        return
      r_pts = get_pari_points()
      if input_points:
        all_x = [k[0] for k in point_labels.keys()] + [
            transform_point(p[0], p[1])[0] for p in r_pts if p[1] != 0
        ]
        all_y = [k[1] for k in point_labels.keys()] + [
            transform_point(p[0], p[1])[1] for p in r_pts if p[1] != 0
        ]
      else:
        all_x = (
            [transform_point(p[0], p[1])[0] for p in r_pts if p[1] != 0]
            if r_pts
            else [-5, 5]
        )
        all_y = (
            [transform_point(p[0], p[1])[1] for p in r_pts if p[1] != 0]
            if r_pts
            else [-5, 5]
        )

      if not all_x:
        all_x = [-5, 5]
        all_y = [-5, 5]

      xmin, xmax = min(all_x), max(all_x)
      ymin, ymax = min(all_y), max(all_y)

      cx = (xmin + xmax) / 2
      cy = (ymin + ymax) / 2
      span = max(xmax - xmin, ymax - ymin, 6) * 1.25

      is_updating[0] = True
      ax.set_xlim(cx - span / 2, cx + span / 2)
      ax.set_ylim(cy - span / 2, cy + span / 2)
      is_updating[0] = False
      update_plot_elements()

    btn_zoom.on_clicked(zoom_to_all)

    txt_box.ax.set_visible(False)
    btn_zoom.ax.set_visible(False)

    fig.text(
        0.08,
        0.01,
        "Hover over points to see coordinates. Check boxes & enter height for"
        " points.",
        fontsize=9,
        color="dimgray",
    )
  else:
    chk = CheckButtons(
        ax_check,
        ["Find ellratpoints (Disabled)", "Integral only", "±45° Scale"],
        [False, False, False],
    )
    chk.ax.set_facecolor("#e0e0e0")
    txt_box = TextBox(ax_box, "Height: ", initial="1000")
    btn_zoom = Button(ax_btn, "Zoom to All Points")
    txt_box.ax.set_visible(False)
    btn_zoom.ax.set_visible(False)
    ax_box.set_visible(False)
    ax_btn.set_visible(False)

    fig.text(
        0.08,
        0.01,
        "*(Note: Install cypari2 via 'pip install cypari2' to unlock"
        " ellratpoints features)*",
        fontsize=9,
        color="crimson",
        weight="bold",
    )

  plt.show()


if __name__ == "__main__":
  if len(sys.argv) == 5:
    try:
      f_x1 = Fraction(sys.argv[1])
      f_y1 = Fraction(sys.argv[2])
      f_x2 = Fraction(sys.argv[3])
      f_y2 = Fraction(sys.argv[4])
      Y1 = f_y1**2 - f_x1**3
      Y2 = f_y2**2 - f_x2**3
      f_a = (Y1 - Y2) / (f_x1 - f_x2)
      f_b = Y1 - f_x1 * f_a
      print("Calculated parameters (Exact Fractions):")
      print(f"a = {f_a}")
      print(f"b = {f_b}")
      plot_elliptic_curve(f_a, f_b, input_points=((f_x1, f_y1), (f_x2, f_y2)))
    except (ValueError, ZeroDivisionError):
      print(
          "Error: Please provide valid numbers or fractions for coordinates"
          " (e.g., 9/2)."
      )
      print_usage()
  elif len(sys.argv) == 3:
    try:
      f_a = Fraction(sys.argv[1])
      f_b = Fraction(sys.argv[2])
      print(f"Using curve parameters: a = {f_a}, b = {f_b}")
      plot_elliptic_curve(f_a, f_b, input_points=None)
    except (ValueError, ZeroDivisionError):
      print(
          "Error: Please provide valid numbers or fractions for a and b (e.g.,"
          " -209 1156)."
      )
      print_usage()
  else:
    print_usage()
