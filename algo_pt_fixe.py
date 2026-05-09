import numpy as np
import matplotlib.pyplot as plt
from tools import *

#ALGO POINT FIXE

#f(x)=... -> x= phi 
def verify_phi(f_expr, phi_expr):
    f_sym   = to_sympy(f_expr)    #convert first
    phi_sym = to_sympy(phi_expr)
    try:
        roots = sp.solve(f_sym, x) #check if phi(x)- x and f(x) share the same roots
        if not roots:
            return True   #if cant verify (cos sin..) pass blindly
        
        for r in roots:
            val = sp.simplify(phi_sym.subs(x, r) - r)
            if val != 0:
                return False    
        return True
    except:
        return True

def verify_K(phi,a,b):
    phi_sym= to_sympy(phi)    

    #calc k = max|g'(x)| sur l intervalle de la racine
    xs = np.linspace(a, b, 1000)
    #calc de la born sup de la derivee
    phi_prim_sym = deriver(phi_sym)
    phi_prim = sympyto_numpy(phi_prim_sym)

    vals = phi_prim(xs)
    k_phi = np.max(np.abs(vals))#const contraction de phi

    if k_phi < 1:
        print(f"k= {k_phi:.4f} < 1 CONVERGE!")
        return k_phi,True
    else:
        print(f"k= {k_phi:.4f} >= 1 DIV!")
        return None, False

#phi is str
def point_fixe(f_expr, a, b, phi_expr, x0, ep):
    maxi=100
    # verifications
    if not continu(to_numpy(f_expr), a, b):
        return None,0
    if not verify_phi(f_expr, phi_expr):
        return None,0

    k, contract = verify_K(phi_expr, a, b)
    if not contract:
        return None,0

    phi= to_numpy(phi_expr)
    f=to_numpy(f_expr)
    x= x0
    row = []
    iterations = [x0]

    for i in range(maxi):
        xi= phi(x)
        errur = abs(xi - x)
        born = (k**1 /(1 - k)) * errur    

        row.append([i +1,f"{xi:.7f}",f"{errur:.7f}",f"{born:.7f}"])
        iterations.append(xi)
        x=xi

        if born <= ep:
            print(f"Converge en {i+1} iterations")
            draw_table(row)
            graphe(f,a,b,xi,iterations)
            return xi, i+1   #racine 

    print("Max iterations atteint sans convergence")
    return xi, i+1

def draw_table(row):
    cols = ["iteration","xi", "erreur", "born"]                         #les colonnes
    fig,ax = plt.subplots(figsize=(9, 6))                               #to position
    ax.axis('off')                                                      #to hide x y its not a graphe 
    ax.table(cellText=row, colLabels=cols, loc='center')                #insert vals
    plt.title("Algo du point fix", fontsize=13, fontweight='bold')
    plt.savefig('resultat/ptfixe_table.png', dpi=300, bbox_inches='tight')

def graphe(f,a,b,racine,iterations):
    x_plot = np.linspace(a, b, 500)
    plt.figure()
    plt.plot( x_plot , f(x_plot), color="black",linewidth=1)

    plt.scatter(iterations, [f(xi) for xi in iterations],marker='+', s=100, color='blue', label='Itérations')
    plt.scatter(racine, f(racine), color='red', label=f'racine = {racine:.5f}')
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.axhline (0 , color ="black", linewidth =0.5)    #les x
    plt.axvline (0 , color ="black", linewidth =0.5)    #les y
    plt.legend(loc='upper right')
    plt.grid()
    plt.savefig('resultat/ptfixe_graphe.png', dpi=300, bbox_inches='tight')
