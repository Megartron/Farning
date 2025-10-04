import tkinter
import random
import math
from tkinter import *

class Taxi():
    def __init__(self, root, startingcode = -1):
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
        self.phase = 0

        self.zustande_fahrgast = [{(0, 0): 100, (0, 1): 100, (0, 2): 100, (0, 3): 100, (0, 4): 100, 
                          (1, 0): 100, (1, 1): 100, (1, 2): 100, (1, 3): 100, (1, 4): 100, 
                          (2, 0): 100, (2, 1): 100, (2, 2): 100, (2, 3): 100, (2, 4): 100, 
                          (3, 0): 100, (3, 1): 100, (3, 2): 100, (3, 3): 100, (3, 4): 100, 
                          (4, 0): 100, (4, 1): 100, (4, 2): 100, (4, 3): 100, (4, 4): 100}
                          for _ in range(500)]
        
        self.zustande_ziel = [{(0, 0): 100, (0, 1): 100, (0, 2): 100, (0, 3): 100, (0, 4): 100, 
                          (1, 0): 100, (1, 1): 100, (1, 2): 100, (1, 3): 100, (1, 4): 100, 
                          (2, 0): 100, (2, 1): 100, (2, 2): 100, (2, 3): 100, (2, 4): 100, 
                          (3, 0): 100, (3, 1): 100, (3, 2): 100, (3, 3): 100, (3, 4): 100, 
                          (4, 0): 100, (4, 1): 100, (4, 2): 100, (4, 3): 100, (4, 4): 100}
                          for _ in range(500)]
        
        self.current_zustand = self.zustande_fahrgast

        """
        for i in range(500):
            for z in range(5):
                for s in range(5):
                    self.zustande[i][(z, s)] = 100
        """

        self.anzahl_züge = 0
        self.code = 0
        self.taxi_gast_code = 0
        self.ziel_code = 0
        self.current_round = []
        self.starting_code = startingcode
        
        # helping variables
        self.dauer = 700
        self.delta_dis = 0
        self.reset = None
        self.info = Label(root, text = "info")
        self.speed = 500
        self.show_rewards = True
        self.counter = tkinter.IntVar(value=0)

        self.felder_koordinaten = {}
        self.animated = False
        self.while_animation = False
        self.vorgegebener_weg = []
        #"unten", "unten", "unten", "unten", "links", "links"
        self.tasten_initiieren()
        self.zurucksetzen()

        self.canvas.pack(expand=True)
        self.info.pack()
        

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

        scale = tkinter.Scale(self.root, from_=1, to=3000, length=400, orient="horizontal",
                 label="Speed", command=self.set_speed)
        scale.pack()
        scale.set(500)

        # Button to trigger the change
        button = tkinter.Button(root, text="Show Reward", command=self.increase)
        button.pack()

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
        self.fill_field(x, y, "orange")

        # Text
        if self.show_rewards:
            for pos in list(self.current_zustand[self.code].keys()):
                x, y = self.get_coords(pos)

                reward = int((1000 - self.current_zustand[self.code][pos]) * 4.5)
                if (reward > 250):
                    color = self.rgb_to_hex(255, 255, 0)
                else:
                    color = self.rgb_to_hex(reward, 255, 0)
                self.fill_field(x, y, color)

                #r = str(self.current_zustand[self.code][pos])
                #self.canvas.create_text(x, y, text=r, font=("Arial", 16), fill="blue")

        x, y = self.get_coords(self.ziel)
        self.canvas.create_rectangle(x + 20, y + 12, x - 20, y - 12, fill = "green")
        self.canvas.create_line(x + 20, y - 12, x + 20, y + 30, fill="black", width=3)

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
        x, y = self.taxi_pos_px if self.phase > 0 else self.get_coords(self.fahrgast)
        self.kreis_zeichnen(x, y, 10, "blue")

    def set_code(self, code: int):
        self.code = code
        ziel, fahrgast_pos, zeile, spalte = self.dekodieren(code)

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
        if (self.starting_code != -1):
            self.code = self.starting_code
            self.set_code(self.code)
        else:
            self.code = self.kodieren(self.taxi_pos, (self.taxi_gast_code, self.ziel_code))
        self.anzahl_züge = 0
        self.phase = 0
        self.new_move(self.taxi_pos)
        self.current_zustand = self.zustande_fahrgast
        self.visuals()

    def rgb_to_hex(self, r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"

    def increase(self):
        self.counter.set(self.counter.get() + 1)
        if self.counter.get() % 2 == 0:
            self.show_rewards = True
        else:
            self.show_rewards = False

    def new_game(self):
        self.reset.destroy()
        self.zurucksetzen()
        self.root.after(2000, self.update)
    
    def quadratische_liste(self, n: int, min: int, max: int) -> list:
        schritte = [(i / (n - 1))**2 for i in range(n)]
        werte = [min + (max - min) * s for s in schritte]
        return werte

    def quadratisch_summe(self, n: int, a: float, e: float) -> list:
        # Quadratische Basiswerte: z.B. [0², 1², 2², ..., (n-1)²]
        basis = [(i / (n - 1))**2 for i in range(n)]
        
        # Skaliere so, dass der kleinste Wert a ist
        min_basis = min(basis)
        basis_shifted = [x - min_basis for x in basis]
        
        # Berechne Skalierungsfaktor, damit Summe = e
        sum_basis = sum(basis_shifted)
        scale = (e - a * n) / sum_basis if sum_basis != 0 else 0
        
        # Endgültige Werte berechnen
        werte = [a + scale * x for x in basis_shifted]
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
    
    def set_speed(self, speed):
        self.speed = int(speed)

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
    
    def get_cord_bewegung(self, richtung) -> tuple:
        if richtung == "rechts":
            if self.taxi_pos[1] + 1 > 4:
                return (-1, -1)
            return (self.taxi_pos[0], self.taxi_pos[1] + 1)
        
        elif richtung == "links":
            if self.taxi_pos[1] - 1 < 0:
                return (-1, -1)
            return (self.taxi_pos[0], self.taxi_pos[1] + -1)
        
        elif richtung == "unten":
            if self.taxi_pos[0] + 1 > 4:
                return (-1, -1)
            return (self.taxi_pos[0] + 1, self.taxi_pos[1])

        elif richtung == "oben":
            if self.taxi_pos[0] - 1 < 0:
                return (-1, -1)
            return (self.taxi_pos[0] - 1, self.taxi_pos[1])


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

    def new_move(self, pos):
        self.current_round.append(pos)
    
    def next_max_reward(self) -> int:
        rewards = []
        for i in self.moglichkeiten:
            cords = self.get_cord_bewegung(i)
            if cords == (-1, -1):
                rewards.append(0)
            else: 
                rewards.append(self.current_zustand[self.code][cords])
        return max(rewards)
    
    def best_next_move(self, rand) -> str:
        if (random.random() < rand):
            return self.random_move()

        rewards = []
        for i in self.moglichkeiten:
            cords = self.get_cord_bewegung(i)
            if cords == (-1, -1):
                rewards.append(100)
            else: 
                rewards.append(self.current_zustand[self.code][cords])

        max_reward = max(rewards)
        max_rewards = []
        for i in range(len(rewards)):
            if rewards[i] == max_reward:
                max_rewards.append(i)
        decicion = random.choice(max_rewards)
        return self.moglichkeiten[decicion]

    def auswertung(self, a: int):
        if self.phase == 1:
            last = self.current_round[-1]
            self.zustande_fahrgast[self.code][last] = 1000
            if len(self.current_round) == 1: return
            self.zustande_fahrgast[self.code][self.current_round[-2]] = 990
            self.phase = 2

        elif self.phase == 3:
            last = self.current_round[-1]
            self.zustande_ziel[self.code][last] = 1000

            self.zustande_ziel[self.code][self.current_round[-2]] = 990
            self.phase = 4
        
        if ((max_reward := self.next_max_reward()) > self.current_zustand[self.code][self.current_round[-1]]):
            if (self.phase == 0):
                self.zustande_fahrgast[self.code][self.current_round[-1]] = max_reward - 10

            elif (self.phase == 2):
                self.zustande_ziel[self.code][self.current_round[-1]] = max_reward - 10
    
    def geschafft(self):
        self.reset = Button(self.canvas, text="Neues Spiel", width=40,
             height=5, bd="10", command=self.new_game)
        self.reset.place(x=65, y=100)

    def training(self, rounds):
        for _ in range(rounds):
            self.taxi_pos = (random.randint(0, 4), random.randint(0, 4))
            self.init_ziel_gast()
            if (self.starting_code != -1):
                self.code = self.starting_code
                self.set_code(self.code)
            else:
                self.code = self.kodieren(self.taxi_pos, (self.taxi_gast_code, self.ziel_code))
            self.anzahl_züge = 0
            self.phase = 0
            self.current_zustand = self.zustande_fahrgast
            self.new_move(self.taxi_pos)

            while self.phase != 4:
                zug = self.best_next_move(0.15)
                self.taxi_bewegen(zug)

                if (self.phase == 0):
                    self.current_zustand = self.zustande_fahrgast
                    if (self.taxi_pos == self.fahrgast):
                        self.phase = 1

                elif (self.phase == 2):
                    self.current_zustand = self.zustande_ziel
                    if (self.taxi_pos == self.ziel):
                        self.phase = 3

                self.new_move(self.taxi_pos)
                self.auswertung(20)
        self.zurucksetzen()

    # Main
    def update(self) -> None:
        self.canvas.delete("all")
        if (self.phase == 4):
            self.geschafft()
            return
        
        zug = self.best_next_move(0.0)

        self.taxi_bewegen(zug)

        # Kontrolle Fahrgast
        if (self.phase == 0):
            self.current_zustand = self.zustande_fahrgast
            if (self.taxi_pos == self.fahrgast):
                self.phase = 1

        elif (self.phase == 2):
            self.current_zustand = self.zustande_ziel
            if (self.taxi_pos == self.ziel):
                self.phase = 3

        self.new_move(self.taxi_pos)

        self.anzahl_züge += 1
        self.auswertung(20)
        
        self.visuals()

        self.root.after(self.speed, self.update)

    

if __name__ == "__main__":

    root = tkinter.Tk()
    taxi1 = Taxi(root, 312)

    taxi1.training(0)

    taxi1.update()

    root.mainloop()
