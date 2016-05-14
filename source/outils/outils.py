#!/usr/bin/python
# -*-coding:Utf-8 -*

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import math
import affiche as af
from copy import deepcopy as cp

####################
# Fonctions outils #
####################

res = []
carres = []
dicoobstacles = dict()

def ameliore(l,i,nb):
    """

    Améliorer une ligne entre deux de ses points, le i et i+1ème, en ajoutant nb points entre eux.

    :param l: liste de points
    :type l: np.array
    :param i: position du premier point
    :type i: int
    :param nb: nombre de points à rajouter
    :type nb: int
    :rtype: numpy.array

    """

    l2 = []
    for cpt,val in enumerate(l):
        if cpt != i and cpt!= i+1:
            l2.append(val.tolist())
        if cpt == i:
            l3 = genLigne(val,l[cpt+1],nb).tolist()
            for val2 in l3:
                l2.append(val2)

    return np.asarray(l2)

def rotxy(point,centre,alpha):
    """
    Calcule la nouvelle position d'un point depuis une rotation alpha depuis le point centre.
    
    :param point: coordonnées d'un points
    :type point: list
    :param centre: coordonnées du centre de rotation
    :type centre: list
    :param alpha: angle pour la rotation
    :type alpha: float
    :rtype: list

    """
    dx = point[0] - centre[0]
    dy = point[1] - centre[1]
    c = math.cos(alpha)
    s = math.sin(alpha)
    return [(dx * c - dy * s) + centre[0], (dy * c + dx * s) + centre[1]]

def rotforme(forme,alpha,tabpos):
    """
    Calcule les nouvelles coordonnées d'un objet après une rotation d'angle alpha depuis tabpos.
    
    :param forme: tableau des points de la forme
    :type forme: list
    :param alpha: angle pour la rotation
    :type alpha: float
    :param tabpos: coordonnées du centre de rotation
    :type tabpos: list
    :rtype: list

    """
    alpha = math.radians(float(alpha))

    newforme = []
    
    for p in forme:
        newforme.append(rotxy(p,tabpos,alpha))

    return newforme

# Découpage obstacles
def decoupobs(x0,y0,obs,car):
    """

    Se chargerait de découper un obstacle en "zones" dans l'optique de déformer successivement des formes complexes en fonction de la position courante.

    :param x0: coordonnée  en x
    :type x0: float
    :param y0: coordonnée  en y
    :type y0: float
    :param obs: forme
    :type obs: numpy.array
    :param car: coordonnée s du carré englobant la forme
    :type car: list
    :rtype: numpy.array, list

    """
    
    global res    
    global carres
    
    if len(car) == 0:
        obs = redefineForme(obs,10)
        res.append(obs)
        car = trouverCote(obs)
        car = redefineForme(car,10)
        carres.append(np.array(car))
    #af.afficherForme([car])
    
    if estDansCarre(x0,y0,car):
        xmax = np.amax(car[:,0])
        xmin = np.amin(car[:,0])
        ymax = np.amax(car[:,1])
        ymin = np.amin(car[:,1])
        
        xmed = xmin+(abs(xmin-xmax)/2)
        ymed = ymin+(abs(ymin-ymax)/2)
        
        car1 = np.array([[xmin,ymin],[xmed,ymin],[xmed,ymed],[xmin,ymed],[xmin,ymin]])
        car2 = np.array([[xmed,ymin],[xmax,ymin],[xmax,ymed],[xmed,ymed],[xmed,ymin]])
        car3 = np.array([[xmed,ymed],[xmax,ymed],[xmax,ymax],[xmed,ymax],[xmed,ymed]])
        car4 = np.array([[xmin,ymed],[xmed,ymed],[xmed,ymax],[xmin,ymax],[xmin,ymed]])
        
        obs1 = []
        obs2 = []
        obs3 = []
        obs4 = []
        
        tmp = [car1,car2,car3,car4]
        
        tmpobs = [obs1,obs2,obs3,obs4]
        
        for cpt, val in enumerate(tmp):
            carres.append(val)
        
        #Decoupage de l'obstacle en sous obstacles
        for val in obs:
            for cpt, val2 in enumerate(tmp):
                if estDansCarre(val[0],val[1],val2):
                    tmpobs[cpt].append([val[0],val[1]])
                    break
            
        for cpt, val in enumerate(tmpobs):
            tmpobs[cpt] = np.array(val)
            if len(val) != 0:
                res.append(tmpobs[cpt])
            
        for cpt, val in enumerate(tmpobs):
            if estDansCarre(x0,y0,tmp[cpt]):
                if len(val) > 0:
                    decoupobs(x0,y0,val,tmp[cpt])
                break
             
    return res, carres

def estDansCarre(x0,y0,car):
    """
    Indique si un point de coordonnées x0, y0 se trouve dans le carré car.

    :param x0: coordonnée en x
    :type x0: float
    :param y0: coordonnée en y
    :type y0: float
    :param car: coordonnées du carré testé
    :type car: np.array
    :rtype: boolean

    """
    return x0 <= np.amax(car[:,0]) and x0 >= np.amin(car[:,0]) and y0 <= np.amax(car[:,1]) and y0 >= np.amin(car[:,1])

