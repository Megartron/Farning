import tkinter
import random
import math
from tkinter import *



class Zeichenfeld():
    def __init__(self, root):
        self.root = root
        self.canvas = tkinter.Canvas(root, width=520, height=520, bg="black")
        

        self.felder_koordinaten = {}
        self.highlighted = [0 for _ in range(25)]

        self.canvas.bind("<Button-1>", self.markfield)
        self.spielfeld_zeichnen()
        self.canvas.pack(expand=True)

    def markfield(self, event):
        x, y = ((event.y - 10) // 100, (event.x - 10) // 100)
        x_px, y_px = self.get_coords((x, y))
        self.canvas.create_rectangle(x_px - 50, y_px - 50, x_px + 50, y_px + 50, fill="#FFFFFF")
        if self.highlighted[x + y * 5] == 1:
            self.highlighted[x + y * 5] = 0
        else:
            self.highlighted[x + y * 5] = 1

    def get_coords(self, coords: tuple) -> tuple:
        return self.felder_koordinaten[coords]

    def highlight_fields(self):
        for i in range(len(self.highlighted)):
            if self.highlighted[i] == 1:
                x, y = self.get_coords((i % 5, i // 5))
                self.canvas.create_rectangle(x - 50, y - 50, x + 50, y + 50, fill="#FFFFFF")

    # Spielfeld erschaffen
    def spielfeld_zeichnen(self) -> None:
        for i in range(6):
            x = 10 + i * 100
            y = 10 + i * 100
            self.canvas.create_line(x, 10, x, 510, fill="white")
            self.canvas.create_line(10, y, 510, y, fill="white")
        
            if i < 5:
                for j in range(5):
                    self.felder_koordinaten[(i, j)] = (60 + j * 100, 60 + i * 100)
    
    def update(self) -> None:
        self.canvas.delete("all")
        self.spielfeld_zeichnen()
        self.highlight_fields()
        self.root.after(100, self.update)


if __name__ == "__main__":

    root = tkinter.Tk()
    z = Zeichenfeld(root)
    z.update()

    root.mainloop()


