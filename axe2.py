import customtkinter
import tkinter as tk
from tkinter import messagebox, filedialog
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from algorithmes import gauss, lu, jacobi, gauss_seidel, relaxation
from operations  import (normes_matricielles, normes_vectorielles,
                          conditionnement, determinant, transposee, inverse)

YELLOW     = "#f5c518"
YELLOW_HVR = "#e6b800"
LIGHT_BG   = "#f4f6f9"
WHITE      = "#ffffff"
DARK       = "#0d1b2e"
GREY       = "#777777"
GREEN      = "#22a361"
BORDER     = "#e0e0e0"
TIP_BG     = "#fffde7"
TIP_BORDER = "#f5e600"

last_errors    = []
last_solutions = []
last_M         = None
last_iters     = 0


#Recommandation dynamique 
def recommander_algo_indirect(A):
    A = np.array(A, dtype=float)
    n = len(A)

    diag = np.abs(np.diag(A))
    off  = np.array([np.sum(np.abs(A[i])) - diag[i] for i in range(n)])

    # Diagonale strictement dominante 
    sdd = np.all(diag > off)
    # Diagonale faiblement dominante 
    wdd = np.all(diag >= off)

    # SDP?
    symetrique = np.allclose(A, A.T, atol=1e-8)
    sdp = False
    if symetrique:
        try:
            np.linalg.cholesky(A)
            sdp = True
        except np.linalg.LinAlgError:
            pass

    # Rayon spectral
    try:
        D_inv = np.diag(1.0 / np.diag(A))
        L_neg = -np.tril(A, -1)
        U_neg = -np.triu(A, 1)
        B_jacobi = np.dot(D_inv, (L_neg + U_neg))
        rho_jacobi = max(abs(np.linalg.eigvals(B_jacobi)))
    except Exception:
        rho_jacobi = 9999.0

    try:
        D  = np.diag(np.diag(A))
        E  = np.tril(A, -1)
        F  = np.triu(A, 1)
        B_gs = np.dot(np.linalg.inv(D - E), F)
        rho_gs = max(abs(np.linalg.eigvals(B_gs)))
    except Exception:
        rho_gs = 9999.0

    # Conditionnement
    cond = np.linalg.cond(A, 2)

    # Cas 1 : aucune diagonale dominante 
    if not wdd and rho_jacobi >= 1.0 and rho_gs >= 1.0:
        return ("Gauss-Seidel",
                " Matrice non diagonalement dominante.\n"
                "Jacobi et GS peuvent diverger.\n"
                f"ρ(Jacobi)={rho_jacobi:.3f}, ρ(GS)={rho_gs:.3f}\n"
                "Gauss-Seidel est légèrement préférable\n"
                "mais envisagez Gauss ou LU.")

    # Cas 2 : SDP GS converge toujours
    if sdp:
        return ("Gauss-Seidel",
                " Matrice symétrique définie positive.\n"
                "Gauss-Seidel est garanti convergent.\n"
                f"ρ(GS) = {rho_gs:.4f}  ρ(Jacobi) = {rho_jacobi:.4f}\n"
                "GS converge en général 2× plus vite.")

    # Cas 3 : diagonale strictement dominante
    if sdd:
        if rho_gs <= rho_jacobi:
            return ("Gauss-Seidel",
                    f" Matrice à diagonale strictement dominante.\n"
                    f"ρ(GS) = {rho_gs:.4f} < ρ(Jacobi) = {rho_jacobi:.4f}\n"
                    "Gauss-Seidel converge plus vite.")
        else:
            return ("Jacobi",
                    f" Matrice à diagonale strictement dominante.\n"
                    f"ρ(Jacobi) = {rho_jacobi:.4f} < ρ(GS) = {rho_gs:.4f}\n"
                    "Jacobi converge plus vite ici (rare).\n"
                    "Peut être parallélisé efficacement.")

    # Cas 4 : diagonale faiblement dominante
    if wdd:
        if rho_gs < rho_jacobi:
            return ("Gauss-Seidel",
                    f" Diagonale faiblement dominante.\n"
                    f"ρ(GS) = {rho_gs:.4f} < ρ(Jacobi) = {rho_jacobi:.4f}\n"
                    "Gauss-Seidel est préférable.")
        else:
            return ("Jacobi",
                    f" Diagonale faiblement dominante.\n"
                    f"ρ(Jacobi) = {rho_jacobi:.4f} ≤ ρ(GS) = {rho_gs:.4f}\n"
                    "Jacobi légèrement avantageux.")

    if rho_gs < rho_jacobi:
        return ("Gauss-Seidel",
                f"ρ(GS) = {rho_gs:.4f} < ρ(Jacobi) = {rho_jacobi:.4f}\n"
                "Gauss-Seidel converge plus rapidement.")
    else:
        return ("Jacobi",
                f"ρ(Jacobi) = {rho_jacobi:.4f} ≤ ρ(GS) = {rho_gs:.4f}\n"
                "Jacobi est préférable pour cette matrice.")



