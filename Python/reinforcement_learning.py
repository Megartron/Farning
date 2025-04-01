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
        self.current_spieler = "X"
        self.züge = 0
        self.comp = True
        

    def spielfeld_erstellen(self):
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
        print(self.buttons[cords[0]][cords[1]])
        self.buttons[r][c].config(fg = "red", highlightbackground="red")
        self.pos.append((cords))

        if len(self.pos) == 2:
            time.sleep(0.1)
            self.reset_colors()
            canmove = self.can_move()
            if canmove:
                self.move()

            if canmove:
                self.current_spieler = "O" if self.current_spieler == "X" else "X"
            if canmove and self.gewinnprüfung(r, c):
                print("Gewonnen!!")
                return
            self.züge += 1
            self.pos = []

            if self.comp and canmove:
                self.random_zug()

        
    def random_zug(self):
        eigene_felder = []
        felder = []
        for i in self.figuren.keys():
            if self.figuren[i] == "O":
                eigene_felder.append(i)
            else:
                felder.append(i)
        
        # Zufällige Figur auswählen
        for _ in range(3):
            figur = random.choice(eigene_felder)
            self.pos.append(figur)
            print("Figur: ", figur)
            self.pos.append((0, 0))
            mögliche_züge = []

            # prüfe mit move() welche züge erlaubt sind
            print("felder: ", felder)
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
        self.current_spieler = "X"
        if self.gewinnprüfung(zug[0], zug[1]):
            print("Gewonnen!!")
            return
        self.pos = []



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
    
    def move(self):
        target = self.pos[0]
        destination = self.pos[1]
        
        self.figuren[destination] = self.figuren[target]
        self.figuren[target] = ""

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
