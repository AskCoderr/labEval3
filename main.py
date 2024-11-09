import tkinter as tk
root = tk.Tk()
root.title("Ping Pong Game")
root.resizable(False, False)
root.geometry("600x400")
canvas = tk.Canvas(root, width=600, height=400, bg="black")
canvas.pack()
paddle1 = canvas.create_rectangle(10, 150, 30, 250, fill="white")
paddle2 = canvas.create_rectangle(570, 150, 590, 250, fill="white")
ball = canvas.create_oval(290, 190, 310, 210, fill="red")
player1_score = 0
player2_score = 0
x_velocity = 100 # im considering the unit as pixel/second
y_velocity = 100
scoredisplay = canvas.create_text(300, 50, text=f"{player1_score} - {player2_score}", fill="yellow", font=("Helvetica", 24))
canvas.itemconfig(scoredisplay, text=f"{player1_score} - {player2_score}")
ps=20

def moveup1(event):
    if canvas.coords(paddle1)[1] > 0:
        canvas.move(paddle1, 0, -ps)
def movedown1(event):
    if canvas.coords(paddle1)[3] < 400:
        canvas.move(paddle1, 0, ps)
def moveup2(event):
    if canvas.coords(paddle2)[1] > 0:
        canvas.move(paddle2, 0, -ps)

def movedown2(event):
    if canvas.coords(paddle2)[3] < 400:
        canvas.move(paddle2, 0, ps)


# when calling this function pass the parameter w if ball collides with wall, p if colliding with paddle
def update_velocity(x):
    if x == "w":
        y_velocity *= -1
    elif x == "p":
        x_velocity *= -1
        

root.bind("w", moveup1)
root.bind("s", movedown1)
root.bind('<Up>',moveup2)
root.bind('<Down>',movedown2)
root.mainloop()