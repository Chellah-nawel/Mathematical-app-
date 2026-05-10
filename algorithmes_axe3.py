import numpy as np

def _add_poly(p1, p2):
    n = max(len(p1), len(p2))
    res = [0.0] * n
    for i in range(n):
        if i < len(p1): res[i] += p1[i]
        if i < len(p2): res[i] += p2[i]
    return res

def _mul_poly(p1, p2):
    res = [0.0] * (len(p1) + len(p2) - 1)
    for i in range(len(p1)):
        for j in range(len(p2)):
            res[i+j] += p1[i] * p2[j]
    return res

def _scalar_mul(p, k):
    return [c * k for c in p]

def calcule_poly(p, x):
    return sum(p[i] * (x ** i) for i in range(len(p)))

def _asc_to_numpy(p_asc):
    return np.array(p_asc[::-1], dtype=float)

def _poly_to_str(coeffs_numpy):
    coeffs = np.array(coeffs_numpy, dtype=float)
    deg = len(coeffs) - 1
    terms = []
    for i, c in enumerate(coeffs):
        power = deg - i
        if abs(c) < 1e-10:
            continue
        c_str = f"{c:.4g}"
        if power == 0:
            terms.append(c_str)
        elif power == 1:
            terms.append(f"{c_str}x")
        else:
            terms.append(f"{c_str}x^{power}")
    if not terms:
        return "P(x) = 0"
    return "P(x) = " + " + ".join(terms).replace("+ -", "− ")



def newton(X, Y):
    n = len(X)

    diff = [[0.0] * n for _ in range(n)]
    for i in range(n):
        diff[i][0] = float(Y[i])

    for j in range(1, n):
        for i in range(n - j):
            diff[i][j] = (diff[i+1][j-1] - diff[i][j-1]) / (X[i+j] - X[i])

    coeffs_dd = [diff[0][j] for j in range(n)]

    P    = [coeffs_dd[0]]
    prod = [1.0]
    for j in range(1, n):
        prod = _mul_poly(prod, [-X[j-1], 1.0])
        P    = _add_poly(P, _scalar_mul(prod, coeffs_dd[j]))

    coeffs_numpy = _asc_to_numpy(P)
    poly_str     = _poly_to_str(coeffs_numpy)

    return coeffs_numpy, poly_str, diff, coeffs_dd
