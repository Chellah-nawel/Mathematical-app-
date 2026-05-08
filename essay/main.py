import customtkinter

import axe3


# ─── fenetre principale unique ─────────────────────────────────────────────────
app = customtkinter.CTk()
app.geometry("1050x680")
app.title("Numerical Lab")
app._set_appearance_mode("light")

def navigate(page):
    for widget in app.winfo_children():
        widget.destroy()

    pages = {

        "axe3"    : lambda: axe3.show(app, navigate),

    }
    pages[page]()

# page de demmarage
navigate("axe3")
app.mainloop()