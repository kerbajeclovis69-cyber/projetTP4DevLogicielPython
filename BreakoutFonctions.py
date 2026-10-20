import random as rd
import tkinter as tk



class Brique:
    def __init__(self, x, y, hp, largeur, hauteur):
        self.hp = hp

        self.id = canvas.create_rectangle(x,y,x + largeur,y + hauteur,fill="purple",outline="white")


class Paddle:
    def __init__(self):
        self.id = canvas.create_rectangle(
            630 - PADDLE_LARGEUR // 2,
            PADDLE_Y,
            630 + PADDLE_LARGEUR // 2,
            PADDLE_Y + PADDLE_LONGEUR,
            fill="white"
        )

    def move_left(self):

        x1, y1, x2, y2 = canvas.coords(self.id)

        if x1 > 0:
            canvas.move(self.id, -20, 0)

    def move_right(self):

        x1, y1, x2, y2 = canvas.coords(self.id)

        if x2 < 1260:
            canvas.move(self.id, 20, 0)


class Balle:
    def __init__(self):

        self.dx = rd.choice([-6, -5, -4, 4, 5, 6])
        self.dy = -5

        self.id = canvas.create_oval(
            630 - BALL_SIZE // 2,
            400 - BALL_SIZE // 2,
            630 + BALL_SIZE // 2,
            400 + BALL_SIZE // 2,
            fill="red"
        )



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

    
    canvas.delete(ball.id)
    canvas.delete(paddle.id)

    init_game_objects()


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

def quitter_partie():

    global HP, points, game_running, ball, paddle, after_id

    HP = 2
    points = 0

    label_text1.config(text="nb de vies : 2")
    label_text2.config(text="points : 0")

    if after_id:
        fenetre.after_cancel(after_id)
        after_id = None

    game_running = False

    supprimer_briques()

    if ball:
        canvas.delete(ball.id)

    if paddle:
        canvas.delete(paddle.id)

    ball = None
    paddle = None

    canvas.delete("message_fin")

    show_menu_principal()



#fonction pour créer toutes les briques ici n = HP d'une brique et r un rapport entre le nombre de ligne et de colonne
def creer_briques(n, r):

    largeur = 900 / ((2 * r))
    hauteur = 15

    for ligne in range(r):

        for col in range(2 * r):

            x = 150 + col * (largeur + 2)
            y = 100 + ligne * (hauteur + 2)

            briques.append(Brique(x, y, n, largeur, hauteur))


#fonction pour retirer toutes les briques de l'écran
def supprimer_briques():

    for brique in briques:
        canvas.delete(brique.id)

    briques.clear()

#Fonctions ball + paddle 
def init_game_objects():

    global paddle
    global ball

    paddle = Paddle()
    ball = Balle()

#déplacement paddle
def move_left(event):
    paddle.move_left()

def move_right(event):
    paddle.move_right()

#fonctions de déplacement de la balle
def move_ball():
    global ball
    global briques
    global HP
    global points
    global game_running
    global after_id
    
    if not game_running:
        return
    canvas.move(ball.id, ball.dx, ball.dy)

    bx1, by1, bx2, by2 = canvas.coords(ball.id)
    px1, py1, px2, py2 = canvas.coords(paddle.id)
    

    # collision murs
    if bx1 <= 0 or bx2 >= 1260:
        ball.dx = -ball.dx
    if by1 <= 0:
        ball.dy = -ball.dy 

    # collision paddle
    if ball.dy > 0:
        if by2 >= py1 and by1 <= py2:
            if bx2 >= px1 and bx1 <= px2:

                ball.dy = -ball.dy - rd.choice([-0.3,-0.6,-0.9,0.3,0.6,0.9])

                ball.dx *= ACCELERATION
                ball.dy *= ACCELERATION
                ball.dx = max(-VITESSE_MAX, min(ball.dx, VITESSE_MAX)) 
                ball.dy = max(-VITESSE_MAX, min(ball.dy, VITESSE_MAX)) 

    # collision briques
    for brique in briques:
        rx1, ry1, rx2, ry2 = canvas.coords(brique.id)
        if (bx2 >= rx1 and
            bx1 <= rx2 and
            by2 >= ry1 and
            by1 <= ry2):

            canvas.move(ball.id, -ball.dx, -ball.dy)
            
            overlap_x = min(bx2, rx2) - max(bx1, rx1)
            overlap_y = min(by2, ry2) - max(by1, ry1)
            if overlap_x < overlap_y :

                ball.dx=-ball.dx 
                ball.dx *= ACCELERATION
                ball.dy *= ACCELERATION
                ball.dx = max(-VITESSE_MAX, min(ball.dx, VITESSE_MAX)) 
                ball.dy = max(-VITESSE_MAX, min(ball.dy, VITESSE_MAX)) 
            else:
                ball.dy = -ball.dy 

                ball.dx *= ACCELERATION
                ball.dy *= ACCELERATION
                ball.dx = max(-VITESSE_MAX, min(ball.dx, VITESSE_MAX)) 
                ball.dy = max(-VITESSE_MAX, min(ball.dy, VITESSE_MAX)) 
            
            
            points += 1
            label_text2.config(text="points : " + str(points))



            brique.hp -= 1
            
            if brique.hp == 3:  
                canvas.itemconfig(brique.id, fill="red")
            
            if brique.hp == 2:
                canvas.itemconfig(brique.id, fill="yellow")
            
            elif brique.hp == 1:
                canvas.itemconfig(brique.id, fill="green")
            if brique.hp <= 0:
            
                canvas.delete(brique.id)
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
        restartGame(HP, points)

        after_id = fenetre.after(20, move_ball)

        return
    

    if game_running:
        after_id = fenetre.after(20, move_ball)

#fonctions changement d'écran en cas de victoire ou de défaite
def victoire():
    global ball, game_running
    
    ball.dx = 0
    ball.dy = 0

    canvas.create_text(630,400,text="VICTOIRE !",fill="green",font=("Arial", 50, "bold"), tags="message_fin")
    game_running = False

def defaite():
    global ball, game_running

    ball.dx = 0
    ball.dy = 0

    canvas.create_text(630,400, text="DEFAITE !", fill="red", font=("Arial", 50, "bold"), tags="message_fin")
    game_running = False