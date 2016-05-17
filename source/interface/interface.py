#!/usr/bin/python
# -*-coding:Utf-8 -*

try:
    from tkinter import *
    import tkinter as Tk
except:
    from Tkinter import *
    import Tkinter as Tk
    
from PIL import Image, ImageTk
from tkMessageBox import *
from tkFileDialog import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import os
import math
import time
import matplotlib.image as mpimg
import shutil

try:
    import winsound as winsound
    from winsound import *
    winsoundval = 1
except ImportError:
    winsoundval = 0
    try:
        import pyglet
        pglet = 1
    except ImportError:
        pglet = 0
    
import outils.lectureXML as lectureXML
import outils.outils as outils
import algo.dijkstra as dij
import algo.appel as exp
import conf
import io

fenetre = Tk.Tk()
fenetre.wm_title("Interface")
fenetre.configure(bg='#d9d9d9')
fenetre.minsize(width=400,height=500)
filepath = ''
txt = []
valaff = 0
valobs = 0
menubar = None
l2 = None
l = None
piecesaparcourir = None
valclick = 1
dicobstacles = dict()
listeobjets = []
pf = 1
tabverif = []
dejaOuvert = 0
avecSeuil = 0

def genfenetre():
    """
    Permet de créer la fenêtre d'accueil.
    
    Des variables globales definissent ses caractéristiques (taille, taille minimale, couleur de fond).
    """
    global l2, l, fenetre, b0
    
    menubar = Menu(fenetre)

    ima = PhotoImage(file='../../data/img/main.ppm')
    
    cadre=Canvas(fenetre,width=400,height=225,bg='#d9d9d9')

    cadre.create_image(0,25, anchor = Tk.NW,image=ima)

    cadre.pack()

    cadre2 = Canvas(fenetre,width=400,height=100,bg='#d9d9d9')
    cadre2.create_text(150,0,text="\n\n\nCréé par Yoann Taillé et Gaspard Ducamp")
    cadre2.pack(side=BOTTOM)

    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label="Charger un fichier", command=chargement)
    menu1.add_separator()
    menu1.add_command(label="Quitter", command=fenetre.quit)
    menubar.add_cascade(label="Fichier", menu=menu1)
    
    Button(fenetre, text ='Quitter',command=fenetre.destroy).pack(side=BOTTOM, padx=5, pady=5,fill="both")

    Button(fenetre, text ='Charger un plan (.xml)',command=chargement).pack(side=BOTTOM, padx=5, pady=5,fill="both")
    
    fenetre.mainloop()
    
def chargementobjet():
    """
    Permet de charger un objet depuis le répertoire "data/objets".
    
    """

    global dicoobjets, valclick, top, nom, seg, listboxobj, rot
    
    filepath2 = askopenfilename(initialdir="../../data/objets/",title="Ouvrir un objet", filetypes=[('xml files','.xml'),('all files','.*')])
    
    if filepath2 != ():
        
        nom, seg = lectureXML.lectureFichierXMLobjet(filepath2)
    
        top = Toplevel()
        top.title(nom.split(' ')[0])
        
        l3 = LabelFrame(top, text="Pieces",pady=0,bg='#d9d9d9')
        l3.pack(side=LEFT, fill="both", expand="yes")

        listboxobj = Listbox(l3)
        listboxobj.pack()

        for val in nomorigin:
            listboxobj.insert(END, val)
            
        rot = StringVar()
        rot.set("Rotation")
        Entry(top, textvariable=rot, width=20).pack(side=TOP,pady=10)

        Button(top, text="Quitter", command=top.destroy).pack(side=BOTTOM,padx=10)
        Button(top, text="Positionner l'objet", command=placementobjet).pack(side=BOTTOM,padx=10)
        
def placementobjet():
    """
    Permet de placer un objet sur la carte, bloque les boutons "Charger un objet".

    Desactive les boutons de chargement et de suppression d'objet.
    """
    global top, b3, b5, valclick, pieceobjtmp, listboxobj
    valclick = 2
    pieceobjtmp = nomorigin[listboxobj.curselection()[0]]
    b5.configure(state=DISABLED)
    b3.configure(state=DISABLED)
    top.destroy()
    return

