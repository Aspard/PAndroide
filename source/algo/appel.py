#!/usr/bin/python
# -*-coding:Utf-8 -*
import matplotlib.pyplot as plt
import numpy as np
import deformAlgo as algo
import deformAux as aux
import outils.affiche as disp
import outils.lectureFichier as io
import outils.outils as tools
import math
import time
import matplotlib.image as mpimg
from copy import deepcopy as cp

def calculerLigneBloque(ligne,formes,pointsdefo):
    """

    Fonction utilisée pour calculer le chemin à emprunter
    Tant que la ligne passe par un obstacle, on définit une cible de déformation pour l'obstacle et on applique l'algorithme de déformation

    Si l'on effectue trop de déformations pour une forme (limite à 10 par défaut), on arrête. Pour faire varier cette limite, modifier la ligne 57
    
    Il est possible de faire varier les paramètres de l'algorithme de déformation en modifiant les lignes 77 et 84 du fichier ( par défaut: newl = algo.algo(obs,newobs,l,50,0.6,0.5) )

    Retourne le tableau des points du chemin final

    :param ligne: Tableau des points de la ligne
    :type ligne: numpy.array
    :param formes: Liste des formes, chaque forme étant un np.array() de points
    :type formes: list
    :param pointsdefo: Centres de déformation pour les obstacles faisant partie des murs de la pièce 
    :type pointsdefo: list

    :rtype: numpy.array
      
    """
    y = time.time()
    frmres = cp(formes) 
    l = cp(ligne)

    cpt = len(l)
    val = 2

    l2 = cp(l)
    test = 0
    while(val!=0):
        
        l = cp(l2)
        
        val = 0

        nbdefo = [0 for forme in frmres]
        
        if len(formes)>0:
            bloque,bloquants = tools.obsbloquants(l[1:-1],frmres)
            while bloque:  
                if not np.all(np.less(nbdefo,10)):
                    break
                for i,obs in enumerate(cp(frmres)):
                    if not bloque:
                        break
                    if i in bloquants:
                        nbdefo[i] += 1
                        frmres[i] = tools.redefineForme(frmres[i],1)
                        #formes[i] = frmres[i]
                        if i < len(pointsdefo):
                            #obstacles de murs
                            points = cp(pointsdefo[i])
                            dists = [np.amin(tools.distMin_point(l,pt)) for pt in points]
                            point = points[np.argmax(dists)]

                            newobs = np.copy(obs)
                            coef = tools.defomin(l,obs,point)

                            if coef!=0.0:
                                newobs = tools.deformerPourc(obs,point,coef)
                                newl = algo.algo(obs,newobs,l,50,0.6,0.5)

                                l = np.copy(newl)
                        else:
                            y = time.time()
                            newobs,coef = tools.genCible(l,obs)

                            newl = algo.algo(obs,newobs,l,50,0.6,0.5)

                            l = np.copy(newl)

                        bloque,bloquants = tools.obsbloquants(l[1:-1],frmres)
                        
        l2 = cp(l)
        '''
        for i in range(test,len(l)-1):
            test+=1
            l3 = tools.ameliore(l2,i,5)
            if estbloque(l3[1:-1],frmres):
                l2 = l3
                val=1
                continue
        '''
                  
    #print len(l)
    return l



def appelPieceBloque(nomfichier,seuil):
    """

    Lit un fichier de piece, fusionne les obstacles et calcule le chemin à emprunter

    Il est possible de faire varier le nombre de points:
    - De la pièce: ligne 129 du fichier( par défaut: piece = tools.redefineForme(piece,50) )
    - Des obstacles: ligne 131 du fichier( par défaut: obss = [tools.redefineForme(obs,20) for obs in obstacles] )
    - Du chemin: ligne 134 du fichier( par défaut: ligne = tools.genLigne(entree,sortie,400))

    Retourne les points du chemin calculé à partir du fichier

    :param nomfichier: Nom du fichier de pièce à lire   
    :type nomfichier: string
    :param seuil: Distance servant à fusionner les obstacles s'ils ne la respectent pas
    :type seuil: float
    :rtype: numpy.array

    """
    #T = time.time()
    #t = time.time()

    entree,sortie,piece,obstacles = io.lecturePieceObs(nomfichier)
    piece = tools.redefineForme(piece,50)

    obss = [tools.redefineForme(obs,20) for obs in obstacles]
    obstacles = cp(obss)

    ligne = tools.genLigne(entree,sortie,400)

    #t = time.time()-t
    #print "LECTURES FINIES EN ",t

    #obsfusion = [tools.redefineForme(obs,20) for obs in obstacles]

    #disp.afficher([piece],obstacles,ligne,ligne)
    #t = time.time()
    obstacles = tools.fusion(obstacles,seuil)

    piece,obstacles = tools.fusionMur(piece,obstacles,seuil)

    #t = time.time()-t
    #print "FUSIONS FINIES EN ",t
    #t = time.time()
    #disp.afficher([piece],obstacles,ligne,ligne)

    rect,formes,pointsdefo = tools.ramenerRect(piece,0)

    #disp.afficher([piece],formes,ligne,ligne)

    formes.extend(obstacles)

    #t = time.time()-t

    #print "OBSTACLES FINIS EN ",t
    #t = time.time()
    l = calculerLigneBloque(ligne,formes,pointsdefo)

    #t = time.time()-t
    #print "LIGNE CALCULEE AU TOTAL EN ",t
    #disp.afficher([piece],obstacles,ligne,l)

    #T = time.time()-T
    #print "TOUT FINI EN:",T
    return l
    

