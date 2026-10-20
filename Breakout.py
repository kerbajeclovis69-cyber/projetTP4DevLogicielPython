# Hadi Elghali et Clovis Kerbaje projet jeu Breakout

#TO DO NEXT TIME : vitesse de la balle selon le niveau / mettre de la musique / verifier la gagne ou la défaite / mettre un chronomètre

import random as rd
import tkinter as tk

fenetre = tk.Tk()
fenetre.title("Break the fuck out")
fenetre.geometry("1260x800")



# Variables du niveau courant
niveau_hp = 1
niveau_lignes = 5



# Fonctions changement de menu
def show_menu_principal():
    frame_menu_principal.pack(fill="both", expand=True)
    frame_breakout.pack_forget()


def show_menu_breakout():
    frame_menu_principal.pack_forget()
    frame_breakout.pack(fill="both", expand=True)



# Lancement d'un niveau
def start_level(hp, lignes):
    global niveau_hp, niveau_lignes     #enregistrement et stockage des variables de difficulté

    niveau_hp = hp
    niveau_lignes = lignes

    show_menu_breakout()
    supprimer_briques()
    creer_briques(hp, lignes)
    init_game_objects()
    global game_running

    if not game_running:
        game_running = True
        move_ball()


# Fonction Restart
def restartGame(HP, points):
    global ball, paddle
    canvas.delete("message_fin")


    label_text1.config(text="nb de vies : " + str(HP))
    label_text2.config(text="points : " + str(points))

    
    canvas.delete(ball)
    canvas.delete(paddle)

    init_game_objects()
    if game_running:
        move_ball()

#fonctions qui recommence la partie
def nouvellePartie():
    global HP, points, game_running
    if after_id:
        fenetre.after_cancel(after_id)
    game_running = False
    HP = 2
    points = 0

    supprimer_briques()
    creer_briques(niveau_hp, niveau_lignes)

    restartGame(HP, points)
    game_running = True
    move_ball()


#fonction pour créer toutes les briques ici n = HP d'une brique et r un rapport entre le nombre de ligne et de colonne
def creer_briques(n, r):
    largeur = 900 / (2 * r)
    hauteur = 15

    for ligne in range(r):
        for col in range(2 * r):

            x = 180 + col * largeur
            y = 100 + ligne * hauteur

            id_rect = canvas.create_rectangle(
                x,
                y,
                x + largeur,
                y + hauteur,
                fill="blue",
                outline="white"
            )

            briques.append([x, y, n, id_rect])

#fonction pour retirer toutes les briques de l'écran
def supprimer_briques():
    for brique in briques:
        canvas.delete(brique[3])

    briques.clear()

#Fonctions ball + paddle 
def init_game_objects():
    global paddle, ball, dx, dy

    dx = rd.choice([-6,-5,-4,4,5,6])
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


#déplacement paddle
def move_left(event):
    x1, y1, x2, y2 = canvas.coords(paddle)
    if x1 > 0:
        canvas.move(paddle, -20, 0)

def move_right(event):
    x1, y1, x2, y2 = canvas.coords(paddle)
    if x2 < 1260:
        canvas.move(paddle, 20, 0)

#fonctions de déplacement de la balle
def move_ball():
    global dx, dy
    global briques
    global HP
    global points
    global game_running
    global after_id
    
    if not game_running:
        return
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

    # collision briques
    for brique in briques:
        
        rx1, ry1, rx2, ry2 = canvas.coords(brique[3])

        if (bx2 >= rx1 and
            bx1 <= rx2 and
            by2 >= ry1 and
            by1 <= ry2):

            canvas.move(ball, -dx, -dy)
            
            overlap_x = min(bx2, rx2) - max(bx1, rx1)
            overlap_y = min(by2, ry2) - max(by1, ry1)
            if overlap_x < overlap_y :
                dx=-dx
            else:
                dy = -dy
            
            
            points += 1
            label_text2.config(text="points : " + str(points))



            brique[2] -= 1
            
            if brique[2] == 3:  
                canvas.itemconfig(brique[3], fill="red")
            
            if brique[2] == 2:
                canvas.itemconfig(brique[3], fill="orange")
            
            elif brique[2] == 1:
                canvas.itemconfig(brique[3], fill="yellow")
            if brique[2] <= 0:
            
                canvas.delete(brique[3])
                briques.remove(brique)


            break

    if len(briques) == 0:
        victoire()
        return

    # tombe en bas
    if by2 >= 800:

        HP -= 1
        label_text1.config(text="nb de vies : " + str(HP))
        if HP == 0:
            defaite()
            return
        else :
            restartGame(HP, points)
            return
    

    if game_running:
        after_id = fenetre.after(20, move_ball)

