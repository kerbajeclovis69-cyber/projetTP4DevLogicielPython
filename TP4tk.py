import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=400, bg="black")
canvas.pack()

PADDLE_LARGEUR = 80
PADDLE_LONGEUR = 15
PADDLE_Y = 350

paddle = canvas.create_rectangle(
    300 - PADDLE_LARGEUR//2, PADDLE_Y,
    300 + PADDLE_LARGEUR//2, PADDLE_Y + PADDLE_LONGEUR,
    fill="white")

def move_left(event):
    x1, y1, x2, y2 = canvas.coords(paddle)
    if x1 > 0:
        canvas.move(paddle, -20, 0)

def move_right(event):
    x1, y1, x2, y2 = canvas.coords(paddle)
    if x2 < 600:
        canvas.move(paddle, 20, 0)

root.bind("<Left>", move_left)
root.bind("<Right>", move_right)
root.bind("a", move_left)
root.bind("d", move_right)
root.bind("q", move_left)



BALL_SIZE = 15

ball = canvas.create_oval( 300 - BALL_SIZE//2, 200 - BALL_SIZE//2, 300 + BALL_SIZE//2, 200 + BALL_SIZE//2, fill="red")

dx = 5
dy = -5

def move_ball():
    global dx, dy
    canvas.move(ball, dx, dy)

    x1, y1, x2, y2 = canvas.coords(ball)

    if x1 <= 0 or x2 >= 600:
        dx = -dx

    if y1 <= 0:
        dy = -dy

    if y2 >= 400:
        dy = -dy

    root.after(20, move_ball)

move_ball() 




def move_ball():
    global dx, dy
    canvas.move(ball, dx, dy)

    bx1, by1, bx2, by2 = canvas.coords(ball)
    px1, py1, px2, py2 = canvas.coords(paddle)

    # Wall collisions
    if bx1 <= 0 or bx2 >= 600:
        dx = -dx
    if by1 <= 0:
        dy = -dy

    # colision avec le rectangle
    if dy > 0:  # quand la ball descend vers le bas
        if by2 >= py1 and by1 <= py2:      
            if bx2 >= px1 and bx1 <= px2:  
                dy = -dy

    # si part en bas
    if by2 >= 400:
        dy = 0
        dx=0


    root.after(20, move_ball)



root.mainloop()
