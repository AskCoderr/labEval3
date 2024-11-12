import tkinter as tk

root = tk.Tk()
root.title("Ping Pong Game")
root.resizable(False, False)
root.geometry("600x400")


class GUIandLogic():
    def __init__(self, main_loop):
        self.canvas = tk.Canvas(root, width=600, height=400, bg="black")
        self.canvas.pack()
        self.paddle1 = self.canvas.create_rectangle(10,
                                                    150,
                                                    20,
                                                    250,
                                                    fill="white")
        self.paddle2 = self.canvas.create_rectangle(580,
                                                    150,
                                                    590,
                                                    250,
                                                    fill="white")
        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill="red")
        self.player1_score = 0
        self.player2_score = 0
        self.x_velocity = 0.3  # im considering the unit as pixel/10 ms
        self.y_velocity = 0.3
        self.scoredisplay = self.canvas.create_text(
            300,
            50,
            text=f"{self.player1_score} - {self.player2_score}",
            fill="yellow",
            font=("Helvetica", 24))
        self.canvas.itemconfig(
            self.scoredisplay,
            text=f"{self.player1_score} - {self.player2_score}")
        self.ps = 20
        self.collision_flag = False
        self.paddle1top = [
            self.canvas.coords(self.paddle1)[2],
            self.canvas.coords(self.paddle1)[1]
        ]
        self.paddle1bottom = [
            self.canvas.coords(self.paddle1)[2],
            self.canvas.coords(self.paddle1)[3]
        ]
        self.paddle2top = [
            self.canvas.coords(self.paddle2)[0],
            self.canvas.coords(self.paddle2)[1]
        ]
        self.paddle2bottom = [
            self.canvas.coords(self.paddle2)[0],
            self.canvas.coords(self.paddle2)[3]
        ]
        self.ballMiddleLeft = [
            self.canvas.coords(self.ball)[0],
            self.canvas.coords(self.ball)[3] - ((self.canvas.coords(self.ball)[3] - self.canvas.coords(self.ball)[1])/2)
        ]
        self.ballMiddleRight = [
            self.canvas.coords(self.ball)[2],
            self.canvas.coords(self.ball)[3] - ((self.canvas.coords(self.ball)[3] - self.canvas.coords(self.ball)[1])/2)
        ]
        self.ballTopMiddle = [
            self.canvas.coords(self.ball)[2] - ((self.canvas.coords(self.ball)[2] - self.canvas.coords(self.ball)[0])/2),
            self.canvas.coords(self.ball)[1]
        ]
        self.ballBottomMiddle = [
            self.canvas.coords(self.ball)[2] - ((self.canvas.coords(self.ball)[2] - self.canvas.coords(self.ball)[0])/2),
            self.canvas.coords(self.ball)[3]
        ]
        self.update_ball_position()
        self.collision()
        
        self.p1_up = False
        self.p1_down = False
        self.p2_up = False
        self.p2_down = False
        self.move_paddles()



    def moveup1(self, event):
        self.p1_up = True

    def movedown1(self, event):
        self.p1_down = True

    def moveup2(self, event):
        self.p2_up = True

    def movedown2(self, event):
        self.p2_down = True

    def stop_moveup1(self, event):
        self.p1_up = False

    def stop_movedown1(self, event):
        self.p1_down = False

    def stop_moveup2(self, event):
        self.p2_up = False

    def stop_movedown2(self, event):
        self.p2_down = False
            
    def move_paddles(self):
        if self.p1_up and self.canvas.coords(self.paddle1)[1] > 0:
            self.canvas.move(self.paddle1, 0, -self.ps)
        if self.p1_down and self.canvas.coords(self.paddle1)[3] < 400:
            self.canvas.move(self.paddle1, 0, self.ps)
        if self.p2_up and self.canvas.coords(self.paddle2)[1] > 0:
            self.canvas.move(self.paddle2, 0, -self.ps)
        if self.p2_down and self.canvas.coords(self.paddle2)[3] < 400:
            self.canvas.move(self.paddle2, 0, self.ps)
        root.after(20, self.move_paddles)  # Run this every 20ms

    # when calling this function pass the parameter w if ball collides with wall, p if colliding with paddle
    def update_velocity(self, x):
        if x == "w":
            self.y_velocity *= -1
        elif x == "p":
            self.x_velocity *= -1

    def update_paddle_points(self):
        self.paddle1top = [self.canvas.coords(self.paddle1)[2], self.canvas.coords(self.paddle1)[1]]
        self.paddle1bottom = [self.canvas.coords(self.paddle1)[2], self.canvas.coords(self.paddle1)[3]]
        self.paddle2top = [self.canvas.coords(self.paddle2)[0], self.canvas.coords(self.paddle2)[1]]
        self.paddle2bottom = [self.canvas.coords(self.paddle2)[0], self.canvas.coords(self.paddle2)[3]]

    def update_ball_points(self):
        self.ballMiddleLeft = [
            self.canvas.coords(self.ball)[0],
            self.canvas.coords(self.ball)[3] - ((self.canvas.coords(self.ball)[3] - self.canvas.coords(self.ball)[1])/2)
        ]
        self.ballMiddleRight = [
            self.canvas.coords(self.ball)[2],
            self.canvas.coords(self.ball)[3] - ((self.canvas.coords(self.ball)[3] - self.canvas.coords(self.ball)[1])/2)
        ]
        self.ballTopMiddle = [
            self.canvas.coords(self.ball)[2] - ((self.canvas.coords(self.ball)[2] - self.canvas.coords(self.ball)[0])/2),
            self.canvas.coords(self.ball)[1]
        ]
        self.ballBottomMiddle = [
            self.canvas.coords(self.ball)[2] - ((self.canvas.coords(self.ball)[2] - self.canvas.coords(self.ball)[0])/2),
            self.canvas.coords(self.ball)[3]
        ]

    def update_ball_position(self):
        self.canvas.move(self.ball, self.x_velocity * 10, self.y_velocity * 10)
        self.update_ball_points()
        root.after(10, self.update_ball_position)

    def reset_collision_flag(self):
        """Resets the collision flag after a brief delay."""
        self.collision_flag = False

    def collision(self):
        ball_coords = self.canvas.coords(self.ball)
        paddle1_coords = self.canvas.coords(self.paddle1)
        paddle2_coords = self.canvas.coords(self.paddle2)

        # Check collision with walls
        if ball_coords[1] < 0 or ball_coords[3] > 400:
            self.update_velocity("w")

        # Check collision with paddles
        if not self.collision_flag:
            # Paddle 1 collision
            if (ball_coords[0] <= paddle1_coords[2]
                    and paddle1_coords[1] <= ball_coords[3] <= paddle1_coords[3]):
                self.update_velocity("p")
                self.x_velocity += (abs(self.x_velocity)/self.x_velocity)*(0.01)
                self.y_velocity += (abs(self.y_velocity)/self.y_velocity)*(0.01)
                self.collision_flag = True
                root.after(1000, self.reset_collision_flag)

            # Paddle 2 collision
            if (ball_coords[2] >= paddle2_coords[0]
                    and paddle2_coords[1] <= ball_coords[3] <= paddle2_coords[3]):
                self.update_velocity("p")
                self.x_velocity += (abs(self.x_velocity)/self.x_velocity)*(0.01)
                self.y_velocity += (abs(self.y_velocity)/self.y_velocity)*(0.01)
                self.collision_flag = True
                root.after(1000, self.reset_collision_flag)

        # Reset ball position if it goes out of bounds
        if ball_coords[0] < 0 or ball_coords[2] > 600:
            self.canvas.coords(self.ball, 290, 190, 310, 210)
            self.x_velocity, self.y_velocity = 0.3, 0.3

        root.after(10, self.collision)


run = GUIandLogic(root)
root.bind("w", run.moveup1)
root.bind("s", run.movedown1)
root.bind('<Up>', run.moveup2)
root.bind('<Down>', run.movedown2)

root.bind("<KeyRelease-w>", run.stop_moveup1)
root.bind("<KeyRelease-s>", run.stop_movedown1)
root.bind("<KeyRelease-Up>", run.stop_moveup2)
root.bind("<KeyRelease-Down>", run.stop_movedown2)

root.mainloop()
