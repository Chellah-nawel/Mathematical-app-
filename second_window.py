import customtkinter
import tkinter as tk

#identifier la palette de couleurs utilisée dans l'application
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

# cree la fenetre principale
win = customtkinter.CTk()
win.geometry("1080x700")
win.title("Axe 1 — Fonctions non linéaires")
win.configure(fg_color=LIGHT_BG)
win._set_appearance_mode("light")

#create the top
header = customtkinter.CTkFrame(win, 
                                fg_color=WHITE, 
                                corner_radius=0, 
                                height=54)
header.pack(fill="x")
header.pack_propagate(False)

#btn retour arrière
retour= customtkinter.CTkButton( header, 
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

#title
title= customtkinter.CTkLabel(header, 
                       text="Axe 1 : Fonctions non linéaires",
                        font=customtkinter.CTkFont(size=17, weight="bold"), 
                        text_color=DARK
)
title.pack(side="left")

#frame principale
body = customtkinter.CTkFrame(win, fg_color="transparent")
body.pack(fill="x", padx=14, pady=(10, 8))

#frame des algorithmes et opérations
left_col = customtkinter.CTkScrollableFrame(body, 
                                  fg_color=WHITE, 
                                  corner_radius=12, 
                                  width=186)
left_col.pack(side="left", fill="y", padx=(0, 8))

#les titres
title_algo= customtkinter.CTkLabel(left_col, 
                                   text="Algorithmes",
                                    font=customtkinter.CTkFont(size=13, weight="bold"),
                                    text_color=DARK
)
title_algo.pack(anchor="w", padx=14, pady=(14, 6))

#declarer les variables a utiliser
algo_btns    = {} # il sert a garder une reference vers les boutons algo pour pouvoir les mettre a jour lors de la selection
op_btns      = {}
current_sel  = tk.StringVar() #il contient l'algo ou l'pt selectionne
current_mode = tk.StringVar(value="algo")  #algo pour les algos, op pour les operations 

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
    #il y aura d'autres fonctions ca depend la logique

#creation des bouttons pour les algorithmes
for algo in ["Dichotomie", "Newton", "Point fixe"]:
    b = customtkinter.CTkButton(left_col, 
                                text=algo, 
                                width=158, 
                                height=38,
                                fg_color= WHITE,
                                text_color=DARK, 
                                hover_color=YELLOW_HVR,
                                anchor="w", 
                                corner_radius=8,
                                border_width=1,
                                border_color=BORDER,
                                font=customtkinter.CTkFont(size=13, weight="normal"),
        command= select_algo(algo)
    )
    b.pack(padx=14, pady=3)
    algo_btns[algo] = b #on les ajoute dans la liste des btn

#separateur
sep= customtkinter.CTkFrame(left_col, 
                            height=1, 
                            fg_color=BORDER)

sep.pack(fill="x", padx=14, pady=(12, 10))

#section des options
title_opt= customtkinter.CTkLabel(left_col, 
                                  text="Opérations sur\nles fonctions",
                                  font=customtkinter.CTkFont(size=13, weight="bold"),
                                  text_color=DARK, 
                                  justify="left"
)
title_opt.pack(anchor="w", padx=14, pady=(0, 6))

#pour options
def select_op(name):
    current_sel.set(name)
    current_mode.set("op")
    refresh_op_btns()
    # on ajoute d'atres fonctions

#options
for op in ["Dérivée", "Continuité", "Table de variation", "Signe de f(x)"]:
    b = customtkinter.CTkButton(left_col, 
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