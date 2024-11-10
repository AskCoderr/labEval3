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
                                                    30,
                                                    250,
                                                    fill="white")
        self.paddle2 = self.canvas.create_rectangle(570,
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

    def moveup1(self, event):
        if self.canvas.coords(self.paddle1)[1] > 0:
            self.canvas.move(self.paddle1, 0, -self.ps)
            self.update_paddle_points()

    def movedown1(self, event):
        if self.canvas.coords(self.paddle1)[3] < 400:
            self.canvas.move(self.paddle1, 0, self.ps)
            self.update_paddle_points()

    def moveup2(self, event):
        if self.canvas.coords(self.paddle2)[1] > 0:
            self.canvas.move(self.paddle2, 0, -self.ps)
            self.update_paddle_points()

    def movedown2(self, event):
        if self.canvas.coords(self.paddle2)[3] < 400:
            self.canvas.move(self.paddle2, 0, self.ps)
            self.update_paddle_points()

    # when calling this function pass the parameter w if ball collides with wall, p if colliding with paddle
    def update_velocity(self, x):
        global y_velocity, x_velocity
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

    def collision(self):
        if (self.ballMiddleLeft[0] < 0) or (self.ballMiddleRight[0] > 600):
            self.canvas.coords(self.ball, 290, 190, 310, 210)
        elif (self.ballTopMiddle[1] < 0) or (self.ballBottomMiddle[1] > 400):
            self.update_velocity("w")
        elif (self.ballMiddleLeft[0] <= self.paddle1bottom[0]
              and self.paddle1top[1]<=self.ballMiddleLeft[1]<=self.paddle1bottom[1]):
            self.update_velocity("p")
        elif (self.ballMiddleRight[0] >= self.paddle2top[0] and self.paddle2top[1]<=self.ballMiddleRight[1]<=self.paddle2bottom[1]):
            self.update_velocity("p")
        root.after(10, self.collision)


run = GUIandLogic(root)
root.bind("w", run.moveup1)
root.bind("s", run.movedown1)
root.bind('<Up>', run.moveup2)
root.bind('<Down>', run.movedown2)
root.mainloop()
