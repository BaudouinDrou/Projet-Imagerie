#!/usr/bin/python2
#-*- coding: UTF-8 -*-

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
background = ImageTk.PhotoImage(image.donneImage())
largeurEcran , hauteurEcran = fen.winfo_screenwidth(),fen.winfo_screenheight()
xsize,ysize = image.largeur, image.hauteur

		
def redimensionner(image_open):
	if((image_open.largeur > largeurEcran) or(image_open.hauteur > hauteurEcran)):
		imTmp1 = image_open.donneImage().copy()
		if(largeurEcran/image_open.largeur <= hauteurEcran/image_open.hauteur):
			imTmp1 = imTmp1.resize((largeurEcran,int(image_open.hauteur*largeurEcran/image_open.largeur)))
			image_open.largeur, image_open.hauteur = (largeurEcran,int(image_open.hauteur*largeurEcran/image_open.largeur))
		else:
			imTmp1 = imTmp1.resize((int(image_open.largeur*hauteurEcran/image_open.hauteur),hauteurEcran))
			image_open.largeur, image_open.hauteur = (int(image_open.largeur*hauteurEcran/image_open.hauteur),hauteurEcran)
		image_open.reinit(imTmp1)
		image_open.tabPix = list(imTmp1.getdata())
		xsize,ysize = image_open.largeur, image_open.hauteur
		

def actualiserCanvas(t,xsize,ysize):
	imTmp = image.donneImage().copy()
	imTmp.putdata(t)
	image.ajouterImage(imTmp)
	photo = ImageTk.PhotoImage(image.donneImage())
	workbench.create_image((largeurEcran - xsize)/2,(hauteurEcran - ysize)/2,anchor = NW,image=photo)
	workbench.pack(photo)

def moyen2():
	filtre = Filtre()
	t = filtre.moyen(image)
	actualiserCanvas(t,image.largeur,image.hauteur)


def contour2():
	filtre = Filtre()
	t = filtre.contour(image)
	actualiserCanvas(t,image.largeur,image.hauteur)


def inversion2():
	filtre = FiltreLut()
	t = filtre.inversionC(image)
	actualiserCanvas(t,image.largeur,image.hauteur)
	
def cryptageC():
	filtre = FiltreLut()
	t = filtre.cryptageCouleur(image)
	actualiserCanvas(t,image.largeur,image.hauteur)
	
def decryptageC():
	filtre = FiltreLut()
	t = filtre.decryptageCouleur(image)
	actualiserCanvas(t,image.largeur,image.hauteur)

def median():
	filtre = Filtre()
	t = filtre.filtreMedian(image)
	actualiserCanvas(t,image.largeur,image.hauteur)

def filtreCouleurVert():
	filtre = Filtre()
	t = filtre.filtreCouleur(image,'V')
	actualiserCanvas(t,image.largeur,image.hauteur)
	
def filtreCouleurRouge():
	filtre = Filtre()
	t = filtre.filtreCouleur(image,'R')
	actualiserCanvas(t,image.largeur,image.hauteur)

def filtreCouleurBleu():
	filtre = Filtre()
	t = filtre.filtreCouleur(image,'B')
	actualiserCanvas(t,image.largeur,image.hauteur)

def filtreGaussien():
	filtre = Filtre()
	t = filtre.gaussien(image)
	actualiserCanvas(t,image.largeur,image.hauteur)

def dessinCanvas():
	filtre = Filtre()
	t = filtre.dessin(image)
	actualiserCanvas(t,image.largeur,image.hauteur)

def histogramme():
	hist = Histogramme()
	hist.reinit(image)
	hist.afficher()
	actualiserCanvas(image.tabPix,image.largeur,image.hauteur)
	
	
def retourArriereCanvas():
	imTmp = image.retourArriere()
	if(imTmp != None):
		photo = ImageTk.PhotoImage(imTmp)
		workbench.create_image((largeurEcran - image.largeur)/2,(hauteurEcran - image.hauteur)/2,anchor = NW,image=photo)
		workbench.pack(photo)
		

def retourAvantCanvas():
	imTmp = image.retourAvant()
	if(imTmp != None):
		photo = ImageTk.PhotoImage(imTmp)
		workbench.create_image((largeurEcran - image.largeur)/2,(hauteurEcran - image.hauteur)/2,anchor = NW,image=photo)
		workbench.pack(photo)
			
