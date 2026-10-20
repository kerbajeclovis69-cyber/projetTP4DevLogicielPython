# Hadi Elghali et Clovis Kerbaje projet jeu Breakout

#TO DO NEXT TIME : vitesse de la balle selon le niveau / mettre de la musique / mettre un chronomètre

import random as rd
import tkinter as tk
import BreakoutFonctions as bf

fenetre = tk.Tk()
fenetre.title("Break the fuck out")
fenetre.geometry("1260x800")



# Variables du niveau courant
niveau_hp = 1
niveau_lignes = 5


# Constantes 
HP = 2

after_id = None

HP_FACILE = 1
HP_MOYEN = 2
HP_DIFFICILE = 4

LIGNES_FACILE = 5
LIGNES_MOYEN = 10
LIGNES_DIFFICILE = 15
ACCELERATION = 1.02
VITESSE_MAX = 15
points = 0

briques = []

game_running = False

PADDLE_LARGEUR = 120
PADDLE_LONGEUR = 20
PADDLE_Y = 700

BALL_SIZE = 20


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


btn_facile = tk.Button(frame_menu_principal, text="Facile", font=("Arial", 25), bg="green", command=lambda: bf.start_level(HP_FACILE,LIGNES_FACILE))
btn_facile.pack(pady=10)


btn_moyen = tk.Button(frame_menu_principal, text="Moyen", font=("Arial", 25), bg="orange", command=lambda: bf.start_level(HP_MOYEN,LIGNES_MOYEN))
btn_moyen.pack(pady=10)


btn_difficile = tk.Button(frame_menu_principal, text="Difficile", font=("Arial", 25), bg="red", command=lambda: bf.start_level(HP_DIFFICILE,LIGNES_DIFFICILE))
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


photo = tk.PhotoImage(file=r"C:\Users\thead\Documents\CPE\3A\python\TP4-breakout\projetTP4DevLogicielPython\space123.png")


canvas = tk.Canvas(frame_breakout, width=1260, height=800)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, anchor="nw", image=photo)


# Textes
label_text1 = tk.Label(canvas, text="nb de vies : " + str(HP), font=("Arial", 20), fg="white", bg="black")

label_text2 = tk.Label(canvas, text="points : " + str(points), font=("Arial", 20), fg="white", bg="black")

canvas.create_window(50, 20, anchor="nw", window=label_text1)
canvas.create_window(1050, 20, anchor="nw", window=label_text2)



# Boutons
button1 = tk.Button(canvas, text="restart", command= bf.nouvellePartie)
button2 = tk.Button(canvas, text="quitter", command=bf.quitter_partie)
canvas.create_window(1200, 600, anchor="center", window=button1)
canvas.create_window(1200, 650, anchor="center", window=button2)



# on partage avec le fichier fonctions les variables de notre programme :
 
bf.fenetre = fenetre

bf.frame_menu_principal = frame_menu_principal
bf.frame_breakout = frame_breakout

bf.canvas = canvas

bf.label_text1 = label_text1
bf.label_text2 = label_text2

bf.briques = briques

bf.HP = HP
bf.points = points
bf.after_id = after_id
bf.game_running = game_running

bf.PADDLE_LARGEUR = PADDLE_LARGEUR
bf.PADDLE_LONGEUR = PADDLE_LONGEUR
bf.PADDLE_Y = PADDLE_Y

bf.BALL_SIZE = BALL_SIZE

bf.ball = ball
bf.paddle = paddle

bf.niveau_hp = niveau_hp
bf.niveau_lignes = niveau_lignes
bf.ACCELERATION= ACCELERATION
bf.VITESSE_MAX = VITESSE_MAX


# PADDLE + BALL 

fenetre.bind("<Left>", bf.move_left)
fenetre.bind("<Right>", bf.move_right)
fenetre.bind("a", bf.move_left)
fenetre.bind("d", bf.move_right)
fenetre.bind("q", bf.move_left)



bf.show_menu_principal()

fenetre.mainloop()