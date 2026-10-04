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


def format_term_frac(f, variable_str):
  """Formats a coefficient Fraction for terms like x with proper signs."""
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
  """Formats a constant Fraction with proper signs."""
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


def plot_elliptic_curve(f_P1, f_P2):
  fx1, fy1 = f_P1
  fx2, fy2 = f_P2

  # 1. Exact fraction arithmetic to solve for a and b:
  # M = [[x1, 1], [x2, 1]], Y = [y1^2 - x1^3, y2^2 - x2^3]
  # Cramer's rule for exact fractions:
  det = fx1 - fx2
  # x1*a + b = y1^2 - x1^3
  # x2*a + b = y2^2 - x2^3
  Y1 = fy1**2 - fx1**3
  Y2 = fy2**2 - fx2**3

  # a = (Y1 - Y2) / (fx1 - fx2)
  f_a = (Y1 - Y2) / (fx1 - fx2)
  # b = Y1 - fx1 * f_a
  f_b = Y1 - fx1 * f_a

  print("Calculated parameters (Exact Fractions):")
  print(f"a = {f_a}")
  print(f"b = {f_b}")

  # Convert to float for numerical plotting/contour evaluation
  a, b = float(f_a), float(f_b)
  x1, y1 = float(fx1), float(fy1)
  x2, y2 = float(fx2), float(fy2)

  eq_str = (
      f"$y^2 = x^3{format_term_frac(f_a, 'x')}{format_constant_frac(f_b)}$"
  )

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

  update_contour(ax)

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
