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
        command= lambda n= algo: select_algo(n)
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

# partie des champs
saisir = customtkinter.CTkFrame(body, 
                                fg_color=WHITE, 
                                corner_radius=12, 
                                width=295,
                                height=400)
saisir.pack(side="left", fill="y", padx=(0, 8))
saisir.pack_propagate(False)

#titre
title_param= customtkinter.CTkLabel(saisir, 
                       text="Paramètres",
                       font=customtkinter.CTkFont(size=15, weight="bold"), 
                       text_color=DARK
)
title_param.pack(anchor="w", padx=16, pady=(14, 8))

#label pour f(x)
flabel= customtkinter.CTkLabel(saisir, 
                       text="Définir la fonction",
                       font=customtkinter.CTkFont(size=13), 
                       text_color=DARK
)
flabel.pack(anchor="w", padx=16)

#input
inputf = customtkinter.CTkEntry(saisir, 
                                width=263, 
                                height=38, 
                                corner_radius=8,
                                border_color=BORDER, 
                                border_width=1,
                                text_color= DARK,
                                fg_color=WHITE,
                                font=customtkinter.CTkFont(size=12),
                                placeholder_text=" ex: x**3 - 2*x - 5"
)
inputf.pack(padx=16, pady=(3, 12))

#intervalle
lbl_interval = customtkinter.CTkLabel(saisir,
                                       text="Intervalle [a, b]",
                                       font=customtkinter.CTkFont(size=13), 
                                       text_color=DARK)

#frame pour les deux champs
group = customtkinter.CTkFrame(saisir, fg_color="transparent")

#a
a = customtkinter.CTkEntry(group, 
                           placeholder_text="a",
                           width=124, 
                           height=38, 
                           corner_radius=8,
                           border_color=BORDER,
                           text_color= DARK,
                           fg_color=WHITE, 
                           border_width=1, 
                           font=customtkinter.CTkFont(size=12))

#b
b = customtkinter.CTkEntry(group, 
                           placeholder_text="b",
                           width=124, 
                           height=38, 
                           corner_radius=8,
                           border_color=BORDER,
                           text_color= DARK,
                           fg_color=WHITE,
                           border_width=1, 
                           font=customtkinter.CTkFont(size=12))

a.pack(side="left", padx=(0, 6))
b.pack(side="left")

#tolerance
toler = customtkinter.CTkLabel(saisir, 
                               text="Tolérance",
                               font=customtkinter.CTkFont(size=13), 
                               text_color=DARK)
toler.pack(anchor="w", padx=16)

inputtol = customtkinter.CTkEntry(saisir, 
                                  width=263, 
                                  height=38,
                                  corner_radius=8, 
                                  border_color=BORDER,
                                  text_color= DARK,
                                  fg_color=WHITE, 
                                  border_width=1,
                                  font=customtkinter.CTkFont(size=12))
inputtol.pack(padx=16, pady=(3, 12))

#btn de calcule
btn_calc= customtkinter.CTkButton(saisir, 
                                  text="▶   Calculer",
                                  width=263, 
                                  height=44,
                                  fg_color=YELLOW, 
                                  text_color=DARK, 
                                  hover_color=YELLOW_HVR,
                                  font=customtkinter.CTkFont(size=14, weight="bold"),
                                  corner_radius=10
    # command=on_calculer a faire
)
btn_calc.pack(side="bottom", pady=14, padx=16)

#partie resultat 
result = customtkinter.CTkFrame(body, 
                                fg_color=WHITE, 
                                corner_radius=12)
result.pack(side="left", fill="both", expand=True)

#titre 
titreres= customtkinter.CTkLabel(result,
                                text="Résultats",
                                font=customtkinter.CTkFont(size=14, weight="bold"), 
                                text_color=DARK
)
titreres.pack(anchor="w", padx=16, pady=(14, 8))

