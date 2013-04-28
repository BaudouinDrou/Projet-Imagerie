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
		self.largeur = 0
		self.hauteur = 0
		self.tabPix = []
		self.tabPixOriginal = []
		self.indice = 0
		self.indiceMax = 0
		try :
			self.reinit(Image.open(nom))
			self.tabPixOriginal = list(self.tabIm[0].getdata())
			self.actualiseDonnees()
		except :
			self.indice = -1
			self.indiceMax = -1
			self.tabIm.append(0)
			print("L'image n'a pas pu etre ouverte")
	
	def donneMode(self):
		return self.mode
	
	def donneImage(self, indice = None): #Par defaut, image en cours
		if (indice == None):
			indice = self.indice
		return self.tabIm[indice]
	
	def ajouterImage(self,image):
		self.indice += 1
		self.indiceMax = self.indice
		if(self.indice < len(self.tabIm)):
			self.tabIm[self.indice] = image
		else:
			self.tabIm.append(image)
		self.actualiseDonnees()
		
	def actualiseTabPix(self):
		try:
			self.tabPix = list(self.tabIm[self.indice].getdata())
		except:
			self.tabPix = 0
			print("L'image n'a pas pu etre converti en tableau de pixel")
	
	def actualiseTaille(self):
		self.largeur, self.hauteur = self.tabIm[self.indice].size
		
	def actualiseMode(self):
		try:
			R,V,B = self.tabPix[self.indice]
			self.mode = "couleur"
		except:
			self.mode = "NB"
	
	def actualiseDonnees(self):
		self.actualiseMode()
		self.actualiseTabPix()
		self.actualiseTaille()
	
	def reinit(self,image):
		self.tabIm = []
		self.tabIm.append(image)
		self.indice = -1
		self.indiceMax = -1
		
	
	def retourArriere(self):
		if(self.indice > 0):
			self.indice -= 1
			self.actualiseDonnees()
			return self.tabIm[self.indice]
		else:
			nonRetourArriere()
			return None
	
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
	
	def donneTabYUV(self):
		t = []
		for i in range(len(self.tabPix)):
			t.append(convertYUV(self.tabPix[i],self.donneMode()))
		return t
	
	def donneTabLuminance(self):
		t = []
		for i in range(len(self.tabPix)):
			y,u,v = convertYUV(self.tabPix[i],self.donneMode())
			t.append(y)
		return t
		
	def donneVoisins(self,x,y,mode):
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
	Chaque  filtre prend en parametre une  Image_open
	Chaque filtre renvoie un tableau de pixel de la taille de l'image
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
				tmp = Image_open.donneVoisins(j,i,8)
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
				tmp = Image_open.donneVoisins(j,i,8)
				#tmp.sort()
				res[j*1 + i*Image_open.largeur] = tmp[4]
		return res

	def moyen(self,Image_open):
		t = list(Image_open.donneImage().getdata())
		mask = [1,1,1,1,1,1,1,1,1]
		size = (Image_open.largeur,Image_open.hauteur)
		return applyMask(mask,t,Image_open.donneMode(), size)

	def gaussien(self,Image_open,sigma=2):
		t = list(Image_open.donneImage().getdata())
		mask = creerMasqueGaussien(sigma)
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
		tmp = -1
		boolMode = (Image_open.donneMode() == "couleur")
		barreC = BarreChargement(Image_open.largeur,Image_open.hauteur)
		for i in range(len(t)):
			if(int(i/Image_open.hauteur) != tmp):
				barreC.remplirBarre(int(i/Image_open.hauteur))
				barreC.canvas.pack()
				tmp = int(i/Image_open.hauteur)
			if(boolMode):
				R,V,B = t[i]
			else:
				R,V,B = t[i],t[i],t[i]
			if(couleur=='R'):
				t[i] = R,0,0
			elif(couleur=='V'):
				t[i] = 0,V,0
			else:
				t[i] = 0,0,B
		barreC.detruireBarre()
		return t
			
	def rotation(self,Image_open,sens):
		t = list(Image_open.getdata())
		data = [0]*Image_open.largeur*Image_open.hauteur
		for x in range(Image_open.largeur):
			for y in range(Image_open.hauteur):
				data[ x*Image_open.hauteur + y] = t[y + (Image_open.hauteur - x - 1)*Image_open.largeur]
		return data
	
	def dessin(self,Image_open):
		t = self.contour(Image_open)
		filtreLut = FiltreLut()
		im = Image_open.donneImage()
		im.putdata(t)
		return(filtreLut.inversionC(Image_open))

class FiltreLut:

	"""Classe permettant de creer differents filtres et de les appliquer
	Ces	filtres sont caractérisés par une LUT
	Chaque  filtre prend en parametre une  Image_open
	Chaque filtre renvoie un tableau de pixel de la taille de l'image
	- LUT NB
	- LUT couleur
	- cryptage ou non cryptage
	"""

	def __init__(self,a=11,b=13,c=15):
		self.LUTC = [1]*3
		self.LUTD = [1]*3
		for i in range(3):
			self.LUTC[i] = [1]*256
			self.LUTD[i] = [1]*256
		for i in range(256):
			self.LUTC[0][i] = (a*i + 7)%256
			self.LUTC[1][i] = (b*i + 1789)%256
			self.LUTC[2][i] = (c*i)%256
			self.LUTD[0][(a*i+ 7)%256] = i
			self.LUTD[1][(b*i + 1789)%256] = i
			self.LUTD[2][(c*i)%256] = i
			

	def inversionC(self,Image_open):
		t = Image_open.tabPix
		taille = (Image_open.largeur,Image_open.hauteur)
		lut = [1]*256
		for i in range(256):
			lut[i] = 255 - i
		if (Image_open.donneMode()=='NB'):
			for i in range(len(t)):
				t[i] = lut[t[i]]	#Application de la LUT
		else:
			lut = self.evolveLUT(lut)
			for i in range(len(t)):
				(R, V, B) = t[i]
				t[i] = (lut[0][R],lut[1][V],lut[2][B])	#Application de la LUT
		return t
			
	def cryptageCouleur(self,Image_open):
		return self.youhouLut(Image_open)
	
	def decryptageCouleur(self,Image_open):
		return self.youhouLut(Image_open,False)
			
	def youhouLut(self,Image_open,zup=True):
		t = Image_open.tabPix
		if Image_open.donneMode() == 'NB':
			for i in range(len(t)):
				if zup :
					t[i] = self.LUTC[0][t[i]]	#Application de la LUT de cryptage
				else:
					t[i] = self.LUTD[0][t[i]]	#Application de la LUT de décryptage
		else:
			for i in range(len(t)):
					(R, V, B) = t[i]
					if zup :
						t[i] = (self.LUTC[0][R], self.LUTC[1][V], self.LUTC[2][B])	#Application de la LUT de cryptage
					else:
						t[i] = (self.LUTD[0][R], self.LUTD[1][V], self.LUTD[2][B])	#Application de la LUT de décryptage
		return t
			

	def evolveLUT(self,LUT):		#Prend en parametre une LUT unidimensionnelle et la renvoie en 2 dimension
		LUT2D = [0] * 3
		for j in range(3):
			LUT2D[j] = [0]*256
		for i in range(256):
			LUT2D[0][i] = LUT[i]
			LUT2D[1][i] = LUT[i]
			LUT2D[2][i] = LUT[i]
		return LUT2D	
