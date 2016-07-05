# train-train, pour jouer au petit train avec LaTeX #

L'idée principale de train-train est qu'on peut former des documents
LaTeX en recomposant des petits blocs de texte puisés dans une base de
documents déjà prêts, si possible facile à chercher.


La première implémentation s'est faite à partir d'une suite de documents
destinés à des élèves de lycée en sciences physiques, des devoirs ou des
interrogations. Ces documents sont structurés à l'aide d'une macro nommée
`\question`, qui permet de délimiter les questions posées aux élèves, et
en même temps de gérer la numérotation, l'affichage d'un barème, et quelques
petites facilités pour le professeur qui en est l'auteur.

Il a été relativement facile de reprendre  les documents créés en quatre ans,
et de les découper en questions indépendantes, du fait de leur structure.

# Comment reconstituer une base qui fonctionne #

## Les documents à découper sont placés dans des sous-répertoires ##

Il faut juste éviter que ces sous-répertoires ne s'appellent `*collection*`
Dans le même sous-répertoire, il y a les fichiers .tex et les images utilisées
pour créer le document.

## Remise à blanc de tout le découpage ##

Commande : `make distclean`

## Découpage en questions et indexation ##

Commande : `make init`

## Compilation de fichiers HTML pour prévisualiser les contenus ##

Commande : `make`

# Moteur de recherche, accès aux sources #

Le moteur de recherche, très rudimentaire, est basé sur le moteur
SWISH++.

On fait en sorte que le répertoire courant soit dans une zone qu'un
serveur Apache2 est en mesure de traiter, et à partir de là il suffit
d'accéder à l'aide d'un navigateur au fichier search.html ; celui-ci
permet d'entrer une chaîne de recherche, puis appelle le script search.cgi
qui met en forme les résultats et donne accès aux archives de sources.


