#coding = <UTF-8>
#-*-coding:Latin-1 -*


from Tkinter import *
import Image
import PSDraw
from filtreTool import *
from fenetres import *

class Image_open:

	""" Classe definissant une image caracterisee par :
	- son nom
	- l'image correspondant au nom
	- son tableau de pixel modifié
	- son tableau de pixel original
	- sa largeur 
	- sa longeur
	- indice image en cours"""
	
	def __init__(self,nom):
		R,V,B = 0,0,0
		self.nom = nom
		self.tabIm = []
		try :
			self.reinit(Image.open(nom))
			try : 
				self.tabPixOriginal = list(self.tabIm[0].getdata())
				self.tabPix = list(self.tabIm[0].getdata())
			except :
				self.tabPix = 0
				print("L'image n'a pas pu etre converti en tableau de pixel")
			self.largeur, self.hauteur = self.tabIm[0].size
			try : 
				R,V,B = self.tabPix[0]
				self.mode = "couleur"
			except :
				self.mode = "NB"
		except :
			self.indice = -1
			self.tabIm.append(0)
			print("L'image n'a pas pu etre ouverte")
	
	def donneMode(self):
		print(self.mode)
		return self.mode
	
	def donneImage(self, indice = None): #Par defaut, image en cours
		if (indice == None):
			indice = self.indice
		return self.tabIm[indice]
	
	def ajouterImage(self,image):
		try:
			self.tabIm[indice] = image
		except:
			self.tabIm.append(image)
		self.indice += 1
		self.indiceMax = self.indice
	
	def reinit(self,image):
		self.tabIm = []
		self.tabIm.append(image)
		self.indice = 0
		self.indiceMax = 0
		
	
	def retourArriere(self):
		if(self.indice > 0):
			self.indice -= 1
			return self.tabIm[self.indice]
		else:
			nonRetourArriere()
	
	def retourAvant(self):
		if(self.indice < self.indiceMax):
			self.indice += 1
			return self.tabIm[self.indice]
		else:
			nonRetourAvant()
			return None
	
	def changerImage(self,nom):
		R,V,B = 0,0,0
		self.nom = nom
		self.tabIm = []
		try :
			self.tabIm.append(Image.open(nom))
			self.indice = 0
			self.indiceMax = 0
			try : 
				self.tabPixOriginal = list(self.tabIm[0].getdata())
				self.tabPix = list(self.tabIm[0].getdata())
			except :
				self.tabPix = 0
				print("L'image n'a pas pu etre converti en tableau de pixel")
			self.largeur, self.hauteur = self.tabIm[0].size
			try : 
				R,V,B = self.tabPix[0]
				self.mode = "couleur"
			except :
				self.mode = "NB"
		except :
			self.indice = -1
			self.tabIm.append(0)
			print("L'image n'a pas pu etre ouverte")
			
	def donneVoisins(self, x,y,mode):
		rep = [(0,0,0)]*9
		#le tableau est de la forme rep = [V(x-1,y-1), V(x,y-1), V(x+1,y-1), ...., V(x+1,y+1)] ou V(x,y) est la valeur du pixel a la pos (x,y).
		if y == 0 : #traitement du cas particulier de la premiere ligne
			for i in range(3):
				rep[i] = 'abs'
		if x == self.largeur-1: #traitement du cas particulier de la derniere colonne
			for i in range(3):
				rep[i*3 +2] = 'abs'
		if y == self.hauteur-1: #traitement du cas particulier de la derniere ligne
			for i in range(3):
				rep[i + 6] = 'abs'
		if x == 0: #traitement du cas particulier de la premiere colonne
			for i in range(3):
				rep[i*3]
		for i in range(3):
			for j in range(3):
				if rep[i*3 + j] != 'abs':
					rep[i*3+j] = self.tabPix[(j-1 + x)*1 + (i-1+y)*self.largeur]
		if(mode == 4):
			rep[0] = rep[1]
			rep[1] = rep[3]
			rep[2] = rep[4]
			rep[3] = rep[5]
			rep[4] = rep[7]
		return rep

