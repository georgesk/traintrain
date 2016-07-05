#!/usr/bin/python3

"""
Recherche des sous-répertoires contenant des fichiers .tex, qui utilisent le
module "devoir.sty", et qui utilisent les macros \question.
"""

import sys, os, os.path, re, random

def findTexFiles(top):
    """
    trouve les fichiers tex qui font appel au module devoir en fouillant
    récursivement le répertoire top.
    @param top la racine de l'arbre de fichier à fouiller
    @return un dictionnaire dont les clés sont les répertoires, et dont
    les feuilles sont des dictionnaires
    (préfixe du fichier => nom complet du fichier), ce qui permet de distinguer
    les fichiers "corrige.tex" quand ils existent
    """
    result={}
    top='.'
    for root, dirs, files in os.walk(top, topdown=False):
        # on vérifie que le répertoire ne contient pas le mot "collection"
        if "collection" in root:
            continue
        for name in files:
            if re.match(r"^.*\.tex$", name):
                path=os.path.join(root,name)
                contents=""
                for encoding in ("utf8","latin1"):
                    try:
                        with open(path, encoding=encoding) as f:
                            contents=f.read()
                    except:
                        continue
                if re.search(r"usepackage.*devoir", contents,re.M):
                    if root not in result:
                        result[root]={}
                    result[root][os.path.splitext(name)[0]]=name
    return result

def decoupe(root, filePref):
    """
    découpe un fichier en questions
    @param root le répertoire qui contient le fichier
    @param filePref le nom d'un fichier .tex sans le suffixe
    @result le chemin vers un sous-répertoire qui contiendra les questions
    issues du fichier à découper.
    """
    newdir=os.path.join(root,"decoupe",filePref)
    os.makedirs(newdir, exist_ok=True)
    questions=[]
    question=[]
    lines=[]
    for encoding in ("utf8","latin1"):
        try:
            with open(os.path.join(root,filePref+".tex"), encoding=encoding) as f:
                lines=f.readlines()
                break
        except:
            continue
    begin=False
    end=False
    for l in lines:
        if not begin:
            if re.match (r"\\question",l):
                question.append(l)
                begin=True
            else:
                continue
        else: # begin == True
            if re.match (r"\\question",l):
                questions.append(question)
                question=[l]
                continue
            elif re.match (r"end{devoir}",l):
                questions.append(question)
                break;
            else:
                question.append(l)
    i=1
    for q in questions:
        with open(os.path.join(root,"decoupe",filePref,"%02d.tex" %i), "w") as outfile:
            for l in q:
                outfile.write(l)
        i=i+1
    return newdir

def collecte(indir, outdir="collection"):
    """
    collecte les fichiers contenus dans un répertoire, les renomme au passage
    avec un préfixe aléatoire, et le suffixe .tex
    @param indir un répertoire, qui est censé contenir uniquement des
    fichiers .tex, encodés en UTF-8
    @param outdir un répertoire cible, par défaut : "collection"
    """
    for f in os.listdir(indir):
        g="%d.tex" %random.randint(1e8, 1e9) # nom de fichier fait de 9 chiffres
        while os.path.exists(os.path.join(outdir,g)):
            # refait le tirage au sort si le fichier existe déjà !
            g="%d.tex" %random.randint(1e8, 1e9)
        with open(os.path.join(indir,f)) as infile, \
             open(os.path.join(outdir,g),"w") as outfile:
            outfile.write(infile.read())
    return

                
if __name__=="__main__":
    d=(findTexFiles('.'))
    os.makedirs("collection", exist_ok=True)
    for k in d:
        for f in d[k]:
            collecte(decoupe(k,f))
    print ("Créé le répertoire collection")
            