#fonctions changement d'écran en cas de victoire ou de défaite
def victoire():
    global dx, dy, game_running
    
    dx = 0
    dy = 0

    canvas.create_text(630,400,text="VICTOIRE !",fill="green",font=("Arial", 50, "bold"), tags="message_fin")
    game_running = False

def defaite():
    global dx, dy, game_running

    dx = 0
    dy = 0

    canvas.create_text(630,400, text="DEFAITE !", fill="red", font=("Arial", 50, "bold"), tags="message_fin")
    game_running = False




# Constantes 
HP = 2

after_id = None

HP_FACILE = 1
HP_MOYEN = 2
HP_DIFFICILE = 4

LIGNES_FACILE = 5
LIGNES_MOYEN = 10
LIGNES_DIFFICILE = 15

points = 0

briques = []

game_running = False

PADDLE_LARGEUR = 120
PADDLE_LONGEUR = 20
PADDLE_Y = 700

BALL_SIZE = 20

dx = 20
dy = -20
paddle = None
ball = None


#
# 
#
#
# 
#
#

frame_menu_principal = tk.Frame(fenetre, bg="black")

titre = tk.Label(frame_menu_principal, text="MENU PRINCIPAL", font=("Arial", 40), fg="white", bg="black")
titre.pack(pady=80)


btn_facile = tk.Button(frame_menu_principal, text="Facile", font=("Arial", 25), bg="green", command=lambda: start_level(HP_FACILE,LIGNES_FACILE))
btn_facile.pack(pady=10)


btn_moyen = tk.Button(frame_menu_principal, text="Moyen", font=("Arial", 25), bg="orange", command=lambda: start_level(HP_MOYEN,LIGNES_MOYEN))
btn_moyen.pack(pady=10)


btn_difficile = tk.Button(frame_menu_principal, text="Difficile", font=("Arial", 25), bg="red", command=lambda: start_level(HP_DIFFICILE,LIGNES_DIFFICILE))
btn_difficile.pack(pady=10)

btn_quit = tk.Button(frame_menu_principal, text="Quitter", font=("Arial", 25), command=fenetre.destroy)
btn_quit.pack(pady=20)


#
# 
#
#
# 
#
#


frame_breakout = tk.Frame(fenetre)

photo = tk.PhotoImage(file=r"C:\Users\kerba\Cours_3ETI\Semestre5\DevLogicielPython\TP4DevLogicielPython_projet\space.png")

canvas = tk.Canvas(frame_breakout, width=1260, height=800)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, anchor="nw", image=photo)


# Textes
label_text1 = tk.Label(canvas, text="nb de vies : " + str(HP), font=("Arial", 20), fg="white", bg="black")

label_text2 = tk.Label(canvas, text="points : " + str(points), font=("Arial", 20), fg="white", bg="black")

canvas.create_window(50, 20, anchor="nw", window=label_text1)
canvas.create_window(1050, 20, anchor="nw", window=label_text2)



# Boutons
button1 = tk.Button(canvas, text="restart", command=nouvellePartie)
button2 = tk.Button(
    canvas,
    text="quitter",
    command=lambda: (globals().__setitem__("HP", 2),globals().__setitem__("points", 0),globals().__setitem__("game_running", False),label_text1.config(text="nb de vies : 2"),label_text2.config(text="points : 0"),supprimer_briques(),canvas.delete("message_fin"),canvas.delete(ball),canvas.delete(paddle),show_menu_principal()))

canvas.create_window(1200, 600, anchor="center", window=button1)
canvas.create_window(1200, 650, anchor="center", window=button2)




# --- PADDLE + BALL ---

fenetre.bind("<Left>", move_left)
fenetre.bind("<Right>", move_right)
fenetre.bind("a", move_left)
fenetre.bind("d", move_right)
fenetre.bind("q", move_left)








show_menu_principal()

fenetre.mainloop()