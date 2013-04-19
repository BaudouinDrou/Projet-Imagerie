#coding = <UTF-8>
#-*-coding:Latin-1 -*


from Tkinter import *
import Image
import PSDraw
from filtreTool import *


class Image_open:

	""" Classe definissant une image caracterisee par :
	- son nom
	- son tableau de pixel (tabPix)
	- sa largeur 
	- sa longeur
	- tableau d'image (tabIm)"""
	
	def __init__(self,nom):
		R,V,B = 0,0,0
		self.nom = nom
		self.tabIm = []
		try :
			self.tabIm.append(Image.open(nom))
			try :
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
			print("L'image n'a pas pu etre ouverte")
			raise
			
	def donneMode(self):
		print(self.mode)
		return self.mode
	
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
	
	def donneTabPix(self): #Donne le tableau de pixels courant
		return self.tabPix
	
	def donneImage(self): #Renvoie l'image courante
		return self.tabIm[len(self.tabIm)-1]
	
	def reinitialiserImage(self): #Remet l'image à sa valeur originelle
		t = list(self.tabIm[0].getdata())
		self.tabPix = copyTabPix(t)

	def actualiseTabPix(self): #Fonction qui reactualise tabPix en fonction de la derniere image ajoutée a la liste
		t = list(self.donneImage().getdata()) #t contient le tableau de pixel de la dernière image ajoutee à la liste
		self.tabPix = copyTabPix(t)

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
		t = list(Image_open.image.getdata())
		mask = [1,1,1,1,1,1,1,1,1]
		size = Image_open.image.size
		return applyMask(mask,t,"couleur", size)


#def gaussien(im):


	def contour(self,Image_open):
		t = list(Image_open.image.getdata())
		mask = [0,0,0,-1,1,0,0,0,0]
		return applyMask(mask,t,'couleur',(Image_open.largeur,Image_open.hauteur))

	def filtreCouleurRouge(self, Image_open):
		if(Image_open.donneMode() == "couleur"):
			t = Image_open.tabPix
			R,V,B = 0,0,0
			print(t[0])
			for i in range(len(t)):
				R,V,B = t[i]
				t[i] = R,0,0
		return t
	
	def filtreCouleurVert(self, Image_open):
		if(Image_open.donneMode() == "couleur"):
			t = Image_open.tabPix
			R,V,B = 0,0,0
			print(t[0])
			for i in range(len(t)):
				R,V,B = t[i]
				t[i] = 0,V,0
		return t
	
	def filtreCouleurBleu(self, Image_open):
		if(Image_open.donneMode() == "couleur"):
			t = Image_open.tabPix
			R,V,B = 0,0,0
			print(t[0])
			for i in range(len(t)):
				R,V,B = t[i]
				t[i] = 0,0,B
		return t
		
	def rotation(self,Image_open,sens):
		t = list(Image_open.getdata())
		data = [0]*Image_open.largeur*Image_open.hauteur
		for x in range(Image_open.largeur):
			for y in range(Image_open.hauteur):
				#data[x*ysize - y] = t[x*1 + y*xsize]
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