# Distance minimale
def distMin(ligne,obs):
    """
    Retourne la distance minimale entre les points de deux formes

    :param ligne: Première forme
    :type ligne: numpy.array
    :param obs: Deuxième forme
    :type obs: numpy.array
    :rtype: float

    """
    for i in range(len(ligne)):
        for j in range(len(obs)):
          tmp=math.sqrt(pow(obs[j,0]-ligne[i,0],2)+pow(obs[j,1]-ligne[i,1],2))
          if j == 0 and i == 0:
                min = tmp
          if tmp < min:
                min = tmp
    return min
    
def inddistMin(ligne,obs):
    """

    Retourne la distance minimale entre les points de deux formes et les deux points les plus proches

    :param ligne: Première forme
    :type ligne: numpy.array
    :param obs: Deuxième forme
    :type obs: numpy.array
    :rtype: float,int,int

    """
    indmini,indminj = 0,0
    for i in range(len(ligne)):
        for j in range(len(obs)):
          tmp=math.sqrt(pow(obs[j,0]-ligne[i,0],2)+pow(obs[j,1]-ligne[i,1],2))
          if j == 0 and i == 0:
                min = tmp
          if tmp < min:
                min = tmp
                indmini,indminj = i,j
    return min,indmini,indminj

# Distance d'un point à la ligne
def distMin_point(ligne,point):
    """

    Retourne les distance d'un point aux points d'une ligne

    :param ligne: Forme
    :type ligne: numpy.array
    :param point: Point
    :type point: [int,int]
    :rtype: float

    """
    min = np.zeros(len(ligne))
    for i in range(len(ligne)):
        min[i]=math.sqrt(pow(point[0]-ligne[i,0],2)+pow(point[1]-ligne[i,1],2))
    return min

def pointLePlusProche(forme,point):
    """

    Retourne le point d'une forme le plus proche d'un autre point

    :param forme: Forme
    :type forme: numpy.array
    :param point: Point
    :type point: [int,int]
    :rtype: [int,int]

    """
    return forme[np.argmin(distMin_point(forme,point))]

# Point du carre le plus eloigne de la ligne
def recupCote(ligne,cote):
    """

    Retourne le point du rectangle le plus eloigne de la ligne

    :param ligne: Forme
    :type ligne: numpy.array
    :param cote: Rectangle
    :type cote: numpy.array
    :rtype: [int,int]

    """
    tabMin = np.zeros(len(cote))
    for i,point in enumerate(cote):
        tabMin[i] = np.amin(distMin_point(ligne,point))
    return cote[np.argmax(tabMin)]

# Trouve le carre
def trouverCote(obs):
    """

    Retourne le rectangle entourant une forme

    :param obs: Forme
    :type obs: numpy.array
    :rtype: numpy.array

    """
    xmax = np.amax(obs[:,0])
    xmin = np.amin(obs[:,0])
    ymax = np.amax(obs[:,1])
    ymin = np.amin(obs[:,1])
    
    res = np.zeros((5,2))
    res[0][0]=xmin
    res[0][1]=ymax
    res[1][0]=xmax
    res[1][1]=ymax
    res[2][0]=xmax
    res[2][1]=ymin
    res[3][0]=xmin
    res[3][1]=ymin
    res[4][0]=xmin
    res[4][1]=ymax
    
    return res

# Rajouter des points, (facteur * points par segment)
def redefineForme(forme, facteur):
  """

  Rajoute des points à une forme
  
  Retourne la nouvelle forme obtenue

  :param forme: Forme
  :type forme: numpy.array
  :param facteur: Nombre de points à ajouter entre chaque point de la forme
  :type facteur:
  :rtype: numpy.array

  """
  res = np.zeros(((len(forme) - 1) * facteur, len(forme[0])))
  for i in range(len(forme) - 1):
    res[i * facteur:i * facteur + facteur, 0] = np.linspace(forme[i, 0], forme[i + 1, 0], facteur)
    res[i * facteur:i * facteur + facteur, 1] = np.linspace(forme[i, 1], forme[i + 1, 1], facteur)

  return res
  
# Réduire une forme avec un certain coeff autour d'un point    
def deformerPourc(forme,point,pourcentage):
    """

    Réduit une forme selon un pourcentage

    :param forme: Forme à réduire
    :type forme: numpy.array
    :param point: Centre de la forme réduite
    :type point: [int,int]
    :param pourcentage: Pourcentage de réduction
    :type pourcentage: float
    :rtype: numpy.array

    """
    formedef = np.copy(forme)
    for i in range(len(forme)):
        formedef[i,0] = point[0] + (forme[i,0] - point[0]) * (1-pourcentage)
        formedef[i,1] = point[1] + (forme[i,1] - point[1]) * (1-pourcentage)

    return formedef
    
def genCible(ligne,forme):
    """

    Génère la cible de déformation d'une forme, déterminée par rapport à la ligne, et la retourne

    :param ligne: Ligne à ne plus bloquer
    :type ligne: numpy.array
    :param forme: Obstacle à déformer
    :type forme: numpy.array
    :rtype: numpy.array

    """
    fig = trouverCote(forme)
    pointCarre = recupCote(ligne,fig)
    point = pointLePlusProche(forme,pointCarre)
    pourc = defomin(ligne,forme,point)
    return deformerPourc(forme,point,pourc), pourc

def genLigne(pt1,pt2,nbPoints):
    """

    Retourne une ligne droite formée d'autant de points que demandé
    
    :param pt1: Premier point
    :type pt1: [int,int]
    :param nbPoints: Nombre de points de la ligne
    :type nbPoints: int
    :rtype: numpy.array
    
    """
    points = np.zeros((2,2))
    points[0][0] = pt1[0]
    points[0][1] = pt1[1]
    points[1][0] = pt2[0]
    points[1][1] = pt2[1]
    return redefineForme(points,nbPoints)   

