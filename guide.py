import customtkinter
import tkinter as tk

YELLOW     = "#f5c518"
YELLOW_HVR = "#e6b800"
LIGHT_BG   = "#f4f6f9"
WHITE      = "#ffffff"
DARK       = "#0d1b2e"
GREY       = "#777777"
BORDER     = "#e0e0e0"
TIP_BORDER = "#f5e600"
TIP_BG     = "#fffde7"




AIDE_CONTENT = {
    "1. Résolution non linéaire": {
        "methods": {
            "Méthode de Dichotomie": {
                "desc"   : "La méthode de dichotomie permet de trouver une racine d'une fonction continue sur [a, b] en divisant l'intervalle en deux à chaque étape.",
                "formula": "xmid = (a + b) / 2",
                "when"   : ["La fonction est continue sur [a, b]"],
            },
            "Méthode de Newton": {
                "desc"   : "La méthode de Newton permet de trouver une racine d'une fonction en utilisant sa dérivée.",
                "formula": "x(n+1) = xn - f(xn) / f'(xn)",
                "when"   : ["f(a)*f(b)<0", "f'(x)<>0 pour toute x dans [a, b]","f''(x) garde un signe constant dans [a, b]","|f'(x)|/|f(x)|<=b-a"],
            },
            "Méthode du Point fixe": {
                "desc"   : "Reformuler f(x)=0 en x = g(x) et itérer jusqu'à convergence.",
                "formula": "x(n+1) = g(xn)",
                "when"   : ["g est stable sur l'intervalle [a, b]", "g est contractante sur l'intervalle [a, b]"],
            },
        }
    },
    "2. Systèmes linéaires": {
        "methods": {
            "Gauss": {
                "desc"   : "Méthode directe qui permit de resoudre un systeme avec la méthode de triangularisation.",
                "formula": "Triangularisation de A",
                "when"   : ["Solution unique (determinant <> 0)"],
            },
            "LU": {
                "desc"   : "methode directe qui sert a décompose A = LU (triangulaire inférieure × supérieure).",
                "formula": "Ly = b  puis  Ux = y",
                "when"   : ["Plusieurs systèmes avec la même matrice A"],
            },
            "Gauss-Seidel": {
                "desc"   : "Méthode itérative qui permet de resoudre un systeme lineaire en utilisant une  suite iterative",
                "formula": "x^(k+1) = (D-E)-1 *F *X^k +(D-E)-1 *b",
                "when"   : ["Matrice DDS", "Matrice symétrique définie positive", "Rayon spectrale de GS=((D-E)-1 *F) <1"],
            },
            "Jacobi": {
                "desc"   : "Méthode itérative qui permet de resoudre un systeme lineaire en utilisant une  suite iterative.",
                "formula": "x^(k+1) = D-1 *(E+F) *X^k + D-1 *b",
                "when"   : ["Matrice DDS", "Rayon spectrale de J=(D-1 *(E+F)) <1"],
            },
        }
    },
    "3. Interpolation & Approximation": {
        "methods": {
            "Lagrange": {
                "desc"   : "Construit un polynôme passant exactement par n points donnés.",
                "formula": "P(x) = Σ yi · Li(x)",
                "when"   : ["Petit nombre de points", "Points bien répartis"],
            },
            "Newton": {
                "desc"   : "Construit le polynôme interpolateur via les différences divisées, permettant d'ajouter des points sans tout recalculer.",
                "formula": "P(x) = f[x0] + f[x0,x1](x-x0) + f[x0,x1,x2](x-x0)(x-x1) + …",
                "when"   : ["Ajout progressif de points", "Calcul incrémental efficace"],
            },
            "Moindres carrés": {
                "desc"   : "Trouve le polynôme qui minimise la somme des erreurs au carré.",
                "formula": "min Σ (yi - P(xi))^2",
                "when"   : ["Données bruitées ou expérimentales", "Degré ne depend pas de nombre de point"],
            },
            "Descente de Gradient": {
                "desc"   : "un algorithme iterative qui consiste a minimiser une fonction réelle différencielle",
                "formula": "x^(k+1) = X^k + pas* nabla(xk)",
                "when"   : [],
            },
        }
    },
    "4. Questions fréquentes": {
        "methods": {
            "Comment saisir une fonction ?": {
                "desc"   : "Utilisez la syntaxe Python : x**2, sin(x), exp(x), log(x). Exemples : x**3 - 2*x - 5, sin(x) - x/2.",
                "formula": "",
                "when"   : [],
            },
            "Que faire si l'algorithme diverge ?": {
                "desc"   : "Essayez un autre algorithme ou changez les paramètres initiaux.",
                "formula": "",
                "when"   : [],
            },
            "Comment exporter les résultats ?": {
                "desc"   : "Cliquez sur « Exporter résultats » dans chaque fenêtre, pour génère un fichier PNG.",
                "formula": "",
                "when"   : [],
            },
        }
    },
}

win = customtkinter.CTk()
win.geometry("920x700")
win.title("Aide / Guide")
win.configure(fg_color=LIGHT_BG)
win._set_appearance_mode("light")

#header
header_bar = customtkinter.CTkFrame(win, 
                                    fg_color=YELLOW, 
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
                                font=customtkinter.CTkFont(size=20), corner_radius=8
)
retour.pack(side="left", padx=(12, 6), pady=8)

aide_lab=customtkinter.CTkLabel(header_bar,
                                text="Aide / Guide",
                                font=customtkinter.CTkFont(size=17, weight="bold"),
                       text_color=DARK
)
aide_lab.pack(side="left")

