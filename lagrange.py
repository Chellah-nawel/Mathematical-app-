import numpy as np
import matplotlib.pyplot as plt

#x, y arrays xi, yi 
def lagrange(x, y, x_val):
    #x_val le x ou evaluer P
  
    n = len(x)          #nbr de pt
    p = 0.0             # = P(x_val)

    for i in range(n):  #construire Li(x_val) 
                        
        li = 1.0        #Li(x_val)
        for j in range(n):
            if j != i:
                li = li* (x_val - x[j]) /(x[i] - x[j])

        p = p + y[i]* li   # p= sum (yi * Li(x_val))

    return p


# x_pts, y_pts user points input
def poly_lagrange(x_pts, y_pts):
   
    x = np.array(x_pts, dtype=float)        #convert to array
    y = np.array(y_pts, dtype=float)
    n = len(x)                              #nbr de point

    #verify inputs 
    if len(x) != len(y):
        print("Erreur: x et y doivent avoir la meme taille")
        return None

    if len(np.unique(x)) != n:
        print("Erreur: les xi doivent etre distincts")
        return None

    #verifier si P(xi)=yi et estimer l erreur
    row = []
    err_max = 0.0

    for i in range(n):
        p_xi  = lagrange(x, y, x[i])          # verifier P(xi) doit = yi
        erreur = abs(p_xi - y[i])             #l erreur doit etre tres petite
        err_max = max(err_max, erreur)
        row.append([i, f"{x[i]:.4f}", f"{y[i]:.4f}",f"{p_xi:.4f}", f"{erreur:.2e}"])

    #print(f"Erreur max sur les noeuds : {err_max:.2e}")

    str_poly= display_poly(x, y ,n)
    draw_table(row)
    fig  = graphe(x, y)


    return err_max , str_poly , fig


def draw_table(row):
    cols = ["i", "xi", "yi", "P(xi)", "Erreur"]
    fig, ax = plt.subplots(figsize=(9, len(row) * 0.5 + 1.5))
    ax.axis('off')
    ax.table(cellText=row, colLabels=cols, loc='center', cellLoc='center')
    plt.title("Vérification — Interpolation de Lagrange",fontsize=12, fontweight='bold')
    fig.savefig('resultat/lagrange_table.png', dpi=300, bbox_inches='tight')
    return fig   


def graphe(x, y):
    a  = min(x) - 0.5
    b  = max(x) + 0.5
    xs = np.linspace(a, b, 500)
    ys = np.array([lagrange(x, y, xi) for xi in xs])

    fig, ax = plt.subplots(figsize=(8, 4))      
    ax.plot(xs, ys, color='black', linewidth=1.5, label='P(x)')
    ax.scatter(x, y, color='blue', zorder=5, s=60, label='Points donnés')
    ax.axhline(0, color='black', linewidth=0.4)
    ax.axvline(0, color='black', linewidth=0.4)
    ax.set_title("Interpolation de Lagrange", fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.savefig('resultat/lagrange_graphe.png', dpi=300, bbox_inches='tight')
    return fig                                  # figure     


def display_poly(x, y ,n):

    xs = np.linspace(min(x), max(x), 300)
    ys = np.array([lagrange(x, y, xi) for xi in xs])

    # numpy trouve les coefficients du polynôme
    coeffs = np.polyfit(xs, ys, n-1)    # degré n-1

    # construire la string P(x) = ax^n + bx^(n-1) + ...
    termes = []
    degre = len(coeffs) - 1

    for i, c in enumerate(coeffs):
        power = degre - i
        c = round(c, 4)              # arrondir pour l'affichage
        if c == 0:
            continue

        if power == 0:
            termes.append(f"{c}")
        elif power == 1:
            termes.append(f"{c}x")
        else:
            termes.append(f"{c}x^{power}")
    if not termes:
        return "P(x) = 0"
    
    poly_str = "P(x) = " + " + ".join(termes)
    poly_str = poly_str.replace("+ -", "- ")   # fix "+ -3x" → "- 3x"

    return poly_str
