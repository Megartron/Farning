import arcade
import arcade.gui 
import random

class TTT(arcade.Window):
    def __init__(self): 
        super().__init__(600, 600, "Tic Tac Toe")
        self.start = False
        self.win = "none"
        self.spieler1 = "Mensch"
        self.spieler2 = "Computer"
        self.aktueller_spieler = self.spieler1
        self.verzögerung = 2


    #def startmenu(self):
     #   self.spielsteinliste = arcade.SpriteList()
     #   while not self.start:
     #       a = 0
      #  self.setup()

        
        
    def setup(self):
        self.start = True
        self.win = "none"
        self.spielsteinliste = arcade.SpriteList()
        audioBG = arcade.load_sound("Hintergrundmusik2.wav", False)
        self.audioX = arcade.load_sound("9mm-pistol-shot-6349.wav", False)
        self.audioO = arcade.load_sound("distant-explosion-80398 (online-audio-converter.com).wav", False)
        self.currentaudio = self.audioX
        self.symbol = "O"
        self.sprite = "Backgroundcolor.png"
        self.spielfeld = [["","",""],
                          ["","",""],
                          ["","",""]]
        arcade.play_sound(audioBG, 1.0, 0)
    
    def __gewinnprüfung(self):
        #Reihen
        if (self.spielfeld[0][0] == "O" and self.spielfeld[0][1] == "O" and self.spielfeld[1][2] == "O") or  (self.spielfeld[1][0] == "O" and self.spielfeld[1][1] == "O" and self.spielfeld[0][2] == "O") or  (self.spielfeld[2][0] == "O" and self.spielfeld[2][1] == "O" and self.spielfeld[2][2] == "O"):
            self.win = "O"
        elif (self.spielfeld[0][0] == "X" and self.spielfeld[0][1] == "X" and self.spielfeld[0][2] == "X") or  (self.spielfeld[1][0] == "X" and self.spielfeld[1][1] == "X" and self.spielfeld[1][2] == "X") or  (self.spielfeld[2][0] == "X" and self.spielfeld[2][1] == "O" and self.spielfeld[2][2] == "X"):
            self.win = "X"
        #Spalten
        elif (self.spielfeld[0][0] == "X" and self.spielfeld[1][0] == "X" and self.spielfeld[2][0] == "X") or (self.spielfeld[0][1] == "X" and self.spielfeld[1][1] == "X" and self.spielfeld[2][1] == "X") or (self.spielfeld[0][2] == "X" and self.spielfeld[1][2] == "X" and self.spielfeld[2][2] == "X"):
            self.win = "X"
        elif (self.spielfeld[0][0] == "O" and self.spielfeld[1][0] == "O" and self.spielfeld[2][0] == "O") or (self.spielfeld[0][1] == "O" and self.spielfeld[1][1] == "O" and self.spielfeld[2][1] == "O") or (self.spielfeld[0][2] == "O" and self.spielfeld[1][2] == "O" and self.spielfeld[2][2] == "O"):
            self.win = "O"
        #Kreuz
        elif (self.spielfeld[0][0] == "X" and self.spielfeld[1][1] == "X" and self.spielfeld[2][2] == "X") or (self.spielfeld[0][2] == "X" and self.spielfeld[1][1] == "X" and self.spielfeld[2][0] == "X"):
            self.win = "X"
        elif (self.spielfeld[0][0] == "O" and self.spielfeld[1][1] == "O" and self.spielfeld[2][2] == "O") or (self.spielfeld[0][2] == "O" and self.spielfeld[1][1] == "O" and self.spielfeld[2][0] == "O"):
            self.win = "O"

    def __Koordinaten_feldmittelpunkt(self, x: int, y: int):
        return (x // 200 * 200 + 100, y // 200 * 200 +100)
    



    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        print(self.spielfeld)
        print("-------------")
        print(button)
        print(modifiers)
        print(x)
        print(y)
        self.symbol = "X" if self.symbol== "O" else "O"
        if self.symbol == "X":
            spielstein = arcade.Sprite("Backgroundcolor.png", 0.2)
        else:
            spielstein = arcade.Sprite("1000_F_601211158_bu0EaLaEqZwLyweHdtsxJf8GfDkMO7hI.jpg", 0.2)
        spielstein_position = self.__Koordinaten_feldmittelpunkt(x, y)
        arcade.play_sound(self.currentaudio,5.0,0)
        print("x " +str(x//200))
        print("y " +str( y//200))
        if self.spielfeld[x//200][y//200] == "" and self.start and self.aktueller_spieler == "Mensch":
            self.spielfeld[x//200][y//200] = self.symbol
            spielstein.center_x = spielstein_position[0]
            spielstein.center_y = spielstein_position[1]
            self.spielsteinliste.append(spielstein)
            #self.aktueller_spieler = self.spieler2
        self.__gewinnprüfung()


        
            
    
    
    def on_key_press(self, symbol: int, modifiers: int):
        print(symbol)
        if symbol == 113:
            arcade.exit()

        if symbol == 114:
            self.setup()

        if symbol == 115:
            self.start = True
            self.setup()
            
    def on_draw(self):
        arcade.gui.UIManager(auto_enable=True)
        if self.win != "none":
            arcade.draw_lrwh_rectangle_textured(0, 0, 600, 600, arcade.load_texture("startbild.jpg"))
            arcade.draw_text(self.win + " has won!",120.0,300.0, arcade.color.GREEN,40,80) 
        elif not self.start:
            arcade.draw_lrwh_rectangle_textured(0, 0, 600, 600, arcade.load_texture("startbild.jpg"))
            arcade.draw_text("Press 'S' To Start",120.0,300.0, arcade.color.GREEN,40,80) 
        elif self.start:
            arcade.draw_lrwh_rectangle_textured(0, 0, 600, 600, arcade.load_texture("Backgroundcolor.png"))
            self.spielsteinliste.draw()

            arcade.draw_line(20, 400, 580, 400, (0, 0, 0), 16)
            arcade.draw_line(20, 200, 580, 200, (0, 0, 0), 16)
            arcade.draw_line(200, 20, 200, 580, (0, 0, 0), 16)
            arcade.draw_line(400, 20, 400, 580, (0, 0, 0), 16)

TTT()

arcade.run()

# 100 600
