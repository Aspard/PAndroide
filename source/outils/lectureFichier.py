#!/usr/bin/python
# -*-coding:Utf-8 -*

import numpy as np
import matplotlib.pyplot as plt

path = '../../data/tmp/'
pathforme = '../../data/formes/'

def lectureForme(nomFichier):
	f = open(pathforme+nomFichier,'r')
	lignes  = f.readlines()
	f.close()
	dim = int(lignes[0].split(" ")[0])
	nbpoints = int(lignes[0].split(" ")[1])
	tab = np.zeros((nbpoints,dim))
	
	for i in range(1,dim+1):
		ligne = lignes[i].split()
		for j in range(len(ligne)):
			tab[j][i-1] = ligne[j]

	return tab

# Ecriture d'une forme (tableau) dans un fichier
def ecrireForme(nomFichier,forme):
	fichier = open(pathforme+nomFichier,'w')
	
	fichier.write(str(len(forme[0])) + " " + str(len(forme)) + "\n")
	
	for coord in forme:
		print coord
		fichier.write(str(coord[0]))
		fichier.write(" ")
	fichier.write("\n")
	for coord in forme:
		fichier.write(str(coord[1]))
		fichier.write(" ")	
	
	fichier.close()

def lecturePiece(nomFichier):
	f = open(path+nomFichier,'r')
	lignes  = f.readlines()
	f.close()
	ligne0 = lignes[0].strip("\n").split(" ")
	entree = [float(ligne0[0].split(";")[0]),float(ligne0[0].split(";")[1])]
	sortie = [float(ligne0[1].split(";")[0]),float(ligne0[1].split(";")[1])]

	piece = []

	lignePiece = lignes[1].strip(" \n").split(" ")
	for coord in lignePiece:
		coord = coord.split(";")
		piece.append([float(coord[0]),float(coord[1])])

	return entree,sortie,np.array(piece)
	
def lecturePieceObs(nomFichier):
  """
  Lit un fichier de pièce et retourne les points de départ et d'arrivée, les murs de la pièce et la liste des obstacles

  :param nomFichier: Nom du fichier de la pièce
  :type nomFichier: string
  :rtype: [int,int],[int,int],numpy.array,list
  """
  f = open(path+nomFichier,'r')
  lignes  = f.readlines()
  f.close()
  ligne0 = lignes[0].strip("\n").split(" ")
  entree = [float(ligne0[0].split(";")[0]),float(ligne0[0].split(";")[1])]
  sortie = [float(ligne0[1].split(";")[0]),float(ligne0[1].split(";")[1])]

  piece = []

  lignePiece = lignes[1].strip("\n").split(" ")
  for coord in lignePiece:
    coord = coord.split(";")
    piece.append([float(coord[0]),float(coord[1])])

  obstacles = []

  for l in lignes[2:]:
    ligne = l.strip("\n").split(" ")
    obs = []
    for coord in ligne:
      coord = coord.split(";")
      obs.append([float(coord[0]),float(coord[1])])
    obstacles.append(np.array(obs))

  return entree,sortie,np.array(piece),obstacles
