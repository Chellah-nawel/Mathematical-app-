import customtkinter
import tkinter as tk
from tkinter import messagebox, filedialog
from appropoint import lancer_mc_depuis_interface
from approdirect import lancer_mc_continu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from algo_descente_gradient import gradient_descent
from sympy import symbols, sympify
from lagrange import *
from algorithmes_axe3 import newton, calcule_poly
import numpy as np


def show(app, navigate):

    YELLOW     = "#f5c518"
    YELLOW_HVR = "#e6b800"
    LIGHT_BG   = "#f4f6f9"
    WHITE      = "#ffffff"
    DARK       = "#0d1b2e"
    GREY       = "#777777"
    GREEN      = "#22a361"
    BORDER     = "#e0e0e0"
    RED_LIGHT  = "#fff0f0"
    RED_BORDER = "#ffcccc"
    BTN_DEL    = "#e53935"

    def format_matrix(M):
        rows = []

        for i, row in enumerate(M):
            formatted = "   ".join(f"{v:8.3f}" for v in row)

            if i == 0:
                rows.append("[[ " + formatted + " ]")
            elif i == len(M) - 1:
                rows.append(" [ " + formatted + " ]]")
            else:
                rows.append(" [ " + formatted + " ]")

        return "\n".join(rows)

    header_bar = customtkinter.CTkFrame(app, bg_color=WHITE, 
                                        fg_color=WHITE, 
                                        corner_radius=0, 
                                        height=54)
    header_bar.pack(fill="x")
    header_bar.pack_propagate(False)

    retour = customtkinter.CTkButton(header_bar, 
                                    text="←", 
                                    width=38, 
                                    height=38,
                                    fg_color="transparent", 
                                    text_color=DARK, 
                                    hover_color="#f0f0f0",
                                    font=customtkinter.CTkFont(size=20), 
                                    corner_radius=8
    )
    retour.configure(command=lambda: navigate("accueil"))
    retour.pack(side="left", padx=(12, 6), pady=8)

    title=customtkinter.CTkLabel(header_bar, 
                        text="Axe 3 : Interpolation & Approximation",
                        font=customtkinter.CTkFont(size=17, weight="bold"), 
                        text_color=DARK
    ) 
    title.pack(side="left")

    # visualisation en bas
    vis_outer = customtkinter.CTkFrame(app, bg_color=WHITE,
                                    fg_color=WHITE, 
                                    corner_radius=12)
    vis_outer.pack(side="bottom", fill="x", padx=14, pady=(0, 14))

    graph_frame = customtkinter.CTkFrame(vis_outer, fg_color="white")
    graph_frame.pack(fill="both", expand=True, padx=10, pady=10)

    vis_header = customtkinter.CTkFrame(vis_outer, 
                                        fg_color="transparent")
    vis_header.pack(fill="x", padx=14, pady=(10, 0))

    customtkinter.CTkLabel(vis_header, 
                        text="Visualisation",
                        font=customtkinter.CTkFont(size=13, weight="bold"),
                        text_color=DARK).pack(side="left")

    def on_export():
        if not hasattr(graph_frame, "figure"):
            messagebox.showerror("Erreur", "Aucun graphe à exporter")
            return

        fig = graph_frame.figure

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG image", "*.png"), ("PDF file", "*.pdf")]
        )

        if file_path:
            fig.savefig(file_path, dpi=300, bbox_inches="tight")
            messagebox.showinfo("Succès", "Graphe exporté avec succès")

    btn_export = customtkinter.CTkButton(vis_header, 
                                        text="⬇  Exporter résultats",
                                        width=160, 
                                        height=30,
                                        fg_color=LIGHT_BG, 
                                        text_color=DARK, 
                                        hover_color=BORDER,
                                        border_width=1, 
                                        border_color=BORDER, 
                                        corner_radius=8,
                                        font=customtkinter.CTkFont(size=11),
                                        command=on_export
    )
    btn_export.pack(side="right")

    body = customtkinter.CTkFrame(app, bg_color=WHITE,
                                fg_color="transparent")
    body.pack(fill="both", expand=True, padx=14, pady=(10, 8))

    # sidebar avec scrollbar
    sidebar = customtkinter.CTkScrollableFrame(body, bg_color=WHITE,
                                            fg_color=WHITE, 
                                            corner_radius=12, 
                                            width=186)
    sidebar.pack(side="left", fill="y", padx=(0, 8))

    algo_btns    = {}
    op_btns      = {}
    current_sel  = tk.StringVar()
    current_mode = tk.StringVar(value="interp")

    def refresh_algo_btns():
        sel = current_sel.get()
        for name, btn in algo_btns.items():
            active= (name == sel)
            if active:
                btn.configure(fg_color=YELLOW,
                            border_width=0,
                            font=customtkinter.CTkFont(size=15, weight="bold")
                )
            else:
                btn.configure(fg_color=WHITE,
                            font=customtkinter.CTkFont(size=13, weight="normal")
                )
        for btn in op_btns.values():
            btn.configure(fg_color=WHITE,
                        font=customtkinter.CTkFont(size=12, weight="normal"))

    def refresh_op_btns():
        sel = current_sel.get()
        for name, btn in op_btns.items():
            active= (name == sel)
            if active:
                btn.configure(fg_color=YELLOW,
                            font=customtkinter.CTkFont(size=15, weight="bold")
                )
            else:
                btn.configure(fg_color=WHITE,
                            font=customtkinter.CTkFont(size=13, weight="normal")
                )

        for btn in algo_btns.values():
            btn.configure(fg_color=WHITE, 
                        border_width=1,
                        font=customtkinter.CTkFont(size=13, weight="normal")
            )   

    def select_algo(name):
        current_sel.set(name) 
        current_mode.set("algo")
        refresh_algo_btns()
        update_params(name)

    def select_op(name):
        current_sel.set(name)
        current_mode.set("op")
        refresh_op_btns()
        update_params(name)

    # interpolation polynomiale
    title_inter= customtkinter.CTkLabel(sidebar, 
                                        text="Interpolation\npolynomiale",
                                        font=customtkinter.CTkFont(size=13, weight="bold"), 
                                        text_color=DARK, 
                                        justify="left"
    )
    title_inter.pack(anchor="w", padx=14, pady=(14, 6))

    for algo in ["Lagrange", "Newton"]:
        b = customtkinter.CTkButton(sidebar, 
                                    text=algo, 
                                    width=158, 
                                    height=38,
                                    fg_color=WHITE, 
                                    text_color=DARK, 
                                    hover_color=YELLOW_HVR,
                                    anchor="w",     
                                    corner_radius=8, 
                                    border_width=1, 
                                    border_color=BORDER,
                                    font=customtkinter.CTkFont(size=13, weight="normal"),
                                    command=lambda n=algo: select_algo(n)
        )
        b.pack(padx=14, pady=3)
        algo_btns[algo] = b

    content= customtkinter.CTkFrame(sidebar, 
                                    height=1, 
                                    fg_color=BORDER)
    content.pack(fill="x", padx=14, pady=(10, 8))

    # approximation
    titre_app= customtkinter.CTkLabel(sidebar,
                                    text="Approximation",
                                    font=customtkinter.CTkFont(size=13, weight="bold"), 
                                    text_color=DARK
    )
    titre_app.pack(anchor="w", padx=14, pady=(0, 6))

    for op in ["Moindres carrés", "Descente de gradient"]:
        b = customtkinter.CTkButton(sidebar, 
                                    text=op, 
                                    width=158, 
                                    height=34,
                                    fg_color=WHITE, 
                                    text_color=DARK, 
                                    hover_color=YELLOW_HVR,
                                    anchor="w", 
                                    corner_radius=8, 
                                    border_width=1, 
                                    border_color=BORDER,
                                    font=customtkinter.CTkFont(size=13),
                                    command=lambda n=op: select_op(n)
        )
        b.pack(padx=14, pady=3)
        op_btns[op] = b

    # les points
    pnt_fram = customtkinter.CTkScrollableFrame(body, bg_color=WHITE,
                                                fg_color=WHITE, 
                                                corner_radius=12, 
                                                width=340)
    pnt_fram.pack(side="left", fill="y", padx=(0, 8))

    titre_pnt= customtkinter.CTkLabel(pnt_fram, 
                                    text="Points (x, y)",
                                    font=customtkinter.CTkFont(size=13, weight="bold"), 
                                    text_color=DARK
    )
    titre_pnt.pack(anchor="w", padx=16, pady=(14, 6))

    # entete du tableau
    hdr = customtkinter.CTkFrame(pnt_fram, 
                                fg_color=LIGHT_BG, 
                                corner_radius=6)
    hdr.pack(fill="x", padx=16, pady=(0, 4))

    for col_txt, w in [("i", 44), ("x", 110), ("y", 110), ("", 36)]:
        txt_hdr=customtkinter.CTkLabel(hdr, 
                                    text=col_txt, 
                                    width=w,
                                        font=customtkinter.CTkFont(size=12, weight="bold"), 
                                        text_color=GREY
        )
        txt_hdr.pack(side="left", padx=2, pady=4)

    # zone des lignes
    points_inner = customtkinter.CTkFrame(pnt_fram, 
                                        fg_color="transparent")
    points_inner.pack(fill="x", padx=16)

    point_rows   = []  
    point_count  = tk.IntVar(value=0)

    #btn ajouter point
    def add_point(x_val="", y_val=""):
        n = len(point_rows) + 1
        #new line frame
        newl = customtkinter.CTkFrame(points_inner, 
                                        fg_color="transparent")
        newl.pack(fill="x", pady=2)

        idx_lbl = customtkinter.CTkLabel(newl, 
                                        text=str(n), 
                                        width=44,
                                        font=customtkinter.CTkFont(size=12), 
                                        text_color=GREY
        )
        idx_lbl.pack(side="left", padx=2)

        x_e = customtkinter.CTkEntry(newl, 
                                    width=100, 
                                    height=32, 
                                    corner_radius=6,
                                    border_color=BORDER, 
                                    border_width=1, 
                                    fg_color=WHITE, 
                                    text_color=DARK,
                                    font=customtkinter.CTkFont(size=12), 
                                    justify="center"
        )
        x_e.pack(side="left", padx=4)

        if x_val != "":
            x_e.insert(0, str(x_val))

        y_e = customtkinter.CTkEntry(newl, 
                                    width=100, 
                                    height=32, 
                                    corner_radius=6,
                                    border_color=BORDER, 
                                    border_width=1, 
                                    fg_color=WHITE, 
                                    text_color=DARK,
                                    font=customtkinter.CTkFont(size=12), 
                                    justify="center"
        )
        y_e.pack(side="left", padx=4)
        #c'est pas la peine d'ajouet une cell vide
        if y_val != "":
            y_e.insert(0, str(y_val))

        def delete_this():
            newl.destroy()
            point_rows[:] = [r for r in point_rows if r["frame"].winfo_exists()]
            renumber_points()
            update_degree_display()

        #btn delete
        del_btn = customtkinter.CTkButton(newl, 
                                        text="✕", 
                                        width=30, 
                                        height=30,
                                        fg_color=RED_LIGHT, 
                                        text_color=BTN_DEL, 
                                        hover_color=RED_BORDER,
                                        corner_radius=6, 
                                        font=customtkinter.CTkFont(size=12),
                                        command=delete_this
        )
        del_btn.pack(side="left", padx=2)

        point_rows.append({"frame": newl, "idx": idx_lbl, "x": x_e, "y": y_e})
        point_count.set(len(point_rows))
        update_degree_display()

    #garder l'ordre
    def renumber_points():
        for i, row in enumerate(point_rows):
            if row["frame"].winfo_exists():
                row["idx"].configure(text=str(i + 1))
        point_count.set(len(point_rows))

    #zone des btns 
    btns_action = customtkinter.CTkFrame(pnt_fram, 
                                        fg_color="transparent")
    btns_action.pack(padx=16, pady=(8, 12))

    #fct de supprime
    def on_supprimer():
        if point_rows:
            last = point_rows[-1]
            if last["frame"].winfo_exists():
                last["frame"].destroy()
            point_rows.pop()
            renumber_points()
            update_degree_display()

    btn_add = customtkinter.CTkButton(btns_action, 
                                    text="+ Ajouter un point", 
                                    width=140, 
                                    height=34,
                                    fg_color=YELLOW,   
                                    text_color=WHITE, 
                                    hover_color=YELLOW_HVR,
                                    corner_radius=8,
                                    font=customtkinter.CTkFont(size=12, weight="bold"),
                                    command=add_point
    )
    btn_add.pack(side="left", padx=(0, 8))

    btn_del = customtkinter.CTkButton(btns_action, 
                                    text="✕ Supprimer", 
                                    width=110, 
                                    height=34,
                                    fg_color=RED_LIGHT, 
                                    text_color=BTN_DEL, 
                                    hover_color=RED_BORDER,
                                    corner_radius=8, 
                                    font=customtkinter.CTkFont(size=12),
                                    command=on_supprimer
    )
    btn_del.pack(side="left")

    # parametres et resultats
    right_col = customtkinter.CTkScrollableFrame(body, bg_color=WHITE,
                                                fg_color=WHITE, 
                                                corner_radius=12)
    right_col.pack(side="left", fill="both", expand=True)

    # param
    param_title= customtkinter.CTkLabel(right_col, 
                        text="Paramètres",
                        font=customtkinter.CTkFont(size=14, weight="bold"), 
                        text_color=DARK
    )
    param_title.pack(anchor="w", padx=16, pady=(14, 8))

    #degre
    deg_display_frame = customtkinter.CTkFrame(right_col, 
                                            fg_color="transparent")
    deg_display_frame.pack(anchor="w", padx=16, pady=(0, 8))

    lab_deg= customtkinter.CTkLabel(deg_display_frame, 
                        text="Degré du polynôme",
                        font=customtkinter.CTkFont(size=12), 
                        text_color=DARK)
    lab_deg.pack(anchor="w")

    deg_display_inner = customtkinter.CTkFrame(deg_display_frame, 
                                            fg_color=LIGHT_BG, 
                                            corner_radius=6,
                                            border_width=1, 
                                            border_color=BORDER)
    deg_display_inner.pack(anchor="w", pady=(4, 0))

    lbl_deg_val = customtkinter.CTkLabel(deg_display_inner, 
                                        text="n − 1  =  —",
                                        font=customtkinter.CTkFont(size=13, weight="bold"), 
                                        text_color=GREEN)
    lbl_deg_val.pack(padx=14, pady=6)

    def update_degree_display():
        n = len([r for r in point_rows if r["frame"].winfo_exists()])
        if n >= 1:
            lbl_deg_val.configure(text=f"n − 1  =  {n - 1}")
        else:
            lbl_deg_val.configure(text="n − 1  =  —")

    # show point
    affiche_point = tk.BooleanVar(value=True)

    switch_row = customtkinter.CTkFrame(right_col, 
                                        fg_color="transparent")
    switch_row.pack(anchor="w", padx=16, pady=(0, 12))

    aff_pnt_lab= customtkinter.CTkLabel(switch_row, 
                        text="Afficher les points",
                        font=customtkinter.CTkFont(size=12), 
                        text_color=DARK)
    aff_pnt_lab.pack(side="left", padx=(0, 10))

    switch_pts = customtkinter.CTkSwitch(switch_row, 
                                        text="", 
                                        variable=affiche_point,  
                                        width=46, 
                                        height=24,
                                        fg_color=BORDER, 
                                        progress_color=YELLOW,
                                        button_color=GREY, 
                                        button_hover_color=BORDER
    )
    switch_pts.pack(side="left")

    #moindre carrees
    mc_frame = customtkinter.CTkFrame(right_col, 
                                      width=450,
                                    fg_color="transparent")

    #discret continue
    mc_mode = tk.StringVar(value="discret")

    mc_mode_row = customtkinter.CTkFrame(mc_frame, 
                                        fg_color="transparent")
    mc_mode_row.pack(anchor="w", pady=(0, 8))

    lab_cas= customtkinter.CTkLabel(mc_mode_row, 
                        text="Cas :",
                        font=customtkinter.CTkFont(size=12), 
                        text_color=DARK)
    lab_cas.pack(side="left", padx=(0, 10))

    radio_discret = customtkinter.CTkRadioButton(mc_mode_row, 
                                                text="Discret (nuage de points)",
                                                variable=mc_mode, 
                                                value="discret",
                                                fg_color=YELLOW, 
                                                hover_color=YELLOW_HVR,
                                                text_color=DARK,
                                                font=customtkinter.CTkFont(size=12),
                                                command=lambda: mode_MC())
    radio_discret.pack(side="left", padx=(0, 12))

    radio_continu = customtkinter.CTkRadioButton(mc_mode_row, 
                                                text="Continu (fonction)",
                                                variable=mc_mode, 
                                                value="continu",
                                                fg_color=YELLOW, 
                                                hover_color=YELLOW_HVR,
                                                text_color=DARK,
                                                font=customtkinter.CTkFont(size=12),
                                                command=lambda: mode_MC())
    radio_continu.pack(side="left")

    # champ fonction (cas continu)
    mc_func_frame = customtkinter.CTkFrame(body, bg_color=WHITE,
                                            fg_color=WHITE, 
                                        corner_radius=12, 
                                        width=186)

    titre_function= customtkinter.CTkLabel(mc_func_frame, 
                        text="Inputs",
                        font=customtkinter.CTkFont(size=15, weight="bold"), 
                        text_color=DARK)
    titre_function.pack(anchor="w")

    func_lab= customtkinter.CTkLabel(mc_func_frame, 
                        text="Définir f(x)",
                        font=customtkinter.CTkFont(size=12), 
                        text_color=DARK)
    func_lab.pack(anchor="w")

    mc_func_input = customtkinter.CTkEntry(mc_func_frame, 
                                        width=263, 
                                        height=36, 
                                        corner_radius=6,
                                        border_color=BORDER, 
                                        border_width=1, 
                                        fg_color=WHITE, 
                                        text_color=DARK,
                                        font=customtkinter.CTkFont(size=12), 
                                        placeholder_text="ex: sin(x)")
    mc_func_input.pack(anchor="w", pady=(0, 0))

    # intervalle
    mc_interval_frame = customtkinter.CTkFrame(mc_func_frame, 
                                            fg_color="transparent")
    mc_interval_frame.pack(anchor="w", pady=(0, 0))

    lab_interval= customtkinter.CTkLabel(mc_interval_frame, 
                        text="Intervalle [a, b]",
                        font=customtkinter.CTkFont(size=12), 
                        text_color=DARK)
    lab_interval.pack(anchor="w", pady=(0, 4))

    mc_ab_row = customtkinter.CTkFrame(mc_interval_frame, 
                                    fg_color="transparent")
    mc_ab_row.pack(anchor="w")

    mc_a_input = customtkinter.CTkEntry(mc_ab_row, 
                                        width=120, 
                                        height=34, 
                                        corner_radius=6,
                                        border_color=BORDER, 
                                        border_width=1, 
                                        fg_color=WHITE, 
                                        text_color=DARK,
                                        font=customtkinter.CTkFont(size=12), 
                                        placeholder_text="a")
    mc_a_input.pack(side="left", padx=(0, 8))

    mc_b_input = customtkinter.CTkEntry(mc_ab_row, 
                                        width=120, 
                                        height=34, 
                                        corner_radius=6,
                                        border_color=BORDER, 
                                        border_width=1, 
                                        fg_color=WHITE, 
                                        text_color=DARK,
                                        font=customtkinter.CTkFont(size=12), 
                                        placeholder_text="b")
    mc_b_input.pack(side="left")

    #degree
    lab_degree= customtkinter.CTkLabel(mc_frame, 
                        text="Degré du polynôme",
                        font=customtkinter.CTkFont(size=12), 
                        text_color=DARK)
    lab_degree.pack(anchor="w", pady=(8, 0))

    mc_deg_input = customtkinter.CTkEntry(mc_frame, 
                                        width=120, 
                                        height=34, 
                                        corner_radius=6,
                                        border_color=BORDER, 
                                        border_width=1, 
                                        fg_color=WHITE, 
                                        text_color=DARK,
                                        font=customtkinter.CTkFont(size=12), 
                                        placeholder_text="ex: 3")
    mc_deg_input.pack(anchor="w", pady=(4, 0))

    sep_mc = customtkinter.CTkFrame(mc_frame, 
                                    height=1, 
                                    fg_color=BORDER)
    sep_mc.pack(fill="x", pady=(12, 8))

    # resultat mc
    frame_resultat_mc= customtkinter.CTkFrame(mc_frame,
                                              width=400,
                                            fg_color="transparent")
    frame_resultat_mc.pack(anchor="w")

    result_lab= customtkinter.CTkLabel(frame_resultat_mc, 
                        text="Résultats",
                        font=customtkinter.CTkFont(size=14, weight="bold"), 
                        text_color=DARK)
    result_lab.pack(anchor="w", pady=(0, 6))

    poly_lab= customtkinter.CTkLabel(frame_resultat_mc, 
                        text="Polynôme trouvé",
                        font=customtkinter.CTkFont(size=11), 
                        text_color=GREY)
    poly_lab.pack(anchor="w")

    lbl_poly = customtkinter.CTkLabel(frame_resultat_mc, 
                                    text="P(x) = —",
                                    font=customtkinter.CTkFont(size=13, weight="bold"), 
                                    text_color=DARK,
                                    wraplength=260, 
                                    justify="left")
    lbl_poly.pack(anchor="w", pady=(4, 10))

    #fonction de cout
    cout_lab= customtkinter.CTkLabel(frame_resultat_mc, 
                        text="Fonction de coût  J",
                        font=customtkinter.CTkFont(size=11), 
                        text_color=GREY)
    cout_lab.pack(anchor="w")

    lbl_cout = customtkinter.CTkLabel(frame_resultat_mc, 
                                    text="—",
                                    font=customtkinter.CTkFont(size=16, weight="bold"), 
                                    text_color=DARK)
    lbl_cout.pack(anchor="w", pady=(2, 10))

    # matrice m
    m_lab= customtkinter.CTkLabel(frame_resultat_mc, 
                        text="Matrice M",
                        font=customtkinter.CTkFont(size=11), 
                        text_color=GREY)
    m_lab.pack(anchor="w")

    lbl_matM = customtkinter.CTkLabel(frame_resultat_mc,
                                        text="—",
                                        font=customtkinter.CTkFont(family="Courier New", size=12, weight="bold"),
                                        text_color=DARK,
                                        justify="left"
    )
    lbl_matM.pack(anchor="w", pady=(2, 10))

    def mode_MC():
        if mc_mode.get() == "discret":
            mc_func_frame.pack_forget()
            pnt_fram.pack(side="left", fill="y", padx=(0, 0))
        else:
            pnt_fram.pack_forget()
            mc_func_frame.pack(padx=0, pady=0)

    #descente de gradient
    grad_frame = customtkinter.CTkFrame(right_col, 
                                        height=0,
                                        fg_color="transparent")

    # fonction
    dg_func= customtkinter.CTkLabel(grad_frame, 
                        text="Définir f(x,y,...)",
                        font=customtkinter.CTkFont(size=12), 
                        text_color=DARK)
    dg_func.pack(anchor="w")

    grad_func_input = customtkinter.CTkEntry(grad_frame, 
                                            width=263, 
                                            height=36, 
                                            corner_radius=6,
                                            border_color=BORDER, 
                                            border_width=1, 
                                            fg_color=WHITE, 
                                            text_color=DARK,
                                            font=customtkinter.CTkFont(size=12), 
                                            placeholder_text="ex: x**2 - 3*y + 2")
    grad_func_input.pack(anchor="w")

    #les inputs
    grad_row1 = customtkinter.CTkFrame(grad_frame, 
                                    fg_color="transparent")
    grad_row1.pack(anchor="w")

    # x0
    grad_x0_col = customtkinter.CTkFrame(grad_row1, 
                                        fg_color="transparent")
    grad_x0_col.pack(side="left")

    x0_lab= customtkinter.CTkLabel(grad_x0_col, 
                        text="Valeurs Initiales",
                        font=customtkinter.CTkFont(size=12), 
                        text_color=DARK)
    x0_lab.pack(anchor="w")

    grad_x0_input = customtkinter.CTkEntry(grad_x0_col, 
                                        width=110, 
                                        height=34, 
                                        corner_radius=6,
                                        border_color=BORDER, 
                                        border_width=1, 
                                        fg_color=WHITE, 
                                        text_color=DARK,
                                        font=customtkinter.CTkFont(size=12), 
                                        placeholder_text="ex: 0, 1,...")
    grad_x0_input.pack()

    sepV= customtkinter.CTkFrame(grad_row1, 
                        width=1, 
                        fg_color=BORDER)
    sepV.pack(side="left", fill="y", padx=4)

    # pas
    grad_pas_col = customtkinter.CTkFrame(grad_row1, 
                                        fg_color="transparent")
    grad_pas_col.pack(side="left")

    pas_lab= customtkinter.CTkLabel(grad_pas_col, 
                        text="Pas (α)",
                        font=customtkinter.CTkFont(size=12), 
                        text_color=DARK)
    pas_lab.pack(anchor="w")

    grad_pas_input = customtkinter.CTkEntry(grad_pas_col, 
                                            width=110, 
                                            height=34, 
                                            corner_radius=6,
                                            border_color=BORDER, 
                                            border_width=1, 
                                            fg_color=WHITE, 
                                            text_color=DARK,
                                            font=customtkinter.CTkFont(size=12), 
                                            placeholder_text="ex: 0.01")
    grad_pas_input.pack()

    # tolerance
    tol_lab= customtkinter.CTkLabel(grad_frame, 
                        text="Tolérance",
                        font=customtkinter.CTkFont(size=12), 
                        text_color=DARK)
    tol_lab.pack(anchor="w")

    gd_tol_input = customtkinter.CTkEntry(grad_frame, 
                                            width=263, 
                                            height=34, 
                                            corner_radius=6,
                                            border_color=BORDER, 
                                            border_width=1, 
                                            fg_color=WHITE, 
                                            text_color=DARK,
                                            font=customtkinter.CTkFont(size=12), 
                                            placeholder_text="ex: 0.0001")
    gd_tol_input.pack(anchor="w")

    sep_dg = customtkinter.CTkFrame(grad_frame, 
                                    height=1, 
                                    fg_color=BORDER)
    sep_dg.pack(fill="x", pady= (5,5))

    # resultats descente
    dg_result_lab= customtkinter.CTkLabel(grad_frame, 
                        text="Résultats",
                        font=customtkinter.CTkFont(size=14, weight="bold"), 
                        text_color=DARK)
    dg_result_lab.pack(anchor="w")

    dg_min= customtkinter.CTkLabel(grad_frame, 
                        text="Minimum local",
                        font=customtkinter.CTkFont(size=11), 
                        text_color=GREY)
    dg_min.pack(anchor="w")

    lab_min = customtkinter.CTkLabel(grad_frame, 
                                        text="—",
                                        font=customtkinter.CTkFont(size=20, weight="bold"), 
                                        text_color=GREEN)
    lab_min.pack(anchor="w")

    dg_erreur_lab= customtkinter.CTkLabel(grad_frame, 
                        text="Erreur",
                        font=customtkinter.CTkFont(size=11), 
                        text_color=GREY)
    dg_erreur_lab.pack(anchor="w")

    lbl_err_grad = customtkinter.CTkLabel(grad_frame, 
                                        text="—",
                                        font=customtkinter.CTkFont(size=16, weight="bold"), 
                                        text_color=BTN_DEL)
    lbl_err_grad.pack(anchor="w")

    #recuperation des input de dg
    def get_input_gd():
        return [
            grad_func_input.get(),
            grad_x0_input.get(),
            grad_pas_input.get(),
            gd_tol_input.get()
        ]

    # ── état partagé Newton ───────────────────────────────────────────────────
    _last = {"poly_str": "", "diff": [], "coeffs_dd": [], "poly_asc": [],
             "xs": [], "ys": []}

    #fonction pour decider quoi faire qund il clique sur c=btn calculer 
    def on_calculer():
        # interpolation ou approximation
        if current_sel.get() == "Lagrange":
            rows_alive = [r for r in point_rows if r["frame"].winfo_exists()]
            if len(rows_alive) < 2:
                messagebox.showerror("Erreur", "Veuillez saisir au moins 2 points.")
                return

            x_pts, y_pts = [], []
            for r in rows_alive:
                raw_x = r["x"].get().strip()
                raw_y = r["y"].get().strip()
                if raw_x == "" or raw_y == "":
                    messagebox.showerror("Erreur", "Tous les champs x et y doivent être remplis.")
                    return
                try:
                    x_pts.append(float(raw_x))
                    y_pts.append(float(raw_y))
                except ValueError:
                    messagebox.showerror("Erreur", f"Valeur invalide : '{raw_x}' ou '{raw_y}'.")
                    return

            if len(set(x_pts)) != len(x_pts):
                messagebox.showerror("Erreur", "Les valeurs de x doivent être distinctes.")
                return

            try:
                resultat = poly_lagrange(x_pts, y_pts)
            except Exception as e:
                messagebox.showerror("Erreur inattendue", str(e))
                return

            if resultat is None:
                messagebox.showerror("Erreur", "Le calcul a échoué. Vérifiez vos points.")
                return

            err_max, str_poly, fig = resultat
            lbl_poly_interp.configure(text=str_poly)

            for widget in graph_frame.winfo_children():
                widget.destroy()

            if not affiche_point.get():
                x_arr = np.array(x_pts)
                y_arr = np.array(y_pts)
                xs = np.linspace(min(x_arr) - 0.5, max(x_arr) + 0.5, 500)
                ys = np.array([lagrange(x_arr, y_arr, xi) for xi in xs])
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(xs, ys, color='black', linewidth=1.5, label='P(x)')
                ax.axhline(0, color='black', linewidth=0.4)
                ax.axvline(0, color='black', linewidth=0.4)
                ax.set_title("Interpolation de Lagrange", fontsize=12, fontweight='bold')
                ax.legend()
                ax.grid(True, linestyle='--', alpha=0.5)

            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            graph_frame.figure = fig

        elif current_sel.get() == "Newton":
            inp = get_inputs()
            rows = inp["points"]
            if len(rows) < 2:
                messagebox.showwarning("Points manquants", "Entrez au moins 2 points.")
                return

            try:
                xs = [float(r["x"]) for r in rows]
                ys = [float(r["y"]) for r in rows]
            except ValueError:
                messagebox.showerror("Erreur", "Les coordonnées doivent être des nombres.")
                return

            if len(set(xs)) != len(xs):
                messagebox.showerror("Erreur", "Les abscisses x doivent être distinctes.")
                return

            try:
                coeffs_numpy, poly_str, diff, coeffs_dd = newton(xs, ys)
            except Exception as e:
                messagebox.showerror("Erreur de calcul", str(e))
                return

            # poly en puissances croissantes pour calcule_poly
            poly_asc = list(coeffs_numpy[::-1])

            # affichage résultats
            lbl_poly_interp.configure(text=poly_str)
            _last.update(poly_str=poly_str, diff=diff, coeffs_dd=coeffs_dd,
                         poly_asc=poly_asc, xs=xs, ys=ys)

            # graphe Newton
            for widget in graph_frame.winfo_children():
                widget.destroy()

            x_arr = np.array(xs)
            x_plot = np.linspace(min(x_arr) - 1, max(x_arr) + 1, 400)
            y_plot = [calcule_poly(poly_asc, x) for x in x_plot]

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(x_plot, y_plot, color="#1a73e8", linewidth=2, label="Newton")
            if affiche_point.get():
                ax.scatter(xs, ys, color=YELLOW, zorder=5, s=55, label="Points")
            ax.set_title(poly_str, fontsize=9, fontweight="bold")
            ax.set_xlabel("x", fontsize=9)
            ax.set_ylabel("P(x)", fontsize=9)
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3, linestyle="--")
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            graph_frame.figure = fig
            plt.close(fig)

        elif current_sel.get() == "Moindres carrés":
            inputs = get_inputs()
            if mc_mode.get() == "discret":
                lancer_mc_depuis_interface(
                    inputs,
                    lbl_poly,
                    lbl_cout,
                    lbl_matM,
                    graph_frame,
                    format_matrix
                )

            else:  # continu
                lancer_mc_continu(inputs, lbl_poly, lbl_cout, lbl_matM, graph_frame, format_matrix)

        elif current_sel.get() == "Descente de gradient":
            f_str, x0_str, alpha_str, tol_str = get_input_gd()

            # fonction
            f = sympify(f_str)

            # variables automatiques (approx simple)
            variables = sorted(list(f.free_symbols), key=lambda s: s.name)

            # conversion les inputs
            start = list(map(float, x0_str.split(",")))
            alpha = float(alpha_str)
            tolerance = float(tol_str)

            #appliquer l'algo 
            x, erreur = gradient_descent(f, variables, start, alpha, tolerance)

            #afficher les resultats
            lab_min.configure(text=str(x))
            lbl_err_grad.configure(text=str(erreur))

    # on_voir_detail — Newton uniquement
    def on_voir_detail():
        if not _last["diff"]:
            messagebox.showinfo("Aucun calcul", "Lancez d'abord un calcul Newton.")
            return

        win2 = tk.Toplevel(app)
        win2.title("Détail — Newton")
        win2.geometry("640x440")
        win2.configure(bg=WHITE)

        customtkinter.CTkLabel(win2,
            text="Tableau des différences divisées",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color=DARK).pack(pady=(14, 6))

        txt = tk.Text(win2, font=("Courier", 10), bg=LIGHT_BG,
                      wrap="none", padx=10, pady=10)
        txt.pack(fill="both", expand=True, padx=14, pady=(0, 6))

        # en-tête
        n = len(_last["xs"])
        header = "i  |  " + "  ".join(f"  d^{j}  " for j in range(n))
        txt.insert("end", header + "\n" + "─" * len(header) + "\n")

        for i, row in enumerate(_last["diff"]):
            vals = "  ".join(f"{v:8.4f}" for v in row)
            txt.insert("end", f"{i}  |  {vals}\n")

        txt.insert("end", "\n── Coefficients de Newton ──\n")
        for j, a in enumerate(_last["coeffs_dd"]):
            txt.insert("end", f"  a_{j} = {a:.6g}\n")

        txt.insert("end", f"\n{_last['poly_str']}\n")
        txt.configure(state="disabled")

    #calcule
    btn_calc = customtkinter.CTkButton(right_col, 
                                    text="▶   Calculer",
                                    width=260, 
                                    height=44,
                                    fg_color=YELLOW, 
                                    text_color=DARK, 
                                    hover_color=YELLOW_HVR,
                                    font=customtkinter.CTkFont(size=14, weight="bold"), 
                                    corner_radius=10,
                                    command=on_calculer
    )
    btn_calc.pack(padx=16, pady=(10, 14))

    f= customtkinter.CTkFrame(right_col, 
                        height=1, 
                        fg_color=BORDER)
    f.pack(fill="x", padx=16, pady=(0, 10))

    # resultats interpolation
    interp_res_frame = customtkinter.CTkFrame(right_col, 
                                            fg_color="transparent")

    inter_res_lab= customtkinter.CTkLabel(interp_res_frame, 
                        text="Résultats",
                        font=customtkinter.CTkFont(size=14, weight="bold"), 
                        text_color=DARK)
    inter_res_lab.pack(anchor="w", pady=(0, 6))

    poly_trouv_lab= customtkinter.CTkLabel(interp_res_frame, 
                        text="Polynôme trouvé",
                        font=customtkinter.CTkFont(size=11), 
                        text_color=GREY)
    poly_trouv_lab.pack(anchor="w")

    lbl_poly_interp = customtkinter.CTkLabel(interp_res_frame, 
                                            text="P(x) = —",
                                            font=customtkinter.CTkFont(size=13, weight="bold"), 
                                            text_color=DARK,
                                            wraplength=260, 
                                            justify="left")
    lbl_poly_interp.pack(anchor="w", pady=(4, 10))

    btn_detail = customtkinter.CTkButton(interp_res_frame, 
                                        text="Voir le détail du calcul",
                                        width=260, 
                                        height=38,
                                        fg_color=WHITE, 
                                        text_color=DARK, 
                                        hover_color=LIGHT_BG,
                                        border_width=1, 
                                        border_color=BORDER,
                                        font=customtkinter.CTkFont(size=13), 
                                        corner_radius=8,
                                        command=on_voir_detail
    )
    btn_detail.pack(pady=(0, 8))

    #recomendation
    RECO = {
        "Lagrange"             : "Lagrange est idéal pour un petit nombre de points bien espacés.",
        "Newton"               : "Newton (différences divisées) est efficace pour ajouter des points progressivement.",
        "Moindres carrés"      : "Moindres carrés minimise l'erreur globale — adapté aux données bruitées.",
        "Descente de gradient" : "Descente de gradient convient aux grands datasets avec de nombreux paramètres.",
    }

    def update_params(name):
        deg_display_frame.pack_forget()
        switch_row.pack_forget()
        mc_frame.pack_forget()
        grad_frame.pack_forget()
        interp_res_frame.pack_forget()

        if name in ("Lagrange", "Newton"):
            deg_display_frame.pack(anchor="w", padx=16, pady=(0, 8))
            switch_row.pack(anchor="w", padx=16, pady=(0, 12))
            interp_res_frame.pack(anchor="w", padx=16, pady=(0, 8))
            pnt_fram.pack(side="left", fill="y", padx=(0, 0))

        elif name == "Moindres carrés":
            mc_frame.pack(anchor="w", padx=16, pady=(0, 8))
            mode_MC()

        elif name == "Descente de gradient":
            grad_frame.pack(anchor="w")
            pnt_fram.pack_forget()
            vis_outer.pack_forget()
            param_title.pack_forget()
            mc_func_frame.pack_forget()

    def get_inputs():
        return {
            "points"     : [{"x": r["x"].get(), "y": r["y"].get()}
                            for r in point_rows if r["frame"].winfo_exists()],
            "show_pts"   : affiche_point.get(),
            "mc_mode"    : mc_mode.get(),
            "mc_func"    : mc_func_input.get(),
            "mc_a"       : mc_a_input.get(),
            "mc_b"       : mc_b_input.get(),
            "mc_deg"     : mc_deg_input.get(),
            "grad_func"  : grad_func_input.get(),
            "grad_x0"    : grad_x0_input.get(),
            "grad_pas"   : grad_pas_input.get(),
            "grad_tol"   : gd_tol_input.get(),
            "mode"       : current_mode.get(),
            "selection"  : current_sel.get()
        }
