import random as rd
import tkinter as tk



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

    paddle = canvas.create_rectangle(630 - PADDLE_LARGEUR//2, PADDLE_Y,630 + PADDLE_LARGEUR//2, PADDLE_Y + PADDLE_LONGEUR,fill="white")

    ball = canvas.create_oval(630 - BALL_SIZE//2, 400 - BALL_SIZE//2,630 + BALL_SIZE//2, 400 + BALL_SIZE//2,fill="red")


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

