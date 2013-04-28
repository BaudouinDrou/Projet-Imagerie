#!/usr/bin/python2
#-*- coding: UTF-8 -*-

from __future__ import print_function, division

import Image
import PSDraw
from random import randint
from math import *
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

def testVoisins():
	image = Image_open("images/imgUbuntu.jpg")
	t = connexN(20,20,image.tabPix,(600,600),4)	
	rep = "["
	for i in range(len(t)):
		rep += str(t[i]) + ","
	rep += "]"
	print(rep)
	print("Longueur :")
	print(len(t))

def testCalculGauss(sigma):
	print(calculGauss(0,0,sigma))
	print(1/(2*pi*sigma**2))
	print(calculGauss(1,2,sigma))
	

def testMasqueGaussien(sigma):
	t = creerMasqueGaussien(sigma)
	rep = "["
	for i in range(len(t)):
		rep += str(t[i]) + ","
	rep += "]"
	print(rep)

testVoisins()
