import customtkinter
import tkinter as tk

def show(app, navigate):
    # palette
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

    # header
    header = customtkinter.CTkFrame(app, bg_color=WHITE,
                                    fg_color=WHITE,
                                    corner_radius=0,
                                    height=54)
    header.pack(fill="x")
    header.pack_propagate(False)

    retour = customtkinter.CTkButton(header,
                                    text="←",
                                    width=38,
                                    height=38,
                                    fg_color="transparent",
                                    text_color=DARK,
                                    hover_color="#f0f0f0",
                                    font=customtkinter.CTkFont(size=20),
                                    corner_radius=8)
    retour.configure(command=lambda: navigate("accueil"))
    retour.pack(side="left", padx=(12, 6), pady=8)

    title = customtkinter.CTkLabel(header,
                                text="Axe 2 : Systèmes linéaires",
                                font=customtkinter.CTkFont(size=17, weight="bold"),
                                text_color=DARK)
    title.pack(side="left")


    vis_frame = customtkinter.CTkFrame(app, bg_color=WHITE,
                                    fg_color=WHITE,
                                    corner_radius=12)
    vis_frame.pack(side="bottom", fill="x", padx=14, pady=(0, 14))

    vis_header = customtkinter.CTkFrame(vis_frame,
                                        fg_color="transparent")
    vis_header.pack(fill="x", padx=14, pady=(10, 0))

    head_title = customtkinter.CTkLabel(vis_header,
                                        text="Visualisation",
                                        font=customtkinter.CTkFont(size=13, weight="bold"),
                                        text_color=DARK)
    head_title.pack(side="left")

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
                                        font=customtkinter.CTkFont(size=11))
    btn_export.pack(side="right")

    # placeholder matplotlib
    vis_place= customtkinter.CTkLabel(vis_frame, 
                        text="", 
                        height=200)
    vis_place.pack()

    # body
    body = customtkinter.CTkFrame(app, bg_color=WHITE,
                                fg_color="transparent")
    body.pack(fill="both", expand=True, padx=14, pady=(10, 8))

    # sidebar
    sidebar = customtkinter.CTkScrollableFrame(body, bg_color=WHITE,
                                            fg_color=WHITE,
                                            corner_radius=12,
                                            width=186)
    sidebar.pack(side="left", fill="y", padx=(0, 8))

    # algorithmes directs
    titre_direct = customtkinter.CTkLabel(sidebar,
                                        text="Algorithmes directs",
                                        font=customtkinter.CTkFont(size=13, weight="bold"),
                                        text_color=DARK)
    titre_direct.pack(anchor="w", padx=14, pady=(14, 6))

    algo_btns    = {}
    op_btns      = {}
    current_sel  = tk.StringVar()
    current_mode = tk.StringVar(value="algo")

    def refresh_algo_btns():
        sel = current_sel.get()
        for name, btn in algo_btns.items():
            actib = (name == sel)
            if actib:
                btn.configure(fg_color=YELLOW,
                            border_width=0,
                            font=customtkinter.CTkFont(size=15, weight="bold"))
            else:
                btn.configure(fg_color=WHITE,
                            font=customtkinter.CTkFont(size=13, weight="normal"))
        for btn in op_btns.values():
            btn.configure(fg_color=WHITE,
                        font=customtkinter.CTkFont(size=12, weight="normal"))

    def refresh_op_btns():
        sel = current_sel.get()
        for name, btn in op_btns.items():
            actib = (name == sel)
            if actib:
                btn.configure(fg_color=YELLOW,
                            font=customtkinter.CTkFont(size=15, weight="bold"))
            else:
                btn.configure(fg_color=WHITE,
                            font=customtkinter.CTkFont(size=13, weight="normal"))
        for btn in algo_btns.values():
            btn.configure(fg_color=WHITE,
                        border_width=1,
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
                                    command=lambda n=algo: select_algo(n))
        b.pack(padx=14, pady=3)
        algo_btns[algo] = b

    separ1 = customtkinter.CTkFrame(sidebar,
                                    height=1,
                                    fg_color=BORDER)
    separ1.pack(fill="x", padx=14, pady=(10, 8))

    # algorithmes indirects
    titre_indirects = customtkinter.CTkLabel(sidebar,
                                            text="Algorithmes indirects",
                                            font=customtkinter.CTkFont(size=13, weight="bold"),
                                            text_color=DARK)
    titre_indirects.pack(anchor="w", padx=14, pady=(0, 6))

    for algo in ["Jacobi", "Gauss-Seidel", "Relaxation"]:
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
                                    command=lambda n=algo: select_algo(n))
        b.pack(padx=14, pady=3)
        algo_btns[algo] = b

    sip2 = customtkinter.CTkFrame(sidebar,
                                height=1,
                                fg_color=BORDER)
    sip2.pack(fill="x", padx=14, pady=(12, 10))

    # operations sur matrices
    titre_op = customtkinter.CTkLabel(sidebar,
                                    text="Opérations sur\nles matrices",
                                    font=customtkinter.CTkFont(size=13, weight="bold"),
                                    text_color=DARK,
                                    justify="left")
    titre_op.pack(anchor="w", padx=14, pady=(0, 6))

    #les options
    for op in ["Normes matricielles", "Normes vectorielles", "Conditionnement", "Déterminant", "Transposée", "Inverse"]:
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
                                    command=lambda n=op: select_op(n))
        b.pack(padx=14, pady=3)
        op_btns[op] = b

    #content
    content = customtkinter.CTkScrollableFrame(body, bg_color=WHITE,
                                    fg_color=WHITE,
                                    corner_radius=12,
                                    width=420)
    content.pack(side="left", fill="y", padx=(0, 8))


    top_row = customtkinter.CTkFrame(content,
                                    fg_color="transparent")
    top_row.pack(fill="x", padx=16, pady=(12, 4))

    lab_mat = customtkinter.CTkLabel(top_row,
                                    text="Matrice A",
                                    font=customtkinter.CTkFont(size=13, weight="bold"),
                                    text_color=DARK)
    lab_mat.pack(side="left")

    lab_b = customtkinter.CTkLabel(top_row,
                                text="Vecteur b",
                                font=customtkinter.CTkFont(size=13, weight="bold"),
                                text_color=DARK)

    size = tk.IntVar(value=3)

    mat_scroll_outer = tk.Frame(content,
                                bg=WHITE)
    mat_scroll_outer.pack(padx=16, pady=(0, 4), fill="x")

    mat_canvas = tk.Canvas(mat_scroll_outer,
                            bg=WHITE,
                            highlightthickness=0,
                            width=374,
                            height=250)

    mat_scroll_y = tk.Scrollbar(mat_scroll_outer,
                                orient="vertical",
                                command=mat_canvas.yview)

    mat_scroll_x = tk.Scrollbar(mat_scroll_outer,
                                orient="horizontal",
                                command=mat_canvas.xview)

    mat_canvas.configure(yscrollcommand=mat_scroll_y.set,
                        xscrollcommand=mat_scroll_x.set)

    mat_scroll_x.pack(side="bottom", fill="x")
    mat_scroll_y.pack(side="right",  fill="y")
    mat_canvas.pack(side="left", fill="both", expand=True)

    # frame interne qui contiendra la grille
    matrix_frame = tk.Frame(mat_canvas, bg=WHITE)
    mat_canvas_win_id = mat_canvas.create_window((0, 0), window=matrix_frame, anchor="nw")

    #pour pouvoir scroller
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
                e = customtkinter.CTkEntry(matrix_frame,
                                        width=52,
                                        height=34,
                                        corner_radius=6,
                                        border_color=BORDER,
                                        border_width=1,
                                        fg_color=WHITE,
                                        text_color=DARK,
                                        font=customtkinter.CTkFont(size=12),
                                        justify="center")
                e.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(e)
            mat_input.append(row_entries)

    def draw_vector(n):
        # afficher label b
        if not lab_b.winfo_ismapped():
            lab_b.pack(side="right")

        for i in range(n):

            # séparateur |
            sep_lbl = tk.Label(matrix_frame,
                            text="│",
                            fg=BORDER,
                            bg=WHITE,
                            font=("Arial", 18))
            sep_lbl.grid(row=i, column=n, padx=4)

            # champ b
            bv = customtkinter.CTkEntry(matrix_frame,
                                        width=52,
                                        height=34,
                                        corner_radius=6,
                                        border_color=BORDER,
                                        border_width=1,
                                        fg_color=WHITE,
                                        text_color=DARK,
                                        font=customtkinter.CTkFont(size=12),
                                        justify="center")
            bv.grid(row=i, column=n + 1, padx=2, pady=2)
            vec_input.append(bv)

    # boutons effacer aleatoire
    btns = customtkinter.CTkFrame(content,
                                fg_color="transparent")
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
        for i in range(n):
            for j in range(n):
                mat_input[i][j].delete(0, "end")
                mat_input[i][j].insert(0, str(random.randint(-9, 9)))
            if i < len(vec_input):
                vec_input[i].delete(0, "end")
                vec_input[i].insert(0, str(random.randint(1, 20)))

    for txt, cmd in [("Effacer", on_vide), ("Aléatoire", on_aleatoire)]:
        button = customtkinter.CTkButton(btns,
                                        text=txt,
                                        width=100,
                                        height=30,
                                        fg_color=LIGHT_BG,
                                        text_color=DARK,
                                        hover_color=BORDER,
                                        border_width=1,
                                        border_color=BORDER,
                                        corner_radius=8,
                                        font=customtkinter.CTkFont(size=12),
                                        command=cmd)
        button.pack(side="left", padx=4)

    # taille de la matrice
    size_row = customtkinter.CTkFrame(content,
                                    fg_color="transparent")
    size_row.pack(padx=16, pady=(0, 6))

    lab_size = customtkinter.CTkLabel(size_row,
                                    text="Taille  n×n :",
                                    font=customtkinter.CTkFont(size=12),
                                    text_color=GREY)
    lab_size.pack(side="left", padx=(0, 8))

    size_menu = customtkinter.CTkOptionMenu(
        size_row,
        values=["2", "3", "4", "5", "6", "7", "8"],
        width=70,
        height=30,
        corner_radius=6,
        fg_color=WHITE,
        text_color=DARK,
        button_color=YELLOW,
        button_hover_color=YELLOW_HVR,
        dropdown_fg_color=WHITE,
        dropdown_text_color=DARK,
        font=customtkinter.CTkFont(size=12),
        command=lambda val: [
            size.set(int(val)),
            clear_grid(),
            draw_matrix(int(val)),
            draw_vector(int(val)) if (current_mode.get() == "algo" or current_sel.get() == "Normes vectorielles") else lab_b.pack_forget()
        ]
    )
    size_menu.set("3")
    size_menu.pack(side="left")

    sep3 = customtkinter.CTkFrame(content,
                                height=1,
                                fg_color=BORDER)
    sep3.pack(fill="x", padx=16, pady=(6, 8))

    # les normes
    norm_section = customtkinter.CTkFrame(content,
                                        fg_color="transparent")

    titre_norm = customtkinter.CTkLabel(norm_section,
                                        text="Type de norme",
                                        font=customtkinter.CTkFont(size=12, weight="bold"),
                                        text_color=DARK)
    titre_norm.pack(anchor="w", pady=(0, 6))

    norm_type_var  = tk.StringVar(value="‖·‖₁")
    norm_btns_row  = customtkinter.CTkFrame(norm_section, fg_color="transparent")
    norm_btns_row.pack(anchor="w")
    norm_btn_refs  = {}

    def select_norm(nrm):
        norm_type_var.set(nrm)
        for n, btn in norm_btn_refs.items():
            btn.configure(fg_color=YELLOW if n == nrm else WHITE)
        if nrm == "‖·‖ₚ":
            norm_p_frame.pack(anchor="w", pady=(6, 0))
        else:
            norm_p_frame.pack_forget()

    for nrm in ["‖·‖₁", "‖·‖₂", "‖·‖∞", "‖·‖ₚ"]:
        nb = customtkinter.CTkButton(norm_btns_row,
                                    text=nrm,
                                    width=66,
                                    height=30,
                                    fg_color=YELLOW if nrm == "‖·‖₁" else WHITE,
                                    text_color=DARK,
                                    hover_color=YELLOW_HVR,
                                    corner_radius=8,
                                    border_width=1,
                                    border_color=BORDER,
                                    font=customtkinter.CTkFont(size=12),
                                    command=lambda n=nrm: select_norm(n))
        nb.pack(side="left", padx=(0, 3))
        norm_btn_refs[nrm] = nb

    norm_p_frame = customtkinter.CTkFrame(norm_section, 
                                        fg_color="transparent")

    p_lab= customtkinter.CTkLabel(norm_p_frame,
                            text="p =",
                            font=customtkinter.CTkFont(size=12),
                            text_color=GREY)
    p_lab.pack(side="left", padx=(0, 6))

    entry_p = customtkinter.CTkEntry(norm_p_frame,
                                    width=60,
                                    height=30,
                                    corner_radius=6,
                                    border_color=BORDER,
                                    fg_color=WHITE,
                                    border_width=1,
                                    font=customtkinter.CTkFont(size=12))
    entry_p.insert(0, "3")
    entry_p.pack(side="left")

    # parametres iteratifs
    parametres = customtkinter.CTkFrame(content,
                                        fg_color="transparent")

    titre_p = customtkinter.CTkLabel(parametres,
                                    text="Paramètres (Itératif)",
                                    font=customtkinter.CTkFont(size=13, weight="bold"),
                                    text_color=DARK)
    titre_p.pack(anchor="w", padx=0, pady=(0, 8))

    # tolerance
    tol_col = customtkinter.CTkFrame(parametres, fg_color="transparent")
    tol_col.pack(anchor="w", pady=(0, 8))

    tolerance_lab= customtkinter.CTkLabel(tol_col,
                            text="Tolérance",
                            font=customtkinter.CTkFont(size=12),
                            text_color=GREY)
    tolerance_lab.pack(anchor="w")

    tol_input = customtkinter.CTkEntry(tol_col,
                                        width=160,
                                        height=34,
                                        corner_radius=6,
                                        border_color=BORDER,
                                        border_width=1,
                                        fg_color=WHITE,
                                        text_color=DARK,
                                        font=customtkinter.CTkFont(size=12),
                                        placeholder_text="0.00001")
    tol_input.pack(anchor="w")

    #omega
    omega_col = customtkinter.CTkFrame(parametres, fg_color="transparent")

    omega_lab= customtkinter.CTkLabel(omega_col,
                            text="Paramètre ω",
                            font=customtkinter.CTkFont(size=12),
                            text_color=GREY)
    omega_lab.pack(anchor="w")

    omega = customtkinter.CTkEntry(omega_col,
                                    width=160,
                                    height=34,
                                    corner_radius=6,
                                    border_color=BORDER,
                                    border_width=1,
                                    fg_color=WHITE,
                                    text_color=DARK,
                                    font=customtkinter.CTkFont(size=12),
                                    placeholder_text="1.25")
    omega.pack(anchor="w")

    #btns calculer et voir iterations
    btns_calc_row = customtkinter.CTkFrame(content, 
                                        fg_color="transparent")
    btns_calc_row.pack(side="bottom", pady=12, padx=16, fill="x")

    btn_calc = customtkinter.CTkButton(btns_calc_row,
                                        text="▶   Calculer",
                                        width=170,
                                        height=40,
                                        fg_color=YELLOW,
                                        text_color=WHITE,
                                        hover_color=YELLOW_HVR,
                                        font=customtkinter.CTkFont(size=14, weight="bold"),
                                        corner_radius=10
                                        # command=on_calculer a faire
                                        )
    btn_calc.pack(side="left", padx=(0, 8))

    btn_iter = customtkinter.CTkButton(btns_calc_row,
                                        text="Voir itérations",
                                        width=160,
                                        height=40,
                                        fg_color=WHITE,
                                        text_color=DARK,
                                        hover_color=YELLOW_HVR,
                                        font=customtkinter.CTkFont(size=13, weight="bold"),
                                        corner_radius=10,
                                        border_color=YELLOW,
                                        border_width=1
                                        # command=on_voir_iterations  a faire
                                        )
    btn_iter.pack(side="left")

    # resultats
    result = customtkinter.CTkScrollableFrame(body, bg_color=WHITE,
                                            fg_color=WHITE,
                                            corner_radius=12)
    result.pack(side="right", fill="both", expand=True)

    res_title = customtkinter.CTkLabel(result,
                                        text="Résultats",
                                        font=customtkinter.CTkFont(size=14, weight="bold"),
                                        text_color=DARK)
    res_title.pack(anchor="w", padx=16, pady=(14, 10))

    #solution
    sol_title = customtkinter.CTkLabel(result,
                                        text="Solution x",
                                        font=customtkinter.CTkFont(size=11),
                                        text_color=GREY)
    sol_title.pack(anchor="w", padx=16)

    solution_frame = customtkinter.CTkFrame(result,
                                            fg_color=LIGHT_BG,
                                            corner_radius=8)
    solution_frame.pack(anchor="w", padx=16, pady=(4, 10))

    iter_frame = customtkinter.CTkFrame(result, 
                                        fg_color="transparent")
    iter_frame.pack(anchor="w", padx=16, pady=(0, 10))

    lbl_= customtkinter.CTkLabel(iter_frame,
                                text="Nombre d'itérations",
                                font=customtkinter.CTkFont(size=11),
                                text_color=GREY)
    lbl_.pack(anchor="w")

    lbl_iterations = customtkinter.CTkLabel(iter_frame,
                                    text="-",
                                    font=customtkinter.CTkFont(size=24, weight="bold"),
                                    text_color=DARK)
    lbl_iterations.pack(anchor="w")


    residu_frame = customtkinter.CTkFrame(result, 
                                        fg_color="transparent")
    iter_frame.pack(anchor="w", padx=16, pady=(0, 10))

    lbl_2= customtkinter.CTkLabel(residu_frame,
                                text="Norme du résidu",
                                font=customtkinter.CTkFont(size=11),
                                text_color=GREY)
    lbl_2.pack(anchor="w")

    lbl_residu = customtkinter.CTkLabel(iter_frame,
                                    text="-",
                                    font=customtkinter.CTkFont(size=18, weight="bold"),
                                    text_color=DARK)
    lbl_residu.pack(anchor="w")

    # convergence
    conv_frame = customtkinter.CTkFrame(result, 
                                        fg_color="transparent")
    conv_frame.pack(anchor="w", padx=16, pady=(0, 8))

    customtkinter.CTkLabel(conv_frame,
                            text="Convergence",
                            font=customtkinter.CTkFont(size=11),
                            text_color=GREY).pack(anchor="w")

    lbl_conv = customtkinter.CTkLabel(conv_frame,
                                    text="—",
                                    font=customtkinter.CTkFont(size=15, weight="bold"),
                                    text_color=GREY)
    lbl_conv.pack(anchor="w")

    def set_convergence(converged: bool):
        if converged:
            lbl_conv.configure(text="Convergé",  text_color=GREEN)
        else:
            lbl_conv.configure(text="Divergé",   text_color="#e53935")

    #matrice iteration
    iter_mat_section = customtkinter.CTkFrame(result, 
                                            fg_color="transparent")

    iter_mat_lab= customtkinter.CTkLabel(iter_mat_section,
                            text="Matrice d'itération",
                            font=customtkinter.CTkFont(size=11),
                            text_color=GREY)
    iter_mat_lab.pack(anchor="w")

    iter_mat_display = customtkinter.CTkFrame(iter_mat_section,
                                            fg_color=LIGHT_BG,
                                            corner_radius=8)
    iter_mat_display.pack(anchor="w", pady=(4, 0), fill="x")

    lbl_iter_mat = customtkinter.CTkLabel(iter_mat_display,
                                        text="—",
                                        font=customtkinter.CTkFont(size=12),
                                        text_color=DARK,
                                        justify="left")
    lbl_iter_mat.pack(anchor="w", padx=10, pady=8)

    #resultats op
    op_result_section = customtkinter.CTkFrame(result, 
                                            fg_color="transparent")

    op_result_lbl_title = customtkinter.CTkLabel(op_result_section,
                                                text="Résultat",
                                                font=customtkinter.CTkFont(size=11),
                                                text_color=GREY)
    op_result_lbl_title.pack(anchor="w")

    lbl_op_val = customtkinter.CTkLabel(op_result_section,
                                        text="—",
                                        font=customtkinter.CTkFont(size=22, weight="bold"),
                                        text_color=GREEN,
                                        justify="left",
                                        wraplength=280)
    lbl_op_val.pack(anchor="w", pady=(2, 0))

    #des recomendations avec explication 
    RECO = {
        "Gauss"              : "Gauss est stable pour la plupart\ndes systèmes bien conditionnés.",
        "LU"                 : "LU est recommandé pour résoudre\nplusieurs systèmes avec la même matrice A.",
        "Jacobi"             : "Jacobi converge si A est à diagonale\nstrictement dominante.",
        "Gauss-Seidel"       : "Gauss-Seidel converge bien pour cette\nmatrice (symétrique à diagonale dominante).",
        "Relaxation"         : "Relaxation accélère la convergence\navec un bon choix de ω (entre 1 et 2).",
        "Normes matricielles": "‖A‖₁ = max colonne, ‖A‖∞ = max ligne,\n‖A‖₂ = plus grande valeur singulière.",
        "Normes vectorielles": "‖x‖₂ (euclidienne) est la plus utilisée.\n‖x‖₁ = somme des valeurs absolues.",
        "Conditionnement"    : "κ(A) grand → système mal conditionné,\nsensible aux erreurs d'arrondi.",
        "Déterminant"        : "Si det(A) = 0, le système n'a pas\nde solution unique.",
        "Transposée"         : "Aᵀ permet de vérifier la symétrie de A.",
        "Inverse"            : "A⁻¹ existe seulement si det(A) ≠ 0.",
    }

    box = customtkinter.CTkFrame(result,
                                fg_color=TIP_BG,
                                corner_radius=10,
                                border_width=1,
                                border_color=TIP_BORDER)
    box.pack(side="bottom", fill="x", padx=16, pady=(4, 12))

    customtkinter.CTkLabel(box,
                            text="💡  Recommandation",
                            font=customtkinter.CTkFont(size=12, weight="bold"),
                            text_color="#7a6500").pack(anchor="w", padx=10, pady=(8, 2))

    lbl_tip = customtkinter.CTkLabel(box,
                                    text=RECO["Gauss"],
                                    font=customtkinter.CTkFont(size=11),
                                    text_color="#7a6500",
                                    justify="left",
                                    wraplength=280)
    lbl_tip.pack(anchor="w", padx=10, pady=(0, 8))

    #affichage
    ITER_ALGOS = {"Jacobi", "Gauss-Seidel", "Relaxation"}
    NORM_OPS   = {"Normes matricielles", "Normes vectorielles"}
    # operation qui n'ont pas besoin de b
    OPS_NO_B   = {"Normes matricielles", "Conditionnement", "Déterminant", "Transposée", "Inverse"}

    #fct pour les mises a jour
    def update_inputs(name):
        # cacher les sections optionnelles
        parametres.pack_forget()
        omega_col.pack_forget()
        norm_section.pack_forget()
        norm_p_frame.pack_forget()

        mode   = current_mode.get()
        show_b = (mode == "algo") or (name == "Normes vectorielles")
        clear_grid()

        n = size.get()

        if mode == "algo":
            draw_matrix(n)
            draw_vector(n)

        elif name == "Normes vectorielles":
            clear_grid()
            draw_vector(n)

        else:
            draw_matrix(n)
            lab_b.pack_forget()

        if mode == "algo" and name in ITER_ALGOS:
            # afficher les parametres iteratifs sous sep3
            parametres.pack(padx=16, pady=(0, 8), anchor="w")
            if name == "Relaxation":
                #si c'est relaxation afficher omega
                omega_col.pack(anchor="w", pady=(0, 8))
                btn_iter.pack(side="left")
        else:
            btn_iter.pack_forget()

        if name in NORM_OPS:
            norm_section.pack(padx=16, pady=(0, 8), anchor="w")


        

        update_results_display(name)
        lbl_tip.configure(text=RECO.get(name, "Sélectionnez un algorithme."))

    def update_results_display(name):

        # cacher TOUT
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

    def get_inputs():
        n   = size.get()
        mat = [[mat_input[i][j].get() for j in range(n)] for i in range(n)]
        bc  = [vec_input[i].get() for i in range(n)] if vec_input else []
        return {
            "matrix"    : mat,
            "vecteur_b" : bc,
            "tol"       : tol_input.get(),
            "omega"     : omega.get(),
            "norm_type" : norm_type_var.get(),
            "norm_p"    : entry_p.get(),
            "mode"      : current_mode.get(),
            "selection" : current_sel.get()
        }