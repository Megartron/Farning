import tkinter as tk
import math

class Pong():
    def __init__(self, root, height, width):
        self.root = root
        self.canvas = tk.Canvas(root, width=width, height=height, bg="black")
        self.key_tracker = {}
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.spielfeld_größe = (width, height)
        self.ball_pos = (60, 60)
        self.paddle_human_pos = [30, 100]
        self.paddle_comp_pos = [width - 30, 140]
        self.paddle_size = (6, 42)
        self.punktestand = (0, 0)
        self.moving_speed = 5
        self.ball_size = 12
        self.tick = 0

        self.ball_vector = (6, -6)

        self.spielfeld_zeichnen()
        self.canvas.pack(expand=True)
    
    def on_key_press(self, event):
        self.key_tracker[event.keysym] = True

    def on_key_release(self, event):
        self.key_tracker[event.keysym] = False

    def move_up(self):
        y = self.paddle_human_pos[1]
        if (y + self.paddle_size[1] + self.moving_speed >= self.spielfeld_größe[1] - 10):
            self.paddle_human_pos[1] = self.spielfeld_größe[1] - 10 - self.paddle_size[1]
        else:
            self.paddle_human_pos[1] = y + self.moving_speed

    def move_down(self):
        y = self.paddle_human_pos[1]
        if (y - self.paddle_size[1] - self.moving_speed <= 10):
            self.paddle_human_pos[1] = 10 + self.paddle_size[1]
        else:
            self.paddle_human_pos[1] = y - self.moving_speed

    def kreis_zeichnen(self, x: int, y: int, r: int, color: str) -> None:
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        self.canvas.create_oval(x0, y0, x1, y1, fill = color)

    def checkPaddleKollision(self, paddle_pos, bx, by):
        px, py = paddle_pos
        
        dis =  math.sqrt((bx - px)**2 + (by - py) ** 2)
        width, height = self.paddle_size
        dis_to_corners = ( # Die Ecken des Paddles im Uhrzeigersinn
            math.sqrt((bx - (px + width))**2 + (by - (py + height)) ** 2),
            math.sqrt((bx - (px + width))**2 + (by - (py - height)) ** 2),
            math.sqrt((bx - (px - width))**2 + (by - (py - height)) ** 2),
            math.sqrt((bx - (px - width))**2 + (by - (py + height)) ** 2)
        )
        
        is_same_y = by >= py - height and by <= py + height
        is_same_x = bx >= px - width and bx <= px + width

        if is_same_y:
            correct_paddle = -1 if px < self.spielfeld_größe[0] / 2 else 1 # -1 für linken Paddle, 1 für rechten Paddle
            furthest_point = bx + self.ball_size * correct_paddle
            if (furthest_point <= px + width and correct_paddle == -1) or (furthest_point >= px - width and correct_paddle == 1):
                return (self.ball_vector[0] * -1, self.ball_vector[1])
        elif is_same_x:
            correct_edge = -1 if py < self.ball_pos[1] else 1
            furthest_point = by + self.ball_size * correct_edge
            if (furthest_point <= py + height and correct_edge == -1) or (furthest_point >= py - height and correct_edge == 1):
                return (self.ball_vector[0], self.ball_vector[1] * -1)
        elif min(dis_to_corners) <= self.ball_size:
            return (self.ball_vector[0] * -1, self.ball_vector[1] * -1)

        return -1

    
    def ball_bewegen(self):
        new_pos = (self.ball_pos[0] + self.ball_vector[0], self.ball_pos[1] + self.ball_vector[1])
        x, y = new_pos

        # An Wand abprallen
        width, height = self.spielfeld_größe
        if x <= 10 + self.ball_size or x >= width - 10 - self.ball_size:
            self.ball_vector = (self.ball_vector[0] * -1, self.ball_vector[1])
            new_pos = self.ball_pos
        if y <= 10 + self.ball_size or y >= height - 10 - self.ball_size:
            self.ball_vector = (self.ball_vector[0], self.ball_vector[1] * -1)
            new_pos = self.ball_pos
        
        # Kollision mit Paddles
        if (paddle_collision := self.checkPaddleKollision(self.paddle_human_pos, x, y)) != -1:
            self.ball_vector = paddle_collision
            new_pos = self.ball_pos
        elif (paddle_collision := self.checkPaddleKollision(self.paddle_comp_pos, x, y)) != -1:
            self.ball_vector = paddle_collision
            new_pos = self.ball_pos

        self.ball_pos = new_pos

    def spielfeld_zeichnen(self):
        # Rände
        width, height = self.spielfeld_größe
        self.canvas.create_line(10, 10, width - 10, 10)
        self.canvas.create_line(10, height - 10, width - 10, height - 10)
        self.canvas.create_line(10, 10, 10, height - 10)
        self.canvas.create_line(width - 10, 10, width - 10, height - 10)

        # Ball
        x, y = self.ball_pos
        self.kreis_zeichnen(x, y, self.ball_size, "#FFFFFF")

        # Paddle
        paddle_width, paddle_height = self.paddle_size
        x, y = self.paddle_human_pos
        self.canvas.create_rectangle(x - paddle_width, y - paddle_height, x + paddle_width, y + paddle_height, fill="#FFFFFF")
        x, y = self.paddle_comp_pos
        self.canvas.create_rectangle(x - paddle_width, y - paddle_height, x + paddle_width, y + paddle_height, fill="#FFFFFF")

        # Punktestand 
        self.canvas.create_text(
            round(self.spielfeld_größe[0] / 2), 30,
            text=f"{self.punktestand[0]} : {self.punktestand[1]}",
            font=("Times New Roman", 25, "bold"),
            fill="white"
        )
        

    def update(self) -> None:
        self.canvas.delete("all")
        self.tick += 1
        self.new_tick()
        self.root.after(20, self.update)
    
    def new_tick(self):

        self.ball_bewegen()

        if self.key_tracker.get("w", False):
            self.move_down()
        elif self.key_tracker.get("s", False):
            self.move_up()

        self.spielfeld_zeichnen()

if __name__ == "__main__":

    root = tk.Tk()
    pong = Pong(root, 600, 900)
    pong.update()

    root.mainloop()