def test(listeNomPiece):

    tabVal = []
    for i in range(len(listeNomPiece)):
        tabVal.append(['0'] * len(listeNomPiece))

    return tabVal
    
def generationgraph(xdeb,ydeb,piecedeb,xfin,yfin,piecefin,resorigin,nomorigin,dico):
    """

    Permet de générer un graphe qui servira à determiner l'ordre des pièces à traverser.
    Les portes serviront de noeuds, leurs identifiants étant composés du nom des deux pièces qu'ils relient.
    
    :param xdeb: coordonnée en x dans la pièce du début
    :type xdeb: float

    :param ydeb: coordonnée en y dans la pièce du début
    :type ydeb: float

    :param piecedeb: Nom de la pièce de départ
    :type piecedeb: str

    :param xfin: coordonnée en x dans la pièce de fin
    :type xfin: float

    :param yfin: coordonnée en x dans la pièce de fin
    :type yfin: float

    :param piecefin: Nom de la pièce visée
    :type piecefin: str

    :param resorigin: Tableau contenant coordonnée d'un des points de chaque piece
    :type resorigin: list()

    :param nomorigin: Tableau contenant le nom des pièces
    :type nomorigin: list()

    :param dico: dictionnaire contenant, pour chaque piece, les coordonnées des portes menant aux pièces connexes.
    :type dico: dict()

    :rtype: dict()

    """

    tab = []
    for key in dico:
        value = resorigin[nomorigin.index(key)].split(';')
        x0 = value[0]
        y0 = value[1]
        values = dico[key].split('/')
        for cpt, val in enumerate(values):
            tmp = val.split(':')
            nompiece = tmp[0]
            coord = tmp[1].split(';')
            x = coord[0]
            y = coord[1]
            
            cptbis = cpt+1
            
            if cptbis < len(values):
                for val2 in values[cptbis:]:
                    tmp2 = val2.split(':')
                    nompiece2 = tmp2[0]
                    coord2 = tmp2[1].split(';')
                    
                    tmp3 = nompiece2.split('*')
                    
                    x2 = coord2[0]
                    y2 = coord2[1]
                    
                    valeur = math.sqrt(math.pow(float(x2)-float(x),2)+math.pow(float(y2)-float(y),2))
                    
                    tab.append(key+'-'+nompiece+'/'+key+'-'+nompiece2+':'+str(valeur))
                    tab.append(key+'-'+nompiece+'/'+nompiece2+'-'+key+':'+str(valeur))
                    tab.append(nompiece+'-'+key+'/'+key+'-'+nompiece2+':'+str(valeur))
                    tab.append(nompiece+'-'+key+'/'+nompiece2+'-'+key+':'+str(valeur))
                    
                    valeurdeb = math.sqrt(math.pow(float(xdeb)-float(x2),2)+math.pow(float(ydeb)-float(y2),2))
                    valeurfin = math.sqrt(math.pow(float(xfin)-float(x2),2)+math.pow(float(yfin)-float(y2),2))
                    
                    if nompiece2 == piecedeb:
                        tab.append('debut/'+key+'-'+nompiece2+':'+str(valeurdeb))
                        tab.append('debut/'+nompiece2+'-'+key+':'+str(valeurdeb))
                        tab.append(key+'-'+nompiece2+'/debut:'+str(valeurdeb))
                        tab.append(nompiece2+'-'+key+'/debut:'+str(valeurdeb))

                    if nompiece2 == piecefin:
                        tab.append('fin/'+key+'-'+nompiece2+':'+str(valeurfin))
                        tab.append('fin/'+nompiece2+'-'+key+':'+str(valeurfin))
                        tab.append(key+'-'+nompiece2+'/fin:'+str(valeurfin))
                        tab.append(nompiece2+'-'+key+'/fin:'+str(valeurfin))
            
            valeurdeb = math.sqrt(math.pow(float(xdeb)-float(x),2)+math.pow(float(ydeb)-float(y),2))
            valeurfin = math.sqrt(math.pow(float(xfin)-float(x),2)+math.pow(float(yfin)-float(y),2))

            if key == piecedeb:
                tab.append('debut/'+key+'-'+nompiece+':'+str(valeurdeb))
                tab.append('debut/'+nompiece+'-'+key+':'+str(valeurdeb))
                tab.append(key+'-'+nompiece+'/debut:'+str(valeurdeb))
                tab.append(nompiece+'-'+key+'/debut:'+str(valeurdeb))
            
            if key == piecefin:
                tab.append('fin/'+key+'-'+nompiece+':'+str(valeurfin))
                tab.append('fin/'+nompiece+'-'+key+':'+str(valeurfin))
                tab.append(key+'-'+nompiece+'/fin:'+str(valeurfin))
                tab.append(nompiece+'-'+key+'/fin:'+str(valeurfin))
            
    dicores = dict()
    dico2 = dict()
    
    for val in tab:
        tmp = val.split('/')
        porte1 = tmp[0]
        tmp2 = tmp[1].split(':')
        porte2 = tmp2[0]
        dist = tmp2[1]
        
        if not porte1 in dicores.keys():
            dicotmp = dict()
            dicotmp[str(porte2)]=float(dist)
            dicores[str(porte1)]=dicotmp
        else:
            dicores[str(porte1)][str(porte2)]=float(dist)
        if not porte2 in dicores.keys():
            dicotmp = dict()
            dicotmp[str(porte1)]=float(dist)
            dicores[str(porte2)]=dicotmp
        else:
            dicores[str(porte2)][str(porte1)]=float(dist)
    
    for key in dicores.keys():
        tmp = key.split('-')
        val1 = tmp[0]
        if val1 != 'debut' and val1 !='fin':
            val2 = tmp[1]
            tmp2 = val1.split('*')
            tmp3 = val2.split('*')
            val3=val2
            val4=val1
            if len(tmp2) == 2:
                val3+='*'+tmp2[1]
                val4=tmp2[0]
            if len(tmp3) == 2:
                val4+='*'+tmp3[1]
                val3 = tmp3[0]
            
            dicores[key].update(dicores[val3+'-'+val4])
            
    return dicores
    
