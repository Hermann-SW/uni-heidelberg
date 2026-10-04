# code from free gemini.google.com, 3 propmpts in only 10 minutes

import sys
import matplotlib.pyplot as plt
import numpy as np


def format_term(val, variable_str):
  """Helper to format terms like + 2 or - 2 cleanly."""
  if val == 0:
    return ""
  elif val > 0:
    return f" + {val:.1f}{variable_str}"
  else:
    return f" - {abs(val):.1f}{variable_str}"


def format_constant(val):
  """Helper to format the constant term b cleanly."""
  if val == 0:
    return ""
  elif val > 0:
    return f" + {val:.1f}"
  else:
    return f" - {abs(val):.1f}"


def plot_elliptic_curve(P1, P2):
  x1, y1 = P1
  x2, y2 = P2

  # 1. Solve the linear system for a and b:
  M = np.array([[x1, 1.0], [x2, 1.0]])
  Y_vals = np.array([y1**2 - x1**3, y2**2 - x2**3])

  a, b = np.linalg.solve(M, Y_vals)

  # Build formatted equation string
  eq_str = f"$y^2 = x^3{format_term(a, 'x')}{format_constant(b)}$"

  print("Calculated parameters:")
  print(f"a = {a}")
  print(f"b = {b}")

  # 2. Set up the plotting grid around the points
  x_min = min(x1, x2) - 4
  x_max = max(x1, x2) + 4
  y_min = -max(abs(y1), abs(y2)) - 6
  y_max = max(abs(y1), abs(y2)) + 6

  x = np.linspace(x_min, x_max, 600)
  y = np.linspace(y_min, y_max, 600)
  X, Y = np.meshgrid(x, y)

  # Implicit function F(x, y) = y^2 - (x^3 + ax + b) = 0
  F = Y**2 - (X**3 + a * X + b)

  # 3. Create the plot
  plt.figure(figsize=(9, 7))

  # Plot the curve where F(x, y) = 0
  plt.contour(X, Y, F, levels=[0], colors="royalblue", linewidths=2.5)

  # Plot the given points
  plt.scatter(
      [x1, x2],
      [y1, y2],
      color="crimson",
      s=70,
      zorder=5,
      label=f"Points: $P_1({x1},{y1})$, $P_2({x2},{y2})$",
  )

  # Axis formatting & aesthetics
  plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
  plt.axvline(0, color="black", linewidth=0.8, linestyle="--")
  plt.title(f"Elliptic Curve: {eq_str}", fontsize=13, pad=12)
  plt.xlabel("$x$", fontsize=11)
  plt.ylabel("$y$", fontsize=11)
  plt.grid(True, linestyle=":", alpha=0.5)
  plt.legend(loc="upper left")
  plt.xlim(x_min, x_max)
  plt.ylim(y_min, y_max)

  plt.show()


if __name__ == "__main__":
  if len(sys.argv) == 5:
    try:
      x1, y1, x2, y2 = map(float, sys.argv[1:5])
      plot_elliptic_curve((x1, y1), (x2, y2))
    except ValueError:
      print("Error: Please provide valid numbers for coordinates.")
      print("Usage: python unique_ec.py x1 y1 x2 y2")
  else:
    print("Usage: python unique_ec.py x1 y1 x2 y2")
    print("Example: python unique_ec.py 9 2 7 6")
