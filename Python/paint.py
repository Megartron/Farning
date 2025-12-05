
import tkinter
import random
import math
from tkinter import *
import csv
import ast
import copy
import re

class Zeichenfeld():
    def __init__(self, root, resolution):
        self.root = root
        self.canvas = tkinter.Canvas(root, width=520, height=620, bg="black")
        
        self.res = resolution
        self.dis = round(500/self.res)
        self.felder_koordinaten = {}
        self.highlighted = [0 for _ in range(resolution**2)]
        self.mouse1_pressed = False
        self.mouse2_pressed = False
        self.mouse_pos = ()
        self.previous_action = ((), ())
        self.datensatz = ()
        self.estimate = ()

        self.canvas.bind("<ButtonPress-1>", lambda event: self.pressed(1))
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.released(1))
        self.canvas.bind("<ButtonPress-3>", lambda event: self.pressed(2))
        self.canvas.bind("<ButtonRelease-3>", lambda event: self.released(2))
        self.canvas.bind("<Motion>", self.track_mouse)
        self.entry = tkinter.Entry(root, background="red")
        self.create = tkinter.Button(root, text="hinzufuegen", command=self.zu_datensatz_hinzufügen)
        self.check = tkinter.Button(root, text="erkennen", command=self.erkennen)
        self.spielfeld_zeichnen()
        self.canvas.pack(expand=True)
        self.entry.pack()
        self.create.pack()
        self.check.pack()

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
        x, y = ((mouse_y - 10) // self.dis, (mouse_x - 10) // self.dis)
        if ((self.previous_action[0] == (x, y) and self.previous_action[1] == (self.mouse1_pressed, self.mouse2_pressed)) or 
            x > self.res - 1 or y > self.res - 1 or x < 0 or y < 0):
            return
        self.previous_field = ((x, y), (self.mouse1_pressed, self.mouse2_pressed))
        x_px, y_px = self.get_coords((x, y))
        if self.mouse1_pressed:
            self.canvas.create_rectangle(x_px - round(self.dis/2), y_px - round(self.dis/2), x_px + round(self.dis/2), y_px + round(self.dis/2), fill="#FFFFFF")
            self.highlighted[x + y * self.res] = 1
        elif self.mouse2_pressed:
            self.highlighted[x + y * self.res] = 0

    def get_coords(self, coords: tuple) -> tuple:
        return self.felder_koordinaten[coords]

    def highlight_fields(self):
        for i in range(len(self.highlighted)):
            if self.highlighted[i] == 1:
                x, y = self.get_coords((i % self.res, i // self.res))
                self.canvas.create_rectangle(x - round(self.dis/2), y - round(self.dis/2), x + round(self.dis/2), y + round(self.dis/2), fill="#FFFFFF")
    
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
        with open("netzwerk/datensatz.csv", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                row_tuple = (ast.literal_eval(row[0]), ast.literal_eval(row[1]))
                if row_tuple == datensatz:
                    return

        with open("netzwerk/datensatz.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(datensatz)  
            print("successfully written into file")
    
    def read_nth_row(self, filename, n):
        with open(filename, newline="") as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == n:   # zero-based index
                    return row
        return None  # if n is out of range

    def erkennen(self):
        value = self.entry.get()

        result = self.read_nth_row("netzwerk/training_results.csv", int(value))
        if result == None:
            print("Please enter a valid row number!")
            return
        
        w_inner = re.sub(r"np\.float64\((.*?)\)", r"\1", result[1])
        w = ast.literal_eval(w_inner)

        b_inner = re.sub(r"np\.float64\((.*?)\)", r"\1", result[2])
        b = ast.literal_eval(b_inner)

        neuron = list(list(0 for _ in inner) for inner in b)

        print(neuron)

        funktion = result[3]
        self.estimate = tuple(self.perzeptron(tuple(self.highlighted), w, b, neuron, funktion))

    # Spielfeld erschaffen
    def spielfeld_zeichnen(self) -> None:
        for i in range(self.res + 1):

            x = 10 + i * self.dis
            y = 10 + i * self.dis
            #self.canvas.create_line(x, 10, x, 510, fill="white")
            #self.canvas.create_line(10, y, 510, y, fill="white")
        
            if i < (self.res + 1):
                for j in range((self.res + 1)):
                    self.felder_koordinaten[(i, j)] = (10 + round(self.dis/2) + j * self.dis, 10 + round(self.dis/2) + i * self.dis)
    
    def kreis_zeichnen(self, x: int, y: int, r: int, color: str) -> None:
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.canvas.create_oval(x0, y0, x1, y1, fill = color)
    
    def show_estimate(self):
        for i in range(10):
            self.canvas.create_text(10 + i * 50, 570, text=str(i) + ":", fill="white")
        if self.estimate == (): return
        for i in range(10):
            brightness = round(self.estimate[i] * 255)
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            self.kreis_zeichnen(40 + i * 50, 570, 10, color)
    
    def update(self) -> None:
        self.canvas.delete("all")
        self.spielfeld_zeichnen()
        self.show_estimate()
        if self.mouse1_pressed or self.mouse2_pressed:
            self.markfield()
        self.highlight_fields()
        self.root.after(5, self.update)


if __name__ == "__main__":

    root = tkinter.Tk()
    z = Zeichenfeld(root, 40)
    z.update()

    root.mainloop()
