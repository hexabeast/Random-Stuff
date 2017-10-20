from tkinter import*
from tkinter.messagebox import*
from random import *

fenetre = Tk()
fenetre.wm_title("Puissance 4")
fenetre.geometry('700x600')

can = Canvas(fenetre, width=700, height=600, background='lightgrey')

can.focus_set()

def iachoice(e):
    global jouerIA
    jouerIA = not askyesno("Mode de jeu","Jouer contre un autre humain?")
    if tour == 1:
        IA()


curseur = 3
tour = -1
grille = [[0 for i in range(6)] for j in range(7)]

curseurlignes = []

jouerIA = True

def drawGrille():
    global curseurlignes
    for i in range(8):
        can.create_line(i*100, 0, i*100, 800)
        can.create_line(0, i*100, 800, i*100)
    curseurlignes = []
    curseurlignes.append(can.create_line(curseur*100, 0, curseur*100, 800,width = 10,fill="red"))
    curseurlignes.append(can.create_line((curseur+1)*100, 0, (curseur+1)*100, 800,width = 10,fill="red"))

def reboot():
    global balle, tour, can, grille, curseur, jouerIA
    can.delete("all")
    tour = -1
    for i in range(7):
        for j in range(6):
            grille[i][j] = 0
    curseur = 3
    drawGrille()
    


def checkLigne(x,y,dx,dy,n):
    t = checkLigne2(x,y,dx,dy,n,-1,0)
    t2 = checkLigne2(x,y,dx,dy,n,1,0)
    if t2!=0:
        t = t2
    return t

def checkLigne2(x,y,dx,dy,n,joueur,erreur):
    if(x+dx*(n-1))> 6 or (y+dy*(n-1)) > 5 or (x+dx*(n-1))<0 or (y+dy*(n-1)) < 0:
        return (0)

    if(x)> 6 or (y) > 5 or (x)<0 or (y) < 0:
        return (0)
    
    for i in range(0,n):
        case = grille[x+i*dx][y+i*dy]
        if joueur != case:
            erreur -=1
            if case != 0:
                erreur = -1
            if erreur<0:
                return (0)
            
    return (joueur)

def check4Lignes(i,j,n):
    t = 0
    t = checkLigne(i,j,1,0,n)
    if t!=0:
        return t
    t = checkLigne(i,j,1,1,n)
    if t!=0:
        return t
    t = checkLigne(i,j,0,1,n)
    if t!=0:
        return t
    t = checkLigne(i,j,1,-1,n)

    return t

def superCheck(i,j,n,joueur,err):
    t = (0,0,0)
    for k in range(n):
        t = checkLigne2(i-k,j,1,0,n,joueur,err)
        if t!=0:
            return t
        t = checkLigne2(i-k,j-k,1,1,n,joueur,err)
        if t!=0:
            return t
        t = checkLigne2(i,j-k,0,1,n,joueur,err)
        if t!=0:
            return t
        t = checkLigne2(i-k,j+k,1,-1,n,joueur,err)
        if t!=0:
            return t
    return t
def checkGagnant():
    for i in range(7):
        for j in range(6):
            t = check4Lignes(i,j,4)
            if t!=0:
                return t
    return 0

def creerballe(x,y,col):
    coul = "red"
    coul2 = "red2"
    if col == -1:
        coul = "yellow"
        coul2 = "gold"
    (can.create_oval(x*100+2, y*100+2, (x+1)*100-2, (y+1)*100-2, fill = coul2))
    (can.create_oval(x*100+10, y*100+10, (x+1)*100-10, (y+1)*100-10, fill = coul, width = 0))
    

def updatecurseur(direction):
    for i in range(2):
        can.move(curseurlignes[i],direction*100,0)

def mooveballeleft(event):
    bougercurseur(-1)

def mooveballeright(event):
    bougercurseur(1)

def bougercurseur(direction):
    global curseur
    if curseur==6 and direction >0:
        return
    if curseur==0 and direction <0:
        return
    curseur+=direction
    updatecurseur(direction)

def checkDraw():
    for i in range(7):
        if grille[i][0] == 0:
            return False
    return True
    
def poserballe(e, pos = -1):
    global tour
    
    if pos == -1:
        pos = curseur
    posy = -1
    for j in range(5,-1,-1):
        if grille[pos][j] == 0:
            posy = j
            break
    if posy>=0:
        grille[pos][posy] = tour
        creerballe(pos,posy,tour)
        tour = -tour
        g = checkGagnant()
        if g != 0:
            st = "jaune"
            if g == 1:
                st = "rouge"
            showinfo("Partie Terminée", "Le joueur "+st+" gagne la partie")
            reboot()
        if checkDraw():
            showinfo("Partie Terminée", "Match nul!")
            reboot()
            
        if jouerIA and tour == 1:
            IA()
    
can.bind("<Left>", mooveballeleft)
can.bind("<Right>", mooveballeright)
can.bind("<Down>", poserballe)
can.bind("<Up>", iachoice)

def SimulateHumanWin():
    possibilites = []
    for i in range(7):
        for j in range(5,-1,-1):
            if grille[i][j] == 0:
                possibilites.append((i,j))
                break
            
    for poss in possibilites:
        if superCheck(poss[0],poss[1],4,-1,1) != 0:
            return True
    return False

def IA():
    possibilites = []
    for i in range(1,6):
        for j in range(5,-1,-1):
            if grille[i][j] == 0:
                possibilites.append((i,j))
                break
            
    shuffle(possibilites)
    for j in range(5,-1,-1):
            if grille[0][j] == 0:
                possibilites.append((0,j))
                break
    for j in range(5,-1,-1):
            if grille[6][j] == 0:
                possibilites.append((6,j))
                break
            
    for err in range(1,4):
        for poss in possibilites:
            c = superCheck(poss[0],poss[1],4,1,err)
            if c != 0:
                grille[poss[0]][poss[1]] = 1
                if SimulateHumanWin():
                    pass
                    grille[poss[0]][poss[1]] = 0
                else:
                    grille[poss[0]][poss[1]] = 0
                    poserballe(None,poss[0])
                    return
                
        for poss in possibilites:
            c = superCheck(poss[0],poss[1],4,-1,err)
            if c != 0:
                grille[poss[0]][poss[1]] = 1
                if SimulateHumanWin():
                    pass
                    grille[poss[0]][poss[1]] = 0
                else:
                    grille[poss[0]][poss[1]] = 0
                    poserballe(None,poss[0])
                    return
    for i in range(len(possibilites)):
        poss = possibilites[i]
        grille[poss[0]][poss[1]] = 1
        if SimulateHumanWin():
            grille[poss[0]][poss[1]] = 0
        else:
            grille[poss[0]][poss[1]] = 0
            poserballe(None,poss[0])
            return
    
    poserballe(None,possibilites[0][0])
    return

can.pack()
can.focus_set()
reboot()
mainloop()