####################################################
# VERSION AVEC AGRANDISSEMENT POUR RESPECTER SEUIl #
####################################################

def calculerLigneAgr(ligne,formes,pointsdefo,seuil):
    """

    Fonction utilisée pour calculer le chemin à emprunter grâce à des obstacles agrandis
    Tant que la ligne passe par un obstacle agrandi, on définit une cible de déformation pour l'obstacle et on applique l'algoritheme de déformation

    Si l'on effectue trop de déformations pour une forme (limite à 5 par défaut), on arrête. Pour faire varier cette limite, modifier la ligne 208

    Il est possible de faire varier les paramètres de l'algorithme de déformation en modifiant les lignes 226 et 230 du fichier ( par défaut: newl = algo.algo(obs,newobs,l,50,0.6,0.5) )

    Retourne les points du chemin final

    :param ligne:   Tableau des points de la ligne
    :type ligne: numpy.array
    :param formes:   Liste des formes, chaque forme étant un np.array() de points
    :type formes: list
    :param pointsdefo:   Centres de déformation pour les obstacles faisant partie des murs de la pièce 
    :type pointsdefo: list
    :param seuil:   Distance utilisée pour ignorer certains points du début et de la fin du chemin, dans le cas où le départ ou l'arrivée sont inclus dans un obstacle   
    :type seuil: float       
    :rtype: nump.array

    """
    y = time.time()

    nbdefo = [0 for forme in formes]

    l = cp(ligne)
    if len(formes)>0:
        bloque,bloquants = tools.obsbloquants(tools.ignorerPoints(l,2*seuil),formes)
        while bloque:
            if not np.all(np.less(nbdefo,5)):
                    break
            for i,obs in enumerate(cp(formes)):
                if not bloque:
                    break
                if i in bloquants:
                    nbdefo[i] += 1
                    #obstacles de murs
                    if len(pointsdefo[i])>0:
                        points = cp(pointsdefo[i])
                        dists = [np.amin(tools.distMin_point(l,pt)) for pt in points]
                        point = points[np.argmax(dists)]

                        newobs = np.copy(obs)
                        coef = tools.defomin(l,obs,point)

                        if coef!=0.0:
                            newobs = tools.deformerPourc(obs,point,coef)
                            newl = algo.algo(obs,newobs,l,50,0.7,0.5)
                            l = np.copy(newl)
                    else:
                        newobs,coef = tools.genCible(l,obs)
                        newl = algo.algo(obs,newobs,l,50,0.7,0.5)
                        l = np.copy(newl)

                    formes[i] = cp(obs)

                    bloque,bloquants = tools.obsbloquants(tools.ignorerPoints(l,2*seuil),formes)
    return l

def appelAgr(nomfichier,seuil,mode=0):
    """

    Lit un fichier de pièce, agrandit les obstacles, fusionne les obstacles agrandis, puis détermine le chemin à emprunter

    Il est possible de faire varier le nombre de points:
    - Du chemin: ligne 257 du fichier( par défaut: ligne = tools.genLigne(entree,sortie,200))

    Retourne les points du chemin calculé à partir du fichier

    :param nomfichier: Nom du fichier de pièce à lire   
    :type nomfichier: string
    :param seuil: Distance servant à fusionner les obstacles s'ils ne la respectent pas
    :type seuil: float
    :rtype: numpy.array

    """
    entree,sortie,piece,obstacles = io.lecturePieceObs(nomfichier)

    ligne = tools.genLigne(entree,sortie,200)

    piece = tools.redefineForme(piece,2)

    rect,formes,pointsdefo = tools.ramenerRectAgr(piece)

    formes.extend(obstacles)

    formespetites = cp(formes)

    formes = [tools.agrandiradd(forme,seuil) for forme in formes]

    formes = [tools.redefineseuil(forme,seuil) for forme in formes]

    formes = tools.fusionAgr(formes)

    #formes = [tools.redefineforme(forme,1) for forme in formes]

    # Centres de réduction des obstacles dégagés des murs (pour être sûr qu'on ne sorte pas de la pièce)
    pointsdefo =  tools.pointsdehors(formes,rect)

    l = calculerLigneAgr(ligne,formes,pointsdefo,seuil)
    cpt = 1
    if mode == 1:
        for val in l:
            if cpt == 7:
                cpt = 1
			#img = mpimg.imread('../../data/img/mv/mv'+str(cpt)+'.png')
            #img = plt.imshow(img,zorder=10, extent=[val[0],val[0]+0.6,val[1], val[1]+0.6])
            cpt+=1
    return l
  

  

