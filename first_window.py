import tkinter 
import customtkinter 
from PIL import Image

app=customtkinter.CTk()
app.geometry("1000x500")
app.title("First Window")
app._set_appearance_mode("light")

BlueFrame = customtkinter.CTkFrame( master=app,
                                    height=900,
                                    width=200,
                                    fg_color="darkblue",
                                    corner_radius=0   # makes it like a real sidebar (flat, no rounded edges)
)

# FIX: make it behave like a real left sidebar
BlueFrame.pack(pady=0, padx=0, side="left", fill="y")

image=Image.open("logo.png")
# Convert for CustomTkinter
img = customtkinter.CTkImage(light_image=image, dark_image=image, size=(200, 200))

# Display in label
label = customtkinter.CTkLabel(BlueFrame, image=img, text="")
label.pack(pady=20)

label_title= customtkinter.CTkLabel(master=BlueFrame,
                                    text="Anum",
                        
                                    font=customtkinter.CTkFont(size=20, weight="bold"))
label_title.pack(pady=10, padx=10)

label_sub_title= customtkinter.CTkLabel(master=BlueFrame,
                                    text="Bib",
                                    font=customtkinter.CTkFont(size=15, weight="bold"),
                                    text_color="yellow")
label_sub_title.pack(pady=9, padx=3, fill="x")

btn_home= customtkinter.CTkButton(master=BlueFrame,
                                    text=" 🏠 Accueil",
                                    width= 200,
                                    height= 40,
                                    hover_color="yellow")
btn_home.pack(pady=10, padx=10, fill="x")
btn1= customtkinter.CTkButton(master=BlueFrame,
                                    text=" Axe 1",
                                    width= 200,
                                    height= 40,
                                    hover_color="yellow")
btn1.pack(pady=10, padx=10, fill="x")
btn2= customtkinter.CTkButton(master=BlueFrame,
                                    text=" Axe 2",
                                    width= 200,
                                    height= 40,
                                    hover_color="yellow")
btn2.pack(pady=10, padx=10, fill="x")
btn3= customtkinter.CTkButton(master=BlueFrame,
                                    text="Axe 3",
                                    width= 200,
                                    height= 40,
                                    hover_color="yellow")
btn3.pack(pady=10, padx=10, fill="x")

def change_mode():
    mode = customtkinter.get_appearance_mode()
    if mode == "Light":
        customtkinter.set_appearance_mode("Dark")
    else:
        customtkinter.set_appearance_mode("Light")

btn_mode = customtkinter.CTkButton(master=BlueFrame,
                                    text="Changer le mode",
                                    width= 200,
                                    height= 40,
                                    hover_color="yellow",
                                    command=change_mode)
btn_mode.pack(pady=100, padx=10)
app.mainloop()