import tkinter
import customtkinter
from PIL import Image

app = customtkinter.CTk()
app.geometry("1050x680")
app.title("Numerical Lab")
app._set_appearance_mode("light")

#start by the left frame
left_frame = customtkinter.CTkFrame(master=app,
                                    width=210,
                                    fg_color="#0d1b2e",
                                    corner_radius=0
)

left_frame.pack(pady=0, padx=0, side="left", fill="y")
left_frame.pack_propagate(False)   # frame ma yetherekch

#logo
LogoFrame = customtkinter.CTkFrame(master=left_frame,
                                    fg_color="transparent",
)
LogoFrame.pack(pady=(20, 5), padx=10, fill="x")

#image
image_logo = Image.open("logo.png")
img_logo = customtkinter.CTkImage(light_image=image_logo,
                                  dark_image=image_logo,
                                  size=(80, 80)
)

label_logo_img = customtkinter.CTkLabel(master=LogoFrame,
                                        image=img_logo,
                                        text=""
)
label_logo_img.pack(side="left", padx=(0, 10))

label_logo_text = customtkinter.CTkLabel(master=LogoFrame,
                                        text="Numerical\nLab",
                                        font=customtkinter.CTkFont(size=15, weight="bold"),
                                        text_color="white",
                                        justify="left"
)
label_logo_text.pack(side="left")

# add a line separator
sep1 = customtkinter.CTkFrame(
    master=left_frame,
    height=1,
    fg_color="#1e3050"
)
sep1.pack(fill="x", padx=10, pady=(5, 10)) #pady=(5, 10) means 5 pixels above and 10 pixels below the separator

#navigation buttons for the 3 axes
def make_nav_btn(icon, main_text, sub_text="", active=False): # active is a boolean that indicates if this button is the currently active page
    txt=""
    if active:
        bg = "#f5c518"  
    else: 
        bg = "transparent"

    if active:
        txt = "#0d1b2e"  
    else: 
        txt = "white"

    hover = "#f5c518" 

    # in 
    BtnFrame = customtkinter.CTkFrame(master=left_frame,
                                    fg_color=bg,
                                    corner_radius=8,
                                    cursor="hand2"
    )
    BtnFrame.pack(pady=2, padx=10, fill="x")

    # Icon + main text on one row
    RowFrame = customtkinter.CTkFrame(master=BtnFrame,
                                    fg_color="transparent"
    )
    RowFrame.pack(fill="x", padx=8, pady=(6, 0 if sub_text else 6))

    label_icon = customtkinter.CTkLabel(master=RowFrame,
                                        text=icon,
                                        font=customtkinter.CTkFont(size=14),
                                        text_color=txt,
                                        width=22
    )
    label_icon.pack(side="left")

    label_main = customtkinter.CTkLabel(
        master=RowFrame,
        text=main_text,
        font=customtkinter.CTkFont(size=13, weight="bold" if active else "normal"),
        text_color=txt
    )
    label_main.pack(side="left", padx=(4, 0))

    # Optional subtitle below
    if sub_text:
        label_sub = customtkinter.CTkLabel(
            master=BtnFrame,
            text=sub_text,
            font=customtkinter.CTkFont(size=10),
            text_color="#0d1b2e" if active else "#8899aa"
        )
        label_sub.pack(anchor="w", padx=34, pady=(0, 6))

    return BtnFrame


btn_home  = make_nav_btn("🏠", "Accueil", active=True)
btn_axe1  = make_nav_btn("⊘", "Axe 1", sub_text="Fonctions non linéaires")
btn_axe2  = make_nav_btn("▦", "Axe 2", sub_text="Systèmes linéaires")
btn_axe3  = make_nav_btn("📈", "Axe 3", sub_text="Interpolation &\nApproximation")

# ── Second group of nav items ─────────────────────────────────────────────────
# sep2 = customtkinter.CTkFrame(master=left_frame, height=1, fg_color="#1e3050")
# sep2.pack(fill="x", padx=10, pady=(8, 8))

# btn_comp  = make_nav_btn(left_frame, "⇌",  "Comparaison")
# btn_hist  = make_nav_btn(left_frame, "◷",  "Historique")
# btn_aide  = make_nav_btn(left_frame, "?",  "Aide / Guide")
# btn_param = make_nav_btn(left_frame, "⚙",  "Paramètres")
# btn_about = make_nav_btn(left_frame, "ℹ",  "À propos")

# ── Mode toggle — pinned to bottom ────────────────────────────────────────────
def change_mode():
    mode = customtkinter.get_appearance_mode()
    if mode == "Light":
        customtkinter.set_appearance_mode("Dark")
    else:
        customtkinter.set_appearance_mode("Light")

btn_mode = customtkinter.CTkButton(master=left_frame,
                                   text="☀  Mode             ›",
                                   width=190,
                                   height=36,
                                   fg_color="transparent",
                                   text_color="#8899aa",
                                   hover_color="#1e3050",
                                   anchor="w", # text aligned to the left
                                   corner_radius=8,
                                   command=change_mode
)
btn_mode.pack(side="bottom", pady=15, padx=10, fill="x")

sep2 = customtkinter.CTkFrame(master=left_frame, height=1, fg_color="#1e3050")
sep2.pack(side="bottom", fill="x", padx=10, pady=(0, 2))