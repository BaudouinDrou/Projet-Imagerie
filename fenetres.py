#!/usr/bin/python2
#-*- coding: UTF-8 -*-

import Tkinter
import tkMessageBox
    
def afficherAPropos():
    tkMessageBox.showinfo("A propos ...","Logiciel classique de traitement\nd'images réalisé dans le cadre de la licence MISMI de l'Université Bordeaux 1.\n\nDéveloppeurs : Pierre-André Geulin, Baudouin Duthoit")

def afficherOutils():
    tkMessageBox.showinfo("Outils","Sandwish et cornichons\n")

def genericTextBox():
    tkMessageBox.showinfo("Title","Text\n")
