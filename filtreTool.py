#!/usr/bin/python2
#-*- coding: UTF-8 -*-

from __future__ import print_function, division

from Tkinter import *
import Image
import PSDraw
from random import randint
from math import *


class BarreChargement:

	def __init__(self,largeurImage,hauteurImage):
		self.hauteurImage = hauteurImage
		self.largeurImage = largeurImage
		self.largeurApplication = largeurImage
		self.hauteurApplication = hauteurImage
		self.ratio = (self.hauteurApplication*self.largeurApplication)/(self.hauteurImage*self.largeurImage)
		self.tailleBarre = largeurImage
		self.fenetre = Toplevel()
		self.fenetre.overrideredirect(1)
		self.fenetre.wm_geometry("%dx%d+%d+%d" % (self.tailleBarre, 10,0, 90))
		self.canvas = Canvas(self.fenetre, height = 10, width = self.tailleBarre, bg = "#666")
		self.canvas.grid(row = 0, column = 0, rowspan = 10, columnspan = self.tailleBarre)
		self.posBarrePrecedent = 0
	
	def changerRatio(self,largeurApplication,hauteurApplication):
		self.hauteurApplication = hauteurApplication
		self.largeurApplication = largeurApplication
		self.ratio = (self.hauteurApplication*self.largeurApplication)/(self.hauteurImage*self.largeurImage)
		
	def remplirBarre(self,indice):
		if(int(self.ratio)*indice != self.posBarrePrecedent):
			self.canvas.create_rectangle(self.posBarrePrecedent,0,int(self.ratio)*indice,10,outline='red')
			self.posBarrePrecedent = int(self.ratio)*indice
			self.canvas.pack()
			self.fenetre.update()
			
	def detruireBarre(self):
		self.fenetre.destroy()

class Histogramme:
	
	def __init__(self):
		self.hauteur = 250
		self.val = [0]*256
	
	def reinit(self,Image_open):
		t = Image_open.donneTabLuminance()
		for i in range(len(t)):
			self.val[t[i]] += 1
		max = 0
		for i in range(len(self.val)):
			if (self.val[i]>max):
				max = self.val[i]
		for i in range(len(self.val)):
			self.val[i] = (self.val[i]*self.hauteur)//max
			
	def afficher(self):
		fenHist = Toplevel()
		canvas = Canvas(fenHist,height = 256, width = 512, bg = "white")
		canvas.grid(row = 2, column = 0)
		tmp = 0
		for i in range(len(self.val)):
			canvas.create_rectangle(tmp,256-self.val[i],tmp+2,256,outline='#55CCFF', fill = '#55CCFF')
			tmp += 2
			canvas.update()
	
	
def connexN(x,y,data,size,n): #Les coordonées du point, le tableaude données, la taille du tableau, la largeur du masque
	xsize, ysize = size
	shift_x = 1
	shift_y = xsize
	rep = []
	for i in range(n):
		for j in range(n):
			try:
				rep.append(data[(j-1 + x)*shift_x + (i-1+y)*shift_y])
			except:
				rep.append(False)
	return rep

def creerMasqueGaussien(sigma):
	tailleTab = int(sigma*2 + 1)
	milieu = tailleTab//2
	rep = []
	for i in range(tailleTab):
		for j in range(tailleTab):
			rep.append(int(calculGauss(i-milieu, j-milieu,sigma)*100))
	return rep
	
def calculGauss(x,y,sigma):
	res = 1/(2*pi*sigma**2)
	res *= exp(-(x**2 + y**2)/(2*sigma**2))
	return res

def convertYUV(pix,mode):
	if mode == 'NB':
		return pix
	else:
		r,v,b = pix
		y = int(r*0.299 + v*0.587 + b*0.114)
		u = int(-r*0.14713 - v*0.28886 + b*0.436)
		v = int(r*0.615 - v*0.51498 - b*0.10001)
	return y,u,v

def convertY(pix,mode):
	if mode == 'NB':
		return pix
	else:
		r,v,b = pix
		y = int(r*0.299 + v*0.587 + b*0.114)
	return y

#Applique un masque de N cases en prenant un voisinnage de 8-connexité sur des données d'images
#Retourne un tableau de la taille du tabelau donné en entrée
def applyMask(mask,data,mode,size):
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
		barreC.canvas.pack()
		for y in range(ysize):
			if mode == 'NB':	#Cas NB
				voisins = connexN(x,y,data,size,n)
				for i in range(n):
					for j in range(n):
						val = 0
						if voisins[i*n+j] != False:
							val = voisins[i*n+j]
						val += mask[i*n+j]*voisins[i*n+j]
				res[x*shift_x+y*shift_y] = (val)/div
			else:				#Cas couleur
				voisins = connexN(x,y,data,size,n)
				valR,valG,valB = 0,0,0
				for i in range(n):
					for j in range(n):
						R,G,B = 0,0,0
						if voisins[i*n+j] != False:
							R,G,B = voisins[i*n+j]
						valR += mask[i*n+j]*R
						valG += mask[i*n+j]*G
						valB += mask[i*n+j]*B
				res[x*shift_x+y*shift_y] = valR//div,valG//div,valB//div
	barreC.detruireBarre()
	return res

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
	Image_open.reinit(Image_open.donneImage(0))
