#!/usr/bin/python
# -*-coding:Utf-8 -*

import matplotlib.pyplot as plt
import numpy

########################
# Fonction d'affichage #
########################

# Affichage de plusieurs formes et des lignes
def afficher(formes,formeDefs,line,lineDef):
	"""
	"""
	for forme in formes:
		plt.plot(forme[:,0],forme[:,1],'ro')

	for formeDef in formeDefs:
		plt.plot(formeDef[:,0],formeDef[:,1],'bo')
	
	plt.plot(line[:,0],line[:,1],'ko')
	plt.plot(lineDef[:,0],lineDef[:,1],'go')
	plt.axis("equal")
	plt.show()

def afficherForme(formes):
	"""
	"""
	for forme in formes:
		c=numpy.random.rand(3,1)
		plt.plot(forme[:,0],forme[:,1],c=c)
	plt.axis("equal")
	plt.show()

