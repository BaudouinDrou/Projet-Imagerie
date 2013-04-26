#!/usr/bin/python2
#-*- coding: UTF-8 -*-

# Objectifs :
#
# -> charger l'image dans le canvas CLEAR
# -> ouvrir une à partir du programmme pour la modifier CLEAR
# -> creer une barre d'outils suplémentaire (afin de pouvoir par exemple revenir en arrière)
# -> rendre fonctionnel le filtre dessin et creer de nouveaux filtres (dont celui de l'histogramme tel qu'enoncé dans le sujet)
# -> creer une barre de chargement
# -> donner la possibilté de revenir en arriere en stockant les anciennes images dans un tableau (à mettre dans la classe Image_open)
# mais en limitant à un maximum de 15 images (arbitraire).
# -> donner la possibilité de réinitialiser l'image (utiliser le champs Image_open.tabPixOriginal)

from __future__ import print_function, division
import sys
from Tkinter import Tk, Frame, Canvas
import ImageTk
from Filtres import *
from tkSimpleDialog import *
import tkFileDialog
from PIL import *
from Image import *

from filtreTool import *
from Filtres import *
from fenetres import *
import time
fen = Tk()
image = Image_open("images/imgUbuntu.jpg")
largeurEcran , hauteurEcran = fen.winfo_screenwidth(),fen.winfo_screenheight()
xsize,ysize = image.largeur, image.hauteur

def actualiserCanvas(image,xsize,ysize):
	photo = ImageTk.PhotoImage(image)
	workbench.create_image((largeurEcran - xsize)/2,(hauteurEcran - ysize)/2,anchor = NW,image=photo)
	workbench.pack(photo)

def moyen2():
	filtre = Filtre()
	filtre.moyen(image)
	actualiserCanvas(image.donneImage(),xsize,ysize)


def contour2():
	filtre = Filtre()
	imTmp = image.donneImage().copy()
	t = filtre.contour(image)
	imTmp.putdata(t)
	image.ajouterImage(imTmp)
	actualiserCanvas(image.donneImage(),xsize,ysize)


def inversion2():
	filtre = FiltreLut()
	imTmp = image.donneImage().copy()
	t = filtre.inversionC(image)
	imTmp.putdata(t)
	image.ajouterImage(imTmp)
	actualiserCanvas(image.donneImage(),xsize,ysize)
	

def filtreCouleurVert():
	filtre = Filtre()
	imTmp = image.donneImage().copy()
	t = filtre.filtreCouleurVert(image)
	imTmp.putdata(t)
	image.ajouterImage(imTmp)
	actualiserCanvas(image.donneImage(),xsize,ysize)
	
def filtreCouleurRouge():
	filtre = Filtre()
	imTmp = image.donneImage().copy()
	t = filtre.filtreCouleurRouge(image)
	imTmp.putdata(t)
	image.ajouterImage(imTmp)
	actualiserCanvas(image.donneImage(),xsize,ysize)

def filtreCouleurBleu():
	filtre = Filtre()
	imTmp = image.donneImage().copy()
	t = filtre.filtreCouleurBleu(image)
	imTmp.putdata(t)
	image.ajouterImage(imTmp)
	actualiserCanvas(image.donneImage(),xsize,ysize)

def dessinCanvas():
	filtre = Filtre()
	imTmp = image.donneImage().copy()
	t = filtre.dessin(image)
	imTmp.putdata(t)
	image.ajouterImage(imTmp)
	actualiserCanvas(image.donneImage(),xsize,ysize)
	
def retourArriereCanvas():
	imTmp = image.retourArriere()
	if(imTmp != None):
			actualiserCanvas(image.donneImage(),xsize,ysize)

def retourAvantCanvas():
	imTmp = image.retourAvant()
	if(imTmp != None):
			actualiserCanvas(image.donneImage(),xsize,ysize)
			
def reinitialiserImageCanvas():
	reinitialiserImage(image)
	actualiserCanvas(image.donneImage(),xsize,ysize)
	
def choisirImage():
	try :
		chemin = tkFileDialog.askopenfilename(filetypes = [("Bilddateien", "*.jpg *.png *.gif *jpeg")])
		flag = True
	except :
		flag = False
	if(flag == True):
		workbench.delete(fen,"All")
		image.changerImage(chemin)
		image.donneImage().resize((xsize-100,ysize - 100))
		actualiserCanvas(image.donneImage(),xsize,ysize)



# -------------- MAIN ----------------------


workbench = Canvas(fen,height=hauteurEcran,width=largeurEcran,bg="#666")
workbench.grid(row = 1, column = 1, rowspan = 20, columnspan = 200)

statut = Label(text="Commencez le traitement !")
statut.grid(column=1,row=22)

menuTop = Menu(fen)

menuImage = Menu(menuTop)
menuImage.add_command(label="Nouvelle Image",command=None)
menuImage.add_separator()
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
bouton1 = Button(fen,background = "#333",command=reinitialiserImageCanvas)
bouton1.width = 1
bouton1.height = 1
imgBouton = ImageTk.PhotoImage(file = "images/annuler.png")
bouton1.configure(image = imgBouton)
bouton1.grid(row = 0, column = 1)
bouton2 = Button(fen, background = "#333",command=choisirImage)
bouton2.width = 1
bouton2.height = 1
bouton2.grid(row = 0, column = 2)
imgBouton2 = ImageTk.PhotoImage(file = "images/ouvrir_fichier.jpg")
bouton2.configure(image = imgBouton2)
bouton3 = Button(fen, background = "#333",command=retourArriereCanvas)
bouton3.width = 1
bouton3.height = 1
bouton3.grid(row = 0, column = 3)
imgBouton3 = ImageTk.PhotoImage(file = "images/precedent.png")
bouton3.configure(image = imgBouton3)
bouton4 = Button(fen, background = "#333",command=retourAvantCanvas)
bouton4.width = 1
bouton4.height = 1
bouton4.grid(row = 0, column = 4)
imgBouton4 = ImageTk.PhotoImage(file = "images/suivant.png")
bouton4.configure(image = imgBouton4)
fen.title("Traitement photo")

fen.config(menu=menuTop)

fen.mainloop()