def chargement():
    """
    Permet de charger un plan, de créer une nouvelle fenêtre ainsi qu'un certain nombre de variable globale servant à la récupération de valeurs.

    Des variables definissent ses caractéristiques (taille, taille minimale, couleur de fond).
    """

    global filepath, listeNomBat, listebatiments, b1, b2, b3, b4, b5, b6, fenetre, menubar, l, l2, b0, entreex, entreey, entreepiece, entreexdest, entreeydest, entreepiecedest, valuex, valuey, valuexdest, valueydest, valuepiece, valuepiecedest, dejaOuvert, valaff, valobs,pieceaparcourir,dicobstacles,listobjets,pf,tabverif, valueseuil, entreeseuil
    
    filepath2 = askopenfilename(initialdir="../../data/plans/",title="Ouvrir un fichier", filetypes=[('xml files', '.xml'), ('all files', '.*')])
    
    if filepath2 != () and filepath2 != '':
    
        if dejaOuvert == 0:
        
            filepath = filepath2
        
            fenetre.destroy()
            
            fenetre = Tk.Tk()
            fenetre.wm_title("Interface")
            fenetre.config(bg='#d9d9d9')
            fenetre.minsize(width=1300,height=800)
            l = LabelFrame(fenetre, text="Plan",pady=0,bg='#d9d9d9')
            l.pack(side=RIGHT, fill="both", expand="yes")
            
            l2 = Frame(l,bg="white")
            l2.pack(side=RIGHT, fill="both", expand="yes")
            
            listeNomBat, listebatiments = lectureXML.lectureFichierXML(filepath)
            
            ima = PhotoImage(file='../../data/img/mainpetit.ppm')

            cadre=Canvas(fenetre,width=200,height=80)

            cadre.create_image(10,0, anchor = Tk.NW,image=ima)
            
            cadre.pack()

            b0 = Button(fenetre, text ='Charger un plan (.xml)',command=chargement).pack(side=TOP, padx=5, pady=5,fill="both")
            b7 = Button(fenetre, text ='Sauvegarder le plan (.xml)',command=sauvegarde).pack(side=TOP,padx=5, pady = 5, fill="both")
            b5 = Button(fenetre,state=DISABLED, text ='Charger un objet (.xml)',command=chargementobjet)
            
            b6 = Button(fenetre,state=DISABLED, text ='Supprimer un objet',command=suppression)
            
            b5.pack(side=TOP,padx=5,pady=5,fill="both")
            
            b6.pack(side=TOP,padx=5,pady=5,fill="both")
            
            b1 = Button(fenetre, text ='Afficher le plan', command=affichageavecobstacles).pack(side=TOP, padx=5, pady=5,fill="both")
            
            b2 = Checkbutton(fenetre, text ='Afficher/Masquer les obstacles',bg='#d9d9d9', command=affichageobstacles).pack(side=TOP, padx=5, pady=5,fill="both")
            
            b4 = Checkbutton(fenetre, text = 'Afficher/Masquer noms pièces',bg='#d9d9d9', command=affichernompieces).pack(side=TOP, padx=5, pady=5,fill="both")
            
            valueseuil = StringVar()
            valueseuil.set("seuil")
            entreeseuil = Entry(fenetre, textvariable=valueseuil, width=30)
            valuex = StringVar() 
            valuex.set("x")
            entreex = Entry(fenetre, textvariable=valuex, width=30)
            valuexdest = StringVar()
            valuexdest.set("x dest")
            entreexdest = Entry(fenetre, textvariable=valuexdest, width=30)
            
            valuey = StringVar() 
            valuey.set("y")
            entreey = Entry(fenetre, textvariable=valuey, width=30)
            valueydest = StringVar()
            valueydest.set("y destination")
            entreeydest = Entry(fenetre, textvariable=valueydest, width=30)
            
            Button(fenetre, text="Quitter", command=fenetre.destroy).pack(side=BOTTOM, padx=10)
            
            b3 = Button(fenetre,state = DISABLED, text ='Calculer chemin',command=compute)
            b3.pack(side=BOTTOM, padx=5, pady=5)
            
            valuepiece = StringVar()
            valuepiece.set("nom de la pièce de départ")
            entreepiece = Entry(fenetre, textvariable=valuepiece, width=30)
            valuepiecedest = StringVar()
            valuepiecedest.set("nom de la pièce d'arrivée")
            entreepiecedest = Entry(fenetre, textvariable=valuepiecedest, width=30)
            
            entreepiecedest.pack(side=BOTTOM)
            entreeydest.pack(side=BOTTOM)
            entreexdest.pack(side=BOTTOM)
            
            entreepiece.pack(side=BOTTOM)
            entreey.pack(side=BOTTOM)
            entreex.pack(side=BOTTOM)
            
            entreeseuil.pack(side=BOTTOM)
            
            fenetre.config(menu=menubar)
            valobs = 0
            valaff = 0
            dejaOuvert = 1
            
            fenetre.mainloop()
            
        else:
                
            filepath = filepath2
            
            for child in fenetre.winfo_children():
                child.destroy()
            l = LabelFrame(fenetre, text="Plan",pady=0)
            l.pack(side=RIGHT, fill="both", expand="yes")
            
            l2 = Frame(l,bg="white")
            l2.pack(side=RIGHT, fill="both", expand="yes")
            
            listeNomBat, listebatiments = lectureXML.lectureFichierXML(filepath)
            
            ima = PhotoImage(file='../../data/img/mainpetit.ppm')

            cadre=Canvas(fenetre,width=200,height=80)

            cadre.create_image(10,0, anchor = Tk.NW,image=ima)
            
            cadre.pack()

            b0 = Button(fenetre, text ='Charger un plan (.xml)',command=chargement).pack(side=TOP, padx=5, pady=5,fill="both")
            b8 = Button(fenetre, text ='Sauvegarder le plan (.xml)',command=sauvegarde).pack(side=TOP,padx=5, pady = 5, fill="both")
                    
            b5 = Button(fenetre,state=DISABLED, text ='Charger un objet (.xml)',command=chargementobjet)
            
            b6 = Button(fenetre,state=DISABLED, text ='Supprimer un objet',command=suppression)
            
            b5.pack(side=TOP,padx=5,pady=5,fill="both")
            
            b6.pack(side=TOP,padx=5,pady=5,fill="both")
            
            b1 = Button(fenetre, text ='Afficher le plan', command=affichageavecobstacles).pack(side=TOP, padx=5, pady=5,fill="both")
            
            b2 = Checkbutton(fenetre, text ='Afficher/Masquer les obstacles', command=affichageobstacles).pack(side=TOP, padx=5, pady=5,fill="both")
            
            b4 = Checkbutton(fenetre, text = 'Afficher/Masquer noms pièces', command=affichernompieces).pack(side=TOP, padx=5, pady=5,fill="both")
            
            valueseuil = StringVar()
            valueseuil.set("seuil")
            entreeseuil = Entry(fenetre, textvariable=valueseuil, width=30)
            valuex = StringVar() 
            valuex.set("x")
            entreex = Entry(fenetre, textvariable=valuex, width=30)
            valuexdest = StringVar()
            valuexdest.set("x dest")
            entreexdest = Entry(fenetre, textvariable=valuexdest, width=30)
            valuey = StringVar() 
            valuey.set("y")
            entreey = Entry(fenetre, textvariable=valuey, width=30)
            valueydest = StringVar()
            valueydest.set("y destination")
            entreeydest = Entry(fenetre, textvariable=valueydest, width=30)
            
            Button(fenetre, text="Quitter", command=fenetre.destroy).pack(side=BOTTOM, padx=10)
            
            b3 = Button(fenetre,state = DISABLED, text ='Calculer chemin',command=compute)
            b3.pack(side=BOTTOM, padx=5, pady=5)
            
            valuepiece = StringVar()
            valuepiece.set("nom de la pièce de départ")
            entreepiece = Entry(fenetre, textvariable=valuepiece, width=30)
            valuepiecedest = StringVar()
            valuepiecedest.set("nom de la pièce d'arrivée")
            entreepiecedest = Entry(fenetre, textvariable=valuepiecedest, width=30)
            
            entreepiecedest.pack(side=BOTTOM)
            entreeydest.pack(side=BOTTOM)
            entreexdest.pack(side=BOTTOM)
            
            entreepiece.pack(side=BOTTOM)
            entreey.pack(side=BOTTOM)
            entreex.pack(side=BOTTOM)
            
            entreeseuil.pack(side=BOTTOM)
            
            fenetre.config(menu=menubar)
            
            valobs = 0
            valaff = 0
            dejaOuvert = 1
            
            piecesaparcourir = None
            valclick = 1
            dicobstacles.clear()
            listeobjets = []
            pf = 1
            tabverif = []
            
            fenetre.mainloop()

