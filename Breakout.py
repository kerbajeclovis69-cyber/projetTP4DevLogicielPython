import tkinter as tk

fenetre = tk.Tk()
fenetre.title("Break the fuck out")
fenetre.geometry("1260x800")

#
#
#
#
#

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
#
#
#
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

# Fonction du bouton
def startGame():
    label_text1.config(text="nb de vie : 2")
    label_text2.config(text="points : 0")

# Boutons
button1 = tk.Button(canvas, text="restart", command=startGame)
button2 = tk.Button(canvas, text="quitter", command=show_menu_principal)

#positions des boutons
canvas.create_window(1200, 600, anchor="center", window=button1)
canvas.create_window(1200, 650, anchor="center", window=button2)


show_menu_principal()

fenetre.mainloop()