def gentabconnexe(listeNomPiece, listeBatiments):
    """
    Permet, pour chaque piece, de récupérer l'ensemble de pièces qui lui sont connexes.

    :param listeNomPiece: Liste comprenant le nom des pièces
    :type listeNomPiece: list
    :param listeBatiments: Liste comprenant le descriptif du bâtiment
    :type listeBatiments: list
    :rtype: list

    """
    tabVal = test(listeNomPiece)
    
    for indPiece in range(len(listeNomPiece)):
        piece = listeBatiments[0][1][indPiece]
        for voisin in piece[3]:
            val = voisin.split(',')
            ind = listeNomPiece.index(val[1])
            values = val[0].split(';')
            tabVal[indPiece][ind] = values[0]+';'+values[1]

    return tabVal
    
def redefineforme(forme, nbpoints):
  """
  Rajoute des points à une forme
  
  Retourne la nouvelle forme obtenue

  :param forme: Forme
  :type forme: numpy.array
  :param nbpoints: Nombre de points à ajouter entre chaque point de la forme
  :type nbpoints: int
  :rtype: numpy.array
  """
  res = []
  for i in range(len(forme) - 1):
    res.append(forme[i])
    res.extend(genLigne(forme[i],forme[i+1],nbpoints).tolist())
    res.append(forme[i+1])
  return np.array(res)

def genpltobs(x0, y0, piece, tabConnexe, listepieces, listebatiments, tabverif, resdata, resobs, piecePrecedente,resorigin,nomorigin,dico,premieriter=0):
    """
    Fonction récursive permettant de remplir un dictionnaire comprenant les descriptifs des différentes pièces, leurs positions dans l'espace, les objets qui les composent, les pièces qui sont voisines ainsi que la position des portes les reliant. Initialement tabverif, resdata, resobs, piecePrecedente, resorigin, nomorigin et dico sont vides.

    :param x0: coordonnée en x de l'origine de la première pièce
    :type x0: float
    
    :param x0: coordonnée en y de l'origine de la première pièce
    :type x0: float
    
    :param piece: nom de la première piece
    :type piece: 
    
    :param tabConnexe: liste de connexité entre pieces 
    :type tabConnexe: list
    
    :param tabverif: liste permettant de verifier si une piece à déjà été traitée
    :type tabverif: list
    
    :param resdata: Liste comprenant le descriptif du bâtiment
    :type resdata: list
       
    :param piecePrecedente: Nom de la pièce traitée précedemment
    :type piecePrecedente: str
    
    :param resorigin: Liste contenant les origines de chaque pieces
    :type resorigin: list
    
    :param nomorigin: Liste contenant les nom de chaque pièces
    :type nomorigin: list
    
    :param dico: dictionnaire comprenant les descriptifs des différentes pièces, leurs positions dans l'espace, les objets qui les composent, les pièces qui sont voisines ainsi que la position des portes les reliant.
    :type dico: dict

    :rtype: list, list, list, list , dict, float, float, float, float, dict

    """
    global xmax, ymax, xmin, ymin, dicoobstacles

    if len(nomorigin) == 0:
        premieriter = 1
    tabverif[listepieces.index(piece[0].text)] += 1

    for pieceConnexe in piece[3]:
        liste = pieceConnexe.split(',')
        val = liste[0].split(';')

        piecesuiv = liste[1]

        if piecesuiv == piecePrecedente:
            x0 -= float(val[0])
            y0 -= float(val[1])
            break
    
    resorigin.append(str(x0)+';'+str(y0))
    nomorigin.append(piece[0].text)
    
    for murs in piece[1]:

        for mur in murs:

            coord = mur.split(',')
            val1 = coord[0].split(';')
            val2 = coord[1].split(';')
            
            xa = float(val1[0]) + x0
            ya = float(val1[1]) + y0
            xb = float(val2[0]) + x0
            yb = float(val2[1]) + y0
            
            xma = max(xa,xb)
            xmi = min(xa,xb)
            yma = max(ya,yb)
            ymi = min(ya,yb)
            
            if premieriter == 1:
                xmax = xma
                xmin = xmi
                ymax = yma
                ymin = ymi
                premieriter = 0
            else:
                if xmax < xma:
                    xmax = xma
                if ymax < yma:
                    ymax = yma
                if xmin > xmi:
                    xmin = xmi
                if ymin > ymi:
                    ymin = ymi

            a = [str(xa), str(xb)]
            b = [str(ya), str(yb)]

            data = [a, b]

            resdata.append(data)

    for obstacles in piece[2]:
      
        datax = []
        datay = []

        for obstacle in obstacles:

            coord = obstacle.split(',')

            val1 = coord[0].split(';')
            val2 = coord[1].split(';')
            xa = float(val1[0]) + x0
            ya = float(val1[1]) + y0
            xb = float(val2[0]) + x0
            yb = float(val2[1]) + y0

            a = [str(xa), str(xb)]
            b = [str(ya), str(yb)]
            
            datax.append(xa)
            datax.append(xb)
            datay.append(ya)
            datay.append(yb)

            data = [a, b]

            resobs.append(data)
        
        data2 = []
        data2.append(datax)
        data2.append(datay)
        
        if piece[0].text in dicoobstacles:
            dicoobstacles[piece[0].text].append(data2)
        else:
            dicoobstacles[piece[0].text] = []
            dicoobstacles[piece[0].text].append(data2)
        
    for pieceConnexe in piece[3]:

        liste = pieceConnexe.split(',')
        val = liste[0].split(';')

        piecesuiv = liste[1]
        
        x0bis = x0 + float(val[0])
        y0bis = y0 + float(val[1])
        
        if not(str(x0bis)+";"+str(y0bis) in dico.values()):
            
            if not piece[0].text in dico:
                dico[piece[0].text] = piecesuiv+':'+str(x0bis)+";"+str(y0bis)
            else:
                temp=''
                while piecesuiv+'*'+temp in dico[piece[0].text] or piecesuiv+temp in dico[piece[0].text]:
                    if temp=='':
                        temp='1'
                    else:
                        temp=str(int(temp)+1)
                if temp == '':
                    dico[piece[0].text] = dico[piece[0].text]+'/'+piecesuiv+':'+str(x0bis)+";"+str(y0bis)
                else :
                    dico[piece[0].text] = dico[piece[0].text]+'/'+piecesuiv+'*'+temp+':'+str(x0bis)+";"+str(y0bis)
        
        if tabverif[listepieces.index(piecesuiv)] == 0:
            genpltobs(x0bis, y0bis, listebatiments[0][1][listepieces.index(piecesuiv)], tabConnexe, listepieces,
                      listebatiments, tabverif, resdata, resobs, piece[0].text,resorigin,nomorigin,dico)
                      
    return resdata, resobs, resorigin, nomorigin, dico,xmax,xmin,ymax,ymin, dicoobstacles