def affichernompieces():
    """
    Gère l'affichage des noms des pièces.
    """
    global valaff
    
    if valaff == 0:
        valaff=1
    else:
       valaff=0
       
def affichageobstacles():
    """
    Gère l'affichage des obstacles des pièces.
    """
    global valobs
        
    if valobs == 0:
        valobs=1
    else:
       valobs=0
       
def compute():
    """
    Permet de calculer, depuis les valeurs présentes dans les champs, le plus court chemin entre le départ et l'arrivée.

    Fait appel à outils.generationgraph() pour générer un graphe puis à dij.shortestPath() pour calculer par où nous devrons passer pour atteindre l'objectif.

    Se termine par un appel à affichageavecpcc()
    """

    global piecesaparcourir, x0,y0,xdest,ydest,res, piecedeb, piecefin
    
    for cpt, val in enumerate(nomorigin):
        if val == entreepiece.get():
            tmp = datorigin[cpt].split(';')
            x0 = float(entreex.get()) - float(tmp[0])
            y0 = float(entreey.get()) - float(tmp[1])
        if val == entreepiecedest.get():
            tmp = datorigin[cpt].split(';')
            xdest = float(entreexdest.get()) - float(tmp[0])
            ydest = float(entreeydest.get()) - float(tmp[1])
    
    piecedeb = entreepiece.get()
    piecefin = entreepiecedest.get()
    
    x0 = entreex.get()
    y0 = entreey.get()
    piecedeb = valuepiece.get()
    xdest = float(entreexdest.get())
    ydest = float(entreeydest.get())
    piecefin = valuepiecedest.get()
    
    if piecefin == piecedeb :
        G = outils.generationgraph(x0,y0,piecedeb,xdest,ydest,piecefin,datorigin,nomorigin,dico)
        piecesaparcourir = [piecefin]
        res = [[piecefin,piecefin]]
    else:    
        G = outils.generationgraph(x0,y0,piecedeb,xdest,ydest,piecefin,datorigin,nomorigin,dico)
        
        piecesaparcourir = dij.shortestPath(G,'debut','fin')

        res = []

        for val in piecesaparcourir[1:len(piecesaparcourir)-1]:
            tmp = val.split('-')
            res.append(tmp)

    affichageavecpcc()

