import tkinter as tk
import time
import random

class hexapawn():

    def __init__(self, root):
        self.root = root
        self.root.title("Hexapawn")
        self.figuren = {}
        self.pos = []
        self.buttons = []
        self.button_reset = None
        self.current_spieler = "X"
        self.züge = 0
        self.comp = False
        self.postionen_zug2 = []
        self.postionen_zug4 = []
        self.postionen_zug6 = []
        self.züge_2 = []
        self.züge_4 = []
        self.züge_6 = []
        self.bewertung_zug6 = {}
        self.bewertung_zug2 = {}
        self.bewertung_zug4 = {}

    def spielfeld_erstellen(self):
        self.figuren = {}
        self.pos = []
        self.buttons = []
        self.current_spieler = "X"
        self.züge = 0
        
        for r in range(3):
            row_buttons = []
            for c in range(3):
                btn = tk.Button(self.root, text="",font=("Arial", 20), width=20, height=6, command=lambda r=r, c=c: self.select(r, c))
                self.figuren[(r, c)] = ""
                btn.grid(row=r, column=c, padx=5, pady=5)
                row_buttons.append(btn)
                if r == 0:
                    self.figuren[(r, c)] = "O"
                    btn.config(text= "O")

                elif r == 2:
                    self.figuren[(r, c)] = "X"
                    btn.config(text= "X")
            self.buttons.append(row_buttons)
    
    def spielfeld_erstellen_auto(self):
        self.figuren = {}
        self.pos = []
        self.buttons = []
        self.current_spieler = "X"
        self.züge = 0
        
        for r in range(3):
            for c in range(3):
                self.figuren[(r, c)] = ""
                if r == 0:
                    self.figuren[(r, c)] = "O"
                elif r == 2:
                    self.figuren[(r, c)] = "X"    

        
    def reset_colors(self):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(fg = "black", highlightbackground="black")

    def select(self, r, c):
        cords = (r, c)
        if self.figuren[cords] != self.current_spieler and len(self.pos) == 0:
            return
        if len(self.pos) != 0 and cords == self.pos[0]:
            return

        self.buttons[r][c].config(fg = "red", highlightbackground="red")
        self.pos.append((cords))

        if len(self.pos) == 2:
            time.sleep(0.1)
            self.reset_colors()
            canmove = self.can_move()
            if canmove:
                self.züge += 1
                self.move()

            if canmove:
                self.current_spieler = "O" if self.current_spieler == "X" else "X"
            if canmove and self.gewinnprüfung(r, c):
                self.button_reset = tk.Button(self.root, text = "New game", command= self.new_game)
                self.button_reset.place(x=100, y=50)
                print("Gewonnen!!")
                return
            
            self.pos = []

            if self.comp and canmove:
                self.comp()
        
        #print("nach random zug: ",self.postionen_zug2)







    def auto(self):
        self.spielfeld_erstellen()
        for _ in range(1000):
            done = False
            while not done:
                done = self.random_zug_auto()
            
            self.spielfeld_erstellen_auto()
        
        self.bewertung_zug6 = self.bewertungen_init(self.züge_6, 100)
        self.bewertung_zug2 = self.bewertungen_init(self.züge_2, 100)
        self.bewertung_zug4 = self.bewertungen_init(self.züge_4, 100)

        print("Zug 2: ", self.züge_2)
        print("Zug 4: ", self.züge_4)
        print("Zug 6: ", self.züge_6)
        print("Zug 2: ", len(self.züge_2), "; Zug 4: ", len(self.züge_4), "; Zug 6: ", len(self.züge_6))
        print("_--------------------")
        print(self.bewertung_zug4)
        print("Finished")

    def mögliche_züge_für_jede_figur(self, eigene_felder, felder):
        figuren_züge = {}
        mögliche_züge = []
        for figur in eigene_felder:

            self.pos.append(figur)
            self.pos.append(0)
            mögliche_züge = []

            # prüfe mit can_move() welche züge erlaubt sind

            for i in felder:
                self.pos[1] = i
                if self.can_move():
                    mögliche_züge.append(i)

            figuren_züge[figur] = mögliche_züge
            self.pos = []



            
    def bewertungen_init(self, züge, bewertung_start):
        d = {}
        for i in züge:
            d[(i[0], i[1])] = bewertung_start
        return d





    def random_zug_auto(self):
        eigene_felder = []
        felder = []
        for i in self.figuren.keys():
            if self.figuren[i] == self.current_spieler:
                eigene_felder.append(i)
            else:
                felder.append(i)
        
        # Zufällige Figur auswählen
        for _ in range(3):
            figur = random.choice(eigene_felder)
            self.pos.append(figur)

            self.pos.append(0)
            mögliche_züge = []

            # prüfe mit can_move() welche züge erlaubt sind

            for i in felder:
                self.pos[1] = i
                if self.can_move():
                    mögliche_züge.append(i)

            if len(mögliche_züge) > 0:
                break
            else:
                self.pos = []
                eigene_felder.remove(figur)

        zug = random.choice(mögliche_züge)
        self.pos[1] = zug
        self.move(True)
        self.züge += 1
        self.current_spieler = "O" if self.current_spieler == "X" else "X"
        self.map_positions()
        #print("Zug 2: ", len(self.postionen_zug2), "; Zug 4: ", len(self.postionen_zug4), "; Zug 6: ", len(self.postionen_zug6))
        if self.gewinnprüfung(zug[0], zug[1]):
            print("Gewonnen!!")
            return True
        self.pos = []
        return False
    


    def computer(self):
        if self.züge == 1:
            züge_bewertung = self.bewertung_zug2
        elif self.züge == 3:
            züge_bewertung = self.bewertung_zug4
        elif self.züge == 5:
            züge_bewertung = self.bewertung_zug6
        else:
            raise Exception("Fehler bei Züge")

        max_belohnung = max(züge_bewertung[j] for j in züge_bewertung)

        züge_alle = []
        for i in züge_bewertung:
            if züge_bewertung[i] > max_belohnung - 21:
                züge_alle.append(i)
        
        züge_möglich = []
        for i in züge_alle:
            self.pos = i
            if self.can_move():
                züge_möglich.append(i)
        
        zug = random.choice(züge_möglich)
        self.pos = zug
        self.move(False)
        self.züge += 1
        self.current_spieler = "O" if self.current_spieler == "X" else "X"
        self.map_positions()
        if self.gewinnprüfung(zug[0], zug[1]):
            print("Gewonnen!!")
            return True
        self.pos = []

            



        
        
    def random_zug(self):
        eigene_felder = []
        felder = []
        for i in self.figuren.keys():
            if self.figuren[i] == self.current_spieler:
                eigene_felder.append(i)
            else:
                felder.append(i)
        
        # Zufällige Figur auswählen
        for _ in range(3):
            figur = random.choice(eigene_felder)
            self.pos.append(figur)

            self.pos.append(0)
            mögliche_züge = []

            # prüfe mit move() welche züge erlaubt sind

            for i in felder:
                self.pos[1] = i
                if self.can_move():
                    mögliche_züge.append(i)

            if len(mögliche_züge) > 0:
                break
            else:
                self.pos = []
                eigene_felder.remove(figur)


        zug = random.choice(mögliche_züge)
        self.pos[1] = zug
        self.move()
        self.züge += 1
        self.current_spieler = "O" if self.current_spieler == "X" else "X"
        self.map_positions()
        
        if self.gewinnprüfung(zug[0], zug[1]):
            self.button_reset = tk.Button(self.root, text = "New game", command= self.new_game)
            self.button_reset.place(x=100, y=50)
            print("Gewonnen!!")
            return 
        self.pos = []
        self.buttons[figur[0]][figur[1]].config(fg = "green", highlightbackground="green")
        self.buttons[zug[0]][zug[1]].config(fg = "green", highlightbackground="green")
        return 

    def map_positions(self):
        d = {}
        if self.züge == 2:
            if self.figuren not in self.postionen_zug2:
                for i in self.figuren:
                    d[i] = self.figuren[i]
                self.züge_2.append(self.pos)
                self.postionen_zug2.append(d)
                
            #print(len(self.postionen_zug2))
        elif self.züge == 4:
            if self.figuren not in self.postionen_zug4:
                for i in self.figuren:
                    d[i] = self.figuren[i]
                self.züge_4.append(self.pos)
                self.postionen_zug4.append(d)

        elif self.züge == 6:
            if self.figuren not in self.postionen_zug6:
                for i in self.figuren:
                    d[i] = self.figuren[i]
                self.züge_6.append(self.pos)
                self.postionen_zug6.append(d)
        

        

    def new_game(self):
        self.button_reset.destroy()
        self.spielfeld_erstellen()

    def can_move(self):
        target = self.pos[0]
        destination = self.pos[1]

        if self.figuren[target] == "":
            #print("Fail!")
            return False
        
        if self.figuren[target] == "X":
            if target[0] - destination[0] != 1:
                #print("Fail!")
                return False
        elif self.figuren[target] == "O":
            if target[0] - destination[0] != -1:
                #print("Fail!")  
                return False
        if self.figuren[destination] != "":
            if abs(target[1] - destination[1]) != 1 or self.figuren[target] == self.figuren[destination]:
                #print("Fail!")
                return False
        else:
            if target[1] - destination[1] != 0:
                #print("Fail!")
                return False

        return True
    
    def move(self, auto):
        target = self.pos[0]
        destination = self.pos[1]
        
        self.figuren[destination] = self.figuren[target]
        self.figuren[target] = ""
        if not auto:
            self.buttons[target[0]][target[1]].config(text = self.figuren[target])
            self.buttons[destination[0]][destination[1]].config(text = self.figuren[destination])
    
    
    def gewinnprüfung(self, r, c):
        # Wenn Bauer am Ende angelangt
        cords = (r, c)
        figur = self.figuren[cords]
        if figur == "X":
            if r == 0:
                return True
            else:
                # Wenn keiner sich mehr bewegen kann
                
                # Überall wo X ist
                list_x = []
                for i in self.figuren:
                    if self.figuren[i] == "X":
                        list_x.append(i)
                
                hindernisse = 0
                for i in list_x:
                    feld_davor = (i[0] - 1, i[1])
                    if i[1] == 1:
                        if self.figuren[feld_davor] != "" and self.figuren[(feld_davor[0], 0)] != "O" and self.figuren[(feld_davor[0], 2)] != "O":
                            hindernisse += 1
                    else:
                        if self.figuren[feld_davor] != "" and self.figuren[(feld_davor[0], 1)] != "O":
                            hindernisse += 1
                
                if len(list_x) == hindernisse:
                    return True
        elif figur == "O":
            if r == 2:
                return True
            
            else:
                # Wenn keiner sich mehr bewegen kann
                
                # Überall wo O ist
                list_o = []
                for i in self.figuren:
                    if self.figuren[i] == "O":
                        list_o.append(i)

                hindernisse = 0
                
                for i in list_o:
                    feld_davor = (i[0] + 1, i[1])
                    if i[1] == 1:
                        if self.figuren[feld_davor] != "" and self.figuren[(feld_davor[0], 0)] != "X" and self.figuren[(feld_davor[0], 2)] != "X":
                            hindernisse += 1
                    else:
                        if self.figuren[feld_davor] != "" and self.figuren[(feld_davor[0], 1)] != "X":
                            hindernisse += 1
                
                if len(list_o) == hindernisse:
                    return True
        # Wenn es keine Bauern gibt
        anzahl_x = 0
        anzahl_o = 0
        for i in self.figuren.values():
            if i == "X":
                anzahl_x += 1
            elif i == "O":
                anzahl_o += 1
        
        if anzahl_x == 0:
            return True
        elif anzahl_o == 0:
            return True
        

root = tk.Tk()

p = hexapawn(root)

p.spielfeld_erstellen()

root.mainloop()