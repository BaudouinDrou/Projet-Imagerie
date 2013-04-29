#!/usr/bin/python2
#-*- coding: UTF-8 -*-

import Tkinter
import tkMessageBox
    
def afficherAPropos():
    tkMessageBox.showinfo("A propos ...","Logiciel classique de traitement\nd'images réalisé dans le cadre de la licence MISMI de l'Université Bordeaux 1.\n\nDéveloppeurs : Pierre-André Geulin, Baudouin Duthoit")

def nonRetourArriere():
	tkMessageBox.showinfo("Erreur","Impossible de revenir en arrière\n")
	
def nonRetourAvant():
	tkMessageBox.showinfo("Erreur","Impossible d'aller à l'image suivante\n")

def erreurDecryptage():
	tkMessageBox.showinfo("Erreur","Impossible de décrypter une image non cryptée\n")

def genericTextBox():
    tkMessageBox.showinfo("Title","Text\n")
