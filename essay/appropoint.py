import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def lancer_mc_depuis_interface(inputs, lbl_poly, lbl_cout, lbl_matM, canvas_frame,format_matrix):
#recuperer donnee
    try:
        X_list = []
        Y_list = []

        for p in inputs["points"]:
            X_list.append(float(p["x"]))
            Y_list.append(float(p["y"]))

        X = np.array(X_list)
        Y = np.array(Y_list)
    except:
        messagebox.showerror("Erreur", "Points invalides")
        return

    if len(X) < 2:
        messagebox.showerror("Erreur", "Pas assez de points")
        return

    try:
        S = int(inputs["mc_deg"])
    except:
        messagebox.showerror("Erreur", "Degré invalide")
        return

    if S >= len(X):
        messagebox.showerror("Erreur", "Degré trop grand")
        return


#moindre carree
    def MC(x, y, s):
        #matrice vander
        V = np.vander(x, s + 1, increasing=True)
        #calc M
        M = np.dot(V.T , V)
        #calc B
        B = np.dot(V.T , y)
        #coeff  calcul
        a = np.linalg.solve(M, B)
        return a, M
# calcul polynome
    def poly(a, x):
        r = np.zeros_like(x, dtype=float)
        for i, ai in enumerate(a):
            r += ai * x**i
        return r
#calc cout
    def cout(y, yp):
        return np.sum((y - yp)**2)


    coefficients = {}
    couts = {}
    matrices = {}

    for i in range(1, S + 1):
        a, M = MC(X, Y, i)

        ycalc = poly(a, X)

        coefficients[i] = a
        couts[i] = cout(Y, ycalc)
        matrices[i] = M
        #recuperer le poly avec le cout min 
    best = min(couts, key=couts.get)
    best_a = coefficients[best]
    best_J = couts[best]
    best_M = matrices[best]


 #affichage graphe
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    canvas_frame.figure = fig

    ax.scatter(X, Y, color="black")

    x_plot = np.linspace(min(X)-0.5, max(X)+0.5, 300)

    colors = []

    for i in range(S):
        r = 0.3 + random.random() * 0.7
        g = 0.3 + random.random() * 0.7
        b = 0.3 + random.random() * 0.7
        colors.append((r, g, b))

    for s in range(1, S + 1):
        y_plot = poly(coefficients[s], x_plot)

        if s == best:
            ax.plot(x_plot, y_plot, linewidth=3, label=f"Best P{s}")
        else:
            ax.plot(x_plot, y_plot, color=colors[s-1],label=f"P{s}", alpha=0.7)

    ax.legend()
    ax.grid(True)

    # effacer ancien graphe
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


#affiche dans interface 
    terms = []

    for i in range(len(best_a)):
        if i == 0:
            terms.append(f"{best_a[i]:.3f}")
        else:
            terms.append(f"{best_a[i]:.3f}x^{i}")

    lbl_poly.configure(
        text="P(x) = " + " + ".join(terms)
    )

    lbl_cout.configure(text=f"{best_J:.6f}")

    lbl_matM.configure(
        text=format_matrix(best_M)
    )