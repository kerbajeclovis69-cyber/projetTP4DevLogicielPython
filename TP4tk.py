import tkinter as tk

fenetre = tk.Tk()
fenetre.title("Break the fuck out")
fenetre.geometry("1260x800")

#
# --- FONCTIONS POUR LES MENUS ---
#

def show_menu_principal():
    frame_menu_principal.pack(fill="both", expand=True)
    frame_breakout.pack_forget()

def show_menu_breakout():
    frame_menu_principal.pack_forget()
    frame_breakout.pack(fill="both", expand=True)
    startGame()  # démarre le jeu automatiquement


#
# --- MENU PRINCIPAL ---
#

frame_menu_principal = tk.Frame(fenetre, bg="black")

titre = tk.Label(frame_menu_principal, text="MENU PRINCIPAL",
                 font=("Arial", 40), fg="white", bg="black")
titre.pack(pady=80)

btn_play = tk.Button(frame_menu_principal, text="Jouer",
                     font=("Arial", 25), command=show_menu_breakout)
btn_play.pack(pady=20)

btn_quit = tk.Button(frame_menu_principal, text="Quitter",
                     font=("Arial", 25), command=fenetre.destroy)
btn_quit.pack(pady=20)


#
# --- BREAKOUT ---
#

frame_breakout = tk.Frame(fenetre)

photo = tk.PhotoImage(
    file=r"C:\Users\kerba\Cours_3ETI\Semestre5\DevLogicielPython\projetTP4DevLogicielPython\space.png"
)

canvas = tk.Canvas(frame_breakout, width=1260, height=800)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, anchor="nw", image=photo)

# Textes 
label_text1 = tk.Label(canvas, text="nb de vies :", font=("Arial", 20), fg="white")
label_text2 = tk.Label(canvas, text="points :", font=("Arial", 20), fg="white")

canvas.create_window(50, 20, anchor="nw", window=label_text1)
canvas.create_window(1050, 20, anchor="nw", window=label_text2)

#
# --- PADDLE + BALL ---
#

PADDLE_LARGEUR = 120
PADDLE_LONGEUR = 20
PADDLE_Y = 700

BALL_SIZE = 20

dx = 5
dy = -5

def init_game_objects():
    global paddle, ball, dx, dy

    dx = 5
    dy = -5

    paddle = canvas.create_rectangle(
        630 - PADDLE_LARGEUR//2, PADDLE_Y,
        630 + PADDLE_LARGEUR//2, PADDLE_Y + PADDLE_LONGEUR,
        fill="white"
    )

    ball = canvas.create_oval(
        630 - BALL_SIZE//2, 400 - BALL_SIZE//2,
        630 + BALL_SIZE//2, 400 + BALL_SIZE//2,
        fill="red"
    )


def move_left(event):
    x1, y1, x2, y2 = canvas.coords(paddle)
    if x1 > 0:
        canvas.move(paddle, -20, 0)

def move_right(event):
    x1, y1, x2, y2 = canvas.coords(paddle)
    if x2 < 1260:
        canvas.move(paddle, 20, 0)

fenetre.bind("<Left>", move_left)
fenetre.bind("<Right>", move_right)
fenetre.bind("a", move_left)
fenetre.bind("d", move_right)
fenetre.bind("q", move_left)


def move_ball():
    global dx, dy

    canvas.move(ball, dx, dy)

    bx1, by1, bx2, by2 = canvas.coords(ball)
    px1, py1, px2, py2 = canvas.coords(paddle)

    # murs
    if bx1 <= 0 or bx2 >= 1260:
        dx = -dx
    if by1 <= 0:
        dy = -dy

    # collision paddle
    if dy > 0:
        if by2 >= py1 and by1 <= py2:
            if bx2 >= px1 and bx1 <= px2:
                dy = -dy

    # tombe en bas
    if by2 >= 800:
        dx = 0
        dy = 0

    fenetre.after(20, move_ball)


def startGame():
    label_text1.config(text="nb de vie : 2")
    label_text2.config(text="points : 0")
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=photo)
    init_game_objects()
    move_ball()


# Boutons
button1 = tk.Button(canvas, text="restart", command=startGame)
button2 = tk.Button(canvas, text="quitter", command=show_menu_principal)

canvas.create_window(1200, 600, anchor="center", window=button1)
canvas.create_window(1200, 650, anchor="center", window=button2)


show_menu_principal()

fenetre.mainloop()