#aide body
aide_frame = customtkinter.CTkFrame(win, 
                                    fg_color="transparent")
aide_frame.pack(fill="both", expand=True, padx=14, pady=(10, 14))

# sidebar
sidebar = customtkinter.CTkScrollableFrame(aide_frame, 
                                           fg_color=WHITE, 
                                           corner_radius=12, 
                                           width=220)
sidebar.pack(side="left", fill="y", padx=(0, 8))

section_btns = {}
current_section = tk.StringVar(value=list(AIDE_CONTENT.keys())[0])
current_method  = tk.StringVar(value="")
lab_sec=customtkinter.CTkLabel(sidebar, 
                               text="Sections",
                                font=customtkinter.CTkFont(size=13, weight="bold"), text_color=DARK
)
lab_sec.pack(anchor="w", padx=14, pady=(14, 6))
#  contenu
content = customtkinter.CTkScrollableFrame(aide_frame, 
                                           fg_color=WHITE, 
                                           corner_radius=12)
content.pack(side="left", fill="both", expand=True)

def render_method(section_name, method_name):
    for w in content.winfo_children():
        w.destroy()

    data = AIDE_CONTENT[section_name]["methods"][method_name]

    # titre metho
    met_label=customtkinter.CTkLabel(content, 
                                     text=method_name,
                                     font=customtkinter.CTkFont(size=18, weight="bold"), 
                                     text_color=DARK
    )
    met_label.pack(anchor="w", padx=20, pady=(16, 6))

    # desc
    desc= customtkinter.CTkLabel(content, 
                           text=data["desc"],
                            font=customtkinter.CTkFont(size=13), 
                            text_color=DARK,
                            wraplength=560, 
                            justify="left"
    )
    desc.pack(anchor="w", padx=20, pady=(0, 12))

    # formule
    if data["formula"]:
        form_lab= customtkinter.CTkLabel(content, 
                                         text="Formule :",
                                         font=customtkinter.CTkFont(size=13, weight="bold"), 
                                         text_color=DARK
        )
        form_lab.pack(anchor="w", padx=20, pady=(0, 4))

        formula_box = customtkinter.CTkFrame(content, 
                                             fg_color=LIGHT_BG, 
                                             corner_radius=8,
                                            border_width=1, border_color=BORDER
        )
        formula_box.pack(anchor="w", padx=20, pady=(0, 14))
        formule=customtkinter.CTkLabel(formula_box, 
                                       text=data["formula"],
                                        font=customtkinter.CTkFont(size=14, weight="bold"), text_color=DARK
        )
        formule.pack(padx=16, pady=10)

    # Quand l'utiliser
    if data["when"]:
        use_lab=customtkinter.CTkLabel(content, 
                                       text="Quand l'utiliser ?",
                                        font=customtkinter.CTkFont(size=13, weight="bold"), text_color=DARK
        )
        use_lab.pack(anchor="w", padx=20, pady=(0, 6))

        for item in data["when"]:
            row = customtkinter.CTkFrame(content, 
                                         fg_color="transparent")
            row.pack(anchor="w", padx=20, pady=2)

            item_lab=customtkinter.CTkLabel(row, text=item,
                                   font=customtkinter.CTkFont(size=13), text_color=DARK)
            item_lab.pack(side="left")

#mise a jour des btns  de sidebar selectionner
def select_section(section_name):
    current_section.set(section_name)
    for name, btn in section_btns.items():
            if name == section_name:
                btn.configure(fg_color=YELLOW, font=customtkinter.CTkFont(size=14, weight="bold") )
            else: 
                btn.configure(fg_color=WHITE, font=customtkinter.CTkFont(size=13, weight="normal"))

    methods = list(AIDE_CONTENT[section_name]["methods"].keys())
    if methods:
        current_method.set(methods[0])
        render_method(section_name, methods[0])
    rebuild_method_list(section_name)

# selecteur de methode dans la sidebar
method_list_frame = customtkinter.CTkFrame(sidebar, 
                                           fg_color="transparent")
#pour refresh des btn apres clique
def rebuild_method_list(section_name):
    for w in method_list_frame.winfo_children():
        w.destroy()
    for m in AIDE_CONTENT[section_name]["methods"].keys():
        btn = customtkinter.CTkButton(method_list_frame, 
                                      text=m,
                                        width=190, 
                                        height=32, 
                                        anchor="w",
                                        fg_color=WHITE, 
                                        text_color=GREY, 
                                        hover_color=LIGHT_BG,
                                        border_width=0, 
                                        corner_radius=6,
            font=customtkinter.CTkFont(size=12),
            command=lambda n=section_name, mn=m: render_method(n, mn)
        )
        btn.pack(padx=8, pady=2)


for sec in AIDE_CONTENT.keys():
    b = customtkinter.CTkButton(sidebar, text=sec, width=192, height=38,
        fg_color=WHITE, text_color=DARK, hover_color=YELLOW_HVR,
        anchor="w", corner_radius=8, border_width=1, border_color=BORDER,
        font=customtkinter.CTkFont(size=13, weight="normal"),
        command=lambda s=sec: select_section(s)
    )
    b.pack(padx=8, pady=3)
    section_btns[sec] = b

f=customtkinter.CTkFrame(sidebar, height=1, fg_color=BORDER)
f.pack(fill="x", padx=8, pady=(8, 6))
method_list_frame.pack(fill="x")

# Afficher la premiere sec par defaut
first_sec = list(AIDE_CONTENT.keys())[0]
select_section(first_sec)

win.mainloop()