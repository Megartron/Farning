import arcade, random

class TTT(arcade.Window):
    def __init__(self):
        # Ein Fenster der Breite 600, Höhe 600 und mit dem Titel "Tic Tac Toe"
        super().__init__(600, 600, "Tic Tac Toe")

        self.phase = 0

        # Gibt an, wie viele Sekunden ein Zug des Computers verzögert wird
        self.verzögerung = 0.2

        self.setup()

    def setup(self):
        self.spielstein_liste = arcade.SpriteList()

        self.spielfeld = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        

        # Wir legen zufällig fest, ob "O" oder "X" beginnt
        self.symbol = random.choice(["X", "O"])
        # Ein Dictionary, das die Symbole den Spielertypen zuordnet
        self.symbol_spieler = {"O": "Mensch", "X": "ComputerRandom"}

        print(self.symbol)
        print(self.symbol_spieler[self.symbol])

        self.verzögerung_delta = 0

        self.vorbei = False

    def __setzen(self, x, y, wert):
        self.spielfeld[-1 - y][x] = wert

    def __lesen(self, x, y):
        return self.spielfeld[-1 - y][x]
    
    def __zeile(self, y):
        return[self.__lesen(x, y) for x in range(3)]
    
    def __zeile(self, x):
        return[self.__lesen(x, y) for y in range(3)]


    # def __koordinaten_feldmittelpunkt(self, x: int, y: int): # TDO: Kurz schreiben
    #     if 0 <= x < 200 and 0 <= y < 200:
    #         return (100, 100)
    #     elif 0 <= x < 200 and 200 <= y < 400:
    #         return (100, 300)
    #     elif 0 <= x < 200 and 400 <= y < 600:
    #         return (100, 500)
    #     elif 200 <= x < 400 and 0 <= y < 200:
    #         return (300, 100)
    #     elif 200 <= x < 400 and 200 <= y < 400:
    #         return (300, 300)
    #     elif 200 <= x < 400 and 400 <= y < 600:
    #         return (300, 500)
    #     elif 400 <= x < 600 and 0 <= y < 200:
    #         return (500, 100)
    #     elif 400 <= x < 600 and 200 <= y < 400:
    #         return (500, 300)
    #     elif 400 <= x < 600 and 400 <= y < 600:
    #         return (500, 500)
        
    def __transformation(self, pos_intern):
        return (2 - pos_intern[1], pos_intern[0])
    
    # Gibt True zurück, falls ein Spieler gewonnen hat, ansonsten False
    def __gewinnprüfung(self):
        return self.__lesen(0, 0) == self.__lesen(0, 1) == self.__lesen(0, 2) != "" or \
            self.__lesen(1, 0)== self.__lesen(1, 1) == self.__lesen(1, 2) != "" or \
            self.__lesen(2, 0) == self.__lesen(2, 1) == self.__lesen(2, 2) != "" or \
            self.__lesen(1, 0) == self.__lesen(0, 0) == self.__lesen(2, 0) != "" or \
            self.__lesen(0, 1) == self.__lesen(1, 1) == self.__lesen(2, 1) != "" or \
            self.__lesen(0, 2)  == self.__lesen(1, 2)  == self.__lesen(2, 2) != "" or \
            self.__lesen(0, 0) == self.__lesen(1, 1) == self.__lesen(2, 2) != "" or \
            self.__lesen(0, 2) == self.__lesen(1, 1) == self.__lesen(2, 0) != ""
        
    def __koordinaten_feldmittelpunkt(self, x: int, y: int):
        return (x // 200 * 200 + 100, y // 200 * 200 + 100)
    
    # Wählt zufällig ein freies Feld aus und gibt dieses zurück
    def __random_zug(self):
        # Freien Felder bestimmen
        gegener_symbol = "X" if self.symbol == "O" else "O"
        anfang = {
            (0, 0): (2, 2),
            (2, 2): (0, 0),
            (0, 2): (2, 0),
            (2, 0): (0, 2)
        }
        seiten = [(0, 1), (1, 0), (1, 2), (2, 1)]
        freie_seiten = []
        freie_ecken = []
        besetzte_ecken = []
        ecken = [(0, 0), (0, 2), (2, 2), (2, 0)]
        for i in ecken:
            if self.__lesen(i[0], i[1]) == "":
                freie_ecken.append(i)
            else:
                besetzte_ecken.append(i)

        for i in seiten:
            if self.__lesen(i[0], i[1]) == "":
                freie_seiten.append(i)

        freie_felder = [(x, y) for x in range(3) for y in range(3) if self.__lesen(x, y) == ""]
        #print(freie_felder)
          
        # Ein freies Feld zufällig auswählen
        
        # Sonderfall1:
        for i in besetzte_ecken:
            if self.__lesen(anfang[i][0], anfang[i][1]) == self.__lesen(i[0], i[1]) and self.__lesen(1, 1) != "":
                return random.choice(freie_seiten)

        # Sonderfall2:
        if (self.__lesen(1, 0) and (self.__lesen(0, 2) or self.__lesen(2, 2)) == gegener_symbol) and self.__lesen(0, 0) == "":
            return (0, 0)
        elif (self.__lesen(2, 1) and (self.__lesen(0, 2) or self.__lesen(0, 2)) == gegener_symbol) and self.__lesen(2, 2) == "":
            return (2, 2)
        elif (self.__lesen(2, 1) and (self.__lesen(0, 0) or self.__lesen(2, 0)) == gegener_symbol) and self.__lesen(2, 0) == "":
            return (2, 0)

        
        #Ecke auswählen
        if freie_ecken != []:
            zufälliges_feld = random.choice(freie_ecken)  
        else:
            zufälliges_feld = random.choice(freie_felder)

        
        return zufälliges_feld
    
    # Gibt zurück, mit welchem Index in der übergebenen Reihe der aktuelle Spieler gewinnen kann
    # Falls Gewinnen nicht möglich ist, wird -1 zurückgegeben
    # reihe ist stets eine Liste mit drei Elementen ("O", "X" oder "")
    def __kann_gewinnen(self, reihe):
        gegener_symbol = "X" if self.symbol == "O" else "O"
        if reihe.count(self.symbol) == 2 and reihe.count("") == 1:
            return reihe.index("")
        elif reihe.count(gegener_symbol) == 2 and reihe.count("") == 1:
            return reihe.index("")
        else:
            return None
    

    
    # Wenn in diesem Zug gewonnen werden kann, wird das hierfür benötigte Feld ausgewählt
    # Falls nicht in diesem Zug gewonnen werden kann, aber im nächsten verloren, wird das hierfür (vom Gegner) benötigte Feld ausgewählt
    # Ansonsten wird ein zufälliges freies Feld ausgewählt
    def __mittelschlauer_zug(self):

        for y in range(len(self.spielfeld)):
            if (x := self.__kann_gewinnen(self.spielfeld[2 - y])) != None:
                return (x, y)
            # Kurzform für:
            # x = self.__kann_gewinnen(self.spielfeld[2 - y])
            # if x != None:
            #   ...
        
        # *self.spielfeld entpackt self.spielfeld, d.h. statt einer Liste von drei Liste stehen dort nun getrennt drei Listen
        # zip fasst alle Einträge dieser Listen an der gleichen Stelle zu einem Tupel zusammen
        # Somit vertauscht zip(*self.spielfeld) die Zeilen und Spalten von self.spielfeld
        spielfeld_transponiert = list(zip(*self.spielfeld))
        for x in range(len(spielfeld_transponiert)):
            if (y := self.__kann_gewinnen(spielfeld_transponiert[x])) != None:
                return (x, 2 - y)
        
        diagonal1, diagonal2 = [self.spielfeld[i][i] for i in range(3)], [self.spielfeld[i][2 - i] for i in range(3)]
        #print(diagonal1, self.__kann_gewinnen(diagonal1), diagonal2, self.__kann_gewinnen(diagonal2))
        if (x_y := self.__kann_gewinnen(diagonal1)) != None:
            return (x_y, 2 - x_y)
        if (x_y := self.__kann_gewinnen(diagonal2)) != None:
            return (2 - x_y, 2 - x_y)
        
        # In der Mitte platzieren
        if(self.__lesen(1, 1) == ""):
            return (1, 1)
        # Feld zurückgeben
            
        return self.__random_zug()
    
    # TODO Auf 20.03.24
    # Eine Funktion diagonalgewinn, die True zurückgibt, wenn der aktuelle Spieler über eine der beiden Diagonalen gewinnen kann, ansonsten False.
    # __kann_gewinnen kann dabei verwendet werden.
    
    # Wird automatisch mit jedem neuen Frame aufgerufen
    def on_update(self, delta_time: float):
        if self.phase == 1 and self.symbol_spieler[self.symbol] == "ComputerRandom" and not self.vorbei:
            self.verzögerung_delta += delta_time
            if self.verzögerung_delta >= self.verzögerung:
                feld = self.__mittelschlauer_zug()
                
                #print(feld)
                spielstein = arcade.Sprite("Muschel2.jpeg", 0.2) if self.symbol == "O" else arcade.Sprite("Seestern.jpeg", 0.1)
                self.spielfeld[2 - feld[1]][feld[0]] = self.symbol
                self.__setzen(feld[0], feld[1], self.symbol)
                spielstein.center_x = 100 + feld[0] * 200
                spielstein.center_y = 100 + feld[1] * 200
                self.spielstein_liste.append(spielstein)
                self.symbol = "X" if self.symbol == "O" else "O"
                self.verzögerung_delta = 0
                #print(self.spielfeld)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.phase == 0:
            if 200 <= x <= 400 and 155 <= y <= 205:
                self.phase = 1
        elif self.phase == 1 and self.symbol_spieler[self.symbol] == "Mensch" and not self.vorbei and self.__lesen(x//200,y//200) == "":
            spielstein_position = self.__koordinaten_feldmittelpunkt(x, y)
            spielstein = arcade.Sprite("Muschel2.jpeg", 0.2) if self.symbol == "O" else arcade.Sprite("Seestern.jpeg", 0.1)
            self.__setzen(x//200,y//200, self.symbol)
            spielstein.center_x = spielstein_position[0]
            spielstein.center_y = spielstein_position[1]
            self.spielstein_liste.append(spielstein)
            self.symbol = "X" if self.symbol == "O" else "O"
            #print(self.spielfeld)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            arcade.exit()
        if symbol == arcade.key.R:
            self.setup()

    def on_draw(self):
        if self.phase == 0:
            arcade.draw_lrwh_rectangle_textured(0, 0, 600, 600, arcade.load_texture("bg.png"))
            arcade.draw_text("Willkommen bei Tic Tac Toe!", 300, 350, font_size=39, width=600, align="center", font_name="Kenney Blocks", anchor_x="center", anchor_y="center", multiline=True)
            arcade.draw_text("START", 300, 183, font_size=22, font_name="Kenney Pixel Square", anchor_x="center", anchor_y="center")
            arcade.draw_rectangle_outline(300, 180, 200, 50, arcade.color.WHITE, 5)
        elif self.phase == 1:
            # Ein Rechteck über das gesamte Spielfeld ((0, 0) der Eckpunkt unten links, Breite 600, Höhe 600) mit der Textur "bg.jpg"
            arcade.draw_lrwh_rectangle_textured(0, 0, 600, 600, arcade.load_texture("bg.png"))

            # Eine Linie von (x=20, y=400) bis (x=580, y= 400) in der Farbe (104, 60, 63) und der Dicke 16 (obere waagerechte Linie)
            arcade.draw_line(20, 400, 580, 400, (104, 60, 63), 17)
            arcade.draw_line(20, 200, 580, 200, (104, 60, 63), 17)
            arcade.draw_line(200, 20, 200, 580, (104, 60, 63), 17)
            arcade.draw_line(400, 20, 400, 580, (104, 60, 63), 17)

            self.spielstein_liste.draw()

            if self.__gewinnprüfung():
                arcade.draw_text("Gewonnen!", 300, 300, font_size=45, font_name="Kenney Blocks", anchor_x="center", anchor_y="center")
                arcade.draw_text("R: Neustart", 300, 200, font_size=20, font_name="Kenney Pixel Square", anchor_x="center", anchor_y="center")
                arcade.draw_text("Q: Beenden", 300, 150, font_size=20, font_name="Kenney Pixel Square", anchor_x="center", anchor_y="center")
                self.vorbei = True
            elif not "" in self.spielfeld[0] + self.spielfeld[1] + self.spielfeld[2]:
                arcade.draw_text("Uentschieden!", 300, 300, font_size=45, font_name="Kenney Blocks", anchor_x="center", anchor_y="center")
                arcade.draw_text("R: Neustart", 300, 200, font_size=20, font_name="Kenney Pixel Square", anchor_x="center", anchor_y="center")
                arcade.draw_text("Q: Beenden", 300, 150, font_size=20, font_name="Kenney Pixel Square", anchor_x="center", anchor_y="center")
                self.vorbei = True

TTT()
# Wir starten das Spiel
arcade.run()

# Gewinnprüfung
# Neustart auf R
# Schließen auf Q
# Startmenü
# Hintergrundmusik
# Toneffekte (beim Platzieren, beim Gewinnen, ...)
# Unentschieden
# Random-Einzelspieler
# Schlau-Einzelspieler
# Sehr-schlau-Einzelspieler
# Unbesiegbar-Einzelspieler (Mini-Max)


# Möglichkeit 1:
# Alles wie grafisch in arcade (Erst Zeile, dann Spalte)


# TODO
# Möglichkeit 2:
# Alles wie im Koordinatensystem wie man es aus Mathe kennt (Erst Spalte: x, dann Zeile: y)

# TODO
# Kümmere dich um die Koordinatentransformation
# Überlege dir außerdem eine geeignete Datenstruktur
# Wesentlich ist eine Funktion zum Setzen und Auslesen von Werten in der Datenstruktur, die das Spielfeld intern repräsentiert
def setzen(self, x, y, wert):
    ...


#   self.spielfeld = [
#            ["", "", ""],
#            ["", "", ""],
#            ["", "", ""]
#        ]
# kann grundsätzlich weiter verwendet werden.