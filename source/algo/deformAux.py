#!/usr/bin/python
# -*-coding:Utf-8 -*

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import math

###################
# Fonctions noyau #
###################

# Noyau RBF
def radial(center, pt, coef):
    """
    :param center:
    :type center: [int,int] 
    :param pt:
    :type pt: [int,int]
    :param coef:
    :type coef: float
    :rtype: float

    """
    return 	np.exp(-(coef * np.linalg.norm(pt - center))**2)

def func_iter(pt1, pt2, pts, division_coef, coef):
    """

    :param pt1: 
    :type pt1: [int,int]
    :param pt2:
    :type pt2: [int,int]
    :param pts:
    :type pts: numpy.array
    :param division_coef:
    :type division_coef: float
    :param coef:
    :type coef: float
    :rtype: numpy.array


    """
    (l,b) = pts.shape
    result = np.zeros((l,2))
    for i in range(l):
	    result[i,:] = pts[i,:] + radial(pt1, pts[i,:], coef) * (pt2 - pt1)/division_coef
    return result

def func_result(centers, targets, coefs, division_coef, nb_iter, pt_in):
    """

    :param centers:
    :type centers: numpy.array 
    :param targets:
    :type targets: numpy.array     
    :param coefs:
    :type coefs: numpy.array 
    :param division_coef:
    :type divison_coef: float   
    :param nb_iter:
    :type nb_iter: int
    :param pt_in:
    :type pt_in: [int,int]
    :rtype: [int,int]

    """
    pt = np.copy(pt_in)
    for j in range(nb_iter):
	    pt = pt + radial(centers[j,:], pt, coefs[j]) * (targets[j,:] - centers[j,:])/division_coef		
    return pt

def func_result_reverse(centers, targets, coefs, division_coef, nb_iter, pt_in):
    """

    :param centers:
    :type centers: numpy.array 
    :param targets:
    :type targets: numpy.array     
    :param coefs:
    :type coefs: numpy.array 
    :param division_coef:
    :type divison_coef: float  
    :param nb_iter:
    :type nb_iter: int
    :param pt_in:
    :type pt_in: [int,int] 
    :rtype: [int,int]

    """
    pt = np.copy(pt_in)
    for j in reversed(range(nb_iter)):
	    V = -(targets[j,:] - centers[j,:])/division_coef
	    b = pt - centers[j,:]
	    lambd = 0.0;
	    r = radial(centers[j,:], pt + lambd * V, coefs[j]);
	    g = 2*np.dot(b+lambd * V,V);
	    deriv = -1 - coefs[j]**2 * g * r;
	    value = r - lambd;    
	    s = 0.5;
	    while (np.absolute(value) > 0.0001):
		    lambd = max(lambd - value/deriv, 0)
		    lambd = min(lambd, 1)
		    r = radial(centers[j,:], pt + lambd * V, coefs[j])
		    g = 2*np.dot(b+lambd * V,V)
		    deriv = -1 - coefs[j]**2 * g * r
		    value = r - lambd 
	    pt  = pt - lambd * (targets[j,:] - centers[j,:])/division_coef
    return pt
