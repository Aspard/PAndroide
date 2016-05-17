.. PAndroide documentation master file, created by Gaspard Ducamp and Yoann Taille

Bienvenue sur la documentation de notre Projet Androide !
=========================================================

"La plupart des méthodes de planification de mouvements sont basées sur une exploration aléatoire de l'espace atteignable.
Elles ne prennent en compte ni la géométrie de l'espace de travail, ni celle des obstacles, et pour cette raison il leur est difficile de trouver des solutions dans des passages étroits.
L'objectif de ce projet est de créer des déformations de l'espace (en utilisant un algorithme récent qui permet d'en construire rapidement) qui réduisent significativement la taille des obstacles et permettent ainsi de résoudre facilement les problèmes de planification de chemin. Cette méthode a plusieurs avantages potentiels : par exemple, la déformation de l'espace sera réutilisable quelles que soient les configurations initiales et finales, et les chemins obtenus seront directement lisses, ce qui n'est pas le cas avec les méthodes classiques basées sur des arbres d'exploration."

Après s'être fait la main sur l'algorithme de déformation proposé le sujet a été contextualisé et il a été décidé que ce qui était à la base un projet plutôt exploratoire allait devenir un projet de planification de mouvements, en deux dimensions, d'un robot dans un bâtiment encombré d'obstacles. Plusieurs options ont été imaginées, décrites dans le rapport elles ont toutes leurs avantages et inconvénients, tant au niveau du temps de calcul qu'au niveau de la précision des résultats.

Afin de trouver notre chemin dans un bâtiment nous commenceront par lire, dans un fichier xml, une description pièce par pièce de celui-ci (les murs, obstacles et connexions qui les composent). Une fois que l'on aura généré des structures de données reliant celles-ci et les caractérisants nous appliqueront un algorithme de type "plus court chemin" afin de déterminer par quelles pièces passer pour relier un point du bâtiment à un autre. Ces dernières seront traitées indépendamment par nos algorithmes.

L'article fondateur
===================

L'algorithme de déformation utilisé provient d'un article (Nicolas Perrin, ISIR) contenant un algorithme d'alignement difféomorphique issu de :download:`cet article <../data/doc/diffeo_matching.pdf>` (en préparation).

Nos approches
=============

Un pdf décrivant les différentes approches imaginées et mises en place est disponible :download:`ici <../data/doc/approches.pdf>`

Table des matières:
===================

.. toctree::
   :maxdepth: 3
   
   code
   algo
   outils
   interface
   exemple
   

Index
==================

* :ref:`genindex`
* :ref:`modindex`