class Filtre:

	"""Classe permettant de creer differents filtres et de les appliquer, ces
	filtres peuvent etre caracterises par une matrice de convolution
	"""

	def __init__(self):
		self.convo = [0,0,0,0,1,0,0,0,0]

	def setConvo(self,matriceConvo):
		self.convo = matriceConvo

	def filtreMoyen(self,Image_open):
		tmp = [(0,0,0)]*9
		res = [(0,0,0)]*(Image_open.longeur)*(Image_open.largeur)
		for i in range(Image_open.hauteur):
			for j  in range(Image_open.largeur):
				tmp = Image_open.donneVoisins(Image_open,j,i,8)
				cmp = 0
				(R,V,B)=(0,0,0)
				moyenR = 0
				moyenV = 0
				moyenB = 0
				for k in range(len(tmp)):
					if tmp[k] != 'abs' :
						cmp+=1
						(R, V, B) = tmp[k]
						moyenR += int(R)
						moyenB += int(B)
						moyenV += int(V)
				moyenR = int(moyenR/cmp)
				moyenB = int(moyenB/cmp)
				moyenV = int(moyenV/cmp)
				res[j*1 + i*Image_open.largeur] = moyenR,moyenV,moyenB
		return res

	def filtreMedian(self,Image_open):
		tmp = [(0,0,0)]*9
		res = [(0,0,0)]*(Image_open.largeur)*(Image_open.hauteur)
		for i in range(Image_open.hauteur):
			for j  in range(Image_open.largeur):
				tmp = Image_open.donneVoisins(Image_open,j,i,8)
				tmp.sort()
				res[j*1 + i*Image_open.largeur] = tmp[3]
		return res

	def moyen(self,Image_open):
		t = list(Image_open.donneImage().getdata())
		mask = [1,1,1,1,1,1,1,1,1]
		size = (Image_open.largeur,Image_open.hauteur)
		return applyMask(mask,t,Image_open.donneMode(), size)

	def gaussien(self,sigma):
		t = list(Image_open.donneImage().getdata())
		mask = [1,2,1,2,5,2,1,2,1]
		size = (Image_open.largeur,Image_open.hauteur)
		return applyMask(mask,t,Image_open.donneMode(), size)

	def contour(self,Image_open):
		t = list(Image_open.donneImage().getdata())
		mask = [0,0,0,-1,1,0,0,0,0]
		size = (Image_open.largeur,Image_open.hauteur)
		return applyMask(mask,t,Image_open.donneMode(),size)

	def filtreCouleur(self, Image_open,couleur): #couleur est soit R, soit V, soit B
		t = Image_open.tabPix
		R,V,B = 0,0,0
		for i in range(len(t)):
			if(Image_open.donneMode() == "couleur"):
				R,V,B = t[i]
			else:
				R,V,V = t[i],t[i],t[i]
			if(couleur=='R'):
				t[i] = R,0,0
			elif(couleur=='V'):
				t[i] = 0,V,0
			else:
				t[i] = 0,0,B
		return t
	
#	def filtreCouleurBleu(self, Image_open):
#		if(Image_open.donneMode() == "couleur"):
#			t = Image_open.tabPix
#			R,V,B = 0,0,0
#			print(t[0])
#			for i in range(len(t)):
#				R,V,B = t[i]
#				t[i] = 0,0,B
#		return t
		
	def rotation(self,Image_open,sens):
		t = list(Image_open.getdata())
		data = [0]*Image_open.largeur*Image_open.hauteur
		for x in range(Image_open.largeur):
			for y in range(Image_open.hauteur):
				data[ x*Image_open.hauteur + y] = t[y + (Image_open.hauteur - x - 1)*Image_open.largeur]
		return data
	
	def dessin(self,Image_open):
		Image_open.tabPix = Filtre.contour(self,Image_open)
		filtreLut = FiltreLut()
		return(filtreLut.inversionC(Image_open))

class FiltreLut:

	def __init__(self):
		self.LUT = [0]*256
		self.LUTR = [0]*256
		self.LUTV = [0]*256
		self.LUTB = [0]*256


	def inversionC(self,Image_open):
		t = Image_open.tabPix
		for i in range(256):
			self.LUT[i] = 255 - i
		LUT2D = evolveLUT(self.LUT)
		return applyLUT(LUT2D,t,'couleur',(Image_open.largeur,Image_open.hauteur))
