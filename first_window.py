import tkinter 
import customtkinter

app=customtkinter.CTk()
app.geometry("1000x500")
app.title("First Window")
app._set_appearance_mode("light")
BlueFrame= customtkinter.CTkFrame(master=app,
                                  height= 900,
                                  width= 200,
                                  fg_color="darkblue")
#put the frame in the let side of the window
BlueFrame.pack(pady=0, padx=0, side="left")
app.mainloop()