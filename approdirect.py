import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import sympy as sp
import random


def lancer_mc_continu(inputs, lbl_poly, lbl_cout,
                      lbl_matM, canvas_frame, format_matrix):

    # =========================================================
    # RECUPERATION DES DONNEES DE L'INTERFACE
    # =========================================================

    # ---------- fonction ----------
    try:
        # exemple :
        # sin(x)
        # x**2 + 3*x
        # exp(x)
        f_str = inputs["mc_func"]

        # verifier que le champ n'est pas vide
        if f_str.strip() == "":
            raise ValueError

    except:
        messagebox.showerror(
            "Erreur",
            "Fonction invalide"
        )
        return

    # ---------- intervalle ----------
    try:
        a = float(inputs["mc_a"])
        b = float(inputs["mc_b"])

    except:
        messagebox.showerror(
            "Erreur",
            "Intervalle invalide"
        )
        return

    # verifier que a < b
    if a >= b:
        messagebox.showerror(
            "Erreur",
            "Il faut que a < b"
        )
        return

    # ---------- degré max ----------
    try:
        S = int(inputs["mc_deg"])

    except:
        messagebox.showerror(
            "Erreur",
            "Degré invalide"
        )
        return

    # le degré doit etre positif
    if S < 0:
        messagebox.showerror(
            "Erreur",
            "Le degré doit être positif"
        )
        return


    # =========================================================
    # TRANSFORMATION DE LA FONCTION TEXTE
    # EN VRAIE FONCTION PYTHON
    # =========================================================

    try:

        # creation du symbole x
        x = sp.Symbol("x")

        # transforme le texte en expression mathematique
        expr = sp.sympify(f_str)

        # transforme l'expression en fonction python
        # compatible avec numpy
        f = sp.lambdify(x, expr, modules=["numpy"])

    except:
        messagebox.showerror(
            "Erreur",
            "Fonction mathématique invalide"
        )
        return


    # =========================================================
    # FONCTION QUI CALCULE LE POLYNOME
    # P(x) = a0 + a1*x + a2*x² + ...
    # =========================================================

    def poly(a, x):

        # tableau resultat rempli de zeros
        res = np.zeros_like(x, dtype=float)

        # ajout de chaque terme
        for i, ai in enumerate(a):
            res += ai * (x ** i)

        return res


    # =========================================================
    # DICTIONNAIRES POUR STOCKER :
    # - coefficients
    # - couts
    # - matrices
    # =========================================================

    coefficients = {}
    couts = {}
    matrices = {}


    # =========================================================
    # BOUCLE SUR TOUS LES DEGRES
    # de 0 jusqu'à S
    # =========================================================

    for s in range(S + 1):

        # =====================================================
        # MATRICE DE GRAM
        # G(i,j) = ∫ x^(i+j)
        # =====================================================

        G = np.zeros((s + 1, s + 1))

        for i in range(s + 1):
            for j in range(s + 1):

                # formule analytique :
                # ∫ x^n dx
                G[i, j] = (
                    (b ** (i + j + 1))
                    - (a ** (i + j + 1))
                ) / (i + j + 1)


        # =====================================================
        # VECTEUR d
        # d(i) = ∫ f(x)*x^i
        # =====================================================

        d = np.zeros(s + 1)

        for i in range(s + 1):

            # quad retourne :
            # valeur_integrale , erreur
            d[i], _ = integrate.quad(
                lambda t: f(t) * (t ** i),
                a,
                b
            )


        # =====================================================
        # RESOLUTION DU SYSTEME
        # G*a = d
        # =====================================================

        a_coef = np.linalg.solve(G, d)


        # =====================================================
        # CALCUL DE L'ERREUR
        # J = ∫ (f(x)-P(x))²
        # =====================================================

        def integrand(x):

            # poly retourne un tableau
            # donc on prend [0]
            return (
                f(x)
                - poly(a_coef, np.array([x]))[0]
            ) ** 2

        J, _ = integrate.quad(
            integrand,
            a,
            b
        )


        # =====================================================
        # SAUVEGARDE DES RESULTATS
        # =====================================================

        coefficients[s] = a_coef
        couts[s] = J
        matrices[s] = G


    # =========================================================
    # RECHERCHE DU MEILLEUR POLYNOME
    # celui qui minimise le cout
    # =========================================================

    best = min(couts, key=couts.get)

    best_a = coefficients[best]
    best_J = couts[best]
    best_M = matrices[best]


    # =========================================================
    # AFFICHAGE TEXTE DU MEILLEUR POLYNOME
    # =========================================================

    termes = []

    for i in range(len(best_a)):

        # terme constant
        if i == 0:
            termes.append(f"{best_a[i]:.5f}")

        # autres termes
        else:
            termes.append(
                f"{best_a[i]:.5f}x^{i}"
            )

    lbl_poly.configure(
        text="P(x) = " + " + ".join(termes)
    )


    # =========================================================
    # AFFICHAGE DU COUT
    # =========================================================

    lbl_cout.configure(
        text=f"{best_J:.8f}"
    )


    # =========================================================
    # AFFICHAGE DE LA MATRICE
    # =========================================================

    lbl_matM.configure(
        text=format_matrix(best_M)
    )


    # =========================================================
    # CREATION DE LA FIGURE MATPLOTLIB
    # =========================================================

    fig = plt.Figure(figsize=(5, 4), dpi=100)

    ax = fig.add_subplot(111)

    # sauvegarde pour exportation
    canvas_frame.figure = fig


    # =========================================================
    # CREATION DES POINTS x POUR LE DESSIN
    # =========================================================

    x_plot = np.linspace(a, b, 400)


    # =========================================================
    # DESSIN DE LA FONCTION REELLE
    # =========================================================

    y_f = f(x_plot)

    ax.plot(
        x_plot,
        y_f,
        color="black",
        linewidth=3,
        label="f(x)"
    )


    # =========================================================
    # GENERATION DE COULEURS ALEATOIRES
    # =========================================================

    colors = []

    for i in range(S + 1):

        r = 0.3 + random.random() * 0.7
        g = 0.3 + random.random() * 0.7
        b_color = 0.3 + random.random() * 0.7

        colors.append((r, g, b_color))


    # =========================================================
    # DESSIN DE TOUS LES POLYNOMES
    # =========================================================

    for s in range(S + 1):

        # calcul du polynome
        y_plot = poly(
            coefficients[s],
            x_plot
        )

        # meilleur polynome
        if s == best:

            ax.plot(
                x_plot,
                y_plot,
                linewidth=3,
                label=f"Best P{s}"
            )

        # autres polynomes
        else:

            ax.plot(
                x_plot,
                y_plot,
                color=colors[s],
                alpha=0.7,
                label=f"P{s}"
            )


    # =========================================================
    # DETAILS GRAPHE
    # =========================================================

    ax.grid(True)

    ax.legend()

    ax.set_title(
        "Approximation continue"
    )


    # =========================================================
    # SUPPRIMER L'ANCIEN GRAPHE
    # =========================================================

    for widget in canvas_frame.winfo_children():
        widget.destroy()


    # =========================================================
    # AFFICHAGE DU NOUVEAU GRAPHE
    # DANS TKINTER
    # =========================================================

    canvas = FigureCanvasTkAgg(
        fig,
        master=canvas_frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )