import tkinter as tk

class Pong():
    def __init__(self, root, height, width):
        self.root = root
        self.canvas = tk.Canvas(root, width=width, height=height, bg="black")
        self.root.bind("w", self.move_down)
        self.root.bind("s", self.move_up)
        self.spielfeld_größe = (width, height)
        self.ball_pos = (20, 20)
        self.paddle_human_pos = [30, 100]
        self.paddle_comp_pos = [width - 30, 140]
        self.paddle_size = (2, 14)
        self.moving_speed = 3

        self.spielfeld_zeichnen()
        self.canvas.pack(expand=True)

    def move_up(self, event):
        print("move up")
        y = self.paddle_human_pos[1]
        if (y + self.paddle_size[1] + self.moving_speed >= self.spielfeld_größe[1] - 10):
            self.paddle_human_pos[1] = self.spielfeld_größe[1] - 10 - self.paddle_size[1]
        else:
            self.paddle_human_pos[1] = y + self.moving_speed

    def move_down(self, event):
        y = self.paddle_human_pos[1]
        print(self.paddle_human_pos)
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

    def spielfeld_zeichnen(self):
        # Rände
        width, height = self.spielfeld_größe
        self.canvas.create_line(10, 10, width - 10, 10)
        self.canvas.create_line(10, height - 10, width - 10, height - 10)
        self.canvas.create_line(10, 10, 10, height - 10)
        self.canvas.create_line(width - 10, 10, width - 10, height - 10)

        # Ball
        x, y = self.ball_pos
        self.kreis_zeichnen(x, y, 4, "#FFFFFF")

        # Paddle
        paddle_width, paddle_height = self.paddle_size
        x, y = self.paddle_human_pos
        self.canvas.create_rectangle(x - paddle_width, y - paddle_height, x + paddle_width, y + paddle_height, fill="#FFFFFF")
        x, y = self.paddle_comp_pos
        self.canvas.create_rectangle(x - paddle_width, y - paddle_height, x + paddle_width, y + paddle_height, fill="#FFFFFF")
        

    def update(self) -> None:
        self.canvas.delete("all")
        self.spielfeld_zeichnen()
        self.root.after(100, self.update)

if __name__ == "__main__":

    root = tk.Tk()
    pong = Pong(root, 200, 300)
    pong.update()

    root.mainloop()
