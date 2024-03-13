def on_update(self, delta_time: float):
        
        if self.aktueller_spieler == "Computer" and self.start:
            feld = self.comp()
            print(feld)
            
            self.verzögerung_delta += delta_time
            if self.verzögerung_delta >= self.verzögerung
                spielstein = arcade.Sprite("1000_F_601211158_bu0EaLaEqZwLyweHdtsxJf8GfDkMO7hI.jpg", 0.2)
                self.spielfeld[feld[0]][feld[1]] = self.symbol
                spielstein.center_x = 100 + feld[0] * 200
                spielstein.center_y = 100 + feld[1] * 200
                self.spielsteinliste.append(spielstein)
                self.symbol = "X" if self.symbol== "O" else "O"
                self.aktueller_spieler = self.spieler1
                self.verzögerung_delta = 0

    def comp(self):
        self.__gewinnprüfung()
        sf = self.spielfeld
        print(sf)
        EckenComp = [(0, 2), (2, 2), (2, 0), (0, 0), (0, 2), (2, 2)]
        Ecken = [(0, 2), (2, 2), (2, 0), (0, 0)]
        SeitenComp = [(1, 2), (0, 1), (1, 0), (2, 1), (1, 2), (0, 1)]
        Seiten = [(1, 2), (0, 1), (2, 1), (1, 0)]
        Mitte = (1, 1)
        j = 0
        Freie_Ecken = []
        Freie_Seiten = []

        for i in Ecken:
            if sf[i[0]][i[1]] == "":
                Freie_Ecken.append(i)

        for i in Seiten:
            if sf[i[0]][i[1]] == "":
                Freie_Seiten.append(i)

        if sf[Mitte[0]][Mitte[1]] == "X":
            for i in Ecken:
                if sf[i[0]][i[1]] == "X":
                    if sf[[EckenComp[j + 2][0]]][[EckenComp[j + 2][1]]] == "":
                        return EckenComp[j + 2]
                    break
                j += 1
            j  = 0
            for i in Seiten:
                if sf[i[0]][i[1]] == "X":
                    if sf[[SeitenComp[j + 2][0]]][[SeitenComp[j + 2][1]]] == "":
                        return SeitenComp[j + 2]
                    break
                j += 1
                    

        if sf[Mitte[0]][Mitte[1]] == "":
            return Mitte
        elif Freie_Ecken != []:
            return random.choice(Freie_Ecken)
        elif Freie_Seiten != []:
            return random.choice(Freie_Seiten)
        