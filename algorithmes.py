import numpy as np

def gauss(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(A)
    A_aug = np.hstack([A, b.reshape(-1, 1)])

    for i in range(n):
        # Pivot partiel 
        pivot_row = np.argmax(np.abs(A_aug[i:, i])) + i

        if pivot_row != i:
            A_aug[[i, pivot_row]] = A_aug[[pivot_row, i]]

        # Verification pivot nul 
        if abs(A_aug[i, i]) < 1e-12:
            raise ValueError(
                f"Pivot nul détecté à la colonne {i+1}.\n"
                "La matrice est singulière ou mal conditionnée.\n"
                "Le système n'admet pas de solution unique."
            )

        # elimination
        for j in range(i + 1, n):
            facteur = A_aug[j, i] / A_aug[i, i]
            A_aug[j, i:] -= facteur * A_aug[i, i:]

    # Substitution arriere
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (A_aug[i, -1] - np.dot(A_aug[i, i+1:n], x[i+1:])) / A_aug[i, i]

    return x, None, None, None


def lu(A, b):
    """Décomposition LU avec pivot partiel (permutation de lignes via matrice P)."""
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(A)

    L = np.eye(n)
    U = A.copy()
    P = np.eye(n)          # Matrice de permutation

    for i in range(n):
        # Pivot partiel
        pivot_row = np.argmax(np.abs(U[i:, i])) + i

        if pivot_row != i:
            U[[i, pivot_row]]    = U[[pivot_row, i]]
            P[[i, pivot_row]]    = P[[pivot_row, i]]
            if i > 0:
                L[[i, pivot_row], :i] = L[[pivot_row, i], :i]

        # Vérification pivot nul
        if abs(U[i, i]) < 1e-12:
            raise ValueError(
                f"Pivot nul détecté à la colonne {i+1}.\n"
                "La matrice est singulière ou mal conditionnée.\n"
                "Le système n'admet pas de solution unique."
            )

        for j in range(i + 1, n):
            L[j, i] = U[j, i] / U[i, i]
            U[j, i:] -= L[j, i] * U[i, i:]

    # Ly = Pb
    Pb = np.dot(P, b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = Pb[i] - sum(L[i, j] * y[j] for j in range(i))

    # Ux = y
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i, j] * x[j] for j in range(i + 1, n))) / U[i, i]

    return x, None, None, None



_SINGULAR_FLAG = "SINGULAR_MATRIX" 

def _check_singular(A):
    """Retourne le message d'erreur si det(A) ≈ 0, sinon None."""
    det = np.linalg.det(A)
    if abs(det) < 1e-10:
        return (
            _SINGULAR_FLAG,
            f"det(A) = {det:.2e}  ≈  0\n"
            "La matrice est singulière.\n"
            "Les méthodes itératives ne peuvent pas converger."
        )
    return None


def jacobi(A, b, tol=1e-5, max_iter=1000):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    err = _check_singular(A)
    if err:
        return None, None, None, None, err  # (x, M, errors, solutions, erreur)

    n = len(A)
    x = np.zeros(n)

    D_inv = np.diag(1 / np.diag(A))
    L = -np.tril(A, -1)
    U = -np.triu(A, 1)
    M = np.dot(D_inv, (L + U))

    errors    = []
    solutions = []

    for iteration in range(max_iter):
        x_new = np.zeros(n)
        for i in range(n):
            somme = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - somme) / A[i, i]

        residu = np.linalg.norm(np.dot(A, x_new) - b)
        errors.append(residu)
        solutions.append(x_new.copy())

        if residu < tol:
            return x_new, M, errors, solutions, iteration + 1

        x = x_new.copy()

    return x, M, errors, solutions, max_iter


def gauss_seidel(A, b, tol=1e-5, max_iter=1000):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    err = _check_singular(A)
    if err:
        return None, None, None, None, err

    n = len(A)
    x = np.zeros(n)

    E = np.tril(A, -1)
    F = np.triu(A, 1)
    D = np.diag(np.diag(A))
    M = np.dot(np.linalg.inv(D - E), F)

    errors    = []
    solutions = []

    for iteration in range(max_iter):
        x_old = x.copy()

        for i in range(n):
            somme1 = sum(A[i, j] * x[j]     for j in range(i))
            somme2 = sum(A[i, j] * x_old[j] for j in range(i + 1, n))
            x[i] = (b[i] - somme1 - somme2) / A[i, i]

        residu = np.linalg.norm(np.dot(A, x) - b)
        errors.append(residu)
        solutions.append(x.copy())

        if residu < tol:
            return x, M, errors, solutions, iteration + 1

    return x, M, errors, solutions, max_iter


def relaxation(A, b, omega=1.25, tol=1e-5, max_iter=1000):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    err = _check_singular(A)
    if err:
        return None, None, None, None, err

    n = len(A)
    x = np.zeros(n)

    errors    = []
    solutions = []

    for iteration in range(max_iter):
        x_old = x.copy()

        for i in range(n):
            somme1 = sum(A[i, j] * x[j]     for j in range(i))
            somme2 = sum(A[i, j] * x_old[j] for j in range(i + 1, n))
            x[i] = (1 - omega) * x_old[i] + omega * (b[i] - somme1 - somme2) / A[i, i]

        residu = np.linalg.norm(np.dot(A, x) - b)
        errors.append(residu)
        solutions.append(x.copy())

        if residu < tol:
            return x, None, errors, solutions, iteration + 1

    return x, None, errors, solutions, max_iter
