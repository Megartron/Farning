import tkinter as tk
import time
class hexapawn():

    def __init__(self, root):
        self.root = root
        self.root.title("3x3 Grid GUI")
        self.figuren = {}
        self.pos = []
        self.buttons = []
        

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
        print(self.buttons)
        
    def reset_colors(self):
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(fg = "black", highlightbackground="black")

    def select(self, r, c):
        cords = (r, c)
        if len(self.pos) != 0 and cords == self.pos[0]:
            return
        print(self.buttons[cords[0]][cords[1]])
        self.buttons[r][c].config(fg = "red", highlightbackground="red")
        self.pos.append((cords))

        if len(self.pos) == 2:
            time.sleep(0.1)
            self.reset_colors()
            self.move()
            self.pos = []

    def move(self):
        print(self.pos)
        target = self.pos[0]
        destination = self.pos[1]

        if self.figuren[target] == "":
            print("Fail!")
            return
        
        if self.figuren[target] == "X":
            if target[0] - destination[0] != 1:
                print("Fail!")
                return
        elif self.figuren[target] == "O":
            if target[0] - destination[0] != -1:
                print("Fail!")
                return
        if self.figuren[destination] != "":
            if abs(target[1] - destination[1]) != 1 or self.figuren[target] == self.figuren[destination]:
                print("Fail!")
                return
        else:
            if target[1] - destination[1] != 0:
                print("Fail!")
                return
        
        self.figuren[destination] = self.figuren[target]
        self.figuren[target] = ""

        self.buttons[target[0]][target[1]].config(text = self.figuren[target])
        self.buttons[destination[0]][destination[1]].config(text = self.figuren[destination])

root = tk.Tk()

p = hexapawn(root)

p.spielfeld_erstellen()

root.mainloop()