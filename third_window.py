import customtkinter

#palette
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

win = customtkinter.CTk()
win.geometry("1100x750")
win.title("Axe 2 — Systèmes linéaires")
win.configure(fg_color=LIGHT_BG)
win._set_appearance_mode("light")

#header
header = customtkinter.CTkFrame(win,
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
                                 corner_radius=8
)
retour.pack(side="left", padx=(12, 6), pady=8)

title = customtkinter.CTkLabel(header, 
                               text="Axe 2 : Systèmes linéaires",
                               font=customtkinter.CTkFont(size=17, weight="bold"), 
                               text_color=DARK
)
title.pack(side="left")

#body
body = customtkinter.CTkFrame(win,
                               fg_color="transparent")
body.pack(fill="both", expand=True, padx=14, pady=(10, 14))

#sidebar
sidebar = customtkinter.CTkScrollableFrame(body,
                                            fg_color=WHITE, 
                                            corner_radius=12, 
                                            width=186)
sidebar.pack(side="left", fill="y", padx=(0, 8))

# Section : Algorithmes directs
titre_direct = customtkinter.CTkLabel(sidebar, 
                                      text="Algorithmes directs",
                                      font=customtkinter.CTkFont(size=13, weight="bold"), 
                                      text_color=DARK
)
titre_direct.pack(anchor="w", padx=14, pady=(14, 6))


algo_btns    = {}
op_btns      = {}
current_sel  = tk.StringVar()
current_mode = tk.StringVar(value="algo")
#algo pour manipulation des btn
#si on click sur un btn d'une algo 
def refresh_algo_btns():
    sel = current_sel.get()
    for name, btn in algo_btns.items():
        active = (name == sel)
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

#si on click sur une opt
def refresh_op_btns():
    sel = current_sel.get()
    for name, btn in op_btns.items():
        active = (name == sel)
        if active:
            btn.configure(fg_color=YELLOW,
                          font=customtkinter.CTkFont(size=15, weight="bold")
            )
        else:
            btn.configure(fg_color=WHITE,
                          font=customtkinter.CTkFont(size=13, weight="normal")
            )

    for btn in algo_btns.values(): # on fait aussi le refresh des boutons algo pour enlever la selection si on vient de cliquer sur une op
        btn.configure(fg_color=WHITE, 
                      border_width=1,
                      font=customtkinter.CTkFont(size=13, weight="normal")
        )   

#on fait une seule fonction qui regroupe tous
def select_algo(name):
    current_sel.set(name) 
    current_mode.set("algo")
    refresh_algo_btns()
    update_inputs(name)
    # update_mode_ui()

#pour options
def select_op(name):
    current_sel.set(name)
    current_mode.set("op")
    refresh_op_btns()
    # update_mode_ui()
    update_inputs(name)
    # on ajoute d'atres fonctions


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
        command=lambda n=algo: select_algo(n)
    )
    b.pack(padx=14, pady=3)
    algo_btns[algo] = b

#separateur
separ1=customtkinter.CTkFrame(sidebar, 
                              height=1, 
                              fg_color=BORDER)
separ1.pack(fill="x", padx=14, pady=(10, 8))

# algo indirects
titre_indirects = customtkinter.CTkLabel(sidebar, 
                                         text="Algorithmes indirects",
                                         font=customtkinter.CTkFont(size=13, weight="bold"),    
                                         text_color=DARK
)
titre_indirects.pack(anchor="w", padx=14, pady=(0, 6))

for algo in ["Jacobi", "Gauss-Seidel", "Relaxation (SOR)"]:
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

sip2= customtkinter.CTkFrame(sidebar, 
                             height=1, 
                             fg_color=BORDER)
sip2.pack(fill="x", padx=14, pady=(12, 10))

#operations sur matrices
titre_op = customtkinter.CTkLabel(sidebar, 
                                 text="Opérations sur\nles matrices",
                                 font=customtkinter.CTkFont(size=13, weight="bold"), 
                                 text_color=DARK, 
                                 justify="left"
)
titre_op.pack(anchor="w", padx=14, pady=(0, 6))

for op in ["Normes induites", "Conditionnement", "Déterminant", "Transposée", "Inverse"]:
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

#body
body = customtkinter.CTkFrame(body, 
                              fg_color=WHITE, 
                              corner_radius=12, 
                              width=420)
body.pack(side="left", fill="y", padx=(0, 8))
body.pack_propagate(False)

top_row = customtkinter.CTkFrame(body, 
                                 fg_color="transparent")
top_row.pack(fill="x", padx=16, pady=(14, 6))

lab_mat= customtkinter.CTkLabel(top_row, 
                                text="Matrice A",
                                font=customtkinter.CTkFont(size=13, weight="bold"),     
                                text_color=DARK
)
lab_mat.pack(side="left", padx=(0, 130))

lab_b= customtkinter.CTkLabel(top_row, 
                              text="bcteur b",
                              font=customtkinter.CTkFont(size=13, weight="bold"), 
                              text_color=DARK
)
lab_b.pack(side="left")