def affichageavecobstacles():
    """
    Permet d'afficher, notamment à l'aide de mathplotlib et de la fonction outils.genpltobs, notre plan.

    L'affichage des obstacles et des noms des pièces dépendra des variables valoff et valabs.

    Débloque les boutons d'ajout d'objets, de suppression d'objets et de calcul de chemin.
    """

    global tabverif, l2, l, valaff,valobs, datorigin, nomorigin,dico, b5, b3, b6, canvas, f, ax, dicobstacles, pf, dat,xmin,xmax,ymin,ymax
    
    b5.configure(state=NORMAL)
    b3.configure(state=NORMAL)
    b6.configure(state=NORMAL)

    listepieces = listebatiments[0][0]

    tabverif = np.zeros(len(listepieces))
    
    dat, datobs, datorigin, nomorigin, dico,xmax,xmin,ymax,ymin, dicobstacles2 = outils.genpltobs(0, 0, listebatiments[0][1][0], outils.gentabconnexe(listepieces, listebatiments),listepieces, listebatiments, tabverif, [], [], 'null',[],[],dict())
       
    if pf == 1:
        for key in dicobstacles2.keys():
            dicobstacles[key] = []
            for val in dicobstacles2[key]:
                dicobstacles[key].append(val)
        pf = 0
        
    outils.dicoobstacles.clear()
    
    f = plt.figure()
    ax = f.add_subplot(111, axisbg='#0275ea')
    
    if conf.affichageplus == 1:
        img = mpimg.imread('../../data/img/cafe.png')
        img2 = mpimg.imread('../../data/img/criterium.png')
        ax.imshow(img2,zorder=10, extent=[xmax-15, xmax+5, ymax-11, ymax+9])
        plt.imshow(img, zorder=0, extent=[xmin-1, xmin+6, ymin-2, ymin+5])
    else:
        img = mpimg.imread('../../data/img/brain.png')
        plt.imshow(img, zorder=0, extent=[xmin, xmin+1, ymin, ymin+1])

    plt.subplots_adjust(left = 0.03, right = 0.97, bottom = 0.05, top= 0.96)
    
    ax.set_xlim((xmin-1), (xmax+1))
    ax.set_ylim(ymin-1, ymax+1)
    
    tx = int(xmin)-1
    ty = int(ymin)-1
    
    while tx<=(xmax+1):
        while ty<=(ymax+1):
            datax = [(xmin-1),(xmax+1)]
            datay = [ty,ty]
            data = [datax,datay]
            line = plt.plot(*data)
            if ty%5 == 0:
                plt.setp(line,color='white',linewidth=0.4)
            else :
                plt.setp(line,color='white',linewidth=0.2)
            ty+=1
        tx+=1
        
    tx = int(xmin)-1
    ty = int(ymin)-1
    
    while ty<=(ymax+1):
        while tx<=(xmax+1):
            datax = [tx,tx]
            datay = [(ymin-1),(ymax+1)]
            data = [datax,datay]
            line = plt.plot(*data)
            if tx%5 == 0:
                plt.setp(line,color='white',linewidth=0.4)
            else :
                plt.setp(line,color='white',linewidth=0.2)
            tx+=1
        ty+=1
    
    if valobs == 1:
        for key in dicobstacles.keys():
            for val in dicobstacles[key]:
                line = plt.plot(*val)
                plt.setp(line,color='white', linewidth=1.5, linestyle='-.')
                    
    for data in dat:
        line = plt.plot(*data)
        plt.setp(line, color='white', linewidth=1.5)
        
    if valaff == 1:
        for ind, val in enumerate(datorigin):
            value = val.split(';')
            x = float(value[0])+0.25
            y = float(value[1])+0.5
            txt.append(plt.text(x, y, nomorigin[ind], fontsize=10, color = 'white', bbox={'facecolor':'grey', 'alpha':0.25, 'pad':10}))
    
    l2.pack_forget()
    l2 = LabelFrame(l, bg="white")
    l2.pack(side=RIGHT, fill="both", expand="yes")

    root = l2

    canvas = FigureCanvasTkAgg(f, master=root)
    
    cid = canvas.mpl_connect('button_press_event', onclick)
    
    canvas.show()

    canvas.get_tk_widget().pack(side=Tk.TOP, fill='both',expand="yes")

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    
def modifaff():
    """
    Permet de réafficher le plan sans devoir regénerer la fenêtre. 
    """

    global tabverif, l2, l, valaff,valobs, datorigin, nomorigin,dico, b5, b3, b6, ax, dicobstacles, dat
    
    b5.configure(state=NORMAL)
    b3.configure(state=NORMAL)
    b6.configure(state=NORMAL)

    listepieces = listebatiments[0][0]

    tabverif = np.zeros(len(listepieces))
    
    ax.cla()

    if conf.affichageplus == 1:
        img = mpimg.imread('../../data/img/cafe.png')
        img2 = mpimg.imread('../../data/img/criterium.png')
        ax.imshow(img2,zorder=10, extent=[xmax-15, xmax+5, ymax-11, ymax+9])
        plt.imshow(img, zorder=0, extent=[xmin-1, xmin+6, ymin-2, ymin+5])
    else:
        img = mpimg.imread('../../data/img/brain.png')
        plt.imshow(img, zorder=0, extent=[xmin, xmin+1, ymin, ymin+1])

    plt.subplots_adjust(left = 0.03, right = 0.97, bottom = 0.05, top= 0.96)

    ax.set_xlim((xmin-1), (xmax+1))
    ax.set_ylim(ymin-1, ymax+1)
    
    tx = int(xmin)-1
    ty = int(ymin)-1
    
    while tx<=(xmax+1):
        while ty<=(ymax+1):
            datax = [(xmin-1),(xmax+1)]
            datay = [ty,ty]
            data = [datax,datay]
            line = plt.plot(*data)
            if ty%5 == 0:
                plt.setp(line,color='white',linewidth=0.4)
            else :
                plt.setp(line,color='white',linewidth=0.2)
            ty+=1
        tx+=1
        
    tx = int(xmin)-1
    ty = int(ymin)-1
    
    while ty<=(ymax+1):
        while tx<=(xmax+1):
            datax = [tx,tx]
            datay = [(ymin-1),(ymax+1)]
            data = [datax,datay]
            line = plt.plot(*data)
            if tx%5 == 0:
                plt.setp(line,color='white',linewidth=0.4)
            else :
                plt.setp(line,color='white',linewidth=0.2)
            tx+=1
        ty+=1

    if valobs == 1:
        for key in dicobstacles.keys():
            for val in dicobstacles[key]:
                line = plt.plot(*val)
                plt.setp(line,color='white', linewidth=1.5, linestyle='-.')
                    
    for data in dat:
        line = plt.plot(*data)
        plt.setp(line, color='white', linewidth=1.5)
        
    if valaff == 1:
        for ind, val in enumerate(datorigin):
            value = val.split(';')
            x = float(value[0])+0.25
            y = float(value[1])+0.5
            txt.append(plt.text(x, y, nomorigin[ind], fontsize=10, color = 'white', bbox={'facecolor':'grey', 'alpha':0.25, 'pad':10}))

    canvas.show()
    
