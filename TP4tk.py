


# Hadi Elghali et Clovis Kerbaje projet jeu Breakout

#TO DO NEXT TIME : quand on restart, les rectangles disparaissent mais ne se raffiche plus / intégrer la raquette et la balle (cf code hadi) / nombre vie à gérer / vitesse de la balle selon le niveau / faire disparaitre les rectangles quand leur vie est à 0 / mettre de la musique / verifier la gagne ou la défaite / mettre un chronomètre



import tkinter as tk

fenetre = tk.Tk()
fenetre.title("Break the fuck out")
fenetre.geometry("1260x800")

dx = 10
dy = -10
paddle = None
ball = None
briques = []

# Fonctions pour changer de menu
def show_menu_principal():
    frame_menu_principal.pack(fill="both", expand=True)
    frame_breakout.pack_forget()

def show_menu_breakout():
    frame_menu_principal.pack_forget()
    frame_breakout.pack(fill="both", expand=True)

#
#
#
#
#
#

frame_menu_principal = tk.Frame(fenetre, bg="black")

titre = tk.Label(frame_menu_principal, text="MENU PRINCIPAL",
                 font=("Arial", 40), fg="white", bg="black")
titre.pack(pady=80)

# Fonctions des boutons de difficulté
def start_facile():
    print("Mode facile sélectionné")
    show_menu_breakout()
    supprimer_briques()
    creer_briques(1,5)
    init_game_objects()
    move_ball()

def start_moyen():
    print("Mode moyen sélectionné")
    show_menu_breakout()
    supprimer_briques()
    creer_briques(2,10)
    init_game_objects()
    move_ball()

def start_difficile():
    print("Mode difficile sélectionné")
    show_menu_breakout()
    supprimer_briques()
    creer_briques(4,15)
    init_game_objects()
    move_ball()

# Boutons de difficulté
btn_facile = tk.Button(frame_menu_principal, text="Facile",font=("Arial", 25),bg="green", command=start_facile)
btn_facile.pack(pady=10)
btn_moyen = tk.Button(frame_menu_principal, text="Moyen",font=("Arial", 25),bg="orange", command=start_moyen)
btn_moyen.pack(pady=10)
btn_difficile = tk.Button(frame_menu_principal, text="Difficile",font=("Arial", 25),bg="red", command=start_difficile)
btn_difficile.pack(pady=10)

btn_quit = tk.Button(frame_menu_principal, text="Quitter",font=("Arial", 25), command=fenetre.destroy)
btn_quit.pack(pady=20)

#
#
#
#
#
#

frame_breakout = tk.Frame(fenetre)

photo = tk.PhotoImage(file=r"C:\Users\thead\Documents\CPE\3A\python\TP4-breakout\projetTP4DevLogicielPython\space123.png")

canvas = tk.Canvas(frame_breakout, width=1260, height=800)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, anchor="nw", image=photo)

# Textes 
label_text1 = tk.Label(canvas, text="nb de vies :", font=("Arial", 20), fg="white")
label_text2 = tk.Label(canvas, text="points :", font=("Arial", 20), fg="white")

canvas.create_window(50, 20, anchor="nw", window=label_text1)
canvas.create_window(1050, 20, anchor="nw", window=label_text2)

# Fonction du bouton restart
def restartGame():
    label_text1.config(text="nb de vie : 2")
    label_text2.config(text="points : 0")
    supprimer_briques()

    init_game_objects()
    move_ball()

# Boutons
button1 = tk.Button(canvas, text="restart", command=restartGame)
button2 = tk.Button(canvas, text="quitter", command=lambda: (supprimer_briques(), show_menu_principal()))

# positions des boutons
canvas.create_window(1200, 600, anchor="center", window=button1)
canvas.create_window(1200, 650, anchor="center", window=button2)

show_menu_principal()


# --- PADDLE + BALL ---#

PADDLE_LARGEUR = 120
PADDLE_LONGEUR = 20
PADDLE_Y = 700

BALL_SIZE = 20



def init_game_objects():
    global paddle, ball, dx, dy

    dx = 5
    dy = -5

    if paddle is not None:
        canvas.delete(paddle)

    if ball is not None:
        canvas.delete(ball)

    paddle = canvas.create_rectangle(
        630 - PADDLE_LARGEUR//2,
        PADDLE_Y,
        630 + PADDLE_LARGEUR//2,
        PADDLE_Y + PADDLE_LONGEUR,
        fill="white"
    )

    ball = canvas.create_oval(
        630 - BALL_SIZE//2,
        400 - BALL_SIZE//2,
        630 + BALL_SIZE//2,
        400 + BALL_SIZE//2,
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
    global briques
    canvas.move(ball, dx, dy)

    bx1, by1, bx2, by2 = canvas.coords(ball)
    px1, py1, px2, py2 = canvas.coords(paddle)

    # murs
    if bx1 <= 0 or bx2 >= 1260:
        dx = -dx

    if by1 <= 0:
        dy = -dy

    # paddle
    if dy > 0:
        if by2 >= py1 and by1 <= py2:
            if bx2 >= px1 and bx1 <= px2:
                dy = -dy

    # collision briques
    for brique in briques:

        rx1, ry1, rx2, ry2 = canvas.coords(brique[3])

        if (
            bx2 >= rx1 and
            bx1 <= rx2 and
            by2 >= ry1 and
            by1 <= ry2
        ):

            canvas.delete(brique[3])
            briques.remove(brique)

            dy = -dy

    # tombe en bas
    if by2 >= 800:
        dx = 0
        dy = 0

    fenetre.after(20, move_ball)

#Création des briques

def creer_briques(n,r): #n = nombre de vie (3 par exemple pour difficile) r = cste pour le nombre de rectangle
    global briques
    largeur = 900/(2*r)
    hauteur = 15
    hp = n 
    for ligne in range(r):
        for col in range(2*r):
            x = 180 + col * (largeur)
            y = 100 + ligne * (hauteur)

            # création du rectangle sur le canvas
            id_rect = canvas.create_rectangle(x, y, x + largeur, y + hauteur,fill="blue", outline="white")

            # on stocke : x, y, vie, id_canvas
            briques.append([x, y, hp, id_rect])



def supprimer_briques():
    global briques
    for brique in briques:
        canvas.delete(brique[3])  # supprimer le rectangle du canvas
    briques.clear()  # vider la liste





fenetre.mainloop()