def show(app, navigate):

    header = customtkinter.CTkFrame(app, fg_color=WHITE, corner_radius=0, height=54)
    header.pack(fill="x")
    header.pack_propagate(False)

    retour = customtkinter.CTkButton(header, text="←", width=38, height=38,
                                      fg_color="transparent", text_color=DARK,
                                      hover_color="#f0f0f0",
                                      font=customtkinter.CTkFont(size=20),
                                      corner_radius=8,
                                      command=lambda: navigate("accueil"))
    retour.pack(side="left", padx=(12, 6), pady=8)

    customtkinter.CTkLabel(header,
                            text="Axe 2 : Systèmes linéaires",
                            font=customtkinter.CTkFont(size=17, weight="bold"),
                            text_color=DARK).pack(side="left")

    #visualisation
    vis_frame = customtkinter.CTkFrame(app, fg_color=WHITE, corner_radius=12)
    vis_frame.pack(side="bottom", fill="x", padx=14, pady=(0, 14))

    vis_header = customtkinter.CTkFrame(vis_frame, fg_color="transparent")
    vis_header.pack(fill="x", padx=14, pady=(10, 0))

    customtkinter.CTkLabel(vis_header,
                            text="Visualisation",
                            font=customtkinter.CTkFont(size=13, weight="bold"),
                            text_color=DARK).pack(side="left")

    def on_export():
        """Exporte la solution / resultats dans un fichier .txt"""
        sel  = current_sel.get()
        mode = current_mode.get()
        lines = [f"=== Résultats — {sel} ===\n"]

        if mode == "algo":
            # solution
            for w in solution_frame.winfo_children():
                if isinstance(w, customtkinter.CTkLabel):
                    lines.append(w.cget("text"))
            if sel in ITER_ALGOS:
                lines.append(f"\nItérations : {lbl_iterations.cget('text')}")
                lines.append(f"Résidu     : {lbl_residu.cget('text')}")
                lines.append(f"Convergence: {lbl_conv.cget('text')}")
                lines.append(f"\nMatrice d'itération :\n{lbl_iter_mat.cget('text')}")
        else:
            lines.append(lbl_op_val.cget("text"))

        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Texte", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            messagebox.showinfo("Export", f"Fichier sauvegardé :\n{path}")

    btn_export = customtkinter.CTkButton(vis_header,
                                          text="⬇  Exporter résultats",
                                          width=160, height=30,
                                          fg_color=LIGHT_BG, text_color=DARK,
                                          hover_color=BORDER,
                                          border_width=1, border_color=BORDER,
                                          corner_radius=8,
                                          font=customtkinter.CTkFont(size=11),
                                          command=on_export)
    btn_export.pack(side="right")

    # frame interne pour le canvas matplotlib
    vis_canvas_frame = customtkinter.CTkFrame(vis_frame, fg_color="transparent", height=200)
    vis_canvas_frame.pack(fill="x", padx=14, pady=(4, 10))
    vis_canvas_frame.pack_propagate(False)

    _current_fig_canvas = None   # reference au canvas matplotlib actif

    def clear_vis():
        nonlocal _current_fig_canvas
        if _current_fig_canvas:
            _current_fig_canvas.get_tk_widget().destroy()
            _current_fig_canvas = None
        for w in vis_canvas_frame.winfo_children():
            w.destroy()

    def draw_convergence(errors, name):
        """Affiche la courbe de convergence"""
        nonlocal _current_fig_canvas
        clear_vis()
        fig, ax = plt.subplots(figsize=(9, 1.9))
        ax.semilogy(range(1, len(errors)+1), errors, "b-", linewidth=2, marker="o", markersize=3)
        ax.axhline(y=1e-5, color="r", linestyle=":", alpha=0.7, label="Tolérance (1e-5)")
        ax.set_xlabel("Itérations", fontsize=9)
        ax.set_ylabel("Résidu (log)", fontsize=9)
        ax.set_title(f"Convergence — {name}", fontsize=10, fontweight="bold")
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.legend(fontsize=8)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=vis_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        _current_fig_canvas = canvas
        plt.close(fig)

    #body
    body = customtkinter.CTkFrame(app, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=14, pady=(10, 8))

    # SIDEBAR
    sidebar = customtkinter.CTkScrollableFrame(body, fg_color=WHITE,
                                                corner_radius=12, width=186)
    sidebar.pack(side="left", fill="y", padx=(0, 8))

    customtkinter.CTkLabel(sidebar, text="Algorithmes directs",
                            font=customtkinter.CTkFont(size=13, weight="bold"),
                            text_color=DARK).pack(anchor="w", padx=14, pady=(14, 6))

    algo_btns    = {}
    op_btns      = {}
    current_sel  = tk.StringVar()
    current_mode = tk.StringVar(value="algo")

    def refresh_algo_btns():
        sel = current_sel.get()
        for name, btn in algo_btns.items():
            active = (name == sel)
            btn.configure(fg_color=YELLOW if active else WHITE,
                          border_width=0 if active else 1,
                          font=customtkinter.CTkFont(size=15 if active else 13,
                                                      weight="bold" if active else "normal"))
        for btn in op_btns.values():
            btn.configure(fg_color=WHITE,
                          font=customtkinter.CTkFont(size=12, weight="normal"))

    def refresh_op_btns():
        sel = current_sel.get()
        for name, btn in op_btns.items():
            active = (name == sel)
            btn.configure(fg_color=YELLOW if active else WHITE,
                          font=customtkinter.CTkFont(size=15 if active else 13,
                                                      weight="bold" if active else "normal"))
        for btn in algo_btns.values():
            btn.configure(fg_color=WHITE, border_width=1,
                          font=customtkinter.CTkFont(size=13, weight="normal"))

    def select_algo(name):
        current_sel.set(name)
        current_mode.set("algo")
        refresh_algo_btns()
        update_inputs(name)

    def select_op(name):
        current_sel.set(name)
        current_mode.set("op")
        refresh_op_btns()
        update_inputs(name)

    for algo in ["Gauss", "LU"]:
        b = customtkinter.CTkButton(sidebar, text=algo, width=158, height=38,
                                     fg_color=WHITE, text_color=DARK,
                                     hover_color=YELLOW_HVR, anchor="w",
                                     corner_radius=8, border_width=1,
                                     border_color=BORDER,
                                     font=customtkinter.CTkFont(size=13, weight="normal"),
                                     command=lambda n=algo: select_algo(n))
        b.pack(padx=14, pady=3)
        algo_btns[algo] = b

    customtkinter.CTkFrame(sidebar, height=1, fg_color=BORDER).pack(fill="x", padx=14, pady=(10, 8))

    customtkinter.CTkLabel(sidebar, text="Algorithmes indirects",
                            font=customtkinter.CTkFont(size=13, weight="bold"),
                            text_color=DARK).pack(anchor="w", padx=14, pady=(0, 6))

    for algo in ["Jacobi", "Gauss-Seidel", "Relaxation"]:
        b = customtkinter.CTkButton(sidebar, text=algo, width=158, height=38,
                                     fg_color=WHITE, text_color=DARK,
                                     hover_color=YELLOW_HVR, anchor="w",
                                     corner_radius=8, border_width=1,
                                     border_color=BORDER,
                                     font=customtkinter.CTkFont(size=13, weight="normal"),
                                     command=lambda n=algo: select_algo(n))
        b.pack(padx=14, pady=3)
        algo_btns[algo] = b

    customtkinter.CTkFrame(sidebar, height=1, fg_color=BORDER).pack(fill="x", padx=14, pady=(12, 10))

    customtkinter.CTkLabel(sidebar, text="Opérations sur\nles matrices",
                            font=customtkinter.CTkFont(size=13, weight="bold"),
                            text_color=DARK, justify="left").pack(anchor="w", padx=14, pady=(0, 6))

    for op in ["Normes matricielles", "Normes vectorielles", "Conditionnement",
               "Déterminant", "Transposée", "Inverse"]:
        b = customtkinter.CTkButton(sidebar, text=op, width=158, height=34,
                                     fg_color=WHITE, text_color=DARK,
                                     hover_color=YELLOW_HVR, anchor="w",
                                     corner_radius=8, border_width=1,
                                     border_color=BORDER,
                                     font=customtkinter.CTkFont(size=13),
                                     command=lambda n=op: select_op(n))
        b.pack(padx=14, pady=3)
        op_btns[op] = b

    # CONTENU
    content = customtkinter.CTkScrollableFrame(body, fg_color=WHITE,
                                                corner_radius=12, width=420)
    content.pack(side="left", fill="y", padx=(0, 8))

    top_row = customtkinter.CTkFrame(content, fg_color="transparent")
    top_row.pack(fill="x", padx=16, pady=(12, 4))

    lab_mat = customtkinter.CTkLabel(top_row, text="Matrice A",
                                      font=customtkinter.CTkFont(size=13, weight="bold"),
                                      text_color=DARK)
    lab_mat.pack(side="left")

    lab_b = customtkinter.CTkLabel(top_row, text="Vecteur b",
                                    font=customtkinter.CTkFont(size=13, weight="bold"),
                                    text_color=DARK)

    size = tk.IntVar(value=3)

    mat_scroll_outer = tk.Frame(content, bg=WHITE)
    mat_scroll_outer.pack(padx=16, pady=(0, 4), fill="x")

    mat_canvas = tk.Canvas(mat_scroll_outer, bg=WHITE, highlightthickness=0,
                            width=374, height=250)
    mat_scroll_y = tk.Scrollbar(mat_scroll_outer, orient="vertical",
                                  command=mat_canvas.yview)
    mat_scroll_x = tk.Scrollbar(mat_scroll_outer, orient="horizontal",
                                  command=mat_canvas.xview)
    mat_canvas.configure(yscrollcommand=mat_scroll_y.set,
                         xscrollcommand=mat_scroll_x.set)
    mat_scroll_x.pack(side="bottom", fill="x")
    mat_scroll_y.pack(side="right", fill="y")
    mat_canvas.pack(side="left", fill="both", expand=True)

    matrix_frame = tk.Frame(mat_canvas, bg=WHITE)
    mat_canvas_win_id = mat_canvas.create_window((0, 0), window=matrix_frame, anchor="nw")

    def on_mat_configure(event):
        mat_canvas.configure(scrollregion=mat_canvas.bbox("all"))

    matrix_frame.bind("<Configure>", on_mat_configure)

    mat_input = []
    vec_input = []

    def clear_grid():
        for widget in matrix_frame.winfo_children():
            widget.destroy()
        mat_input.clear()
        vec_input.clear()

    def draw_matrix(n):
        for i in range(n):
            row_entries = []
            for j in range(n):
                e = customtkinter.CTkEntry(matrix_frame, width=52, height=34,
                                           corner_radius=6, border_color=BORDER,
                                           border_width=1, fg_color=WHITE,
                                           text_color=DARK,
                                           font=customtkinter.CTkFont(size=12),
                                           justify="center")
                e.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(e)
            mat_input.append(row_entries)

    def draw_vector(n):
        if not lab_b.winfo_ismapped():
            lab_b.pack(side="right")
        for i in range(n):
            sep = tk.Label(matrix_frame, text="│", fg=BORDER, bg=WHITE,
                           font=("Arial", 18))
            sep.grid(row=i, column=n, padx=4)
            bv = customtkinter.CTkEntry(matrix_frame, width=52, height=34,
                                        corner_radius=6, border_color=BORDER,
                                        border_width=1, fg_color=WHITE,
                                        text_color=DARK,
                                        font=customtkinter.CTkFont(size=12),
                                        justify="center")
            bv.grid(row=i, column=n+1, padx=2, pady=2)
            vec_input.append(bv)

    #boutons Effacer / Aleatoire
    btns = customtkinter.CTkFrame(content, fg_color="transparent")
    btns.pack(padx=16, pady=(4, 6))

    def on_vide():
        for row in mat_input:
            for e in row:
                e.delete(0, "end")
        for e in vec_input:
            e.delete(0, "end")

    def on_aleatoire():
        import random
        n = size.get()
        # Genere une matrice a diagonale dominante 
        for i in range(n):
            total = 0
            for j in range(n):
                if i != j:
                    v = random.randint(-5, 5)
                    mat_input[i][j].delete(0, "end")
                    mat_input[i][j].insert(0, str(v))
                    total += abs(v)
            # diagonale > somme des autres
            diag = total + random.randint(1, 5)
            mat_input[i][i].delete(0, "end")
            mat_input[i][i].insert(0, str(diag))
            if i < len(vec_input):
                vec_input[i].delete(0, "end")
                vec_input[i].insert(0, str(random.randint(1, 20)))

    for txt, cmd in [("Effacer", on_vide), ("Aléatoire", on_aleatoire)]:
        customtkinter.CTkButton(btns, text=txt, width=100, height=30,
                                 fg_color=LIGHT_BG, text_color=DARK,
                                 hover_color=BORDER, border_width=1,
                                 border_color=BORDER, corner_radius=8,
                                 font=customtkinter.CTkFont(size=12),
                                 command=cmd).pack(side="left", padx=4)

    # taille n×n 
    size_row = customtkinter.CTkFrame(content, fg_color="transparent")
    size_row.pack(padx=16, pady=(0, 6))

    customtkinter.CTkLabel(size_row, text="Taille  n×n :",
                            font=customtkinter.CTkFont(size=12),
                            text_color=GREY).pack(side="left", padx=(0, 8))

    def on_size_change(val):
        size.set(int(val))
        clear_grid()
        n = int(val)
        mode = current_mode.get()
        sel  = current_sel.get()
        if mode == "algo":
            draw_matrix(n)
            draw_vector(n)
        elif sel == "Normes vectorielles":
            draw_vector(n)
        else:
            draw_matrix(n)
            lab_b.pack_forget()

    size_menu = customtkinter.CTkOptionMenu(
        size_row,
        values=["2", "3", "4", "5", "6", "7", "8"],
        width=70, height=30, corner_radius=6,
        fg_color=WHITE, text_color=DARK,
        button_color=YELLOW, button_hover_color=YELLOW_HVR,
        dropdown_fg_color=WHITE, dropdown_text_color=DARK,
        font=customtkinter.CTkFont(size=12),
        command=on_size_change)
    size_menu.set("3")
    size_menu.pack(side="left")

    customtkinter.CTkFrame(content, height=1, fg_color=BORDER).pack(fill="x", padx=16, pady=(6, 8))

    #section normes
    norm_section = customtkinter.CTkFrame(content, fg_color="transparent")

    customtkinter.CTkLabel(norm_section, text="Type de norme",
                            font=customtkinter.CTkFont(size=12, weight="bold"),
                            text_color=DARK).pack(anchor="w", pady=(0, 6))

    norm_type_var = tk.StringVar(value="‖·‖₁")
    norm_btns_row = customtkinter.CTkFrame(norm_section, fg_color="transparent")
    norm_btns_row.pack(anchor="w")
    norm_btn_refs = {}

    norm_p_frame = customtkinter.CTkFrame(norm_section, fg_color="transparent")
    customtkinter.CTkLabel(norm_p_frame, text="p =",
                            font=customtkinter.CTkFont(size=12),
                            text_color=GREY).pack(side="left", padx=(0, 6))
    entry_p = customtkinter.CTkEntry(norm_p_frame, width=60, height=30,
                                      corner_radius=6, border_color=BORDER,
                                      fg_color=WHITE, border_width=1,
                                      font=customtkinter.CTkFont(size=12))
    entry_p.insert(0, "3")
    entry_p.pack(side="left")

    def select_norm(nrm):
        norm_type_var.set(nrm)
        for n, btn in norm_btn_refs.items():
            btn.configure(fg_color=YELLOW if n == nrm else WHITE)
        if nrm == "‖·‖ₚ":
            norm_p_frame.pack(anchor="w", pady=(6, 0))
        else:
            norm_p_frame.pack_forget()

    for nrm in ["‖·‖₁", "‖·‖₂", "‖·‖∞", "‖·‖ₚ"]:
        nb = customtkinter.CTkButton(norm_btns_row, text=nrm, width=66, height=30,
                                      fg_color=YELLOW if nrm == "‖·‖₁" else WHITE,
                                      text_color=DARK, hover_color=YELLOW_HVR,
                                      corner_radius=8, border_width=1,
                                      border_color=BORDER,
                                      font=customtkinter.CTkFont(size=12),
                                      command=lambda n=nrm: select_norm(n))
        nb.pack(side="left", padx=(0, 3))
        norm_btn_refs[nrm] = nb

    #parametres iteratifs
    parametres = customtkinter.CTkFrame(content, fg_color="transparent")

    customtkinter.CTkLabel(parametres, text="Paramètres (Itératif)",
                            font=customtkinter.CTkFont(size=13, weight="bold"),
                            text_color=DARK).pack(anchor="w", padx=0, pady=(0, 8))

    tol_col = customtkinter.CTkFrame(parametres, fg_color="transparent")
    tol_col.pack(anchor="w", pady=(0, 8))
    customtkinter.CTkLabel(tol_col, text="Tolérance",
                            font=customtkinter.CTkFont(size=12),
                            text_color=GREY).pack(anchor="w")
    tol_input = customtkinter.CTkEntry(tol_col, width=160, height=34,
                                        corner_radius=6, border_color=BORDER,
                                        border_width=1, fg_color=WHITE,
                                        text_color=DARK,
                                        font=customtkinter.CTkFont(size=12),
                                        placeholder_text="0.00001")
    tol_input.pack(anchor="w")

    omega_col = customtkinter.CTkFrame(parametres, fg_color="transparent")
    customtkinter.CTkLabel(omega_col, text="Paramètre ω",
                            font=customtkinter.CTkFont(size=12),
                            text_color=GREY).pack(anchor="w")
    omega = customtkinter.CTkEntry(omega_col, width=160, height=34,
                                    corner_radius=6, border_color=BORDER,
                                    border_width=1, fg_color=WHITE,
                                    text_color=DARK,
                                    font=customtkinter.CTkFont(size=12),
                                    placeholder_text="1.25")
    omega.pack(anchor="w")

    # boutons Calculer / Voir iterations
    btns_calc_row = customtkinter.CTkFrame(content, fg_color="transparent")
    btns_calc_row.pack(side="bottom", pady=12, padx=16, fill="x")

    btn_iter = customtkinter.CTkButton(btns_calc_row, text="Voir itérations",
                                        width=160, height=40, fg_color=WHITE,
                                        text_color=DARK, hover_color=YELLOW_HVR,
                                        font=customtkinter.CTkFont(size=13, weight="bold"),
                                        corner_radius=10,
                                        border_color=YELLOW, border_width=1)
    btn_iter.pack(side="left")   # sera retiré dynamiquement si non itératif

    # RESULTATS
    result = customtkinter.CTkScrollableFrame(body, fg_color=WHITE, corner_radius=12)
    result.pack(side="right", fill="both", expand=True)

    customtkinter.CTkLabel(result, text="Résultats",
                            font=customtkinter.CTkFont(size=14, weight="bold"),
                            text_color=DARK).pack(anchor="w", padx=16, pady=(14, 10))

    # solution
    sol_title = customtkinter.CTkLabel(result, text="Solution x",
                                        font=customtkinter.CTkFont(size=11),
                                        text_color=GREY)
    sol_title.pack(anchor="w", padx=16)

    solution_frame = customtkinter.CTkFrame(result, fg_color=LIGHT_BG, corner_radius=8)
    solution_frame.pack(anchor="w", padx=16, pady=(4, 10))

    # itérations
    iter_frame = customtkinter.CTkFrame(result, fg_color="transparent")
    iter_frame.pack(anchor="w", padx=16, pady=(0, 10))
    customtkinter.CTkLabel(iter_frame, text="Nombre d'itérations",
                            font=customtkinter.CTkFont(size=11),
                            text_color=GREY).pack(anchor="w")
    lbl_iterations = customtkinter.CTkLabel(iter_frame, text="-",
                                             font=customtkinter.CTkFont(size=24, weight="bold"),
                                             text_color=DARK)
    lbl_iterations.pack(anchor="w")

    # résidu
    residu_frame = customtkinter.CTkFrame(result, fg_color="transparent")
    residu_frame.pack(anchor="w", padx=16, pady=(0, 10))
    customtkinter.CTkLabel(residu_frame, text="Norme du résidu",
                            font=customtkinter.CTkFont(size=11),
                            text_color=GREY).pack(anchor="w")
    lbl_residu = customtkinter.CTkLabel(residu_frame, text="-",
                                         font=customtkinter.CTkFont(size=18, weight="bold"),
                                         text_color=DARK)
    lbl_residu.pack(anchor="w")

    # convergence
    conv_frame = customtkinter.CTkFrame(result, fg_color="transparent")
    conv_frame.pack(anchor="w", padx=16, pady=(0, 8))
    customtkinter.CTkLabel(conv_frame, text="Convergence",
                            font=customtkinter.CTkFont(size=11),
                            text_color=GREY).pack(anchor="w")
    lbl_conv = customtkinter.CTkLabel(conv_frame, text="—",
                                       font=customtkinter.CTkFont(size=15, weight="bold"),
                                       text_color=GREY)
    lbl_conv.pack(anchor="w")

    def set_convergence(converged: bool):
        if converged:
            lbl_conv.configure(text="Convergé",  text_color=GREEN)
        else:
            lbl_conv.configure(text="Divergé",   text_color="#e53935")

    # matrice d'iteration
    iter_mat_section = customtkinter.CTkFrame(result, fg_color="transparent")
    customtkinter.CTkLabel(iter_mat_section, text="Matrice d'itération",
                            font=customtkinter.CTkFont(size=11),
                            text_color=GREY).pack(anchor="w")
    iter_mat_display = customtkinter.CTkFrame(iter_mat_section, fg_color=LIGHT_BG, corner_radius=8)
    iter_mat_display.pack(anchor="w", pady=(4, 0), fill="x")
    lbl_iter_mat = customtkinter.CTkLabel(iter_mat_display, text="—",
                                           font=customtkinter.CTkFont(size=12),
                                           text_color=DARK, justify="left")
    lbl_iter_mat.pack(anchor="w", padx=10, pady=8)

    # resultats operations
    op_result_section = customtkinter.CTkFrame(result, fg_color="transparent")
    customtkinter.CTkLabel(op_result_section, text="Résultat",
                            font=customtkinter.CTkFont(size=11),
                            text_color=GREY).pack(anchor="w")
    lbl_op_val = customtkinter.CTkLabel(op_result_section, text="—",
                                         font=customtkinter.CTkFont(size=18, weight="bold"),
                                         text_color=GREEN, justify="left",
                                         wraplength=280)
    lbl_op_val.pack(anchor="w", pady=(2, 0))

    # recommandation
    RECO = {
        "Gauss"              : "Gauss est stable pour la plupart\ndes systèmes bien conditionnés.",
        "LU"                 : "LU est recommandé pour résoudre\nplusieurs systèmes avec la même matrice A.",
        "Jacobi"             : "Entrez votre matrice et cliquez\n▶ Calculer pour obtenir une\nrecommandation dynamique.",
        "Gauss-Seidel"       : "Entrez votre matrice et cliquez\n▶ Calculer pour obtenir une\nrecommandation dynamique.",
        "Relaxation"         : "Relaxation accélère la convergence\navec un bon choix de ω (entre 1 et 2).\nEntrez la matrice pour une analyse.",
        "Normes matricielles": "‖A‖₁ = max colonne, ‖A‖∞ = max ligne,\n‖A‖₂ = plus grande valeur singulière.",
        "Normes vectorielles": "‖x‖₂ (euclidienne) est la plus utilisée.\n‖x‖₁ = somme des valeurs absolues.",
        "Conditionnement"    : "κ(A) grand → système mal conditionné,\nsensible aux erreurs d'arrondi.",
        "Déterminant"        : "Si det(A) = 0, le système n'a pas\nde solution unique.",
        "Transposée"         : "Aᵀ permet de vérifier la symétrie de A.",
        "Inverse"            : "A⁻¹ existe seulement si det(A) ≠ 0.",
    }


    def update_tip_indirect(A):
        """Met à jour la recommandation dynamiquement pour Jacobi / Gauss-Seidel / Relaxation."""
        try:
            algo_rec, explication = recommander_algo_indirect(A)
            sel = current_sel.get()
            if sel in ("Jacobi", "Gauss-Seidel"):
                if sel == algo_rec:
                    prefix = "✅ Vous utilisez le bon algorithme.\n"
                else:
                    prefix = f"💡 Recommandé : {algo_rec}\n"
                lbl_tip.configure(text=prefix + explication)
            elif sel == "Relaxation":
                lbl_tip.configure(
                    text=f"Relaxation est basée sur GS.\n"
                         f"Algo itératif conseillé : {algo_rec}\n"
                         + explication
                )
        except Exception:
            pass  # matrice incomplete ou invalide on garde le texte statique

    box = customtkinter.CTkFrame(result, fg_color=TIP_BG, corner_radius=10,
                                  border_width=1, border_color=TIP_BORDER)
    box.pack(side="bottom", fill="x", padx=16, pady=(4, 12))
    customtkinter.CTkLabel(box, text="💡  Recommandation",
                            font=customtkinter.CTkFont(size=12, weight="bold"),
                            text_color="#7a6500").pack(anchor="w", padx=10, pady=(8, 2))
    lbl_tip = customtkinter.CTkLabel(box, text=RECO["Gauss"],
                                      font=customtkinter.CTkFont(size=11),
                                      text_color="#7a6500", justify="left",
                                      wraplength=280)
    lbl_tip.pack(anchor="w", padx=10, pady=(0, 8))

    # CONSTANTES
    ITER_ALGOS = {"Jacobi", "Gauss-Seidel", "Relaxation"}
    NORM_OPS   = {"Normes matricielles", "Normes vectorielles"}
    OPS_NO_B   = {"Normes matricielles", "Conditionnement", "Déterminant",
                  "Transposée", "Inverse"}

    # FONCTIONS UTILITAIRES
    def _parse_matrix():
        n = size.get()
        A = []
        for i in range(n):
            row = []
            for j in range(n):
                val = mat_input[i][j].get().strip()
                if val == "":
                    raise ValueError(f"Case A[{i+1}][{j+1}] vide.")
                row.append(float(val))
            A.append(row)
        return A

    def _parse_vector():
        n = size.get()
        b = []
        for i in range(n):
            val = vec_input[i].get().strip()
            if val == "":
                raise ValueError(f"Case b[{i+1}] vide.")
            b.append(float(val))
        return b

    def _get_tol():
        t = tol_input.get().strip()
        return float(t) if t else 1e-5

    def _get_omega():
        w = omega.get().strip()
        return float(w) if w else 1.25

    def _get_p():
        p = entry_p.get().strip()
        return int(p) if p else 3

    #affichage
    def show_solution(x):
        for w in solution_frame.winfo_children():
            w.destroy()
        for i, xi in enumerate(x):
            customtkinter.CTkLabel(solution_frame,
                                    text=f"x{i+1} = {xi:.8f}",
                                    font=customtkinter.CTkFont(size=14, weight="bold"),
                                    text_color=GREEN).pack(anchor="w", padx=10, pady=1)

    #logique principale
    def on_calculer():
        global last_errors, last_solutions, last_M, last_iters

        sel  = current_sel.get()
        mode = current_mode.get()

        if not sel:
            messagebox.showwarning("Aucune sélection",
                                   "Veuillez choisir un algorithme ou une opération.")
            return

        try:
            #MODE ALGORITHME
            if mode == "algo":
                A = _parse_matrix()
                b = _parse_vector()

                if sel == "Gauss":
                    x, _, _, _ = gauss(A, b)
                    show_solution(x)
                    clear_vis()

                elif sel == "LU":
                    x, _, _, _ = lu(A, b)
                    show_solution(x)
                    clear_vis()

                elif sel == "Jacobi":
                    tol = _get_tol()
                    x, M, errors, solutions, result_val = jacobi(A, b, tol=tol)
                    if isinstance(result_val, tuple) and result_val[0] == "SINGULAR_MATRIX":
                        messagebox.showerror("Matrice singulière — erreur", result_val[1])
                        return
                    n_iter = result_val
                    last_errors = errors; last_solutions = solutions
                    last_M = M; last_iters = n_iter
                    show_solution(x)
                    lbl_iterations.configure(text=str(n_iter))
                    lbl_residu.configure(text=f"{errors[-1]:.2e}" if errors else "—")
                    set_convergence(errors[-1] < tol if errors else False)
                    if M is not None:
                        lbl_iter_mat.configure(text=np.array2string(M, precision=4))
                    draw_convergence(errors, "Jacobi")
                    update_tip_indirect(A)

                elif sel == "Gauss-Seidel":
                    tol = _get_tol()
                    x, M, errors, solutions, result_val = gauss_seidel(A, b, tol=tol)
                    if isinstance(result_val, tuple) and result_val[0] == "SINGULAR_MATRIX":
                        messagebox.showerror("Matrice singulière — erreur", result_val[1])
                        return
                    n_iter = result_val
                    last_errors = errors; last_solutions = solutions
                    last_M = M; last_iters = n_iter
                    show_solution(x)
                    lbl_iterations.configure(text=str(n_iter))
                    lbl_residu.configure(text=f"{errors[-1]:.2e}" if errors else "—")
                    set_convergence(errors[-1] < tol if errors else False)
                    if M is not None:
                        lbl_iter_mat.configure(text=np.array2string(M, precision=4))
                    draw_convergence(errors, "Gauss-Seidel")
                    update_tip_indirect(A)

                elif sel == "Relaxation":
                    tol = _get_tol()
                    om  = _get_omega()
                    x, _, errors, solutions, result_val = relaxation(A, b, omega=om, tol=tol)
                    if isinstance(result_val, tuple) and result_val[0] == "SINGULAR_MATRIX":
                        messagebox.showerror("Matrice singulière — erreur", result_val[1])
                        return
                    n_iter = result_val
                    last_errors = errors; last_solutions = solutions
                    last_M = None; last_iters = n_iter
                    show_solution(x)
                    lbl_iterations.configure(text=str(n_iter))
                    lbl_residu.configure(text=f"{errors[-1]:.2e}" if errors else "—")
                    set_convergence(errors[-1] < tol if errors else False)
                    lbl_iter_mat.configure(text="—")
                    draw_convergence(errors, f"Relaxation (ω={om})")
                    update_tip_indirect(A)

            # MODE OPERATION 
            else:
                if sel == "Normes vectorielles":
                    x   = _parse_vector()
                    nrm = norm_type_var.get()
                    if nrm == "‖·‖ₚ":
                        res = normes_vectorielles(x, p=_get_p()).split("\n")[-1]
                    elif nrm == "‖·‖₁":
                        res = normes_vectorielles(x).split("\n")[0]
                    elif nrm == "‖·‖₂":
                        res = normes_vectorielles(x).split("\n")[1]
                    elif nrm == "‖·‖∞":
                        res = normes_vectorielles(x).split("\n")[2]
                    else:
                        res = "Norme inconnue"
                    lbl_op_val.configure(text=res)

                elif sel == "Normes matricielles":
                    A   = _parse_matrix()
                    nrm = norm_type_var.get()
                    if nrm == "‖·‖ₚ":
                        res = "La norme ‖·‖ₚ n'est définie\nque pour les vecteurs."
                    elif nrm == "‖·‖₁":
                        res = normes_matricielles(A).split("\n")[0]
                    elif nrm == "‖·‖₂":
                        res = normes_matricielles(A).split("\n")[1]
                    elif nrm == "‖·‖∞":
                        res = normes_matricielles(A).split("\n")[2]
                    else:
                        res = "Norme inconnue"
                    lbl_op_val.configure(text=res)

                elif sel == "Conditionnement":
                    A = _parse_matrix()
                    lbl_op_val.configure(text=conditionnement(A))

                elif sel == "Déterminant":
                    A = _parse_matrix()
                    lbl_op_val.configure(text=determinant(A))

                elif sel == "Transposée":
                    A = _parse_matrix()
                    lbl_op_val.configure(text=transposee(A))

                elif sel == "Inverse":
                    A = _parse_matrix()
                    lbl_op_val.configure(text=inverse(A))

        except ValueError as ve:
            messagebox.showerror("Entrée invalide", str(ve))
        except np.linalg.LinAlgError as e:
            messagebox.showerror("Erreur algèbre linéaire", str(e))
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # VOIR ITERATIONS
    def on_voir_iterations():
        if not last_solutions:
            messagebox.showinfo("Aucune donnée",
                                "Lancez d'abord un calcul itératif.")
            return

        win2 = tk.Toplevel(app)
        win2.title("Détail des itérations")
        win2.geometry("700x500")
        win2.configure(bg=WHITE)

        customtkinter.CTkLabel(win2,
                                text=f"Itérations — {current_sel.get()}",
                                font=customtkinter.CTkFont(size=14, weight="bold"),
                                text_color=DARK).pack(pady=(12, 6))

        cols = ["Iter"] + [f"x{i+1}" for i in range(len(last_solutions[0]))] + ["Résidu"]
        tree_frame = tk.Frame(win2, bg=WHITE)
        tree_frame.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        import tkinter.ttk as ttk
        style = ttk.Style()
        style.configure("Treeview", rowheight=22, font=("Helvetica", 10))
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

        tv = ttk.Treeview(tree_frame, columns=cols, show="headings")
        for c in cols:
            tv.heading(c, text=c)
            tv.column(c, width=90, anchor="center")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        tv.pack(fill="both", expand=True)

        for k, (sol, err) in enumerate(zip(last_solutions, last_errors)):
            row = [k+1] + [f"{v:.6f}" for v in sol] + [f"{err:.2e}"]
            tv.insert("", "end", values=row)

    # M A J DE L INTERFACE SELON LA SELECTION
    def update_inputs(name):
        parametres.pack_forget()
        omega_col.pack_forget()
        norm_section.pack_forget()
        norm_p_frame.pack_forget()
        clear_vis()

        mode = current_mode.get()
        n    = size.get()
        clear_grid()

        if mode == "algo":
            draw_matrix(n)
            draw_vector(n)
        elif name == "Normes vectorielles":
            draw_vector(n)
        else:
            draw_matrix(n)
            lab_b.pack_forget()

        if mode == "algo" and name in ITER_ALGOS:
            parametres.pack(padx=16, pady=(0, 8), anchor="w")
            if name == "Relaxation":
                omega_col.pack(anchor="w", pady=(0, 8))
            btn_iter.pack(side="left")
        else:
            btn_iter.pack_forget()

        if name in NORM_OPS:
            norm_section.pack(padx=16, pady=(0, 8), anchor="w")

        update_results_display(name)

        # Pour les algos indirects, tenter une analyse dynamique si la matrice est deja remplie
        if name in ITER_ALGOS:
            try:
                A = _parse_matrix()
                update_tip_indirect(A)
            except Exception:
                # Matrice vide ou incomplete : message d'invite
                lbl_tip.configure(text=RECO.get(name, "Sélectionnez un algorithme."))
        else:
            lbl_tip.configure(text=RECO.get(name, "Sélectionnez un algorithme."))


    def update_results_display(name):
        sol_title.pack_forget()
        solution_frame.pack_forget()
        iter_frame.pack_forget()
        residu_frame.pack_forget()
        conv_frame.pack_forget()
        iter_mat_section.pack_forget()
        op_result_section.pack_forget()

        mode = current_mode.get()
        if mode == "algo":
            sol_title.pack(anchor="w", padx=16)
            solution_frame.pack(anchor="w", padx=16, pady=(4, 10))
            if name in ITER_ALGOS:
                iter_frame.pack(anchor="w", padx=16, pady=(0, 10))
                residu_frame.pack(anchor="w", padx=16, pady=(0, 10))
                conv_frame.pack(anchor="w", padx=16, pady=(0, 8))
                iter_mat_section.pack(anchor="w", padx=16, pady=(0, 8), fill="x")
        else:
            op_result_section.pack(anchor="w", padx=16, pady=(0, 10))


    # branchement boutons principaux 
    btn_calc = customtkinter.CTkButton(btns_calc_row,
                                        text="▶   Calculer",
                                        width=170, height=40,
                                        fg_color=YELLOW, text_color=WHITE,
                                        hover_color=YELLOW_HVR,
                                        font=customtkinter.CTkFont(size=14, weight="bold"),
                                        corner_radius=10,
                                        command=on_calculer)
    btn_calc.pack(side="left", padx=(0, 8))

    btn_iter.configure(command=on_voir_iterations)

    # initialisation : selectionne Gauss par defaut 
    select_algo("Gauss")

