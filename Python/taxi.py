import tkinter
import random;

class Taxi():
    def __init__(self, root):
        self.root = root
        self.canvas = tkinter.Canvas(root, width=520, height=520)
        self.felder = ((" " for _ in range(5)) for _ in range(5))
        self.sonderfelder = ((0, 1), (1, 4), (3, 0), (4, 2))
        self.felder_koordinaten = {}

        self.spielfeld_zeichnen()
        self.felder_markieren()
        self.spawn_taxi()
        
        self.canvas.pack(expand=True)


    def spielfeld_zeichnen(self) -> None:
        for i in range(6):
            x = 10 + i * 100
            y = 10 + i * 100
            self.canvas.create_line(x, 10, x, 510)
            self.canvas.create_line(10, y, 510, y)

            if i > 5:
                break

            for j in range(5):
                self.felder_koordinaten[(i, j)] = (60 + j * 100, 60 + i * 100)
        
        

    def get_coords(self, coords: tuple) -> tuple:
        return self.felder_koordinaten[coords]
    
    def create_circle(self, x, y, r) -> None:
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        self.canvas.create_oval(x0, y0, x1, y1)

    def felder_markieren(self) -> None:
        for coords in self.sonderfelder:
            x, y = self.get_coords(coords)
            self.create_circle(x, y, 10)
    
    def spawn_taxi(self) -> None:
        feld = (random.randint(0, 4), random.randint(0, 4))
        x, y = self.get_coords(feld)
        self.canvas.create_rectangle(x - 10, y - 15, x + 10, y + 15, fill="yellow")


if __name__ == "__main__":

    root = tkinter.Tk()
    taxi1 = Taxi(root)

    root.mainloop()