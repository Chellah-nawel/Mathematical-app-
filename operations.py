import numpy as np

def normes_matricielles(A):
    A = np.array(A, dtype=float)
    norm1 = np.linalg.norm(A, 1)      # norme colonne
    norm2 = np.linalg.norm(A, 2)      # norme spectrale
    norm_inf = np.linalg.norm(A, np.inf)  # norme ligne
    return f"‖A‖₁ = {norm1:.4f}\n‖A‖₂ = {norm2:.4f}\n‖A‖∞ = {norm_inf:.4f}"

def normes_vectorielles(x, p=None):
    x = np.array(x, dtype=float)
    norm1 = np.linalg.norm(x, 1)
    norm2 = np.linalg.norm(x, 2)
    norm_inf = np.linalg.norm(x, np.inf)
    
    result = f"‖x‖₁ = {norm1:.4f}\n‖x‖₂ = {norm2:.4f}\n‖x‖∞ = {norm_inf:.4f}"
    if p and p > 0:
        norm_p = np.linalg.norm(x, float(p))
        result += f"\n‖x‖_{p} = {norm_p:.4f}"
    return result

def conditionnement(A):
    A = np.array(A, dtype=float)
    cond = np.linalg.cond(A, 2)
    if cond < 1e3:
        etat = "Bien conditionné"
    elif cond < 1e6:
        etat = "Conditionnement moyen"
    else:
        etat = "Mal conditionné "
    return f"κ(A) = {cond:.2e}\n{etat}"

def determinant(A):
    A = np.array(A, dtype=float)
    det = np.linalg.det(A)
    if abs(det) < 1e-10:
        return f"det(A) = {det:.2e}\n(≈ 0) → Matrice singulière"
    return f"det(A) = {det:.4f}"

def transposee(A):
    A = np.array(A, dtype=float)
    return str(A.T)

def inverse(A):
    A = np.array(A, dtype=float)
    try:
        inv = np.linalg.inv(A)
        return str(inv)
    except:
        return "Matrice non inversible (det = 0)"