def angleCommun(pt1,pt2,angles):
    """
    Détermine l'angle commun entre deux points, 0 s'il n'y en a pas

    :param pt1: Premier point
    :type pt1: [int,int]
    :param pt2: Deuxième point
    :type pt2: [int,int]
    :param angles: Liste des angles
    :type angles: list
    :rtype: [int,int] ou int
    """
    tab1 = []
    tab2 = []
    for i,a in enumerate(angles):
        if pt1[0]==a[0] or pt1[1]==a[1]:
            tab1.append(i)
        if pt2[0]==a[0] or pt2[1]==a[1]:
            tab2.append(i)

    if tab1==tab2:
        return 0
    else:
        for t1 in tab1:
            for t2 in tab2:
                if (angles[t1]==angles[t2]).all():
                    return angles[t1]

##########
# FUSION #
##########

def fusion(obstacles,seuil):
    """
    Fusionne les obstacles trop proches selon le seuil

    Retourne la nouvelle liste des obstacles

    :param obstacles: Liste des obstacles à fusionner
    :type obstacles: list
    :param seuil: Distance à respecter
    :type seuil: float

    :rtype: list
    """
    newobstacles = cp(obstacles)
    i = 0

    while i <len(newobstacles):
        obs1 = newobstacles[i] 
        for j,obs2 in enumerate(newobstacles):
            if i!=j :
                distmin,indminobs1,indminobs2 = inddistMin(obs1,obs2)
                if distmin<2*seuil:
                    newobs = obs1.tolist()
                    first = cp(newobs[:indminobs1+1])
                    last = cp(newobs[indminobs1:])
                    o = obs2.tolist()
                    line = genLigne(o[indminobs2],newobs[indminobs1],5)
                    first.extend(o)
                    first.extend(line)
                    first.extend(last)
                    newobs = np.array(cp(first))
                    newobstacles[i] = newobs
                    del newobstacles[j]
                    i = -1
                    break
        i += 1
    return newobstacles

def fusionMur(piece,obstacles,seuil):
    """
    Fusionne les obstacles trop proches des murs de la piece selon le seuil

    Retourne les nouveaux murs et les nouveaux obstacles

    :param piece: Murs de la piece
    :type piece: numpy.array
    :param obstacles: Liste des obstacles à fusionner
    :type obstacles: list
    :param seuil: Distance à respecter
    :type seuil: float
    :rtype: list,list
    """
    newobstacles = []
    cache = []
    newpiece = cp(piece)

    for obs in obstacles:
        distmin,indminobs,indminpiece = inddistMin(obs,newpiece)
        if distmin<2*seuil:
            pc = newpiece.tolist()
            first = cp(pc[:indminpiece+1])
            last = cp(pc[indminpiece:])
            o = obs.tolist()
            line = genLigne(obs[indminobs],pc[indminpiece],5)
            first.extend(o)
            first.extend(line.tolist())
            first.extend(last)
            newpiece = np.array(first)
        else:
            newobstacles.append(cp(obs))
    return newpiece,newobstacles

###############################
# DEGAGER OBSTACLES DE PIECES #
###############################

