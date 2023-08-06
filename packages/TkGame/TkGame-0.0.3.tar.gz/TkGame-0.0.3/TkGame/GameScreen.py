from tkinter import *

class GameScreen:
    def __init__(self, master, color="black", title="TkGame - GameScreen", icon="TkGame\\images\\icon.ico"):
        self.master = master
        self.color = color
        self.frame = Frame(master)
        self.frame.pack(fill="both", expand=True)
        self.canvas = Canvas(self.frame)
        self.canvas.pack(fill="both", expand=True)
        self.title = title

        master.title(title)
        self.canvas.config(bg=self.color, highlightthickness=0)
        master.iconbitmap(icon)
        print("GameScreen Created! " +  "Tkinter version: " + str(TkVersion), end="\n\n")

        master.bind("<Escape>", lambda e: master.destroy())
    def destroy(self):
        self.frame.destroy()

    def update(self):
        self.canvas.update()
        print("Screen Updated!")