def selectionpiecedep():
    """
    Permet d'attribuer à valuepiece, nom de la pièce de départ, la valeur choisie.
    """
    global valuepiece, valuepiecedest, top
    valuepiece.set(nomorigin[listbox.curselection()[0]])
    top.destroy()
    
def selectionpiecearr():
    """
    Permet d'attribuer à valuepiecedest, nom de la pièce d'arrivée, la valeur choisie.
    """
    global valuepiece, valuepiecedest, top
    valuepiecedest.set(nomorigin[listbox2.curselection()[0]])
    top.destroy()
    
def validationposition():
    """
    Réactive les boutons de chargement et de suppresion d'objets, rajoute l'objet dans le dictionnaire des obstacles.
    """
    global valclick, b3, b5, top, listeobjets, pieceobjtmp, dicobstacles
    valclick = 1
    b3.configure(state='normal')
    b5.configure(state='normal')
    if pieceobjtmp in dicobstacles:
        dicobstacles[pieceobjtmp].append(datatmp)
    else:
        dicobstacles[pieceobjtmp] = [] 
        dicobstacles[pieceobjtmp].append(datatmp)
    top.destroy()
    
def annulation():
    """
    Réactive les boutons de chargement et de suppresion d'objets, annule l'ajout d'un objet. 

    Appel à modifaff afin de nettoyer le plan.
    """
    global valclick, b3, b5
    b3.configure(state='normal')
    b5.configure(state='normal')
    modifaff()
    valclick = 1
    top.destroy()
    
def reposition():
    """
    Permet de replacer un objet sur le plan.
    """
    global top, canvas, f, f2, ax
    top.destroy()
    modifaff()
    
def suppression():
    """
    Permet la suppression d'un objet via un clic gauche.
    """
    global b6, valclick
    b6.configure(state='normal')
    valclick = 3
    
def cccv():
    """
    Permet de positionner à nouveau un objet.
    """
    global valclick, b3, b5, top, listeobjets, pieceobjtmp, dicobstacles
    valclick = 2
    if pieceobjtmp in dicobstacles:
        dicobstacles[pieceobjtmp].append(datatmp)
    else:
        dicobstacles[pieceobjtmp] = [] 
        dicobstacles[pieceobjtmp].append(datatmp)
    top.destroy()
    
def onclick(event):
    """
    Gère les clics sur le plan de l'utilisateur en fonction des différents modes (suppression d'objets, chargement d'objets, remplissage des champs).
    """
    global valclick, x0,y0,xdest,ydest, entreey, entreex, entreeydest, entreexdest, valuex, valuey, valuexdest, valueydest, top, listbox, listbox2, b3, b5, canvas, datatmp, linetmp,dicobstacles, rot
    
    ## Si on est en mode suppression ##
    if event.button == 3:
        valclick = 1
        
    elif valclick == 3:
    
        x = event.xdata
        y = event.ydata
        
        ## On trouve l'obstacle le plus proche du point choisi ##
        cpt2 = 0
        cpt3min = 0
        min = -1  
        for cpt, key in enumerate(dicobstacles.keys()):
            for cpt3, obs in enumerate(dicobstacles[key]):
                for j in range(len(obs[0])-1):
                    if len(obs[0]) == 0:
                        break
                    tmp=math.sqrt(pow(obs[0][j]-x,2)+pow(obs[1][j]-y,2))
                    if cpt2 == 0:
                        min = tmp
                        cpt2 = 1
                        keymin = key
                        cpt3min = cpt3
                    if tmp < min:
                        min = tmp
                        keymin = key
                        cpt3min = cpt3
                        
        if min == -1:
            return 
            
        ## On regarde si il est a une distance seuil ##
        
        if min < 1.0:
            listobs = dicobstacles[keymin]
            del listobs[cpt3min]
        
        modifaff()
        
    elif valclick == 2:
        x = event.xdata
        y = event.ydata
        
        #Chargement de l'objet
        
        datax = []
        datay = []
        
        tabpos = [x,y]
        
        for val in seg:
            tmp = val.split(',')
            tmp1 = tmp[0].split(';')
            tmp2 = tmp[1].split(';')
            datax.append(float(tmp1[0])+float(x))
            datax.append(float(tmp2[0])+float(x))
            datay.append(float(tmp1[1])+float(y))
            datay.append(float(tmp2[1])+float(y))
        
        data = []
        data.append(datax)
        data.append(datay)
        
        forme = []
        datax = []
        datay = []
        
        for cpt, val in enumerate(data[0]):
            tab2 = []
            tab2.append(val)
            tab2.append(data[1][cpt])
            forme.append(tab2)    
        
        try:
            forme = outils.rotforme(forme,rot.get(),tabpos)
        except ValueError:
            forme = outils.rotforme(forme,0.0,tabpos)
            
        for val in forme:
            datax.append(val[0])
            datay.append(val[1])
            
        data = [datax,datay]
        
        linetmp = plt.plot(*data)
        plt.setp(linetmp, color='white', linewidth=1.5, linestyle='-.')
        
        datatmp = data
        
        canvas.show()
        
        top = Toplevel()
        top.protocol('WM_DELETE_WINDOW', annulation)
        top.minsize(width=280, height=130)
        top.title('Confirmation de la position')
        
        Button(top, text="Valider", command=validationposition).pack(padx=10, fill="both", expand="yes")
        Button(top, text="Repositionner", command=reposition).pack(padx=10, fill="both", expand="yes")
        Button(top, text="Placer à nouveau", command=cccv).pack(padx=10, fill="both", expand="yes")
        Button(top, text="Annuler", command=annulation).pack(padx=10, fill="both", expand="yes")
    
    elif valclick == 1:
        valclick = 0
        x0 = event.xdata
        y0 = event.ydata

        valuex.set(str(x0))
        valuey.set(str(y0))

        top = Toplevel()
        top.title("Selectionnez la piece de départ")

        l3 = LabelFrame(top, text="Pieces",pady=0)
        l3.pack(side=LEFT, fill="both", expand="yes")

        listbox = Listbox(l3)
        listbox.pack()

        for val in nomorigin:
            listbox.insert(END, val)
            
        Button(top, text="Valider", command=selectionpiecedep).pack(pady=10,padx=10)
        Button(top, text="Quitter", command=top.destroy).pack(padx=10)
        
    elif valclick == 0:
        valclick = 1

        xdest = event.xdata
        ydest = event.ydata

        valuexdest.set(str(xdest))
        valueydest.set(str(ydest))

        top = Toplevel()
        top.title("Selectionnez la piece d'arrivée")

        l3 = LabelFrame(top, text="Pieces",pady=0)
        l3.pack(side=LEFT, fill="both", expand="yes")

        listbox2 = Listbox(l3)
        listbox2.pack()

        for val in nomorigin:
            listbox2.insert(END, val)

        Button(top, text="Valider", command=selectionpiecearr).pack(pady=10,padx=10)
        Button(top, text="Quitter", command=top.destroy).pack(padx=10)

