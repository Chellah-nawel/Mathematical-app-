import customtkinter
import acceuille
import axe1
import axe2
import axe3
import guide

# ─── fenetre principale unique ─────────────────────────────────────────────────
app = customtkinter.CTk()
app.geometry("1050x680")
app.title("Numerical Lab")
app._set_appearance_mode("light")

def navigate(page):
    for widget in app.winfo_children():
        widget.destroy()

    pages = {
        "accueil" : lambda: acceuille.show(app, navigate),
        "axe1"    : lambda: axe1.show(app, navigate),
        "axe2"    : lambda: axe2.show(app, navigate),
        "axe3"    : lambda: axe3.show(app, navigate),
        "guide"   : lambda: guide.show(app, navigate),
    }
    pages[page]()

# page de demmarage
navigate("accueil")
app.mainloop()