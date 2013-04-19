#!/usr/bin/python2
#-*- coding: UTF-8 -*-

# Objectifs :
#
# -> charger l'image dans le canvas
# -> ouvrir une à partir du programmme pour la modifier
# -> creer une barre d'outils suplémentaire (afin de pouvoir par exemple revenir en arrière)
# -> rendre fonctionnel le filtre dessin et creer de nouveaux filtres (dont celui de l'histogramme tel qu'enoncé dans le sujet)
# -> creer une barre de chargement
# -> donner la possibilté de revenir en arriere en stockant les anciennes images dans un tableau tabIm (à mettre dans la classe Image_open)
# mais en limitant à un maximum de 15 images (arbitraire).=> implique compliqcations pour connaitre l'emplacement de la dernière image : on fait un champ indice en plus ?
# -> donner la possibilité de réinitialiser l'image (utiliser le champ tabIm donnant la liste des images )

from __future__ import print_function, division

from Tkinter import Tk, Frame, Canvas
import ImageTk

from Filtres import *

from PIL import *
from Image import *

from filtreTool import *
from Filtres import *

from fenetres import *
import time

image = Image_open("images/imgtest.jpg")
#im = Image.open("images/imgtest.jpg")
xsize,ysize = image.largeur, image.hauteur
xsize, ysize = xsize//2,ysize//2
im = image.donneImage().resize((xsize, ysize))

def moyen2():
	filtre = Filtre()
	filtre.moyen(image)


def contour2():
    im2 = image.donneImage().copy()
    filtre = Filtre()
    t = filtre.contour(image)
    im2.putdata(t)
    im2.show()


def inversion2():
    im2 = image.donneImage().copy()
    filtre = FiltreLut()
    t = filtre.inversionC(image)
    im2.putdata(t)
    im2.show()
    workbench.create_image(xsize/2,ysize/2, image = ImageTk.PhotoImage(im2))
    workbench.grid(column=1,row=1)

def filtreCouleurVert():
	im2 = image.donneImage().copy()
	filtre = Filtre()
	t = filtre.filtreCouleurVert(image)
	im2.putdata(t)
	im2.show()
	
def filtreCouleurRouge():
	filtre = Filtre()
	t = filtre.filtreCouleurRouge(image)
	image.donneImage().putdata(t)
	image.tabIm[len(image.tabIm)-1] = image.donneImage().resize((xsize, ysize))

def filtreCouleurBleu():
	#im = donneImage().copy()
	filtre = Filtre()
	t = filtre.filtreCouleurBleu(image)
	image.donneImage().putdata(t)
	image.tabIm[len(image.tabIm)-1] = image.donneImage().resize((xsize, ysize))

def dessinCanvas():
	im2 = image.donneImage().copy()
	filtre = Filtre()
	t = filtre.dessin(image)
	im2.putdata(t)
	im2.show()
	
def reinitialiserImageCanvas():
	reinitialiserImage(image)
	
# -------------- MAIN ----------------------

fen = Tk()

filtreCouleurRouge()
defaultBackground = ImageTk.PhotoImage(image.donneImage())

workbench = Canvas(fen,height=ysize,width=xsize,bg="#000")
workbench.create_image(xsize/2,ysize/2, image=defaultBackground)
workbench.grid(column=1,row=1)

statut = Label(text="Commencez le traitement !")
statut.grid(column=1,row=2)

menuTop = Menu(fen)

menuImage = Menu(menuTop)
menuImage.add_command(label="Nouvelle Image",command=None)
menuImage.add_separator()
menuImage.add_command(label="Afficher",command=im.show)
menuImage.add_command(label="Quitter",command=fen.destroy)

menuFiltre = Menu(menuTop)
menuFiltre.add_command(label="Median",command=None)
menuFiltre.add_separator()
menuFiltre.add_command(label="Moyen",command=moyen2)
menuFiltre.add_command(label="Contour",command=contour2)
menuFiltre.add_command(label="Inversion",command=inversion2)
menuFiltre.add_command(label="Rouge",command=filtreCouleurRouge)
menuFiltre.add_command(label="Vert",command=filtreCouleurVert)
menuFiltre.add_command(label="Bleu",command=filtreCouleurBleu)
menuFiltre.add_command(label="Dessin",command=dessinCanvas)
menuFiltre.add_command(label="Reinit",command=reinitialiserImageCanvas)

menuAide = Menu(menuTop)
menuAide.add_command(label="Les outils",command=afficherOutils)
menuAide.add_command(label="A propos ...",command=afficherAPropos)

menuTop.add_cascade(label="Image",menu=menuImage)
menuTop.add_cascade(label="Filtre",menu=menuFiltre)
menuTop.add_cascade(label="?",menu=menuAide)

fen.title("Traitement photo")

fen.config(menu=menuTop)

fen.mainloop()

