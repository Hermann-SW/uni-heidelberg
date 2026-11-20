import cmath
import sys


def parse_complex(s: str) -> complex:
    # Support both math notation (1+2i) and Python notation (1+2j)
    s = s.strip().replace(" ", "").replace("i", "j")
    return complex(s)


def mat_mul(A, B):
    return [
        [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
        [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
    ]


def to_standard_matrix(p1: complex, p2: complex, p3: complex):
    """Matrix for the Möbius transform mapping (p1, p2, p3) -> (0, 1, inf)."""
    return [
        [p2 - p3, -p1 * (p2 - p3)],
        [p2 - p1, -p3 * (p2 - p1)],
    ]


def compute_mobius(z1, z2, z3, w1, w2, w3):
    if len({z1, z2, z3}) < 3:
        raise ValueError("z1, z2, z3 must be pairwise distinct.")
    if len({w1, w2, w3}) < 3:
        raise ValueError("w1, w2, w3 must be pairwise distinct.")

    Mz = to_standard_matrix(z1, z2, z3)
    Mw = to_standard_matrix(w1, w2, w3)

    # Adjugate of Mw (proportional to Mw^-1; scale cancels in Möbius transforms)
    adj_Mw = [
        [Mw[1][1], -Mw[0][1]],
        [-Mw[1][0], Mw[0][0]],
    ]

    M = mat_mul(adj_Mw, Mz)
    a, b = M[0]
    c, d = M[1]

    # Normalize so that ad - bc = 1 (unique up to a global sign ±1)
    det = a * d - b * c
    scale = cmath.sqrt(det)
    return a / scale, b / scale, c / scale, d / scale


def apply_mobius(a: complex, b: complex, c: complex, d: complex, z: complex):
    denom = c * z + d
    if cmath.isclose(denom, 0, abs_tol=1e-12):
        return "inf"
    return (a * z + b) / denom


def main():
    if len(sys.argv) < 7:
        print("Usage: python unique.py z1 z2 z3 w1 w2 w3 [z ...]")
        sys.exit(1)

    try:
        z1, z2, z3, w1, w2, w3 = (parse_complex(arg) for arg in sys.argv[1:7])
        extra_z = [parse_complex(arg) for arg in sys.argv[7:]]
        a, b, c, d = compute_mobius(z1, z2, z3, w1, w2, w3)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"a = {a}")
    print(f"b = {b}")
    print(f"c = {c}")
    print(f"d = {d}")

    if extra_z:
        print()
        for z in extra_z:
            mapped = apply_mobius(a, b, c, d, z)
            print(f"{z} -> {mapped}")


if __name__ == "__main__":
    main()