# Taille de la matrice par defaut 3
size = tk.IntVar(value=3)

# Frame contenant la grille
matrix_frame = customtkinter.CTkFrame(body, 
                                      fg_color="transparent")
matrix_frame.pack(padx=16, pady=(0, 8))

# Stockage des Entry widgets
mat_input = []
vec_input = [] 

def mat_grid(n):
    for widget in matrix_frame.winfo_children():
        widget.destroy()
    mat_input.clear()
    vec_input.clear()

    for i in range(n):
        row = []
        for j in range(n):
            e = customtkinter.CTkEntry(matrix_frame, 
                                       width=58, 
                                       height=36,
                                       corner_radius=6, 
                                       border_color=BORDER, 
                                       border_width=1,
                                       fg_color=WHITE, 
                                       text_color=DARK,
                                       font=customtkinter.CTkFont(size=12),
                                       justify="center"
            )
            e.grid(row=i, column=j, padx=3, pady=3)
            row.append(e)
        mat_input.append(row)

        # separateur entre A et b
        sep_lbl = customtkinter.CTkLabel(matrix_frame, 
                                         text="│", 
                                         text_color=BORDER,
                                         font=customtkinter.CTkFont(size=18))
        sep_lbl.grid(row=i, column=n, padx=4)

        # vecteur b
        b= customtkinter.CTkEntry(matrix_frame, 
                                  width=58, 
                                  height=36,
                                  corner_radius=6, 
                                  border_color=BORDER,
                                  border_width=1,
                                  fg_color=WHITE, 
                                  text_color=DARK,
                                  font=customtkinter.CTkFont(size=12),
                                  justify="center"
        )
        b.grid(row=i, column=n + 1, padx=3, pady=3)
        vec_input.append(b)

mat_grid(3)


# boutons remplir / aleatoire 
btns= customtkinter.CTkFrame(body, 
                                 fg_color="transparent")
btns.pack(padx=16, pady=(4, 12))

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
        vec_input[i].delete(0, "end")
        vec_input[i].insert(0, str(random.randint(1, 20)))


for txt, cmd in [("Effacer", on_vide), ("Aléatoire", on_aleatoire)]:
    button= customtkinter.CTkButton(btns, 
                            text=txt, 
                            width=100, 
                            height=32,
                            fg_color=LIGHT_BG, 
                            text_color=DARK, 
                            hobr_color=BORDER,
                            border_width=1, 
                            border_color=BORDER,
                            corner_radius=8,
                            font=customtkinter.CTkFont(size=12),
                            command=cmd
    )
    button.pack(side="left", padx=4)

#changer size 
size_row = customtkinter.CTkFrame(body, 
                                  fg_color="transparent")
size_row.pack(padx=16, pady=(0, 10))

lab_size= customtkinter.CTkLabel(size_row, text="Taille  n×n :",
                                 font=customtkinter.CTkFont(size=12), 
                                 text_color=GREY
)
lab_size.pack(side="left", padx=(0, 8))

size_menu = customtkinter.CTkOptionMenu(size_row, 
                                        values=["2", "3", "4", "5", "6"],
                                        width=70, 
                                        height=30, 
                                        corner_radius=6,
                                        fg_color=WHITE, 
                                        text_color=DARK,
                                        button_color=YELLOW, 
                                        button_hobr_color=YELLOW_HVR,
                                        dropdown_fg_color=WHITE, 
                                        dropdown_text_color=DARK,
                                        font=customtkinter.CTkFont(size=12),
                                        command=lambda val: [size.set(int(val)), mat_grid(int(val))]
)
size_menu.set("3")
size_menu.pack(side="left")

sep3= customtkinter.CTkFrame(body, 
                            height=1, 
                            fg_color=BORDER)
sep3.pack(fill="x", padx=16, pady=(4, 10))

#parametres iteratifs 
parametres = customtkinter.CTkFrame(body, 
                                    fg_color="transparent")

titre_p = customtkinter.CTkLabel(parametres, 
                                    text="Paramètres (Itératif)",
                                    font=customtkinter.CTkFont(size=13, weight="bold"), 
                                    text_color=DARK
)
titre_p.pack(anchor="w", padx=0, pady=(0, 6))

param_frame = customtkinter.CTkFrame(parametres, 
                                    fg_color="transparent")
param_frame.pack(anchor="w")

tol=customtkinter.CTkLabel(param_frame, 
                           text="Tolérance",
                            font=customtkinter.CTkFont(size=12), 
                            text_color=DARK)
tol.grid(row=0, column=0, sticky="w", padx=(0,12))

tol_input = customtkinter.CTkEntry(param_frame, 
                                   width=110, 
                                   height=34, 
                                   corner_radius=6,
                                   border_color=BORDER, 
                                   border_width=1, 
                                   fg_color=WHITE, 
                                   text_color=DARK,
                                   font=customtkinter.CTkFont(size=12), 
                                   placeholder_text="0.00001")

tol_input.grid(row=1, column=0, padx=(0, 12), pady=(4, 0))