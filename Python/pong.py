import tkinter as tk
import math
import copy
import random

class Pong():
    def __init__(self, root, height, width, resolution):
        self.root = root
        self.canvas = tk.Canvas(root, width=width, height=height, bg="black")
        self.key_tracker = {}
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.spielfeld_größe = (width, height)
        self.ball_pos = (75, 70) # width height
        self.paddle_human_pos = [30, 100]
        self.paddle_comp_pos = [width - 30, int(height/2)]
        self.paddle_size = (12, 50)
        self.punktestand = [0, 0]
        self.moving_speed = 6
        self.ball_size = 20
        self.tick = 0
        self.random = 0.01
        self.resolution = resolution
        self.actions = ("up", "down", "ignore")
        self.verloren = False
        self.tickspeed = 85
        self.wall = False
        self.can_ignore = True
        self.hits = 0
        self.misses = 0
        self.showing_rewards = False
        self.move_sequence = []
        self.quadrant_sequence = []
        self.real_resolution = 7
        self.fails = 0
        self.centers = self.calc_centers(10)
        print(self.centers)

        self.save = [] # ball_pos, ball_vector, paddle_y, paddle_move

        self.comp_kontakt_mit_ball = False
        self.letzter_zustand = (0, 0)
        self.spiel_zustand = [[0 for _ in range(self.resolution)] for _ in range(self.resolution)]
        self.state = () # spielzustand, paddle high
        self.q_tabelle = {(("ball pos"), "y", "y_vector"): "reward"}
        self.q_super_table = {(("ball pos"), "quadrant"): "reward"}

        self.ball_vector = (10, -10)

        scale = tk.Scale(self.root, from_=1, to=100, length=400, orient="horizontal",
                 label="Speed in %", command=self.set_speed)
        scale.pack()
        scale.set(50)

        scale1 = tk.Scale(self.root, from_=1, to=100, length=400, orient="horizontal",
                 label="Random", command=self.set_random)
        scale1.pack()
        scale.set(self.random)

        button = tk.Button(root, text="Turn on Wall", command=self.set_wall)
        button.pack()
        button2 = tk.Button(root, text="Can Ignore Action", command=self.set_canIgnore)
        button2.pack()
        button3 = tk.Button(root, text="Show Rewards", command=self.show_rewards)
        button3.pack()
        button4 = tk.Button(root, text="Reset", command=self.reset)
        button4.pack()

        self.show_grid = False
        self.spielfeld_zeichnen()
        self.canvas.pack(expand=True)

    def calc_centers(self, areas):
        edge_margin = self.paddle_size[1]/2 + 5
        height = self.spielfeld_größe[1] - 2 * edge_margin
        centers = []
        dis_between_centers = height * (1/areas)
        start = height * (1/(2*areas))
        for i in range(areas):
            centers.append(start + i * dis_between_centers + edge_margin)
        return tuple(centers)
    
    def show_rewards(self):
        self.showing_rewards = not self.showing_rewards

    def set_canIgnore(self):
        self.can_ignore = not self.can_ignore
        print(self.can_ignore)

    def set_wall(self):
        self.wall = not self.wall
        print(self.wall)

    def set_random(self, r):
        self.random = int(r)/100
        print(self.random)

    def set_speed(self, speed):
        maxspeed = 300
        self.tickspeed = maxspeed + 1 - int((int(speed)/100) * maxspeed)
    
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
    
    def move_computer(self, action, paddle_y) -> int:
        if action == "up":
            if (paddle_y + self.paddle_size[1] + self.moving_speed >= self.spielfeld_größe[1] - 10):
                return self.spielfeld_größe[1] - 10 - self.paddle_size[1]
            else:
                return paddle_y + self.moving_speed
        elif action == "down":
            if (paddle_y - self.paddle_size[1] - self.moving_speed <= 10):
                return 10 + self.paddle_size[1]
            else:
                return paddle_y - self.moving_speed
        elif action == "ignore":
            return paddle_y

    def round_to_x(sefl, number, x = 1.5) -> float:
        """
        Rounds a number to the nearest multiple of x.
        e.g., round_to_x(9.34, 0.5) -> 9.5
        """
        if x == 0:
            return float(number)
        return round(number / x) * x

    def kreis_zeichnen(self, x: int, y: int, r: int, color: str) -> None:
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        self.canvas.create_oval(x0, y0, x1, y1, fill = color)
    
    def checkPaddleCollisionImproved(self, paddle_pos, bx, by):
        px, py = paddle_pos
        pw, ph = self.paddle_size[0] / 2, self.paddle_size[1] / 2
        br = self.ball_size
        
        p_left = px - pw
        p_right = px + pw
        p_top = py - ph
        p_bottom = py + ph

        # 1. Check for collision
        if (bx + br >= p_left and bx - br <= p_right) and \
        (by + br >= p_top and by - br <= p_bottom):
            
            vx, vy = self.ball_vector
            
            # 2. RESOLVE POSITION (The Fix)
            # Determine if this is the left or right paddle to push the ball out
            if px < self.spielfeld_größe[0] / 2: # Left Paddle
                self.ball_pos = (p_right + br + 1, by) # Teleport to just outside the right edge
            else: # Right Paddle
                self.ball_pos = (p_left - br - 1, by) # Teleport to just outside the left edge

            # 3. Calculate new velocities
            new_vx = -vx
            self.punktestand[1] += 1
            

            relative_intersect_y = (by - py) / ph
            new_vy = self.round_to_x(relative_intersect_y * 5)
            return (new_vx, new_vy)

        return -1

    def ball_bewegen(self):
        new_pos = (self.ball_pos[0] + self.ball_vector[0], self.ball_pos[1] + self.ball_vector[1])
        x, y = new_pos

        # An Wand abprallen
        width, height = self.spielfeld_größe
        wall_dis = self.paddle_size[0] + 30 if self.wall else 0
        if x <= 10 + self.ball_size + wall_dis or x >= width - 10 - self.ball_size:
            self.ball_vector = (self.ball_vector[0] * -1, self.ball_vector[1])
            if (x <= 10 + self.ball_size + wall_dis):
                if not self.wall:
                    self.reset()
                self.save = [self.ball_vector, self.ball_pos, self.paddle_comp_pos]
            else:
                self.punktestand[0] += 1
                self.verloren = True
            new_pos = self.ball_pos
        if y <= 10 + self.ball_size or y >= height - 10 - self.ball_size:
            self.ball_vector = (self.ball_vector[0], self.ball_vector[1] * -1)
            new_pos = self.ball_pos

        return new_pos
    
    def simulate_ball(self) -> tuple:
        new_pos = (self.ball_pos[0] + self.ball_vector[0], self.ball_pos[1] + self.ball_vector[1])
        x, y = new_pos
        new_vector = self.ball_vector

        # An Wand abprallen
        width, height = self.spielfeld_größe
        wall_dis = self.paddle_size[0] + 30 if self.wall else 0
        if x <= 10 + self.ball_size + wall_dis or x >= width - 10 - self.ball_size:
            new_vector = (self.ball_vector[0] * -1, self.ball_vector[1])
            new_pos = self.ball_pos
        if y <= 10 + self.ball_size or y >= height - 10 - self.ball_size:
            new_vector = (self.ball_vector[0], self.ball_vector[1] * -1)
            new_pos = self.ball_pos

        return (new_pos, new_vector)

    def paddle_pos_reward(self, y, max_reward, min_reward, k=0.1):
        center = self.spielfeld_größe[1]/2
        distance = abs(y - center)
        # k controls how fast the reward drops (higher k = faster drop)
        reward = min_reward + (max_reward - min_reward) * math.exp(-k * distance)
        if (self.misses > 120):
            return -1 * float(reward)
        return float(reward)

    def get_ballpos(self, x, y):
        width, height = self.spielfeld_größe
        grid_width = width - 20
        grid_height = height - 20

        dis_grids_width = grid_width / self.resolution
        dis_grids_height = grid_height / self.resolution

        state_x = int((x - 10) // dis_grids_width)
        state_y = int((y - 10) // dis_grids_height)
    
        state_x = max(0, min(self.resolution - 1, state_x))
        state_y = max(0, min(self.resolution - 1, state_y))
        
        return (state_x, state_y)
    
    def get_paddle_pos (self, y, resolution) -> int:
        return y//resolution

    def reset(self):
        width, height = self.spielfeld_größe
        self.ball_pos = (75, 70)
        self.paddle_comp_pos = [width - 30, int(height/2)]
        self.verloren = False
        self.ball_vector = (8, -8)
        self.comp_kontakt_mit_ball = False

    def run_back(self):
        self.ball_vector, self.ball_pos, self.paddle_comp_pos = self.save
        self.comp_kontakt_mit_ball = False
        self.verloren = False

    def get_vector(self):
        return (self.ball_vector[0], self.round_to_x(self.ball_vector[1]))

    def spielfeld_zeichnen(self):
        # Rände
        width, height = self.spielfeld_größe
        self.canvas.create_line(10, 10, width - 10, 10)
        self.canvas.create_line(10, height - 10, width - 10, height - 10)
        self.canvas.create_line(10, 10, 10, height - 10)
        self.canvas.create_line(width - 10, 10, width - 10, height - 10)

        # Grid lines:
        dis_grids_width = (width - 20)/self.resolution
        dis_grids_height = (height - 20)/self.resolution
        if (self.show_grid):
            for i in range(self.resolution):
                self.canvas.create_line(10 + int(round(i * dis_grids_width)), 10, 10 + int(round(i * dis_grids_width)), height - 10)
                self.canvas.create_line(10, 10 + int(round(i * dis_grids_height)), width - 10, 10 + int(round(i * dis_grids_height)))
            self.canvas.create_line(10 + int(round((i + 1) * dis_grids_width)), 10, 10 + int(round((i + 1) * dis_grids_width)), height - 10)
        
        # Besetzes Feld markieren
        for i in range(len(self.spiel_zustand)):
            for j in range(len(self.spiel_zustand[i])):
                if self.spiel_zustand[i][j] != 1: continue
                x = j * dis_grids_width + 10
                y = i * dis_grids_height + 10
                self.canvas.create_rectangle(
                    x, y,
                    round(x + dis_grids_width),
                    round(y + dis_grids_height),
                    fill="blue")

        # Ball
        x, y = self.ball_pos
        self.kreis_zeichnen(x, y, self.ball_size, "#FFFFFF")

        # Paddle
        paddle_width, paddle_height = self.paddle_size
        x, y = self.paddle_human_pos
        self.canvas.create_rectangle(x - paddle_width, y - paddle_height, x + paddle_width, y + paddle_height, fill="#FFFFFF")
        x, y = self.paddle_comp_pos
        self.canvas.create_rectangle(x - paddle_width, y - paddle_height, x + paddle_width, y + paddle_height, fill="#FFFFFF")

        # Rewards
        current_quadrant = self.get_quadrant(self.paddle_comp_pos[1])
        quadrant_rewards = [self.q_super_table.get((self.get_ballpos(self.ball_pos[0], self.ball_pos[1]), i, self.get_vector()), 0)
                            for i in range(len(self.centers))]
        seen_before = max(quadrant_rewards) != 0
        chosen = self.get_best_quadrant(current_quadrant)
        for i in range(len(quadrant_rewards)):
            center = self.centers[i]
            reward = int(quadrant_rewards[i])
            if (reward < 0):
                self.kreis_zeichnen(width - 50, center, 7, self.rgb_to_hex(255, 255 + reward, 0))
            else:
                self.kreis_zeichnen(width - 50, center, 7, self.rgb_to_hex(255 - reward, 255, 0))
        if seen_before:
            self.kreis_zeichnen(width - 60, self.centers[chosen], 7, "#FF00F2")
        else:
            self.kreis_zeichnen(width - 60, self.centers[chosen], 7, "#FFFFFF")


        # Punktestand 
        self.canvas.create_text(
            round(self.spielfeld_größe[0] / 2), 30,
            text=f"{self.punktestand[0]} : {self.punktestand[1]}",
            font=("Times New Roman", 25, "bold"),
            fill="white"
        )
    
    def rgb_to_hex(self, r, g, b):
        r = max(0, min(255, int(r)))
        g = max(0, min(255, int(g)))
        b = max(0, min(255, int(b)))
    
        return "#{:02x}{:02x}{:02x}".format(r, g, b).upper()

    def comp_verloren(self) -> bool:
        return self.ball_pos[0] >= self.spielfeld_größe[0] - 10 - self.ball_size

    def neuer_zustand(self):
        x, y = self.spielfeld_größe
        i = int((self.ball_pos[1] - 10) // ((y - 20)/self.resolution))
        j = int((self.ball_pos[0] - 10) // ((x - 20)/self.resolution))
        self.spiel_zustand[i][j] = 1
        self.letzter_zustand = (i, j)
    
    def get_tuple_copy(self, l) -> tuple:
            return tuple(tuple(copy.deepcopy(i)) for i in l)

    def get_collision(self):
        x, y = self.ball_pos
        if (paddle_collision := self.checkPaddleCollisionImproved(self.paddle_human_pos, x, y)) != -1 and not self.wall:
            self.ball_vector = paddle_collision
            self.save = [self.ball_vector, self.ball_pos, self.paddle_comp_pos]
        elif (paddle_collision := self.checkPaddleCollisionImproved(self.paddle_comp_pos, x, y)) != -1:
            self.comp_kontakt_mit_ball = True
            self.ball_vector = paddle_collision

    def is_between(self, x, max, min) -> bool:
        return x > min and x < max

    def get_quadrant(self, y) -> int:
        quadrant = self.centers.index(min(self.centers, key=lambda val: abs(val - y)))
        return quadrant
            
    def update_q_table(self, verloren, state: tuple, quadrant_state, a: float, y: float, reward_last: int):
        if (verloren):
            reward = -200
            self.fails += 1
        elif self.comp_kontakt_mit_ball:
            reward = 333
            self.comp_kontakt_mit_ball = False
            self.fails = 0
        else:
            reward = 0
        
        if (self.ball_pos[0] < self.spielfeld_größe[0]/3 - 40 or self.ball_vector[0] < 0):
            reward += self.paddle_pos_reward(self.paddle_comp_pos[1], 10, -10, 0.043)

        if (self.showing_rewards):
            print(reward)

        best_next = 0
        best_next = max(self.get_next_state_reward("up"), self.get_next_state_reward("down"), self.get_next_state_reward("ignore")) if self.can_ignore else max(self.get_next_state_reward("up"), self.get_next_state_reward("down"))
        best_next_quadrant = max(self.get_next_qudrant_reward("up"), self.get_next_qudrant_reward("down"), self.get_next_qudrant_reward("ignore")) if self.can_ignore else max(self.get_next_qudrant_reward("up"), self.get_next_qudrant_reward("down"))

        self.q_tabelle[state] = (1 - a) * self.q_tabelle[state] + a * (reward + y * best_next)
        self.q_super_table[quadrant_state] = (1 - a) * self.q_super_table[quadrant_state] + a * (reward + y * best_next_quadrant)

        if (not (reward < 50 and reward > -50)):
            for i in range(2, reward_last + 1):
                if (i < len(self.move_sequence)):
                    self.q_tabelle[self.move_sequence[-i]] = (1 - a) * self.q_tabelle[self.move_sequence[-i]] + a * reward * y**(i - 1)
                    self.q_super_table[self.quadrant_sequence[-i]] = (1 - a) * self.q_super_table[self.quadrant_sequence[-i]] + a * reward * y**(i - 1)
            self.move_sequence = []
            self.quadrant_sequence = []
        else:
            for i in range(2, 4):
                if (i < len(self.move_sequence)):
                    self.q_tabelle[self.move_sequence[-i]] = (1 - a) * self.q_tabelle[self.move_sequence[-i]] + a * reward * y**(i - 1)
                    self.q_super_table[self.quadrant_sequence[-i]] = (1 - a) * self.q_super_table[self.quadrant_sequence[-i]] + a * reward * y**(i - 1)
        
    def get_next_qudrant_reward(self, action) -> int:
        new_ball_pos, new_vector = self.simulate_ball()
        next_quadrant = self.get_quadrant(self.move_computer(action, self.paddle_comp_pos[1]))
        return self.q_super_table.get((self.get_ballpos(new_ball_pos[0], new_ball_pos[1]), next_quadrant, new_vector), 0)

    def get_next_state_reward(self, action) -> int:
        new_ball_pos, new_vector = self.simulate_ball()
        current_pos = self.get_paddle_pos(self.paddle_comp_pos[1], self.real_resolution)
        next_pos = current_pos + 1 if action == "up" else current_pos - 1
        return self.q_tabelle.get((self.get_ballpos(new_ball_pos[0], new_ball_pos[1]), next_pos, new_vector), 0)
    
    def get_best_quadrant(self, current_quadrant) -> int:
        
        quadrant_rewards = [self.q_super_table.get((self.get_ballpos(self.ball_pos[0], self.ball_pos[1]), i, self.get_vector()), 0)
                            for i in range(len(self.centers))]
        
        if (self.showing_rewards):
            print(quadrant_rewards)
        
        max_val = max(quadrant_rewards)
        max_qudrants = [i for i, val in enumerate(quadrant_rewards) if val == max_val]
        nearest = min([abs(q - current_quadrant) for q in max_qudrants])
        best_quadrants = [quadrant for quadrant in max_qudrants if abs(quadrant - current_quadrant) == nearest]
        return random.choice(best_quadrants)

    def get_next_move(self, e) -> str:
        if (random.random() < e):
            return random.choice(self.actions)
        
        current_quadrant = self.get_quadrant(self.paddle_comp_pos[1])
        best_quadrant = self.get_best_quadrant(current_quadrant)

        if (current_quadrant == best_quadrant):
            quality = (self.get_next_state_reward("up"), self.get_next_state_reward("down"), self.get_next_state_reward("ignore")) if self.can_ignore else (self.get_next_state_reward("up"), self.get_next_state_reward("down"))
                
            best = max(quality)
            best_moves = []
            for r in range(len(quality)):
                if (quality[r] == best):
                    best_moves.append(self.actions[r])
            return random.choice(best_moves)

        elif (current_quadrant < best_quadrant):
            return "up"
        else:
            return "down"

    def update(self) -> None:
        self.canvas.delete("all")
        self.tick += 1
        self.state = self.game_tick() # return ein Tuple mit aktuellen Ballposition im Spielfeld und y-Kord des comp. Paddles
        quadrant_state = (self.state[0], self.get_quadrant(self.paddle_comp_pos[1]), self.get_vector())
        self.move_sequence.append(self.state)
        self.quadrant_sequence.append(quadrant_state)
        if (self.state != None):
            if (self.q_tabelle.get(self.state) == None):
                self.q_tabelle[self.state] = 0 # reward für Aktionen (up, down)

            if (self.q_super_table.get(quadrant_state) == None):
                self.q_super_table[quadrant_state] = 0

            self.update_q_table(self.verloren, self.state, quadrant_state, 0.4, 0.99, 88)
        if (self.verloren):
            if self.save != []:
                self.run_back()
            else:
                self.reset()

        if (self.fails > 50):
            self.random = (self.fails - 30)/100
        elif (self.fails > 125):
            self.reset()
        else:
            self.random = 0.001

        self.neuer_zustand()
        self.spielfeld_zeichnen()

        self.root.after(self.tickspeed, self.update)
    
    def game_tick(self) -> tuple:
        self.spiel_zustand[self.letzter_zustand[0]][self.letzter_zustand[1]] = 0
        self.ball_pos = self.ball_bewegen()
        
        if self.key_tracker.get("w", False):
            self.move_down()
        elif self.key_tracker.get("s", False):
            self.move_up()

        comp_move = self.get_next_move(self.random)
        if (self.showing_rewards):
            print("Chosen move: ", comp_move)
        x, y = self.paddle_comp_pos
        self.paddle_comp_pos = [x, self.move_computer(comp_move, y)]

        self.get_collision()
        return (self.get_ballpos(self.ball_pos[0], self.ball_pos[1]), self.get_paddle_pos(self.paddle_comp_pos[1], self.real_resolution), self.get_vector())
 
    def training_against_wall(self, episodes):
        self.wall = True
        revise = 0.23
        self.can_ignore = True
        progress = 0.1
        for _ in range(episodes):
            self.ball_pos = self.ball_bewegen()
            comp_move = self.get_next_move(self.random)
            x, y = self.paddle_comp_pos
            self.paddle_comp_pos = [x, self.move_computer(comp_move, y)]
            self.get_collision()
            self.state = (self.get_ballpos(self.ball_pos[0], self.ball_pos[1]), self.get_paddle_pos(self.paddle_comp_pos[1], self.real_resolution), self.get_vector())
            quadrant_state = (self.state[0], self.get_quadrant(self.paddle_comp_pos[1]), self.get_vector())
            self.quadrant_sequence.append(quadrant_state)
            self.move_sequence.append(self.state)
            if (self.q_tabelle.get(self.state) == None):
                self.q_tabelle[self.state] = 0
            if (self.q_super_table.get(quadrant_state) == None):
                self.q_super_table[quadrant_state] = 0

            self.update_q_table(self.verloren, self.state, quadrant_state, 0.4, 0.99, 88)

            if (self.verloren):
                if self.save != []:
                    self.run_back()
                else:
                    self.reset()
            
            if (self.fails > 300):
                self.random = (self.fails - 330)/100
            elif (self.fails > 400):
                self.reset()
            else:
                self.random = 0.001
            
            if (_ > episodes * progress):
                print(round(progress * 100), "'%' finished")
                #print("Hits: ", self.hits, " Misses: ", self.misses, " Accuracy: ", self.hits/(self.misses + self.hits))
                self.misses = 0
                progress += 0.1
                if (progress > revise):
                    self.reset()
                    revise += 0.15
                    print("Revise")


if __name__ == "__main__":

    root = tk.Tk()
    pong = Pong(root, 520, 780, 10)
    pong.training_against_wall(500_000)
    pong.update()

    root.mainloop()
