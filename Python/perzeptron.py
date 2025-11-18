import tkinter
import random
import math
from tkinter import *
import csv
import ast



class Zeichenfeld():
    def __init__(self, root):
        self.root = root
        self.canvas = tkinter.Canvas(root, width=520, height=520, bg="black")
        

        self.felder_koordinaten = {}
        self.highlighted = [0 for _ in range(25)]
        self.mouse1_pressed = False
        self.mouse2_pressed = False
        self.mouse_pos = ()
        self.previous_action = ((), ())
        self.datensatz = ()

        self.canvas.bind("<ButtonPress-1>", lambda event: self.pressed(1))
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.released(1))
        self.canvas.bind("<ButtonPress-3>", lambda event: self.pressed(2))
        self.canvas.bind("<ButtonRelease-3>", lambda event: self.released(2))
        self.canvas.bind("<Motion>", self.track_mouse)
        self.entry = tkinter.Entry(root)
        self.create = tkinter.Button(root, text="hinzufuegen", command=self.zu_datensatz_hinzufügen)
        self.spielfeld_zeichnen()
        self.canvas.pack(expand=True)
        self.entry.pack()
        self.create.pack()

    def track_mouse(self, event):
        self.mouse_pos = (event.x, event.y)

    def pressed(self, button):
        if button == 1:
            self.mouse1_pressed = True
        else:
            self.mouse2_pressed = True
    
    def released(self, button):
        if button == 1:
            self.mouse1_pressed = False
        else:
            self.mouse2_pressed = False

    def markfield(self):
        mouse_x, mouse_y = self.mouse_pos
        x, y = ((mouse_y - 10) // 100, (mouse_x - 10) // 100)
        if ((self.previous_action[0] == (x, y) and self.previous_action[1] == (self.mouse1_pressed, self.mouse2_pressed)) or x > 4 or y > 4):
            return
        self.previous_field = ((x, y), (self.mouse1_pressed, self.mouse2_pressed))
        x_px, y_px = self.get_coords((x, y))
        if self.mouse1_pressed:
            self.canvas.create_rectangle(x_px - 50, y_px - 50, x_px + 50, y_px + 50, fill="#FFFFFF")
            self.highlighted[x + y * 5] = 1
        elif self.mouse2_pressed:
            self.highlighted[x + y * 5] = 0

    def get_coords(self, coords: tuple) -> tuple:
        return self.felder_koordinaten[coords]

    def highlight_fields(self):
        for i in range(len(self.highlighted)):
            if self.highlighted[i] == 1:
                x, y = self.get_coords((i % 5, i // 5))
                self.canvas.create_rectangle(x - 50, y - 50, x + 50, y + 50, fill="#FFFFFF")
    
    def zu_datensatz_hinzufügen(self):
        value = self.entry.get()
        y = [0 for _ in range(10)]
        try:
            y[int(value)] = 1
            self.datensatz = (tuple(self.highlighted), tuple(y))
            print("neuer Datensatz:", self.datensatz)
            self.entry.delete(0, tkinter.END)
            self.highlighted = [0 for _ in range(25)]
            self.in_datei_schreiben(self.datensatz)
        except (ValueError, IndexError):
            print("Please enter a number from 0 to 9 as solution")
    
    def in_datei_schreiben(self, datensatz):
        with open("Zahlenerkennen/datensatz.csv", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                row_tuple = (ast.literal_eval(row[0]), ast.literal_eval(row[1]))
                if row_tuple == datensatz:
                    return

        with open("Zahlenerkennen/datensatz.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(datensatz)
            print("successfully written into file")

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
        if self.mouse1_pressed or self.mouse2_pressed:
            self.markfield()
        self.highlight_fields()
        self.root.after(10, self.update)


if __name__ == "__main__":

    root = tkinter.Tk()
    z = Zeichenfeld(root)
    z.update()

    root.mainloop()
