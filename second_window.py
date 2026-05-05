import customtkinter

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