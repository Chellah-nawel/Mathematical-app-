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