def reinitialiserImageCanvas():
	reinitialiserImage(image)
	actualiserCanvas(image.tabPix,image.largeur,image.hauteur)
	
def choisirImage():
	try :
		chemin = tkFileDialog.askopenfilename(filetypes = [("Bilddateien", "*.jpg *.png *.gif *jpeg")])
		flag = True
	except :
		flag = False
	if(flag == True):
		workbench.delete(fen,"all")
		image.changerImage(chemin)
		redimensionner(image)
		actualiserCanvas(image.tabPix,image.largeur,image.hauteur)

def saveFile():
	fichier = tkFileDialog.asksaveasfilename()
	image.donneImage().save(fichier)


# -------------- MAIN ----------------------


workbench = Canvas(fen,height=hauteurEcran,width=largeurEcran,bg="#666")
workbench.create_image((largeurEcran - xsize)/2,(hauteurEcran - ysize)/2,anchor = NW,image=background)
workbench.grid(row = 1, column = 1, rowspan = 20, columnspan = 200)

statut = Label(text="Commencez le traitement !")
statut.grid(column=1,row=22)
menuTop = Menu(fen)

menuImage = Menu(menuTop)
menuImage.add_command(label="Nouvelle Image",command=None)
menuImage.add_separator()
menuImage.add_command(label="Quitter",command=fen.destroy)

menuFiltre = Menu(menuTop)
menuFiltre.add_command(label="Median",command=median)
menuFiltre.add_command(label="Moyen",command=moyen2)
menuFiltre.add_command(label="Contour",command=contour2)
menuFiltre.add_command(label="Inversion",command=inversion2)
menuFiltre.add_command(label="Crypatage couleur",command=cryptageC)
menuFiltre.add_command(label="Decryptage couleur",command=decryptageC)
menuFiltre.add_command(label="Rouge",command=filtreCouleurRouge)
menuFiltre.add_command(label="Vert",command=filtreCouleurVert)
menuFiltre.add_command(label="Bleu",command=filtreCouleurBleu)
menuFiltre.add_command(label="Dessin",command=dessinCanvas)
menuFiltre.add_command(label="Gaussien",command=filtreGaussien)
menuFiltre.add_command(label="Histogramme",command=histogramme)

menuAide = Menu(menuTop)
menuAide.add_command(label="A propos ...",command=afficherAPropos)

menuTop.add_cascade(label="Image",menu=menuImage)
menuTop.add_cascade(label="Filtre",menu=menuFiltre)
menuTop.add_cascade(label="?",menu=menuAide)
bouton1 = Button(fen,background = "#333",command=reinitialiserImageCanvas)
bouton1.width = 1
bouton1.height = 1
imgBouton = ImageTk.PhotoImage(file = "images/annuler.png")
bouton1.configure(image = imgBouton)
bouton1.grid(row = 0, column = 2)
bouton2 = Button(fen, background = "#333",command=choisirImage)
bouton2.width = 1
bouton2.height = 1
bouton2.grid(row = 0, column = 3)
imgBouton2 = ImageTk.PhotoImage(file = "images/ouvrir_fichier.jpg")
bouton2.configure(image = imgBouton2)
bouton3 = Button(fen, background = "#333",command=retourArriereCanvas)
bouton3.width = 1
bouton3.height = 1
bouton3.grid(row = 0, column = 4)
imgBouton3 = ImageTk.PhotoImage(file = "images/precedent.png")
bouton3.configure(image = imgBouton3)
bouton4 = Button(fen, background = "#333",command=retourAvantCanvas)
bouton4.width = 1
bouton4.height = 1
bouton4.grid(row = 0, column = 5)
imgBouton4 = ImageTk.PhotoImage(file = "images/suivant.png")
bouton4.configure(image = imgBouton4)
bouton5 = Button(fen, background = "#333",command=saveFile)
bouton5.width = 1
bouton5.height = 1
bouton5.grid(row = 0, column = 6)
imgBouton5 = ImageTk.PhotoImage(file = "images/save.png")
bouton5.configure(image = imgBouton5)
fen.title("Traitement photo")
fen.config(menu=menuTop)
fen.mainloop()
