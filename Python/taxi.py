import tkinter
import random
import math

class Taxi():
    def __init__(self, root):
        self.root = root

        self.canvas = tkinter.Canvas(root, width=520, height=520, bg="black")
        # main variables
        self.felder = ((" " for _ in range(5)) for _ in range(5))
        self.sonderfelder = ((0, 1), (1, 4), (3, 0), (4, 2))
        self.taxi_bewegung = (0, 0)
        self.moglichkeiten = ("oben", "unten", "links", "rechts")
        self.fahrgast = ()
        self.ziel = ()
        self.taxi_pos = ()
        self.taxi_pos_px = ()
        self.aufgenommen = 0
        self.map = [[] for _ in range(500)]
        self.anzahl_züge = 0
        self.code = 0
        self.taxi_gast_code = 0
        self.ziel_code = 0
        self.current_round = []

        # helping variables
        self.dauer = 700
        self.delta_dis = 0

        self.felder_koordinaten = {}
        self.animated = False
        self.while_animation = False
        self.vorgegebener_weg = ["links", "oben", "rechts", "oben"]

        self.create_widgets()
        self.zurucksetzen()

        self.canvas.pack(expand=True)
        self.tasten_initiieren()

    # Animation, Grafiks
    def taxi_animation(self, start_x: int, start_y):
        v = 50/self.dauer
        self.taxi_pos_px = (start_x + self.taxi_bewegung[0] * v, start_y + self.taxi_bewegung[1] * v)

        if (self.delta_dis + abs(self.taxi_bewegung[0] * v) + abs(self.taxi_bewegung[1] * v) >= 100):
            self.delta_dis = 0
            self.taxi_pos_px = self.get_coords(self.taxi_pos)
        else:
            self.delta_dis += (abs(self.taxi_bewegung[0] * v) + abs(self.taxi_bewegung[1] * v))

        self.taxi_zeichnen(self.taxi_pos_px, "converted")
    
    def set_animation(self, value) -> None:
        if (self.while_animation):
            return
        self.dauer = int(value)

    def create_widgets(self) -> None:
        scale_animation = tkinter.Scale(self.root, from_=10, to=1000, orient="horizontal", label="Animation speed", 
                                        command=self.set_animation)
        scale_animation.pack()

    def taxi_zeichnen(self, coords: tuple, state: str) -> None:
        if state == "converted":
            x, y = coords
        else:
            x, y = self.get_coords(coords)

        self.canvas.create_rectangle(x - 37, y - 10, x + 37, y + 10, fill="yellow", outline="yellow")

        self.canvas.create_polygon((x - 30, y - 9, x - 15, y - 26, x - 15, y - 9), fill="#4cd5ff", outline="yellow", width=2)
        self.canvas.create_rectangle(x - 15, y - 25, x + 8, y - 9, fill="#4cd5ff", outline="yellow", width=2)
        self.canvas.create_polygon((x + 8, y - 9, x + 8, y - 25, x + 23, y - 9), fill="#4cd5ff", outline="yellow", width=2)

        self.kreis_zeichnen(x - 19, y + 13, 16, "black")
        self.kreis_zeichnen(x + 15, y + 13, 16, "black")
        self.kreis_zeichnen(x - 19, y + 13, 12, "grey")
        self.kreis_zeichnen(x + 15, y + 13, 12, "grey")
        self.kreis_zeichnen(x - 19, y + 13, 2, "black")
        self.kreis_zeichnen(x + 15, y + 13, 2, "black")

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
    
    def felder_markieren(self) -> None:
        for coords in self.sonderfelder:
            x, y = self.get_coords(coords)
            self.fill_field(x, y, "red")

    def tasten_initiieren(self) -> None:
        self.root.bind("w", lambda x: self.taxi_bewegen("oben"))
        self.root.bind("a", lambda x: self.taxi_bewegen("links"))
        self.root.bind("s", lambda x: self.taxi_bewegen("unten"))
        self.root.bind("d", lambda x: self.taxi_bewegen("rechts"))

    def init_ziel_gast(self) -> None:
        ziel = random.randint(0, 3)
        gast = random.randint(0, 4)
        while (gast == ziel):
                gast = random.randint(0, 4)
        
        self.ziel = self.sonderfelder[ziel]
        if (gast == 4):
            self.fahrgast = self.taxi_pos
        else:
            self.fahrgast = self.sonderfelder[gast]
        
        self.taxi_gast_code = gast
        self.ziel_code = ziel

    def visuals(self) -> None:
        self.spielfeld_zeichnen()
        self.felder_markieren()

        x, y = self.get_coords(self.ziel)
        self.fill_field(x, y, "green")

        # Taxi
        if self.animated:
            x0, y0 = self.taxi_pos_px
            x1, y1 = self.get_coords(self.taxi_pos)
            
            if math.sqrt((x0 - x1)**2 + (y0 - y1)**2) <= 3:
                self.taxi_bewegung = (0, 0)
                self.taxi_zeichnen(self.taxi_pos, "not converted")
                self.taxi_pos_px = self.get_coords(self.taxi_pos)
                self.while_animation = False
            else:
                self.delta_dis = 0
                self.while_animation = True
                sx, sy = self.taxi_pos_px
                self.taxi_animation(sx, sy)
        else:
            self.taxi_zeichnen(self.taxi_pos, "not converted")
            self.taxi_pos_px = self.get_coords(self.taxi_pos)

        # Fahrgast, Ziel
        x, y = self.taxi_pos_px if self.aufgenommen > 0 else self.get_coords(self.fahrgast)
        self.kreis_zeichnen(x, y, 10, "blue")     

    def set_code(self, code: int):
        ziel, fahrgast_pos, zeile, spalte = self.dekodieren(code)

        print((ziel, fahrgast_pos, zeile, spalte))

        self.taxi_pos = (spalte, zeile)
        self.ziel_code = ziel
        self.taxi_gast_code = fahrgast_pos

        self.ziel = self.sonderfelder[ziel]
        if (fahrgast_pos == 4):
            self.fahrgast = self.taxi_pos
        else:
            self.fahrgast = self.sonderfelder[fahrgast_pos]

    # Helpers
    def zurucksetzen(self) -> None:
        self.spielfeld_zeichnen()
        self.felder_markieren()
        self.taxi_erschaffen()
        self.init_ziel_gast()
        self.code = self.kodieren(self.taxi_pos, (self.taxi_gast_code, self.ziel_code))
        self.anzahl_züge = 0
        self.aufgenommen = 0
    
    def quadratische_liste(self, n: int) -> list:
        a = 5
        e = 100
        schritte = [(i / (n - 1))**2 for i in range(n)]
        werte = [a + (e - a) * s for s in schritte]
        return werte

    def kreis_zeichnen(self, x: int, y: int, r: int, color: str) -> None:
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.canvas.create_oval(x0, y0, x1, y1, fill = color)

    def get_coords(self, coords: tuple) -> tuple:
        return self.felder_koordinaten[coords]
    
    def fill_field(self, x, y, color: str) -> None:
        x0 = x - 50
        y0 = y - 50
        x1 = x + 50
        y1 = y + 50
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="white", fill=color)

    def taxi_erschaffen(self) -> None:
        feld = (random.randint(0, 4), random.randint(0, 4))
        self.taxi_pos_px = self.get_coords(feld)
        self.taxi_pos = feld
    
    # Logik
    def taxi_bewegen(self, richtung: str) -> None:
        if self.while_animation:
            return
        if richtung == "rechts":
            if self.taxi_pos[1] + 1 > 4:
                return
            self.taxi_bewegung = (100, 0)
            self.taxi_pos = (self.taxi_pos[0], self.taxi_pos[1] + 1)
        
        elif richtung == "links":
            if self.taxi_pos[1] - 1 < 0:
                return
            self.taxi_bewegung = (-100, 0)
            self.taxi_pos = (self.taxi_pos[0], self.taxi_pos[1] + -1)
        
        elif richtung == "unten":
            if self.taxi_pos[0] + 1 > 4:
                return
            self.taxi_bewegung = (0, 100)
            self.taxi_pos = (self.taxi_pos[0] + 1, self.taxi_pos[1])

        elif richtung == "oben":
            if self.taxi_pos[0] - 1 < 0:
                return
            self.taxi_bewegung = (0, -100)
            self.taxi_pos = (self.taxi_pos[0] - 1, self.taxi_pos[1])

        else:
            raise Exception("Ungultige Bewegungseingabe!")

    def kodieren(self, coords: tuple, einstellungen: tuple) -> int:
        return ((5 * coords[0] + coords[1]) * 5 + einstellungen[0]) * 4 + einstellungen[1]

    def dekodieren(self, code: int) -> tuple:
        ziel = code % 4
        code //= 4

        fahrgast_pos = code % 5
        code //= 5

        zeile = code // 5
        spalte = code % 5

        return (ziel, fahrgast_pos, zeile, spalte)

    # Computer
    def random_move(self) -> str:
        return random.choice(self.moglichkeiten)

    def new_move(self):
        if (len(self.map[self.code]) <= self.anzahl_züge):
            self.map[self.code].append({
                "oben": 100,
                "unten": 100,
                "links": 100,
                "rechts": 100
            })
    
    def next_max_reward(self):
        # TODO
        ...
    
    def auswertung(self, richtung: str, a: int):
        self.map[self.code][self.anzahl_züge][richtung] -= self.anzahl_züge * a

        l = len(self.map[self.code])
        if self.aufgenommen == 1:
            belohnungen = self.quadratische_liste(l)
            for i in range(l):
                self.map[self.code][i][self.current_round[i]] += belohnungen[i]
            self.aufgenommen = 2




    # Main
    def update(self) -> None:
        self.canvas.delete("all")
        self.visuals()
        
        
        zug = self.random_move()
        self.taxi_bewegen(zug)

        # Kontrolle Fahrgast
        if (self.taxi_pos == self.fahrgast and self.aufgenommen == 0):
            self.aufgenommen = 1

        self.new_move()
        self.current_round.append(zug)
        self.auswertung(zug, 0.5)
        self.anzahl_züge += 1
        
        print(self.map[self.code])
        print("-------------------------------------------------------------")

        self.root.after(250, self.update)

    

if __name__ == "__main__":

    root = tkinter.Tk()
    taxi1 = Taxi(root)

    taxi1.set_code(143)
    taxi1.update()

    root.mainloop()
