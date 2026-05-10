import customtkinter
import tkinter as tk
from tkinter import *
from tools import *
from algo_dichotomie import *
from algo_newtonR import *
from algo_pt_fixe import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import numpy as np
import threading
import os

#to store figures and tables
if not os.path.exists("Resultat"):
        os.makedirs("Resultat")

def show(app, navigate):
    YELLOW     = "#f5c518"
    YELLOW_HVR = "#e6b800"
    WHITE      = "#ffffff"
    DARK       = "#0d1b2e"
    GREY       = "#777777"
    GREEN      = "#22a361"
    BORDER     = "#e0e0e0"
    TIP_BG     = "#fffde7"
    TIP_BORDER = "#f5e600"
    RED        = "#e03030"

    last_row    = []
    last_fig    = [None]
    last_racine = [None]
    last_graph_path = [None]
    last_table_path = [None]

    # ── header ────────────────────────────────────────────────────
    header = customtkinter.CTkFrame(app, fg_color=WHITE, bg_color=WHITE,corner_radius=0, height=54)
    header.pack(fill="x")
    header.pack_propagate(False)

    customtkinter.CTkButton(header, text="←", width=38, height=38,
                            fg_color="transparent", text_color=DARK,
                            hover_color="#f0f0f0",
                            font=customtkinter.CTkFont(size=20),corner_radius=8,
                            command=lambda: navigate("accueil")).pack(side="left", padx=(12,6), pady=8)

    customtkinter.CTkLabel(header,text="Axe 1 : Fonctions non linéaires",
                           font=customtkinter.CTkFont(size=17, weight="bold"),text_color=DARK).pack(side="left")

    #body
    body = customtkinter.CTkFrame(app, fg_color="transparent", bg_color=WHITE,height=300)
    body.pack(fill="x", expand=False, padx=14, pady=(10,8))
    body.pack_propagate(False)

    #colonne gauche
    left_col = customtkinter.CTkScrollableFrame(
        body,fg_color=WHITE,bg_color=WHITE,
        corner_radius=12,width=190
    )

    left_col.pack(side="left", fill="y", padx=(0,8))

    customtkinter.CTkLabel(left_col, text="Algorithmes",
                           font=customtkinter.CTkFont(size=13, weight="bold"),
                           text_color=DARK).pack(anchor="w", padx=14,pady=(14,6))

    algo_btns = {}
    op_btns   = {}
    current_sel  = tk.StringVar(value="")
    current_mode = tk.StringVar(value="algo")

    #saisir
    saisir = customtkinter.CTkScrollableFrame(body, fg_color=WHITE, bg_color=WHITE,corner_radius=12, width=295)
    saisir.pack(side="left", fill="y", padx=(0,8))

    param= customtkinter.CTkLabel(saisir, text="Paramètres",font=customtkinter.CTkFont(size=15, weight="bold"),
                           text_color=DARK)
    param.pack(anchor="w", padx=16, pady=(14,8))

    f=customtkinter.CTkLabel(saisir, text="Définir f(x)",
                           font=customtkinter.CTkFont(size=13),
                           text_color=DARK)
    f.pack(anchor="w", padx=16)

    inputf = customtkinter.CTkEntry(saisir, width=263, height=36,
                                    corner_radius=8, border_color=BORDER,
                                    border_width=1, text_color=DARK,
                                    fg_color=WHITE,
                                    font=customtkinter.CTkFont(size=12),
                                    placeholder_text="ex: sin(x)+x**3")
    inputf.pack(padx=16, pady=(3,10))

    # widgets caches
    lbl_phi   = customtkinter.CTkLabel(saisir, text="Fonction phi(x)",
                                       font=customtkinter.CTkFont(size=13),
                                       text_color=DARK)
    
    input_phi = customtkinter.CTkEntry(saisir, width=263, height=36,
                                       corner_radius=8, border_color=BORDER,
                                       border_width=1, fg_color=WHITE,
                                       text_color=DARK,
                                       font=customtkinter.CTkFont(size=12),
                                       placeholder_text="ex: x**2")

    lbl_x0   = customtkinter.CTkLabel(saisir, text="Point de départ x0",
                                      font=customtkinter.CTkFont(size=13),
                                      text_color=DARK)
    input_x0 = customtkinter.CTkEntry(saisir, width=263, height=36,
                                      corner_radius=8, border_color=BORDER,
                                      border_width=1, fg_color=WHITE,
                                      text_color=DARK,
                                      font=customtkinter.CTkFont(size=12),
                                      placeholder_text="ex: 0")

    lbl_interval = customtkinter.CTkLabel(saisir, text="Intervalle [a, b]",
                                          font=customtkinter.CTkFont(size=13),
                                          text_color=DARK)
    group   = customtkinter.CTkFrame(saisir, bg_color=WHITE,
                                     fg_color="transparent")
    a_entry = customtkinter.CTkEntry(group, placeholder_text="a",
                                     width=124, height=36, corner_radius=8,
                                     border_color=BORDER, text_color=DARK,
                                     fg_color=WHITE, border_width=1,
                                     font=customtkinter.CTkFont(size=12))
    b_entry = customtkinter.CTkEntry(group, placeholder_text="b",
                                     width=124, height=36, corner_radius=8,
                                     border_color=BORDER, text_color=DARK,
                                     fg_color=WHITE, border_width=1,
                                     font=customtkinter.CTkFont(size=12))
    a_entry.pack(side="left", padx=(0,6))
    b_entry.pack(side="left")

    # Tolérance en slider seul
    toler = customtkinter.CTkLabel(saisir, text="Tolérance",
                                    font=customtkinter.CTkFont(size=13),text_color=DARK)
    lbl_tol_val = customtkinter.CTkLabel(saisir, text="10⁻⁶",
                                        font=customtkinter.CTkFont(size=11),text_color=GREY)
    tol_slider  = customtkinter.CTkSlider(saisir, from_=1, to=10, width=263,
                                           number_of_steps=9)
    tol_value = [1e-6]   # stocke la valeur courante

    def on_tol_slider(val):
        exp = int(val)
        tol_value[0] = 10**(-exp)
        lbl_tol_val.configure(text=f"10⁻{exp}")

    tol_slider.set(6)
    tol_slider.configure(command=on_tol_slider)

    # message erreur
    lbl_err = customtkinter.CTkLabel(saisir, text="",
                                      font=customtkinter.CTkFont(size=11),
                                      text_color=RED, wraplength=263)
    lbl_err.pack(anchor="w", padx=16)

    #help
    def show_err(msg):
        lbl_err.configure(text=msg)
        app.after(4000, lambda: lbl_err.configure(text=""))

    def update_inputs(name):
        mode = current_mode.get()
        for w in [lbl_interval, group, toler, lbl_tol_val, tol_slider,
                  lbl_phi, input_phi, lbl_x0, input_x0]:
            w.pack_forget()

        if mode == "algo":
            if name == "Dichotomie":
                lbl_interval.pack(anchor="w", padx=16)
                group.pack(padx=16, pady=(3,10))
                toler.pack(anchor="w", padx=16)
                tol_slider.pack(padx=16, pady=(3,2))
                lbl_tol_val.pack(anchor="e", padx=16)

            elif name == "Newton":
                lbl_interval.pack(anchor="w", padx=16)
                group.pack(padx=16, pady=(3,10))
                lbl_x0.pack(anchor="w", padx=16)
                input_x0.pack(padx=16, pady=(3,10))
                toler.pack(anchor="w", padx=16)
                tol_slider.pack(padx=16, pady=(3,2))
                lbl_tol_val.pack(anchor="e", padx=16)

            elif name == "Point fixe":
                lbl_interval.pack(anchor="w", padx=16)
                group.pack(padx=16, pady=(3,10))
                lbl_phi.pack(anchor="w", padx=16)
                input_phi.pack(padx=16, pady=(3,10))
                lbl_x0.pack(anchor="w", padx=16)
                input_x0.pack(padx=16, pady=(3,10))
                toler.pack(anchor="w", padx=16)
                tol_slider.pack(padx=16, pady=(3,2))
                lbl_tol_val.pack(anchor="e", padx=16)

        elif mode == "op":
            if name in ["Continuité", "Table de variation", "Signe de f(x)"]:
                lbl_interval.pack(anchor="w", padx=16)
                group.pack(padx=16, pady=(3,10))

    def update_mode_ui():
        mode = current_mode.get()
        if mode == "algo":
            visualisation.pack(fill="both", expand=True, padx=14, pady=(0,14))
            result.pack(side="left", fill="both", expand=True)
            resultat.pack_forget()
        elif mode == "op":
            visualisation.pack_forget()
            result.pack_forget()
            resultat.pack(side="left", fill="both", expand=True)

    def refresh_algo_btns():
        sel = current_sel.get()
        for name, btn in algo_btns.items():
            if name == sel:
                btn.configure(fg_color=YELLOW, border_width=0,
                              font=customtkinter.CTkFont(size=14, weight="bold"))
            else:
                btn.configure(fg_color=WHITE, border_width=1,
                              font=customtkinter.CTkFont(size=13, weight="normal"))
        for btn in op_btns.values():
            btn.configure(fg_color=WHITE,
                          font=customtkinter.CTkFont(size=12, weight="normal"))

    def refresh_op_btns():
        sel = current_sel.get()
        for name, btn in op_btns.items():
            if name == sel:
                btn.configure(fg_color=YELLOW,
                              font=customtkinter.CTkFont(size=14, weight="bold"))
            else:
                btn.configure(fg_color=WHITE,
                              font=customtkinter.CTkFont(size=13, weight="normal"))
        for btn in algo_btns.values():
            btn.configure(fg_color=WHITE, border_width=1,
                          font=customtkinter.CTkFont(size=13, weight="normal"))

    def select_algo(name):
        current_sel.set(name)
        current_mode.set("algo")
        refresh_algo_btns()
        update_inputs(name)
        update_mode_ui()
        lbl_racine.configure(text="—")
        lbl_iters.configure(text="—")
        lbl_frac.configure(text="—")
        lbl_saved.configure(text="")
        last_racine[0] = None
        last_row.clear()
        last_graph_path[0] = None
        last_table_path[0] = None
        _update_reco(name)
        # clear canvas
        for w in canvas_frame.winfo_children():
            w.destroy()
        customtkinter.CTkLabel(canvas_frame,
                               text="Le graphe apparaîtra ici après le calcul.",
                               font=customtkinter.CTkFont(size=12),
                               text_color=GREY).pack(expand=True)

    def select_op(name):
        current_sel.set(name)
        current_mode.set("op")
        refresh_op_btns()
        update_mode_ui()
        update_inputs(name)

    #boutons
    for algo in ["Dichotomie", "Newton", "Point fixe"]:
        btn = customtkinter.CTkButton(left_col, text=algo, width=158,
                                      height=38, fg_color=WHITE,
                                      text_color=DARK, hover_color=YELLOW_HVR,
                                      anchor="w", corner_radius=8,
                                      border_width=1, border_color=BORDER,
                                      font=customtkinter.CTkFont(size=13),
                                      command=lambda n=algo: select_algo(n))
        btn.pack(padx=14, pady=3)
        algo_btns[algo] = btn

    customtkinter.CTkFrame(left_col, height=1,
                           fg_color=BORDER).pack(fill="x", padx=14, pady=(12,10))

    customtkinter.CTkLabel(left_col, text="Opérations sur\nles fonctions",
                           font=customtkinter.CTkFont(size=13, weight="bold"),
                           text_color=DARK,
                           justify="left").pack(anchor="w", padx=14, pady=(0,6))

    for op in ["Dérivée", "Continuité", "Table de variation", "Signe de f(x)"]:
        btn = customtkinter.CTkButton(left_col, text=op, width=158, height=34,
                                      fg_color=WHITE, text_color=DARK,
                                      hover_color=YELLOW_HVR, anchor="w",
                                      corner_radius=8, border_width=1,
                                      border_color=BORDER,
                                      font=customtkinter.CTkFont(size=13),
                                      command=lambda n=op: select_op(n))
        btn.pack(padx=14, pady=3)
        op_btns[op] = btn

    # ── affichage image png  ────────────────────
    def show_png_in_canvas(path):
        for w in canvas_frame.winfo_children():
            w.destroy()

        if not path or not os.path.exists(path):
            customtkinter.CTkLabel(canvas_frame,
                                   text="Aucune image disponible.",
                                   text_color=GREY).pack(expand=True)
            return

        # conteneur scrollable
        scroll = customtkinter.CTkScrollableFrame(canvas_frame,fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        img = Image.open(path)
        #redimensionner pour tenir dans la largeur dispo (~580px)
        max_w = 580
        ratio = max_w / img.width if img.width > max_w else 1
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        lbl_img = tk.Label(scroll, image=photo, bg=WHITE)
        lbl_img.image = photo   # garder ref
        lbl_img.pack(padx=8, pady=8)

    # ── on_calculer ───────────────────────────────────────────────
    def get_params():
        f_expr = inputf.get().strip()
        if not f_expr:
            show_err("Entrez f(x)")
            return None

        ep = tol_value[0]
        params = {"f": f_expr, "ep": ep}

        sel = current_sel.get()
        if sel in ["Dichotomie", "Newton", "Point fixe",
                   "Continuité", "Table de variation", "Signe de f(x)"]:
            a_str = a_entry.get().strip()
            b_str = b_entry.get().strip()
            if not a_str or not b_str:
                show_err("Entrez a et b")
                return None
            try:
                params["a"] = float(a_str)
                params["b"] = float(b_str)
            except ValueError:
                show_err("a ou b invalide")
                return None

        if sel in ["Newton", "Point fixe"]:
            x0_str = input_x0.get().strip()
            if not x0_str:
                show_err("Entrez x0")
                return None
            try:
                params["x0"] = float(x0_str)
            except ValueError:
                show_err("x0 invalide")
                return None

        if sel == "Point fixe":
            phi_str = input_phi.get().strip()
            if not phi_str:
                show_err("Entrez phi(x)")
                return None
            params["phi"] = phi_str

        return params

    def run_algo(params, sel):
        f_expr = params["f"]
        ep     = params["ep"]
        av     = params.get("a")
        bv     = params.get("b")

        try:
            #================= DICHOTOMIE =================
            if sel == "Dichotomie":
                # dichotomie return r, i
                res = dichotomie(f_expr, av, bv, ep)

                if res is None or res[0] is None:
                    app.after(0, lambda: _algo_error(
                        "Dichotomie : pas de racine dans [a,b] ou fonction discontinue."))
                    return

                racine, nb_iter = res

                app.after(
                    0,
                    lambda r=racine, n=nb_iter:
                    _update_result(f_expr, av, bv, r, n, sel)
                )

            # ================= NEWTON =================
            elif sel == "Newton":

                x0v = params["x0"]

                # verifications additionel in case
                f_np = to_numpy(f_expr)

                if not continu(f_np, av, bv):
                    app.after(0, lambda: _algo_error(
                        "Newton : f(x) n'est pas continue sur [a,b]."))
                    return

                if not check_x0(av, bv, x0v):
                    app.after(0, lambda: _algo_error(
                        "Newton : x0 doit être dans [a,b]."))
                    return
                # newton return r,i
                res = newton_r(f_expr, av, bv, x0v, ep)

                if res is None or res[0] is None:
                    app.after(0, lambda: _algo_error(
                        "Newton ne converge pas sur cet intervalle.\nVérifiez [a,b] et x0."))
                    return

                racine, nb_iter = res

                app.after(
                    0,
                    lambda r=racine, n=nb_iter:
                    _update_result(f_expr, av, bv, r, n, sel)
                )

            # ================= POINT FIXE =================
            elif sel == "Point fixe":

                x0v     = params["x0"]
                phi_str = params["phi"]

                f_np = to_numpy(f_expr)

                if not continu(f_np, av, bv):
                    app.after(0, lambda: _algo_error(
                        "Point fixe : f(x) n'est pas continue sur [a,b]."))
                    return

                if not check_x0(av, bv, x0v):
                    app.after(0, lambda: _algo_error(
                        "Point fixe : x0 doit être dans [a,b]."))
                    return

                # pt fixe return r,i
                res = point_fixe(f_expr, av, bv, phi_str, x0v, ep)

                if res is None or res[0] is None:
                    app.after(0, lambda: _algo_error(
                        "Point fixe ne converge pas.\nVérifiez phi(x) : il faut |phi'(x)| < 1 sur [a,b]."))
                    return

                racine, nb_iter = res

                app.after(0,lambda r=racine, n=nb_iter:
                    _update_result(f_expr, av, bv, r, n, sel)
                )

        except Exception as e:
            err = str(e)
            app.after(0, lambda: _algo_error(f"Erreur inattendue : {err}"))

    def _algo_error(msg):
        show_err(msg)
        btn_calc.configure(state="normal", text="▶   Calculer")

    def _update_result(f_expr, av, bv, racine, nb_iter, sel):
        last_racine[0] = racine
        f_np = to_numpy(f_expr)

        lbl_racine.configure(text=f"{racine:.7f}",
                             font=customtkinter.CTkFont(size=18, weight="bold"))
        lbl_iters.configure(text=str(nb_iter) if nb_iter is not None else "—")
        try:
            lbl_frac.configure(text=f"{float(f_np(racine)):.2e}")
        except:
            lbl_frac.configure(text="—")
        lbl_saved.configure(text="✓ Table et graphe enregistrés automatiquement")

        #chemins image
        graph_map = {
            "Dichotomie" : "resultat/dichotomie_graphe.png",
            "Newton"     : "resultat/newtonR_graphe.png",
            "Point fixe" : "resultat/ptfixe_graphe.png",
        }

        table_map = {
            "Dichotomie" : "resultat/dichotomie_table.png",
            "Newton"     : "resultat/newtonR_table.png",
            "Point fixe" : "resultat/ptfixe_table.png",
        }
        last_graph_path[0] = graph_map.get(sel)
        last_table_path[0] = table_map.get(sel)

        # afficher graphe par l algo
        show_png_in_canvas(last_graph_path[0])
        btn_calc.configure(state="normal", text="▶   Calculer")

    def on_calculer():
        sel  = current_sel.get()
        mode = current_mode.get()

        if not sel:
            show_err("Sélectionnez un algorithme ou une opération")
            return

        params = get_params()
        if params is None:
            return

        f_expr = params["f"]
        ep     = params["ep"]

        if mode == "algo":
            btn_calc.configure(state="disabled", text="Calcul...")
            t = threading.Thread(target=run_algo, args=(params, sel), daemon=True)
            t.start()

        elif mode == "op":
            try:
                if sel == "Dérivée":
                    df_sym = deriver(to_sympy(f_expr))        #call deriver()
                    lbl_res_op.configure(
                        text=f"f'(x) = {df_sym}",
                        font=customtkinter.CTkFont(size=13))

                elif sel == "Continuité":
                    av = params.get("a")
                    bv = params.get("b")
                    if av is None:
                        show_err("Entrez a et b")
                        return
                    f_np = to_numpy(f_expr)
                    ok = continu(f_np, av, bv)        #call continu()
                    lbl_res_op.configure(
                        text="✓ f(x) est continue sur [a, b]" if ok
                             else "✗ f(x) est discontinue sur [a, b]\n(division par zéro ou valeur infinie détectée)",
                        font=customtkinter.CTkFont(size=13),
                        text_color=GREEN if ok else RED)

                elif sel == "Table de variation":
                    av = params.get("a")
                    bv = params.get("b")
                    if av is None:
                        show_err("Entrez a et b")
                        return
                    # verify continu
                    f_np = to_numpy(f_expr)
                    if not continu(f_np, av, bv):
                        lbl_res_op.configure(
                            text="✗ Impossible : f(x) discontinue sur [a, b]",
                            text_color=RED,
                            font=customtkinter.CTkFont(size=12))
                        return
                    df_sym = deriver(to_sympy(f_expr))        #calc df deriver()
                    df_np  = sympyto_numpy(df_sym)
                    xs = np.linspace(av, bv, 9)
                    lines  = [f"{'x':>8}   {'f(x)':>12}   {'f\'(x)':>12}   {'variation'}"]
                    lines += ["-"*52]        #draw table vari
                    for xi in xs:
                        fval  = f_np(xi)
                        dfval = df_np(xi)
                        arrow = "↗" if dfval > 0 else ("↘" if dfval < 0 else "→")
                        lines.append(f"{xi:>8.4f}   {fval:>12.5f}   {dfval:>12.5f}   {arrow}")
                    lbl_res_op.configure(
                        text="\n".join(lines),
                        font=customtkinter.CTkFont(size=11, family="Courier"),
                        text_color=DARK)

                elif sel == "Signe de f(x)":
                    av = params.get("a")
                    bv = params.get("b")
                    if av is None:
                        show_err("Entrez a et b")
                        return
                    f_np = to_numpy(f_expr)
                    if not continu(f_np, av, bv):        #call continu()
                        lbl_res_op.configure(
                            text="✗ Impossible : f(x) discontinue sur [a, b]",
                            text_color=RED,
                            font=customtkinter.CTkFont(size=12))
                        return
                    xs  = np.linspace(av, bv, 9)          #try pt for le signe
                    lines = [f"{'x':>8}   {'f(x)':>12}   {'signe'}"]
                    lines += ["-"*36]
                    for xi in xs:
                        fval  = f_np(xi)
                        signe = "(+)" if fval > 0 else ("(-)" if fval < 0 else "(0)")
                        lines.append(f"{xi:>8.4f}   {fval:>12.5f}   {signe}")
                    lbl_res_op.configure(
                        text="\n".join(lines),
                        font=customtkinter.CTkFont(size=11, family="Courier"),
                        text_color=DARK)

            except Exception as e:
                lbl_res_op.configure(
                    text=f"Erreur : {e}",
                    text_color=RED,
                    font=customtkinter.CTkFont(size=12))

    # ── comparer les 3 methodes ───────────────────────────────────
    def on_comparer():

        f_expr = inputf.get().strip()
        a_str  = a_entry.get().strip()
        b_str  = b_entry.get().strip()
        ep = tol_value[0]
        x0_str = input_x0.get().strip()

        if not f_expr or not a_str or not b_str:
            show_err("Entrez f(x), a et b pour comparer")
            return

        try:
            av = float(a_str)
            bv = float(b_str)

        except ValueError:
            show_err("Paramètre invalide")
            return

        if not x0_str:
            show_err("Entrez x0 (requis pour Newton et point fixe)")
            return

        try:
            x0v = float(x0_str)

        except ValueError:
            show_err("x0 invalide")
            return

        results = {}
        iters_map = {}

        # ================= DICHOTOMIE =================
        try:
            res = dichotomie(f_expr, av, bv, ep)
            if res and res[0] is not None:
                racine, nb_iter = res
                results["Dichotomie"]   = racine
                iters_map["Dichotomie"] = nb_iter
            else:
                results["Dichotomie"] = None
        except Exception as e:
            results["Dichotomie"] = f"Erreur: {e}"

        # ================= NEWTON =================
        try:
            res = newton_r(f_expr, av, bv, x0v, ep)
            if res and res[0] is not None:
                racine, nb_iter = res
                results["Newton"] = racine
                iters_map["Newton"] = nb_iter
            else:
                results["Newton"] = None
        except Exception as e:
            results["Newton"] = f"Erreur: {e}"

        # ================= POINT FIXE =================
        phi_str = input_phi.get().strip()
        if phi_str:
            try:
                res = point_fixe(f_expr, av, bv, phi_str, x0v, ep)
                if res and res[0] is not None:
                    racine, nb_iter = res
                    results["Point fixe"] = racine
                    iters_map["Point fixe"] = nb_iter
                else:
                    results["Point fixe"] = None
            except Exception as e:
                results["Point fixe"] = f"Erreur: {e}"
        else:
            results["Point fixe"] = "phi(x) non fourni"

        # ================= MEILLEURE METHODE =================
        valid_iters = {
            k: v for k, v in iters_map.items()
            if isinstance(v, int)
        }
        best = min(valid_iters, key=valid_iters.get) if valid_iters else None

        # ================= AFFICHAGE =================
        #si une methode a trouve une racine valide l'afficher dans les champs
        best_racine = None
        best_nb_iter = None
        best_method = None
        
        for meth, val in results.items():
            if isinstance(val, float):
                if best_racine is None or iters_map.get(meth, 999) < best_nb_iter if best_nb_iter else True:
                    best_racine = val
                    best_nb_iter = iters_map.get(meth)
                    best_method = meth
        
        if best_racine is not None:
            #afficher la meilleure racine 
            lbl_racine.configure(text=f"{best_racine:.7f}",
                                font=customtkinter.CTkFont(size=18, weight="bold"))
            lbl_iters.configure(text=str(best_nb_iter) if best_nb_iter is not None else "—")
            
            #calc f(racine)
            try:
                f_np = to_numpy(f_expr)
                lbl_frac.configure(text=f"{float(f_np(best_racine)):.2e}")
            except:
                lbl_frac.configure(text="—")
            
            #message confirmation
            lbl_saved.configure(text=f"✓ Comparaison terminée - Les graphes et tables sont enregistrer")
            
            #get et affiche le graphe pour la meilleure methode
            try:
                #choisir le graphe de la meilleure méthode
                graph_path = {
                    "Dichotomie": "resultat/dichotomie_graphe.png",
                    "Newton": "resultat/newtonR_graphe.png", 
                    "Point fixe": "resultat/ptfixe_graphe.png"
                }.get(best_method)
                
                if graph_path and os.path.exists(graph_path):
                    show_png_in_canvas(graph_path)
                    last_graph_path[0] = graph_path
                    last_table_path[0] = {
                        "Dichotomie": "resultat/dichotomie_table.png",
                        "Newton": "resultat/newtonR_table.png",
                        "Point fixe": "resultat/ptfixe_table.png"
                    }.get(best_method)
            except:
                pass
                
            #afficher un les resultat compar
            summary_text = f"📊 Comparaison des 3 méthodes:\n"
            for meth, val in results.items():
                if isinstance(val, float):
                    summary_text += f"• {meth}: {val:.7f} ({iters_map.get(meth, '?')} itérations)\n"
                elif val is None:
                    summary_text += f"• {meth}: Pas de convergence\n"
                else:
                    summary_text += f"• {meth}: {str(val)[:30]}\n"
            
            summary_text += f"🏆 Meilleure méthode: {best_method} ({best_nb_iter} itérations)"
            
            #mettre a jour label de recommandation
            lbl_tip.configure(text=summary_text, wraplength=350)
            
        else:
            show_err("Aucune méthode n'a convergé vers une racine")

    def on_voir_iter():
        sel = current_sel.get()

        #afficher le PNG de la table dans visualisation
        if last_table_path[0] and os.path.exists(last_table_path[0]):
            show_png_in_canvas(last_table_path[0])
            return

        show_err("Lancez d'abord un calcul")

    # ── btn calculer ──────────────────────────────────────────────
    btn_calc = customtkinter.CTkButton(saisir, text="▶   Calculer",
                                       width=263, height=42,
                                       fg_color=YELLOW, text_color=DARK,
                                       hover_color=YELLOW_HVR,
                                       font=customtkinter.CTkFont(size=14,
                                                                   weight="bold"),
                                       corner_radius=10,
                                       command=on_calculer)
    btn_calc.pack(side="bottom", pady=14, padx=16)

    # resultat
    result = customtkinter.CTkScrollableFrame(body, bg_color=WHITE, fg_color=WHITE,corner_radius=12)
    result.pack(side="left", fill="both", expand=True)

    customtkinter.CTkLabel(result, text="Résultats",
                           font=customtkinter.CTkFont(size=14, weight="bold"),
                           text_color=DARK).pack(anchor="w", padx=16, pady=(14,8))

    def result_block(parent, title, default="—", val_color=DARK, val_size=18):
        fr = customtkinter.CTkFrame(parent, fg_color="transparent")
        fr.pack(anchor="w", padx=16, pady=(0,8))
        customtkinter.CTkLabel(fr, text=title,
                               font=customtkinter.CTkFont(size=11),
                               text_color=GREY).pack(anchor="w")
        lv = customtkinter.CTkLabel(fr, text=default,
                                    font=customtkinter.CTkFont(size=val_size,weight="bold"),
                                    text_color=val_color)
        lv.pack(anchor="w")
        return lv

    lbl_racine = result_block(result, "Racine trouvée",       "—", GREEN, 18)
    lbl_iters  = result_block(result, "Nombre d'itérations",  "—", DARK,  16)
    lbl_frac   = result_block(result, "f(racine)",            "—", DARK,  12)

    lbl_saved = customtkinter.CTkLabel(result, text="",
                                       font=customtkinter.CTkFont(size=11),text_color="#0F6E56")
    lbl_saved.pack(anchor="w", padx=16, pady=(0,6))

    RECO = {
        "Dichotomie" : "Dichotomie : robuste, ordre 1. \nLent mais sûr.",
        "Newton"     : "Newton : ordre 2, très rapide si f'(x) ≠ 0.",
        "Point fixe" : "Point fixe : dépend de phi. \nChoisir |phi'| < 1.",
    }
    box = customtkinter.CTkFrame(result, fg_color=TIP_BG, corner_radius=10,
                                  border_width=1, border_color=TIP_BORDER)
    box.pack(fill="x", padx=16, pady=(4,8))
    customtkinter.CTkLabel(box, text="💡  Recommandation",
                           font=customtkinter.CTkFont(size=12, weight="bold"),
                           text_color="#7a6500").pack(anchor="w", padx=10, pady=(8,2))
    lbl_tip = customtkinter.CTkLabel(box,
                                     text="Sélectionnez un algorithme.\n Veuillez saisir ces fonction correctement:\n- e^x: exp(x),      -Ln(x): log(x),       -log10(x): log(x,10),       -|x|: abs(x),       -π: pi.",
                                     font=customtkinter.CTkFont(size=11),
                                     text_color="#7a6500", justify="left",
                                     wraplength=500)
    lbl_tip.pack(anchor="w", padx=10, pady=(0,8))

    def _update_reco(name):
        lbl_tip.configure(text=RECO.get(name, "Sélectionnez un algorithme."))

    btn_row = customtkinter.CTkFrame(result, fg_color="transparent")
    btn_row.pack(fill="x", padx=16, pady=(4,8))

    btn_iter = customtkinter.CTkButton(btn_row, text="Voir itérations",
                                       width=130, height=36,
                                       fg_color=WHITE, text_color=DARK,
                                       hover_color=YELLOW_HVR,font=customtkinter.CTkFont(size=12),
                                       corner_radius=8,border_color=YELLOW, border_width=1,command=on_voir_iter)
    btn_iter.pack(side="left")

    btn_meth = customtkinter.CTkButton(btn_row, text="Comparer méthodes",
                                       width=150, height=36,
                                       fg_color=YELLOW, text_color=DARK,
                                       hover_color=YELLOW_HVR,font=customtkinter.CTkFont(size=12),
                                       corner_radius=8,command=on_comparer)
    btn_meth.pack(side="right")

    # ── visualisation ───────────────────────────────
    visualisation = customtkinter.CTkFrame(app, bg_color=WHITE, fg_color=WHITE,corner_radius=12)
    visualisation.pack(fill="both", expand=True, padx=14, pady=(0,14))

    vis_header = customtkinter.CTkFrame(visualisation, fg_color="transparent")
    vis_header.pack(fill="x", padx=14, pady=(10,4))
    customtkinter.CTkLabel(vis_header, text="Visualisation",
                           font=customtkinter.CTkFont(size=13, weight="bold"),
                           text_color=DARK).pack(side="left")

    #boutons graphe / table dans visualisation
    vis_btn_row = customtkinter.CTkFrame(vis_header, fg_color="transparent")
    vis_btn_row.pack(side="right")

    def show_graph_view():
        show_png_in_canvas(last_graph_path[0])

    def show_table_view():
        show_png_in_canvas(last_table_path[0])

    customtkinter.CTkButton(vis_btn_row, text="Graphe", width=80, height=28,
                             fg_color=WHITE, text_color=DARK,
                             hover_color=YELLOW_HVR,
                             border_width=1, border_color=BORDER,
                             font=customtkinter.CTkFont(size=11),
                             corner_radius=6,
                             command=show_graph_view).pack(side="left", padx=3)
    customtkinter.CTkButton(vis_btn_row, text="Table", width=80, height=28,
                             fg_color=WHITE, text_color=DARK,
                             hover_color=YELLOW_HVR,
                             border_width=1, border_color=BORDER,
                             font=customtkinter.CTkFont(size=11),
                             corner_radius=6,
                             command=show_table_view).pack(side="left", padx=3)

    canvas_frame = customtkinter.CTkFrame(visualisation, fg_color="transparent")
    canvas_frame.pack(fill="both", expand=True, padx=14, pady=(0,10))
    customtkinter.CTkLabel(canvas_frame,text="Le graphe apparaîtra ici après le calcul.",
                           font=customtkinter.CTkFont(size=12),
                           text_color=GREY).pack(expand=True)
    # ── resultats mode op ─────────────────────────────────────────
    resultat = customtkinter.CTkScrollableFrame(
        body,fg_color=WHITE,bg_color=WHITE,corner_radius=12)
    customtkinter.CTkLabel(resultat, text="Résultats",font=customtkinter.CTkFont(size=14, weight="bold"),
                           text_color=DARK).pack(anchor="w", padx=16, pady=(14,8))
    lbl_res_op = customtkinter.CTkLabel(resultat, text="—",
                                         font=customtkinter.CTkFont(size=12),
                                         text_color=DARK, justify="left",
                                         wraplength=350)
    lbl_res_op.pack(anchor="w", padx=16, pady=8)