#fonction pour creer  les lables de le bloc resultat 
def result_block(title, default="—", val_color=DARK, val_size=22):
    f = customtkinter.CTkFrame(result,
                               fg_color="transparent")
    f.pack(anchor="w", padx=16, pady=(0, 10))
    l= customtkinter.CTkLabel(f, 
                              text=title,
                              font=customtkinter.CTkFont(size=11), 
                              text_color=GREY
    )
    l.pack(anchor="w")
    lv = customtkinter.CTkLabel(f, 
                                text=default,
                                font=customtkinter.CTkFont(size=val_size, weight="bold"),
                                text_color=val_color)
    lv.pack(anchor="w")
    return lv

lbl_racine = result_block("Racine trouvée",      "—", GREEN, 20)
lbl_iters  = result_block("Nombre d'itérations", "—", DARK,  24)
lbl_frac   = result_block("Valeur de f(racine)", "—", DARK,  14)

#recommandation message 
RECO = {
    "Dichotomie"  : "Méthode de dichotomie est recommandee pour cette fonction (convergence rapide)",
    "Newton"      : "Méthode de Newton est recommandee pour cette fonction (convergence rapide)",
    "Point fixe"  : "Méthode de Point fixe est recommandee pour cette fonction (convergence rapide)",
}

#recommandation
box = customtkinter.CTkFrame(result, 
                                fg_color=TIP_BG,
                                corner_radius=10, 
                                border_width=1, 
                                border_color=TIP_BORDER)
box.pack(fill="x", padx=16, pady=(4, 8))

rec=customtkinter.CTkLabel(box, 
                       text="💡  Recommandation",
                       font=customtkinter.CTkFont(size=12, weight="bold"), 
                       text_color="#7a6500"
)
rec.pack(anchor="w", padx=10, pady=(8, 2))

lbl_tip = customtkinter.CTkLabel(box,
                                 text=RECO["Dichotomie"],
                                 font=customtkinter.CTkFont(size=11), 
                                 text_color="#7a6500",
                                 justify="left", 
                                 wraplength=190)
lbl_tip.pack(anchor="w", padx=10, pady=(0, 8))

#  a faire
def best_algo():
    return 

def update_reco():
    algo = best_algo()
    lbl_tip.configure(text=RECO.get(algo, ""))

#btn iterations
btn_iter= customtkinter.CTkButton(result, 
                                  text="voir iteration",
                                  width=263, 
                                  height=44,
                                  fg_color=WHITE, 
                                  text_color=DARK, 
                                  hover_color=YELLOW_HVR,
                                  font=customtkinter.CTkFont(size=14, weight="bold"),
                                  corner_radius=10,
                                  border_color= YELLOW,
                                  border_width=1
    # command=tableau des resultats a faire
)
btn_iter.pack(side="left" , pady=10, padx=15)

#btn comparaison
btn_meth= customtkinter.CTkButton(result, 
                                  text="comparer methodes",
                                  width=263, 
                                  height=44,
                                  fg_color=YELLOW, 
                                  text_color=DARK, 
                                  hover_color=YELLOW_HVR,
                                  font=customtkinter.CTkFont(size=14, weight="bold"),
                                  corner_radius=10
    # command=tableau des resultats a faire
)
btn_meth.pack(side="right", pady=10, padx=16)

#partie visaulaisation
visualisation = customtkinter.CTkFrame(win, 
                                       fg_color=WHITE, 
                                       corner_radius=12)
visualisation.pack(fill="both", expand=True, padx=14, pady=(0, 14))

#header
header = customtkinter.CTkFrame(visualisation, 
                                fg_color="transparent")
header.pack(fill="x", padx=14, pady=(10, 0))

#title
vistitle=customtkinter.CTkLabel(header, 
                                text="Visualisation",
                                font=customtkinter.CTkFont(size=13, weight="bold"), 
                                text_color=DARK
)
vistitle.pack(side="left")

#btn sauvgarde grph
btnsauv= customtkinter.CTkButton(header, 
                                 text="⬇  Exporter résultats",
                                 width=160,
                                 height=30,
                                 fg_color=LIGHT_BG, 
                                 text_color=DARK,
                                 hover_color=BORDER,
                                 border_width=1,
                                 border_color=BORDER,
                                 corner_radius=8, 
                                 font=customtkinter.CTkFont(size=11)
    # command=on_exporter a faire
)
btnsauv.pack(side="right")
