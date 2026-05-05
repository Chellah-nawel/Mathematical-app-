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