.. PAndroide documentation master file, created by
   sphinx-quickstart on Wed May 11 13:23:13 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Bienvenue sur la documentation de notre Projet Androide !
=========================================================

"La plupart des méthodes de planification de mouvements sont basées sur une exploration aléatoire de l'espace atteignable.
Elles ne prennent en compte ni la géométrie de l'espace de travail, ni celle des obstacles, et pour cette raison il leur est difficile de trouver des solutions dans des passages étroits.
L'objectif de ce projet est de créer des déformations de l'espace (en utilisant un algorithme récent qui permet d'en construire rapidement) qui réduisent significativement la taille des obstacles et permettent ainsi de résoudre facilement les problèmes de planification de chemin. Cette méthode a plusieurs avantages potentiels : par exemple, la déformation de l'espace sera réutilisable quelles que soient les configurations initiales et finales, et les chemins obtenus seront directement lisses, ce qui n'est pas le cas avec les méthodes classiques basées sur des arbres d'exploration."

Après s'être fait la main sur l'algorithme de déformation proposé le sujet a été contextualisé et il a été décidé que ce qui était à la base un projet plutôt exploratoire allait devenir un projet de planification de mouvements, en deux dimensions, d'un robot dans un batiment encombré d'obstacles. Plusieurs options ont été imaginées, décrites dans le rapport elles ont toutes leurs avantages et inconvénients, tant au niveau du temps de calcul qu'au niveau de la précision des résultats.

Table des matières:
===================

.. toctree::
   :maxdepth: 2
   
   code
   algo
   interface
   outils
   

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`