def ramenerRect(murs,ext):
    """
    Identifie les murs pouvant être des obstacles au sein de la pièce

    Retourne les coins du rectangle entourant la pièce, les obstacles en dépassant et les points de déformation pour ces obstacles

    :param murs: Murs de la pièce
    :type murs: numpy.array
    :param ext:
    :type ext: int
    :rtype: numpy.array,list,list
    """
    m = np.array(murs)
    mx = [ms[0] for ms in m]
    my = [ms[1] for ms in m]
    
    maxx = np.amax(np.array(mx))
    minx = np.amin(np.array(mx))
    maxy = np.amax(np.array(my))
    miny = np.amin(np.array(my))
    tabextx = [maxx,minx]
    tabexty = [maxy,miny]

    rect = np.array([[minx-ext,maxy+ext],[maxx+ext,maxy+ext],[maxx+ext,miny-ext],[minx-ext,miny-ext],[minx-ext,maxy+ext]])

    # Parcourir tous les points de la forme pour voir lesquels s'ecartent du carre
    # tant qu'on s'ecarte, sauver la portion de la forme et du carre
    # rabattre la portion de la forme sur le carre

    obstacles = []
    pointsdefo = []

    murs = murs.tolist()

    i = 0
    
    #for i,p in enumerate(murs):
    while i<len(murs):
        p = murs[i][:]
        if p[0] not in tabextx and p[1] not in tabexty:
            # la portion n'appartient plus au carré
            if i > 0:
                debut = i-1
            else:
                debut = 0
            obs = [murs[debut][:],p[:]]
            i += 1
            if i < len(murs):
                p = murs[i+1][:]
                while p[0] not in tabextx and p[1] not in tabexty and i+1<len(murs):
                    if not p in obs:
                        obs.append(p[:])
                    p = murs[i+1][:]
                    i += 1
            if i+1<len(murs):
                obs.append(murs[i+1][:])
            else:
                obs.append(murs[0][:])

            ptdefo=[obs[0],obs[-1]]

            a = angleCommun(obs[0],obs[-1],rect)

            if type(a)!=int and a!=None:
                l1 = genLigne(obs[-1],a,10)[1:-1]
                l2 = genLigne(a,obs[0],10)[1:-1]
                obs.extend(l1.tolist())
                obs.append(a)
                obs.extend(l2.tolist())
                ptdefo.append(a.tolist())
            else:
                l1 = genLigne(obs[-1],obs[0],20)[1:-1]
                obs.extend(l1.tolist())

            obs.append(murs[debut][:])
            obstacles.append(np.array(obs))
            pointsdefo.append(ptdefo)

        i+= 1

    rect = redefineForme(rect,len(murs)/4)
    
    return rect,obstacles,pointsdefo
    
# Retourne la liste des points non ignorés
def ignorerPoints(ligne,seuil):
    """
    Retire les points d'une ligne à une certaine distance du début ou de la fin de celle-ci
  
    Retourne le nouveau tableau des points obtenus
  
    :param ligne: Ligne à raccourcir
    :type ligne: numpy.array
    :param seuil: Distance
    :type seuil: float
    :rtype: numpy.array
    """
    depart = ligne[0]
    arrivee = ligne[-1]
    newLigne = []
    for i in range(1,len(ligne)-1):
        p = ligne[i][:]
        distDep = tmp=math.sqrt(pow(p[0]-depart[0],2)+pow(p[1]-depart[1],2))
        distArr = tmp=math.sqrt(pow(p[0]-arrivee[0],2)+pow(p[1]-arrivee[1],2))

        if distDep>seuil and distArr>seuil:
            newLigne.append(p)

    return np.array(newLigne)

def inside(point,poly):
    """
    Rend vrai si un point est inscrit dans un polygone, faux sinon

    :param point: Point à tester
    :type point: [int,int]
    :param poly: Polygone
    :type poly: list([int,int])
    :rtype: boolean
    """
    x,y = point
    # check if point is a vertex
    if (x,y) in poly: return True
    # check if point is on a boundary
    for i in range(len(poly)):
        p1 = None
        p2 = None
        if i==0:
           p1 = poly[0]
           p2 = poly[1]
        else:
           p1 = poly[i-1]
           p2 = poly[i]
        if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
           return True

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
           if y <= max(p1y,p2y):
              if x <= max(p1x,p2x):
                 if p1y != p2y:
                    xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                 if p1x == p2x or x <= xints:
                    inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def bloque(courbe,obss):
    """
    Vérifie si une ligne est bloquée par un ensemble d'obstacles
    
    :param courbe: Ligne
    :type courbe: numpy.array
    :param obss: Liste des obstacles potentiels
    :type obss: list
    :rtype: boolean
    """
    for obs in obss:
        for point in courbe:
            if inside(point,obs.tolist()):
                return True
    return False

def obsbloquants(courbe,obss):
    """
    Retourne la liste des obstacles sur le chemin

    :param courbe: Chemin
    :type courbe: numpy.array
    :param obss: Liste des obstacles
    :type obss: list
    :rtype: boolean,list
    """
    bloquants = []
    bloque = False
    for i,obs in enumerate(obss):
        for point in courbe:
            if inside(point,obs.tolist()):
                bloquants.append(i)
                bloque = True
    return bloque,bloquants

