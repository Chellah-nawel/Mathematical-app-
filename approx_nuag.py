
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox


# SAISIE DES DONNEES

x_input = input("Entrer les valeurs de X : ")

# L'utilisateur entre les valeurs de Y séparées par des espaces
y_input = input("Entrer les valeurs de Y : ")


# Transfert str into array 
X = np.array(list(map(float, x_input.split())))
Y = np.array(list(map(float, y_input.split())))


# nb points nuage 
n = len(X)


#verification donnee inserer 

# X et Y de meme taille
if len(X) != len(Y):
    messagebox.showerror(
        "Erreur",
        "X et Y doivent avoir le même nombre de valeurs"
    )

    exit()




S = int(input("Entrer le degré maximal : "))



# Le degré doit être inférieur au nombre de points
if S >= n:
    messagebox.showerror(
        "Erreur",
        "le degré doit être inférieur au nombre de points""
    )
    exit()




#fonction des moindre carree
def MC(x, y, s):


    #matrice vandermonde
    V = np.vander(x, s + 1, increasing=True)

    # M = V^T * V
    M = np.dot(V.T, V)

    # B = V^T * y
    B = np.dot(V.T, y)


 #resoulution de sys lineaire M A=B
    a = np.linalg.solve(M, B)

    return a, M



# calculer le polynome 
def affiche_p(a, x):

    resultat = np.zeros_like(x, dtype=float)
  
    for i, ai in enumerate(a):

        resultat += ai * x**i


    return resultat




def cout(y, y_approx):

    # J = Σ (yi - Pi)^2
    return np.sum((y - y_approx)**2)



# ============================================================
# DICTIONNAIRES POUR STOCKER LES RESULTATS
# ============================================================

# coefficients des polynômes
coefficients = {}

# fonctions de coût
couts = {}

# matrices M
matrices_M = {}



# ============================================================
# CALCUL DE TOUS LES POLYNOMES
# ============================================================

# Boucle :
# on calcule tous les polynômes de degré 1 jusqu'à S
for s in range(1, S + 1):


    # --------------------------------------------------------
    # Calcul des coefficients
    # --------------------------------------------------------
    a, M = MC(X, Y, s)


    # --------------------------------------------------------
    # Valeurs approchées
    # --------------------------------------------------------
    y_approx = affiche_p(a, X)


    # --------------------------------------------------------
    # Calcul du coût
    # --------------------------------------------------------
    J = cout(Y, y_approx)


    # --------------------------------------------------------
    # Sauvegarde des résultats
    # --------------------------------------------------------
    coefficients[s] = a
    couts[s] = J
    matrices_M[s] = M



# ============================================================
# RECHERCHE DU MEILLEUR POLYNOME
# ============================================================

# min(couts, key=couts.get)
# retourne la clé correspondant au plus petit coût
meilleur_degre = min(couts, key=couts.get)


# coût minimal
meilleur_cout = couts[meilleur_degre]


# coefficients du meilleur polynôme
meilleur_polynome = coefficients[meilleur_degre]



# ============================================================
# AFFICHAGE DES RESULTATS
# ============================================================

print("\n================ RESULTATS ================\n")


# Affichage des informations pour chaque polynôme
for s in range(1, S + 1):

    print(f"Polynôme de degré {s}")

    print("Coefficients :")
    print(coefficients[s])

    print("\nMatrice M :")
    print(matrices_M[s])

    print(f"\nFonction de coût J = {couts[s]:.6f}")

    print("\n------------------------------------------\n")



# ============================================================
# AFFICHAGE DU MEILLEUR POLYNOME
# ============================================================

print("=========== MEILLEUR POLYNOME ===========")

print(f"Meilleur degré : {meilleur_degre}")

print(f"Coût minimal : {meilleur_cout:.6f}")

print("Coefficients :")
print(meilleur_polynome)



# ============================================================
# PREPARATION DU GRAPHE
# ============================================================

# Création de plusieurs valeurs de x
# pour avoir des courbes lisses
x_plot = np.linspace(min(X) - 0.5,
                     max(X) + 0.5,
                     500)



# ============================================================
# AFFICHAGE DU GRAPHE GLOBAL
# ============================================================

# Taille de la fenêtre
plt.figure(figsize=(10, 7))


# ------------------------------------------------------------
# Affichage du nuage de points
# ------------------------------------------------------------
plt.scatter(X,
            Y,
            color='black',
            s=60,
            zorder=5,
            label='Nuage de points')


import random

# Liste de couleurs possibles
couleurs_possibles = [
    'blue',
    'red',
    'green',
    'purple',
    'orange',
    'brown',
    'pink',
    'gray',
    'cyan',
    'magenta',
    'olive',
    'navy',
    'gold',
    'lime'
]

# Génération aléatoire des couleurs
couleurs = random.sample(couleurs_possibles, S)





for s in range(1, S + 1):

    # --------------------------------------------------------
    # Calcul des valeurs du polynôme
    # --------------------------------------------------------
    y_plot = affiche_p(coefficients[s], x_plot)


    # --------------------------------------------------------
    # Si c'est le meilleur polynôme
    # on l'affiche plus épais
    # --------------------------------------------------------
    if s == meilleur_degre:

        plt.plot(x_plot,
                 y_plot,
                 linewidth=4,
                 color=couleurs[s % len(couleurs)],
                 label=f'Meilleur P{s}(x)  -  J={couts[s]:.4f}')

    else:

        plt.plot(x_plot,
                 y_plot,
                 linewidth=2,
                 color=couleurs[s % len(couleurs)],
                 label=f'P{s}(x)  -  J={couts[s]:.4f}')



# ============================================================
# PERSONNALISATION DU GRAPHE
# ============================================================

plt.title("Approximation polynomiale par la méthode des moindres carrés")

plt.xlabel("x")

plt.ylabel("y")

plt.grid(True, linestyle='--', alpha=0.5)

plt.legend()



# ============================================================
# AFFICHAGE FINAL
# ============================================================

plt.show()