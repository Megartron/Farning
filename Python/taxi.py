import tkinter
import random;

class Taxi():
    def __init__(self, root):
        self.root = root
        self.canvas = tkinter.Canvas(root, width=520, height=520)
        self.felder = ((" " for _ in range(5)) for _ in range(5))
        self.sonderfelder = ((0, 1), (1, 4), (3, 0), (4, 2))
        self.fahrgast_feld = ()
        self.aufgenommen = False
        self.felder_koordinaten = {}
        self.feld = ()
        self.einstellungen = (random.randint(0, 4), random.randint(0, 3)) # fahrgast, ziel

        self.anzahl_züge = 0
        self.code
        self.map = [[] for _ in range(500)]

        self.bewegungen = ("up", "down", "left", "right")

        self.spielfeld_zeichnen()
        self.felder_markieren()
        self.spawn_taxi()
        
        self.canvas.pack(expand=True)

        self.main_loop()

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

    def new_move(self, richtung: str):
        if (len(self.map[self.code]) < self.anzahl_züge):
            self.map[self.code].append({
                "up": 100,
                "down": 100,
                "left": 100,
                "right": 100
            })
        
        self.map[self.code][self.anzahl_züge][richtung] -= self.anzahl_züge
        
    def kodieren(self, coords: tuple, einstellungen: tuple) -> int:
        return ((5 * coords[0] + coords[1]) * 5 + einstellungen[0]) * 4 + einstellungen[1]
    
    def move(self, richtung: str) -> bool:
        if (richtung == "up"):
            if (self.feld[1] - 1 < 0):
                return False
            self.feld = (self.feld[0], self.feld[1] - 1)

        if (richtung == "down"):
            if (self.feld[1] + 1 > 4):
                return False
            self.feld = (self.feld[0], self.feld[1] + 1)

        if (richtung == "left"):
            if (self.feld[0] - 1 < 0):
                return False
            self.feld = (self.feld[0] - 1, self.feld[1])

        if (richtung == "right"):
            if (self.feld[0] + 1 > 4):
                return False
            self.feld = (self.feld[0] + 1, self.feld[1])

    def main_loop(self):
        self.canvas.delete("all")
        x, y = self.get_coords(self.feld)
        self.canvas.create_rectangle(x - 10, y - 15, x + 10, y + 15, fill="yellow")

        self.spielfeld_zeichnen()
        self.felder_markieren()

        richtung = random.choice(self.bewegungen)
        self.move(richtung)

        if (self.fahrgast_feld == self.feld):
            self.aufgenommen = True

        self.root.after(250, self.main_loop)

    def dekodieren(code: int) -> tuple:
        ziel = code % 4
        code //= 4

        fahrgast_pos = code % 5
        code //= 5

        zeile = code // 5
        spalte = code % 5

        return (ziel, fahrgast_pos, zeile, spalte)

    def get_coords(self, coords: tuple) -> tuple:
        return self.felder_koordinaten[coords]
    
    def create_circle(self, x, y, r, color) -> None:
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        self.canvas.create_oval(x0, y0, x1, y1, fill= color)

    def felder_markieren(self) -> None:
        for coords in self.sonderfelder:
            x, y = self.get_coords(coords)
            self.create_circle(x, y, 10, "black")
        
        x, y = self.get_coords(self.sonderfelder[self.einstellungen[1]])
        self.create_circle(x, y, 10, "green")

        if (self.aufgenommen):
            self.fahrgast_feld = self.feld
            x, y = self.get_coords(self.fahrgast_feld)
            self.create_circle(x, y, 10, "blue")

        else: 
            if (self.einstellungen[0] == 4):
                self.fahrgast_feld = self.feld
                

            elif (self.einstellungen[0] == self.einstellungen[1]):
                while (self.einstellungen[0] == self.einstellungen[1]):
                    self.einstellungen[0] = (random.randint(0, 3), self.einstellungen[1])
                
                self.fahrgast_feld = self.sonderfelder[self.einstellungen[0]]

            else: 
                self.fahrgast_feld = self.sonderfelder[self.einstellungen[0]]

            x, y = self.get_coords(self.fahrgast_feld)
            self.create_circle(x, y, 10, "blue")
    
    def spawn_taxi(self) -> None:
        self.feld = (random.randint(0, 4), random.randint(0, 4))
        x, y = self.get_coords(self.feld)
        self.canvas.create_rectangle(x - 10, y - 15, x + 10, y + 15, fill="yellow")


if __name__ == "__main__":

    root = tkinter.Tk()
    taxi1 = Taxi(root)

    root.mainloop()
