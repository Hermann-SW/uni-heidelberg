from fractions import Fraction
import sys
import matplotlib.pyplot as plt
import numpy as np


def format_frac_tex(f):
  """Formats a Fraction into a clean LaTeX string for the plot."""
  if f.denominator == 1:
    return str(f.numerator)
  else:
    return f"\\frac{{{f.numerator}}}{{{f.denominator}}}"


def format_term(val, variable_str):
  if val == 0:
    return ""
  elif val > 0:
    return f" + {val:.1f}{variable_str}"
  else:
    return f" - {abs(val):.1f}{variable_str}"


def format_constant(val):
  if val == 0:
    return ""
  elif val > 0:
    return f" + {val:.1f}"
  else:
    return f" - {abs(val):.1f}"


def plot_elliptic_curve(f_P1, f_P2):
  fx1, fy1 = f_P1
  fx2, fy2 = f_P2
  x1, y1 = float(fx1), float(fy1)
  x2, y2 = float(fx2), float(fy2)

  # 1. Solve for a and b
  M = np.array([[x1, 1.0], [x2, 1.0]])
  Y_vals = np.array([y1**2 - x1**3, y2**2 - x2**3])
  a, b = np.linalg.solve(M, Y_vals)

  eq_str = f"$y^2 = x^3{format_term(a, 'x')}{format_constant(b)}$"

  print("Calculated parameters:")
  print(f"a = {a}")
  print(f"b = {b}")

  fig, ax = plt.subplots(figsize=(9, 7))

  # Enforce aspect-preserving 1:1 scaling ratio
  ax.set_aspect("equal", adjustable="datalim")

  # Initial view bounds centered around the points
  x_span = max(abs(x1 - x2) * 2, 8)
  y_span = max(abs(y1 - y2) * 2, 12)
  ax.set_xlim(min(x1, x2) - x_span, max(x1, x2) + x_span)
  ax.set_ylim(-max(abs(y1), abs(y2)) - y_span, max(abs(y1), abs(y2)) + y_span)

  contour_holder = [None]

  def update_contour(ax_obj):
    if contour_holder[0] is not None:
      for coll in contour_holder[0].collections:
        coll.remove()

    xmin, xmax = ax_obj.get_xlim()
    ymin, ymax = ax_obj.get_ylim()

    # Generate fresh grid matching current view limits
    x = np.linspace(xmin, xmax, 800)
    y = np.linspace(ymin, ymax, 800)
    X, Y = np.meshgrid(x, y)
    F = Y**2 - (X**3 + a * X + b)

    contour_holder[0] = ax_obj.contour(
        X, Y, F, levels=[0], colors="royalblue", linewidths=2.5
    )
    fig.canvas.draw_idle()

  is_updating = [False]

  def on_lims_changed(ax_obj):
    if is_updating[0]:
      return
    is_updating[0] = True
    update_contour(ax_obj)
    is_updating[0] = False

  ax.callbacks.connect("xlim_changed", on_lims_changed)
  ax.callbacks.connect("ylim_changed", on_lims_changed)

  # Initial draw
  update_contour(ax)

  # Plot the given points
  p1_str = f"({format_frac_tex(fx1)}, {format_frac_tex(fy1)})"
  p2_str = f"({format_frac_tex(fx2)}, {format_frac_tex(fy2)})"
  ax.scatter(
      [x1, x2],
      [y1, y2],
      color="crimson",
      s=70,
      zorder=5,
      label=f"Points: $P_1{p1_str}$, $P_2{p2_str}$",
  )

  ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
  ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
  ax.set_title(f"Elliptic Curve: {eq_str}", fontsize=13, pad=12)
  ax.set_xlabel("$x$", fontsize=11)
  ax.set_ylabel("$y$", fontsize=11)
  ax.grid(True, linestyle=":", alpha=0.5)
  ax.legend(loc="upper left")

  plt.show()


if __name__ == "__main__":
  if len(sys.argv) == 5:
    try:
      f_x1 = Fraction(sys.argv[1])
      f_y1 = Fraction(sys.argv[2])
      f_x2 = Fraction(sys.argv[3])
      f_y2 = Fraction(sys.argv[4])
      plot_elliptic_curve((f_x1, f_y1), (f_x2, f_y2))
    except (ValueError, ZeroDivisionError):
      print(
          "Error: Please provide valid numbers or fractions for coordinates"
          " (e.g., 9/2)."
      )
      print("Usage: python unique_ec.py x1 y1 x2 y2")
  else:
    print("Usage: python unique_ec.py x1 y1 x2 y2")
    print("Example: python unique_ec.py 9/2 1 7/6 1")