def defomin(ligne,obs,point):
    """
    Réduit la taille de l'obstacle jusqu'à ce que la ligne n'y passe plus

    Retourne le nouvel obstacle

    :param ligne: Chemin à ne plus bloquer
    :type ligne: numpy.array
    :param obs: Obstacle
    :type obs: numpy.array
    :param point: Point vers lequel les points de l'obstacle seront envoyés
    :type point: [int,int]
    :rtype: numpy.array
    """
    res = 0.0
    ligne = redefineForme(ligne,5)
    obsFin = np.copy(obs)
    while bloque(ligne,[obsFin]) and res<0.9:
        obsFin = redefineForme(obsFin,10)
        res += 0.1
        obsFin = deformerPourc(obs,point,res)
    return res

def dehors(obs,forme):
  """
  Vérifie si une première forme a au moins un point qui n'est pas inclus dans une autre

  :param obs: Première forme
  :type obs: numpy.array
  :param forme: Deuxièmre forme
  :type forme: numpy.array
  :rtype: boolean
  """
  for point in obs:
    if not inside(point,forme.tolist()):
      return True
  return False

def dehorspts(obs,forme):
  """
  Retourne la liste des points d'une première forme qui ne sont pas inclus dans une autre

  :param obs: Première forme
  :type obs: numpy.array
  :param forme: Deuxièmre forme
  :type forme: numpy.array
  :rtype: list
  """
  ptdehors = []
  for point in obs:
    if not inside(point,forme.tolist()):
      ptdehors.append(point)
  return ptdehors

# En dehors du rect
def ptsdehorsrect(obs,rect):
  """
  Retourne la liste des points d'une forme qui sont en dehors d'un rectangle

  :param obs: Première forme
  :type obs: numpy.array
  :param rect: Deuxièmre forme
  :type rect: numpy.array
  :rtype: list
  """
  ptdehors = []
  
  mx = [ms[0] for ms in rect]
  my = [ms[1] for ms in rect]
  maxx = np.amax(np.array(mx))
  minx = np.amin(np.array(mx))
  maxy = np.amax(np.array(my))
  miny = np.amin(np.array(my))
  tabextx = [maxx,minx]
  tabexty = [maxy,miny]

  for point in obs:
    if not inside(point,rect.tolist()) or point[0] in tabextx or point[1] in tabexty:
      ptdehors.append(point)
  return ptdehors

# Points de defo
def pointsdehors(obstacles,piece):
  """
  Retourne la liste des points situés en dehors de la pièce
  Utilisé pour déterminer les points autour desquels les réductions des obstacles seront faites, et pour s'assurer que le chemin ne sorte pas de la pièce

  :param obstacles: Liste des obstacles
  :type obstacles: list
  :param piece: Murs de la piece
  :type piece: numpy.array
  :rtype: list
  """
  pointsdehors = [[] for o in obstacles]
  for i,obs in enumerate(obstacles):
    pts = ptsdehorsrect(obs,piece)
    if len(pts)>0:
      pointsdehors[i]=pts
  return pointsdehors


def dedanspts(obs,forme):
  """
  Retourne la liste des points d'une première forme qui sont inclus dans une autre

  :param obs: Première forme
  :type obs: numpy.array
  :param forme: Deuxièmre forme
  :type forme: numpy.array
  :rtype: list
  """
  ptdedans = []
  for point in obs:
    if inside(point,forme.tolist()):
      ptdedans.append(point)
  return ptdedans

# Indices des carres avec le minimum de points dans une forme
def minptsdedans(carres,forme):
  """
  Retourne la liste des indices d'une liste de carres ayant le minimum de points dans une forme

  :param carres: Liste des carres
  :type carres: list
  :param forme: Forme
  :type forme: numpy.array
  """
  nbptsdedans = np.array([len(dedanspts(carre,forme)) for carre in carres])
  res = np.where(nbptsdedans == nbptsdedans.min())
  return res[0]



def agrandiradd(forme,seuil):
  """
  Agrandit l'obstacle (pour obstacles de murs)

  Retourne le nouvel obstacle

  :param forme: Forme à agrandir
  :type forme: numpy.array
  :param seuil: Distance à respecter
  :type seuil: float
  :rtype: numpy.array
  """
  formedef = []
  for i in range(len(forme)):
    x = forme[i][0]
    y = forme[i][1]
    xp = x+seuil
    xm = x-seuil
    yp = y+seuil
    ym = y-seuil
    carre1 = np.array([[xm,yp],[x,yp],[x,y],[xm,y]]) 
    carre2 = np.array([[x,yp],[xp,yp],[xp,y],[x,y]])
    carre3 = np.array([[x,y],[xp,y],[xp,ym],[x,ym]])
    carre4 = np.array([[xm,y],[x,y],[x,ym],[xm,ym]])
    carres = [carre1,carre2,carre3,carre4]

    ptscarres = [[xm,yp],[xp,yp],[xp,ym],[xm,ym]]
    carresmin = minptsdedans(carres,forme)
    for ind in carresmin:
      formedef.append(ptscarres[ind])
  return np.array(formedef)


