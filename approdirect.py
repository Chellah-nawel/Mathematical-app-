import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import sympy as sp
import random


def lancer_mc_continu(inputs, lbl_poly, lbl_cout, lbl_matM, canvas_frame, format_matrix):
    #recuperation donnee
    try:

        f_str = inputs["mc_func"]
        if f_str.strip() == "":
            raise ValueError

    except:
        messagebox.showerror(
            "Erreur",
            "Fonction invalide"
        )
        return

    try:
        a = float(inputs["mc_a"])
        b = float(inputs["mc_b"])

    except:
        messagebox.showerror(
            "Erreur",
            "Intervalle invalide"
        )
        return

    if a >= b:
        messagebox.showerror(
            "Erreur",
            "Il faut que a < b"
        )
        return

    try:
        S = int(inputs["mc_deg"])

    except:
        messagebox.showerror(
            "Erreur",
            "Degré invalide"
        )
        return

    if S < 0:
        messagebox.showerror(
            "Erreur",
            "Le degré doit être positif"
        )
        return



#transfert fonction str en fnct nqdro nkhdmo biha
    try:
        x = sp.Symbol("x")
        # txt en expression math
        expr = sp.sympify(f_str)
        f = sp.lambdify(x, expr, modules=["numpy"])

    except:
        messagebox.showerror(
            "Erreur",
            "Fonction mathématique invalide"
        )
        return



#calc polynome
    def poly(a, x):
        res = np.zeros_like(x, dtype=float)
        for i, ai in enumerate(a):
            res += ai * (x ** i)

        return res

    coefficients = {}
    couts = {}
    matrices = {}

    for s in range(S + 1):

        M = np.zeros((s + 1, s + 1))

        for i in range(s + 1):
            for j in range(s + 1):
                M[i, j] = (
                    (b ** (i + j + 1))
                    - (a ** (i + j + 1))
                ) / (i + j + 1)



        # vecteur d
        d = np.zeros(s + 1)
        for i in range(s + 1):

        # afin de calculer l integrale
            d[i], _ = integrate.quad(lambda t: f(t) * (t ** i),a,b)

        #resoudre systeme lineaire
        a_coef = np.linalg.solve(M, d)


     
        # calcul cout 
        

        def fonccout(x):

            return (f(x)- poly(a_coef, np.array([x]))[0]) ** 2

        J, _ = integrate.quad(fonccout,a,b)

        coefficients[s] = a_coef
        couts[s] = J
        matrices[s] = M



    #best poly
    best = min(couts, key=couts.get)

    best_a = coefficients[best]
    best_J = couts[best]
    best_M = matrices[best]



# affiche meilleur polynome
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



    # affiche cout
    lbl_cout.configure(
        text=f"{best_J:.8f}"
    )


#affiche matrice
    lbl_matM.configure(
        text=format_matrix(best_M)
    )


#graphe
    fig = plt.Figure(figsize=(5, 4), dpi=100)

    ax = fig.add_subplot(111)

    # sauvegarde pour exportation
    canvas_frame.figure = fig


#creation points

    x_plot = np.linspace(a, b, 400)


#fonction
    y_f = f(x_plot)

    ax.plot(
        x_plot,
        y_f,
        color="black",
        linewidth=3,
        label="f(x)"
    )


    colors = []

    for i in range(S + 1):

        r = 0.3 + random.random() * 0.7
        g = 0.3 + random.random() * 0.7
        b_color = 0.3 + random.random() * 0.7

        colors.append((r, g, b_color))


#dessinzz

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


    ax.grid(True)
    ax.legend()
    ax.set_title(
        "Approximation continue"
    )


#supp ancien graphe
    for widget in canvas_frame.winfo_children():
        widget.destroy()


#affiche nv grapghe
    canvas = FigureCanvasTkAgg(fig,master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both",expand=True)