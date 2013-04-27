#!/usr/bin/python2
#-*- coding: UTF-8 -*-

from __future__ import print_function, division

import Image
import PSDraw
from random import randint
from math import *

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

testMasqueGaussien(1)
