#!/usr/bin/python
# -*-coding:Utf-8 -*

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import math
import deformAux as aux
import outils.affiche as disp
import outils.outils as tools

"""
.. module:: deformAlgo

"""

def algo(forme,cible,line,nb_iterations,mu_coef,beta_coef):

    """
    Applique l'algorithme de déformation et retourne la ligne obtenue

    Décommenter les lignes 68 à 75 pour afficher sur l'interface les cibles des agrandissements et réductions
    
    Utiliser coef = coefmax, ligne 59, au lieu de opt.fminbound(...), ligne 58, donnera un résultat plus rapidement, la courbe sera cependant moins lisse (les déformations se font de manière plus prononcées).

    :param forme: Forme à envoyer sur la cible pour calculer la déformation   
    :type forme: numpy.array
    :param cible: Forme cible
    :type cible: numpy.array
    :param line: Ligne à déformer
    :type line: numpy.array
    :param nb_iterations: Nombre d'itérations
    :type nb_iterations: int
    :param mu_coef: mu dans l'algorithme, l'augmenter "aplatira" la gaussienne
    :type mu_coef: float
    :param beta_coef: beta dans l'algorithme
    :type beta_coef: float
    :rtype: numpy.array
    """

    frm = np.copy(forme)

    centers = np.zeros((nb_iterations,2))
    targets = np.zeros((nb_iterations,2))
    coefs = np.zeros(nb_iterations)

    for j in range(nb_iterations):
	    # calcul de m (argmax)
	    S = np.sum((forme - cible)**2, axis=1)
	    idmax = S.argmax()
	    themax = S[idmax]
	    # calcul de pj, q et vj
	    f = lambda x: np.linalg.norm(aux.func_iter(forme[idmax,:], cible[idmax,:], forme, (1.0/beta_coef), x) - cible)
	    coefmax = mu_coef * 1.0/(np.sqrt(2) * np.exp(-0.5) * np.linalg.norm(cible[idmax,:] - forme[idmax,:]))
	    # calcul de rhoj
	    coef = opt.fminbound(func = f, x1 = 0.0, x2 = min(coefmax, 50), disp = 0)
	    #coef = coefmax
	    centers[j,:] = forme[idmax,:]
	    targets[j,:] = cible[idmax,:]
	    coefs[j] = coef
	    # calcul de psi(Z)
	    forme = aux.func_iter(forme[idmax,:], cible[idmax,:], forme, 1.0/beta_coef, coef)
    fun = lambda pt: aux.func_result(centers, targets, coefs, (1.0/beta_coef), nb_iterations, pt);
    fun_reverse = lambda pt: aux.func_result_reverse(centers, targets, coefs, (1.0/beta_coef), nb_iterations, pt);
		
    
    obs = np.array([fun(pt) for pt in frm])

    newobs = np.array([fun_reverse(pt) for pt in cible])

    plt.plot(obs[:,0],obs[:,1],'brown')
    plt.plot(newobs[:,0],newobs[:,1],'orange')
    

    PT1 = fun_reverse(line[0][:])
    PT2 = fun_reverse(line[-1][:])

    trans0 = [-(PT1[0]-line[0][0]),-(PT1[1]-line[0][1])]
    transN = [-(PT2[0]-line[-1][0]),-(PT2[1]-line[-1][1])]

    N = len(line)
    n = float(N)

    Z_rev = np.zeros((N,2))
    for i in range(N):
	    Z_rev[i] = fun_reverse(line[i])

    res = np.array([[Z_rev[i][0]+(i/n)*transN[0]+((n-i)/n)*trans0[0],Z_rev[i][1]+(i/n)*transN[1]+((n-i)/n)*trans0[1]] for i in range(N)])

    return res