def agrandirobs(forme,seuil):
    """
    Agrandit l'obstacle (pour obstacles hors des murs)

    Retourne le nouvel obstacle
  
    :param forme: Forme à agrandir
    :type forme: numpy.array
    :param seuil: Distance à respecter
    :type seuil: float
    :rtype: numpy.array
    """
    bary = np.mean(forme,axis=0)
    
    formedef = np.copy(forme)
    for i in range(len(forme)):
        coefx = 1
        coefy = 1
        if abs(forme[i,0] - bary[0])>0:
            coefx = (abs(forme[i,0] - bary[0])+seuil)/abs(forme[i,0] - bary[0])
        if abs(forme[i,1] - bary[1])>0:
            coefy = (abs(forme[i,1] - bary[1])+seuil)/abs(forme[i,1] - bary[1])
        formedef[i,0] = bary[0] + ((forme[i,0] - bary[0]) * (coefx))
        formedef[i,1] = bary[1] + ((forme[i,1] - bary[1]) * (coefy))
    return formedef

def fusionAgr(obstacles):
    """
    Fusionne les obstacles agrandis

    Retourne la nouvelle liste des obstacles

    :param obstacles: Liste des obstacles à fusionner
    :type obstacles: list
    :param seuil: Distance à respecter
    :type seuil: float

    :rtype: list
    """
    newobstacles = cp(obstacles)
    cache = []
  
    i = 0  

    while i <len(newobstacles):
        obs1 = cp(newobstacles[i])
        for j,obs2 in enumerate(newobstacles):
            if i!=j and (bloque(obs2,[obs1]) or bloque(obs1,[obs2])) :
                pdehors1 = np.array(dehorspts(obs1,obs2))
                pdehors2 = np.array(dehorspts(obs2,obs1))
                if len(pdehors1)>0 or len(pdehors2)>0:
                    #disp.afficher([],[],obs1,obs2)
                    #disp.afficher([],[],pdehors1,pdehors2)
                    distmin,indmin1,indmin2 = inddistMin(pdehors1,pdehors2)
                    newobs = pdehors1.tolist()
                    first = cp(newobs[:indmin1+1])
                    last = cp(newobs[indmin1:])
                    o = pdehors2.tolist()
                    line = genLigne(o[indmin2],newobs[indmin1],1)
                    first.extend(o)
                    first.extend(line)
                    first.extend(last)
                    newobs = np.array(cp(first))
                    newobstacles[i] = newobs
                    #disp.afficher([],[],newobstacles[j],newobstacles[i])

                    del newobstacles[j]
                    i = 0
                    break
        i += 1
    return newobstacles

def ramenerRectAgr(murs):
  """
  Dégage les obstacles de la pièce

  Retourne les coins du rectangle entourant la pièce, la liste des obstacles dégagés et des points de déformation pour ces obstacles

  :param murs: Murs de la pièce
  :type murs: numpy.array
  :rtype: numpy.array,list,list
  """
  m = np.array(murs)
  mx = [ms[0] for ms in m]
  my = [ms[1] for ms in m]
  
  maxx = np.amax(np.array(mx))
  minx = np.amin(np.array(mx))
  maxy = np.amax(np.array(my))
  miny = np.amin(np.array(my))
  tabextx = [maxx,minx]
  tabexty = [maxy,miny]

  rect = np.array([[minx,maxy],[maxx,maxy],[maxx,miny],[minx,miny]])#,[minx,maxy]])

  # Parcourir tous les points de la forme pour voir lesquels s'ecartent du carre
  # tant qu'on s'ecarte, sauver la portion de la forme et du carre
  # rabattre la portion de la forme sur le carre

  obstacles = []
  pointsdefo = []

  murs = murs.tolist()

  i = 0
  
  #for i,p in enumerate(murs):
  while i<len(murs):
    p = murs[i][:]
    if p[0] not in tabextx and p[1] not in tabexty:
      # la portion n'appartient plus au carré
      if i > 0:
        debut = i-1
      else:
        debut = 0
      obs = [murs[debut][:],p[:]]
      i += 1
      if i < len(murs):
        p = murs[i+1][:]
        while p[0] not in tabextx and p[1] not in tabexty and i+1<len(murs):
          if not p in obs:
            obs.append(p[:])
          p = murs[i+1][:]
          i += 1
      if i+1<len(murs):
        obs.append(murs[i+1][:])
      else:
        obs.append(murs[0][:])

      ptdefo=[obs[0],obs[-1]]

      a = angleCommun(obs[0],obs[-1],rect)

      if type(a)!=int:
        l1 = genLigne(obs[-1],a,1)
        l2 = genLigne(a,obs[0],1)
        obs.extend(l1.tolist())
        obs.append(a)
        obs.extend(l2.tolist())
        ptdefo.append(a.tolist())
      else:
        l1 = genLigne(obs[-1],obs[0],1)
        obs.extend(l1.tolist())

      obs.append(murs[debut][:])
      obstacles.append(np.array(obs))
      pointsdefo.append(ptdefo)

    i+= 1

  return rect,obstacles,pointsdefo

def redefineseuil(forme, seuil):
  """
  Rajoute des points à une forme de manière à ce qu'ils respectent une certaine distance
  
  Retourne la nouvelle forme obtenue

  :param forme: Forme
  :type forme: numpy.array
  :param seuil: Distance à respecter entre chaque point
  :type seuil:
  :rtype: numpy.array
  """
  res = []
  for i in range(len(forme) - 1):
    facteur = int(math.sqrt(pow(forme[i, 0]-forme[i + 1, 0],2)+pow(forme[i, 1]-forme[i + 1, 1],2))/seuil)+1
    res.extend([[np.linspace(forme[i, 0], forme[i + 1, 0], facteur)[j],np.linspace(forme[i, 1], forme[i + 1, 1], facteur)[j]] for j in range(facteur)])
    
  return np.array(res)


