#!/usr/bin/python2
#-*- coding: UTF-8 -*-

from __future__ import print_function, division

from Tkinter import Tk, Canvas
import Image
import PSDraw
from random import randint
from math import sqrt


class BarreChargement:

	def __init__(self,hauteurImage,largeurImage):
		self.hauteurImage = hauteurImage
		self.largeurImage = largeurImage
		self.largeurApplication = largeurImage
		self.hauteurApplication = hauteurImage
		self.ratio = (self.hauteurApplication*self.largeurApplication)/(self.hauteurImage*self.largeurImage)
		if(largeurImage > hauteurImage):
			self.tailleBarre = largeurImage
		else :
			self.tailleBarre = hauteurImage
		self.fenetre = Tk()
		self.canvas = Canvas(self.fenetre, height = 10, width = self.tailleBarre, bg = "#666")
		self.canvas.grid(row = 0, column = 0, rowspan = 10, columnspan = self.tailleBarre)
		self.posBarrePrecedent = 0
	
	def changerRatio(self,largeurApplication,hauteurApplication):
		self.hauteurApplication = hauteurApplication
		self.largeurApplication = largeurApplication
		self.ratio = (self.hauteurApplication*self.largeurApplication)/(self.hauteurImage*self.largeurImage)
		
	def remplirBarre(self,indice):
		if(int(self.ratio)*indice != self.posBarrePrecedent):
			self.canvas.create_rectangle(self.posBarrePrecedent,0,int(self.ratio)*indice,10,fill = "#006")
			self.posBarrePrecedent = int(self.ratio)*indice
			self.canvas.pack()
			#self.fenetre.mainloop()
			
	def detruireBarre(self):
		self.fenetre.destroy()





def connex8(x,y,data, size):
	xsize, ysize = size
	shift_x = 1
	shift_y = xsize
	rep = [(0,0,0)]*9
	#le tableau est de la forme rep = [V(x0,y0), V(x,y0), V(x+1,y0), ...., V(x+1,y+1)] ou V(x,y) est la valeur du pixel a la pos (x,y).
	if y == 0 : #traitement du cas particulier de la premiere ligne
		for i in range(3):
			rep[i] = False
	if x == xsize-1: #traitement du cas particulier de la derniere colonne
		for i in range(3):
			rep[i*3+2] = False
	if y == ysize-1: #traitement du cas particulier de la derniere ligne
		for i in range(3):
			rep[i+6] = False
	if x == 0: #traitement du cas particulier de la premiere colonne
		for i in range(3):
			rep[i*3] = False
	#Cas général
	for i in range(3):
		for j in range(3):
			if (rep[i*3 + j] != False):
				rep[i*3+j] = data[(j-1 + x)*shift_x + (i-1+y)*shift_y]
	return rep


def applyMask(mask,data,mode, size): #Applique un masque de 9 cases en prenant un voisinnage de 8-connexité sur des données d'images
	xsize, ysize = size
	shift_x = 1
	shift_y = xsize
	res = [0]*ysize*xsize
	div = 0
	N = len(mask)
	n = int(sqrt(N))
	barreC = BarreChargement(xsize,ysize)
	for a in range(N):
		div += mask[a]
	if div == 0:
		div = 1
	for x in range(xsize):
		barreC.remplirBarre(x)
		for y in range(ysize):
			if mode == 'NB':	#Cas NB
				voisins = connex8(x,y,data, size)
				for i in range(n):
					for j in range(n):
						val = 0
						if voisins[i*n+j] != False:
							val = voisins[i*n+j]
						val += mask[i*n+j]*voisins[i*n+j]
				res[x*shift_x+y*shift_y] = val/div
			else:				#Cas couleur
				voisins = connex8(x,y,data, size)
				valR,valG,valB = 0,0,0
				for i in range(n):
					for j in range(n):
						R,G,B = 0,0,0
						if voisins[i*n+j] != False:
							R,G,B = voisins[i*n+j]
						valR += mask[i*n+j]*R
						valG += mask[i*n+j]*G
						valB += mask[i*n+j]*B
				res[x*shift_x+y*shift_y] = (int(valR/div),int(valG/div),int(valB/div))
	barreC.detruireBarre()
	return res

def applyLUT(LUT,data,mode, size):			#LUT unidimensionnel en NB et bidimensionnel (3*256) en couleurs
	xsize, ysize = size
	shift_x = 1
	shift_y = xsize
	if mode == 'NB':
		for y in range(ysize):
			for x in range(xsize):
				data[x*shift_x + y*shift_y] = LUT[data[x*shift_x + y*shift_y]]	#Application de la LUT au pixel de coordonées (x,y) : pix(x,y) = LUT[pix(x,y)]
	else:
		for y in range(ysize):
			for x in range(xsize):
				(R, V, B) = data[x*shift_x + y*shift_y]
				data[x*shift_x + y*shift_y] = (LUT[0][R], LUT[1][V], LUT[2][B])	#Application de la LUT au pixel de coordonées (x,y) : pix(x,y) = LUT[pix(x,y)]
	return data

def evolveLUT(LUT):		#Prend en parametre une LUT unidimensionnelle et la renvoie en 2 dimension
	LUT2D = [0] * 3
	for j in range(3):
		LUT2D[j] = [0]*256
	for i in range(256):
		LUT2D[0][i] = LUT[i]
		LUT2D[1][i] = LUT[i]
		LUT2D[2][i] = LUT[i]
	return LUT2D

def copyTabPix(tabPix):
	try :
		R,V,B = tabPix[0]
		mode = "couleur"
	except :
		mode = "NB"
	if(mode == "couleur"):
		tabCopy = [0] * len(tabPix)
		for i in range(len(tabPix)):
			tabCopy[i] = tabPix[i]
	else:
		tabCopy = [0]*len(tabPix)
		for i in range(len(tabPix)):
			tabCopy[i] = tabPix[i]
	return tabCopy

def reinitialiserImage(Image_open):
	Image_open.tabPix = copyTabPix(Image_open.donneImage(0).getdata())
	Image_open.donneImage().putdata(Image_open.tabPix)
	print("tabReinit : ")
	print(Image_open.tabPix[0])	
