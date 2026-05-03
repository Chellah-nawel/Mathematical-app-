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

#changer mode
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

#main
main_frame = customtkinter.CTkFrame(master=app,
                                    fg_color="#f4f6f9",
                                    corner_radius=0
)
main_frame.pack(side="left", fill="both", expand=True)

#top bar
top = customtkinter.CTkFrame(master=main_frame,
                                fg_color="#f4f6f9",
                                height=52,
                                corner_radius=0
)
top.pack(fill="x")
top.pack_propagate(False) #fixed

label_page_title = customtkinter.CTkLabel(master=top,
                                        text="Accueil",
                                        font=customtkinter.CTkFont(size=16, weight="bold"),
                                        text_color="#0d1b2e"
)
label_page_title.pack(side="left", padx=25, pady=12)

# "Guide rapide" yellow pill button
btn_guide = customtkinter.CTkButton(master=top,
                                    text="⚡  Guide rapide",
                                    width=140,
                                    height=34,
                                    fg_color="#f5c518",
                                    text_color="#0d1b2e",
                                    hover_color="#e6b800",
                                    font=customtkinter.CTkFont(size=12, weight="bold"),
                                    corner_radius=20
)
btn_guide.pack(side="right", padx=(5, 8), pady=9)

#introduction
intro = customtkinter.CTkFrame(master=main_frame,
                               fg_color="white",
                               corner_radius=12,
                               height=165
)
intro.pack(fill="x", padx=20, pady=(15, 10))
intro.pack_propagate(False)

#text block
left_text = customtkinter.CTkFrame(master=intro, 
                                   fg_color="transparent"
)
left_text.pack(side="left", padx=25, pady=15, fill="y")

label_welcome = customtkinter.CTkLabel(master=left_text,
                                        text="Bienvenue dans",
                                        font=customtkinter.CTkFont(size=15),
                                        text_color="#555"
)
label_welcome.pack(anchor="w")

label_app_name = customtkinter.CTkLabel(master=left_text,
                                        text="Numerical Lab",
                                        font=customtkinter.CTkFont(size=32, weight="bold"),
                                        text_color="#0d1b2e"
)
label_app_name.pack(anchor="w")

label_app_sub = customtkinter.CTkLabel(master=left_text,
                                        text="Votre outil interactif pour l'analyse numérique",
                                        font=customtkinter.CTkFont(size=12),
                                        text_color="#888"
)
label_app_sub.pack(anchor="w", pady=(4, 0))

#graph image
graph = customtkinter.CTkFrame(master=intro, 
                               fg_color="transparent"
)
graph.pack(side="right", padx=20, pady=10)

image_graph = Image.open("graphe.png")
img_graph = customtkinter.CTkImage(size=(240, 130))
label_graph = customtkinter.CTkLabel(master=graph, image=img_graph, text="")
label_graph.pack()
#central cards for axes
cards = customtkinter.CTkFrame(master=main_frame, 
                               fg_color="transparent"
)
cards.pack(fill="both", expand=True, padx=20, pady=(0, 5))

#we use a function to create each card to avoid code repetition
def make_axis_card(icon_file, title, subtitle, description, btn_color, hover, bg_color):
    carte = customtkinter.CTkFrame(master=cards,
                                   fg_color=bg_color,
                                   corner_radius=12,
                                   border_width=1,
                                   border_color="#e8e8e8"
    )
    carte.pack(side="left", fill="both", expand=True, padx=6)

    # Icon image
    img_raw = Image.open(icon_file)
    img_ctk = customtkinter.CTkImage(light_image=img_raw,
                                    dark_image=img_raw,
                                    size=(100, 100)
    )
    lbl_icon = customtkinter.CTkLabel(master=carte, image=img_ctk, text="")
    lbl_icon.pack(expand=True)

    # card body
    body = customtkinter.CTkFrame(master=carte, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=12, pady=8)

    lbl_title = customtkinter.CTkLabel( master=body,
                                        text=title,
                                        font=customtkinter.CTkFont(size=25, weight="bold"),
                                        text_color="#0d1b2e"
    )
    lbl_title.pack(anchor="w")

    lbl_sub = customtkinter.CTkLabel(master=body,
                                     text=subtitle,
                                     font=customtkinter.CTkFont(size=18, weight="bold"),
                                     text_color="#0d1b2e"
    )
    lbl_sub.pack(anchor="w", pady=(10, 5))

    lbl_desc = customtkinter.CTkLabel(master=body,
                                      text=description,
                                      font=customtkinter.CTkFont(size=15),
                                      text_color="#666",
                                      justify="left",
                                      wraplength=190
    )
    lbl_desc.pack(anchor="w")

    # Arrow button — bottom right
    btn_arrow = customtkinter.CTkButton(master=body, 
                                        text="→",
                                        width=36,
                                        height=36,
                                        fg_color=btn_color,
                                        text_color="white",
                                        hover_color=hover,
                                        font=customtkinter.CTkFont(size=18),
                                        corner_radius=50
    )
    btn_arrow.pack(pady=(50, 4), anchor= tkinter.CENTER)

    return carte


# axe 1
make_axis_card("fx.png", "Axe 1", "Fonctions non linéaires", "Résolution d'équations non linéaires et analyse de fonctions.","#f5c518", "#e6b800", "#ece8d8")

# axe 2
make_axis_card("matrix.png", "Axe 2", "Systèmes linéaires", "Résolution de systèmes linéaires directs et itératifs.", "#4285f4", "#2a6dd9", "#cad9f3")

# axe 3
make_axis_card("scatter.png", "Axe 3","Interpolation & Approximation", "Interpolation polynomiale, approximation et descente de gradient.", "#34a853", "#2a8a43", "#cdf1d7")

app.mainloop()