def affichageavecpcc():
    """

    Est utilisée après un appel à compute(). Lance l'algorithme via algo.appelAgr() ou algo.appelPieceBloque() en fonction de la valeur du seuil.

    Gère l'affichage des différentes courbes de résultat. Celle du résultat de l'appel à dij.shortestPath() est paramétrable depuis le fichier conf.py situé dans le répertoire 'source/interface'.

    Sauvegarde les points de la courbe de résultat dans un fichier situé dans "data/res" (son nom sera composé de la date d'éxecution, du plan choisi ansi que du seuil).
    """

    global tabverif, l2, l, valaff,valobs, datorigin, nomorigin,dico,piecesaparcourir,x0,y0,xdest,ydest,res, canvas, f, f2,listpieces,avecSeuil, ax
    
    #listepieces = listebatiments[0][0]

    #tabverif = np.zeros(len(listepieces))

    #dat, datobs, datorigin, nomorigin, dico,xmax,xmin,ymax,ymin, nul = outils.genpltobs(0, 0, listebatiments[0][1][0], outils.gentabconnexe(listepieces, listebatiments),listepieces, listebatiments, tabverif, [], [], 'null',[],[],dict())
    
    outils.dicoobstacles.clear()
                                   
    ax.cla()

    if conf.affichageplus == 1:
        img = mpimg.imread('../../data/img/cafe.png')
        img2 = mpimg.imread('../../data/img/criterium.png')
        ax.imshow(img2,zorder=10, extent=[xmax-15, xmax+5, ymax-11, ymax+9])
        plt.imshow(img, zorder=0, extent=[xmin-1, xmin+6, ymin-2, ymin+5])
    else:
        img = mpimg.imread('../../data/img/brain.png')
        plt.imshow(img, zorder=0, extent=[xmin, xmin+1, ymin, ymin+1])

    plt.subplots_adjust(left = 0.03, right = 0.97, bottom = 0.05, top= 0.96)
    
    ax.set_xlim((xmin-1), (xmax+1))
    ax.set_ylim(ymin-1, ymax+1)
    
    tx = int(xmin)-1
    ty = int(ymin)-1
    
    while tx<=(xmax+1):
        while ty<=(ymax+1):
            datax = [(xmin-1),(xmax+1)]
            datay = [ty,ty]
            data = [datax,datay]
            line = plt.plot(*data)
            if ty%5 == 0:
                plt.setp(line,color='white',linewidth=0.4)
            else :
                plt.setp(line,color='white',linewidth=0.2)
            ty+=1
        tx+=1
        
    tx = int(xmin)-1
    ty = int(ymin)-1
    
    while ty<=(ymax+1):
        while tx<=(xmax+1):
            datax = [tx,tx]
            datay = [(ymin-1),(ymax+1)]
            data = [datax,datay]
            line = plt.plot(*data)
            if tx%5 == 0:
                plt.setp(line,color='white',linewidth=0.4)
            else :
                plt.setp(line,color='white',linewidth=0.2)
            tx+=1
        ty+=1

    if valobs == 1:
        for key in dicobstacles.keys():
            for val in dicobstacles[key]:
                line = plt.plot(*val)
                plt.setp(line,color='white', linewidth=1.5, linestyle='-.')
            
    for val in listeobjets:
        line = plt.plot(*val)
        plt.setp(line,color='white', linewidth=1.5, linestyle='-.')
                
    for data in dat:
        line = plt.plot(*data)
        plt.setp(line, color='white', linewidth=1.5)
        
    if valaff == 1:
        for ind, val in enumerate(datorigin):
            value = val.split(';')
            x = float(value[0])+0.25
            y = float(value[1])+0.5
            txt.append(plt.text(x, y, nomorigin[ind], fontsize=10, color = 'white', bbox={'facecolor':'grey', 'alpha':0.25, 'pad':10}))
    
    datax = [x0]
    datay = [y0]
    data = []
    
    listpieces = [piecedeb]
    listorigin = [datorigin[nomorigin.index(piecedeb)]]
    
    for val in piecesaparcourir[1:-2]:
        tmp = val.split('-')
        tmp2 = tmp[0].split('*')
        tmp3 = tmp[1].split('*')
        if not tmp2[0] in listpieces:
            listpieces.append(tmp2[0])
            listorigin.append(datorigin[nomorigin.index(tmp2[0])])
        if not tmp3[0] in listpieces:
            listpieces.append(tmp3[0])
            listorigin.append(datorigin[nomorigin.index(tmp3[0])])
    
    if not piecefin in listpieces:
        listpieces.append(piecefin)
        listorigin.append(datorigin[nomorigin.index(piecefin)])

    pieces = listebatiments[0][1]

    for cpt, val in enumerate(res):
        tmp = val[0]
        try:
            tmp2 = dico[tmp]
            tmp3 = tmp2.split('/')
            for val2 in tmp3:
                tmp4 = val2.split(':')
                if tmp4[0] == val[1]:
                    tmp5 = tmp4[1].split(';')
                    datax.append(float(tmp5[0]))
                    datay.append(float(tmp5[1]))
        except KeyError:
            tmp = val[1]
            tmp2 = dico[tmp]
            tmp3 = tmp2.split('/')
            for val2 in tmp3:
                tmp4 = val2.split(':')
                if tmp4[0] == val[0]:
                    tmp5 = tmp4[1].split(';')
                    datax.append(float(tmp5[0]))
                    datay.append(float(tmp5[1]))
    
    datax.append(xdest)
    datay.append(ydest)
    
    tabcoord = []
    
    for cpt, val in enumerate(datax):
        if cpt == len(datax)-1:
            break
        if cpt == 0:
            tabcoord.append(str(val)+';'+str(datay[cpt]))
            if cpt < len(datax)-1:
                tabcoord[cpt]+=' '+str(datax[cpt+1])+';'+str(datay[cpt+1])
        else:
            tabcoord.append(str(val)+';'+str(datay[cpt]))
            if cpt < len(datax)-1:
                tabcoord[cpt]+=' '+str(datax[cpt+1])+';'+str(datay[cpt+1])
    
    listedespieces = []
    for val in pieces:
        listedespieces.append(str(val[0])[5:-6])   
    
    for cpt, val in enumerate(listedespieces):
        nom = val
        if nom in listpieces:
            val = listorigin[listpieces.index(nom)].split(';')
            x0tmp = float(val[0])
            y0tmp = float(val[1])
            
            fic = open('../../data/tmp/'+nom,'w')
            ind = listpieces.index(nom)
            temp = tabcoord[ind].split(' ')
            fic.write(temp[0]+' '+temp[1]+'\n')
            mur = pieces[cpt][1][0]
            tabtmp = []
            for point in mur:
                tmp = point.split(',')
                if len(tabtmp) == 0:
                    tmp2 = tmp[0].split(';')
                    tabtmp.append(tmp[0])
                    fic.write(str(float(tmp2[0])+x0tmp)+';'+str(float(tmp2[1])+y0tmp)+' ')
                    premierpoint = str(float(tmp2[0])+x0tmp)+';'+str(float(tmp2[1])+y0tmp)
                if tabtmp[-1] != tmp[0]:
                    tmp2 = tmp[0].split(';')
                    tabtmp.append(tmp[0])
                    fic.write(str(float(tmp2[0])+x0tmp)+';'+str(float(tmp2[1])+y0tmp)+' ')
                tabtmp.append(tmp[1])
                tmp2 = tmp[1].split(';')
                fic.write(str(float(tmp2[0])+x0tmp)+';'+str(float(tmp2[1])+y0tmp)+' ')
            fic.write(premierpoint)
            if nom in dicobstacles.keys():
                fic.write('\n')
                listobs = dicobstacles[nom]
                testdejadedans = []
                for val in listobs:
                    for cpt, val2 in enumerate(val[0]):
                        if cpt == len(val[0])-1:
                            test = str(val2)+';'+str(val[1][cpt])
                            if not(test in testdejadedans):
                                fic.write(test)
                                testdejadedans.append(test)
                        else:
                            test = str(val2)+';'+str(val[1][cpt])+' '
                            if not(test in testdejadedans):
                                fic.write(test)
                                testdejadedans.append(test)
                    fic.write('\n')
            fic.close()
                    
    data.append(datax)
    data.append(datay)
    
    if conf.affichedij == 1: 
        line = plt.plot(*data)   
        dij = plt.setp(line, color='black', linewidth=1)
    
    if valaff == 1:
        for ind, val in enumerate(datorigin):
            value = val.split(';')
            x = float(value[0])+0.25
            y = float(value[1])+0.5
            txt.append(plt.text(x, y, nomorigin[ind], fontsize=10, bbox={'facecolor':'grey', 'alpha':0.25, 'pad':10}))
    
    courbes = []
    data = []
    
    try:
        seuil = float(entreeseuil.get())
        if seuil == 0.0:
            avecSeuil = 0
        else:
            avecSeuil = 1
        t=0
    except ValueError:    
        seuil = 0.0
        avecSeuil = 0
        s = entreeseuil.get()
        t=0
        if s == 'terminator':
            seuil = 0.3
            avecSeuil = 1
            t=1
        
    T = time.time()

    tab = []
    
    fname = time.strftime("%d_%m_%Y_%H_%M_%S")
    pname = (filepath.split('/')[-1]).split('.')[0]
    
    if t != 1:
        fichier = open("../../data/res/"+fname+'_'+pname+'_'+str(seuil)+".txt", "w")
    
    for fic in listpieces:

        if avecSeuil == 1:
            courbes = exp.appelAgr(fic,seuil,t)
            tab.append(courbes)
        else :
            courbes = exp.appelPieceBloque(fic,seuil)
        if t != 1:
            datax = []
            datay = []
            for val in courbes:
                datax.append(val[0])
                datay.append(val[1])
                fichier.write(str(val[0])+"\t"+str(val[1])+'\n')
            data.append(datax)
            data.append(datay)
            
            line2 = plt.plot(*data)
            plt.setp(line2, color ='red',linewidth=1)
            canvas.show()

    if t!= 1:
        fichier.close()
    
    tab2 = []
    
    if t == 1:
        modifaff()
        
        for piece in tab:
            tab2.append(traitementPiece(piece.tolist()))

        tabimg = []
        for val in range(1,7):
            for val2 in range(1,5):
                tabimg.append(mpimg.imread('../../data/img/mv/mv'+str(val)+'-'+str(val2)+'.png'))
                
        if winsoundval == 1:
            PlaySound('../../data/sound/chiptune.wav', winsound.SND_ASYNC)
        else:
            if pglet == 1:
                player = pyglet.media.Player()
                song = pyglet.media.load('../../data/sound/chiptune.wav')
                player.queue(song)
                player.volume=1.0
                player.play()
            
        cpt = 0
        for val in tab2:
            for cpt2, val2 in enumerate(val):
                if cpt == 4:
                    cpt = 0
                
                if cpt2 < len(val)-1:
                    valtmp = val[cpt2+1]

                    dx = valtmp[0]-val2[0]
                    dy = valtmp[1]-val2[1]
                    
                    if dx >= 0 and dy >= 0:
                    
                        if dx >= dy:
                             t = plt.imshow(tabimg[4*cpt+3],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                        else:
                             t = plt.imshow(tabimg[4*cpt+2],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                             
                    elif dx < 0 and dy < 0:
                    
                        if dx <= dy:
                            t = plt.imshow(tabimg[4*cpt+1],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                        else:
                            t = plt.imshow(tabimg[4*cpt],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                            
                    elif dx>=0 and dy<0:
                        
                        if abs(dy) >= abs(dx):
                            t = plt.imshow(tabimg[4*cpt],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                        else:
                            t = plt.imshow(tabimg[4*cpt+3],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                            
                    else:
                    
                        if abs(dx) >= abs(dy):
                            t = plt.imshow(tabimg[4*cpt+1],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                        else:
                            t = plt.imshow(tabimg[4*cpt+2],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                else:
                    t = plt.imshow(tabimg[4*cpt],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                     
                canvas.show()
                time.sleep(.050)
                t.remove()
                cpt+=1
                
        if winsoundval == 1:
            PlaySound('../../data/sound/be_back.wav', winsound.SND_FILENAME)
        else:
            if pglet == 1:
                player = pyglet.media.Player()
                song = pyglet.media.load('../../data/sound/be_back.wav')
                player.queue(song)
                player.volume=1.0
                player.play()
                
        cpt = 0
        for val in reversed(tab2):
            for cpt2, val2 in enumerate(reversed(val)):
                if cpt == 4:
                    cpt = 0
                
                if cpt2 > len(val)-1:
                    valtmp = val[cpt2+1]

                    dx = valtmp[0]-val2[0]
                    dy = valtmp[1]-val2[1]
                    
                    if dx >= 0 and dy >= 0:
                    
                        if dx >= dy:
                             t = plt.imshow(tabimg[4*cpt+3],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                        else:
                             t = plt.imshow(tabimg[4*cpt+2],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                             
                    elif dx < 0 and dy < 0:
                    
                        if dx <= dy:
                            t = plt.imshow(tabimg[4*cpt+1],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                        else:
                            t = plt.imshow(tabimg[4*cpt],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                            
                    elif dx>=0 and dy<0:
                        
                        if abs(dy) >= abs(dx):
                            t = plt.imshow(tabimg[4*cpt],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                        else:
                            t = plt.imshow(tabimg[4*cpt+3],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                            
                    else:
                    
                        if abs(dx) >= abs(dy):
                            t = plt.imshow(tabimg[4*cpt+1],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                        else:
                            t = plt.imshow(tabimg[4*cpt+2],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                else:
                    t = plt.imshow(tabimg[4*cpt],zorder=10, extent=[val2[0]-0.4,val2[0]+0.4,val2[1]-0.4, val2[1]+0.4])
                     
                canvas.show()
                time.sleep(.050)
                t.remove()
                cpt+=1

    tmpath = '../../data/tmp'

    for file in os.listdir(tmpath):
        os.remove(tmpath+'/'+file)

def traitementPiece(tab):
    """

    Est utilisée pour l'affichage d'Arnold sur la courbe. Un point sera ajouté à un tableau tous les 10 centimètres.

    Ce dernier servira pour ancrer les sprites sur le plan.

    :param tab: liste des points de la ligne calculée après les déformations
    :type tab: list

    :rtype: list

    """

    res = []
    valtmp = []
    for cpt, val in enumerate(tab):
        if cpt == 0:
            valtmp = val
            res.append(val)
        if math.sqrt(pow(valtmp[0]-val[0],2)+pow(valtmp[1]-val[1],2))>0.1:
            valtmp = val
            res.append(val)
    return res

def sauvegarde():
    """
    Lance la sauvegarde du plan courant. 

    Celle-ci sera effectuée par la fonction outils.lectureXML.sauvegardeXML().
    """

    tmp = filepath.split('/')
    nomfic = '../../data/tmp/'+tmp[-1].split('.xml')[0]+'_tmp.xml'
    shutil.copy2(filepath,nomfic)
    
    fic = asksaveasfile(initialdir="../../data/plans/",mode='w',defaultextension=".xml")

    if fic == () or fic == '':
        return

    lectureXML.sauvegardeXML(nomfic,fic,dicobstacles,nomorigin,datorigin)
