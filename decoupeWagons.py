#!/usr/bin/python3

"""
Recherche des sous-répertoires contenant des fichiers .tex, qui utilisent le
module "devoir.sty", et qui utilisent les macros \question.
"""

import sys, os, os.path, re, hashlib, tarfile
from shutil import copyfile

def hash(s):
    """
    fabrique un hash hexadécimal à partir d'une chaîne d'octets
    @param s une chaîne d'octets (bytes) ou une chaîne unicode qui sera
    convertie en octets (encodage utf-8)
    @return une suite de nombres hexadécimaux
    """
    if isinstance(s, str):
        s=s.encode("utf-8")
    return hashlib.md5(s).hexdigest()

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
    images={}
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
    for l in lines:
        # repérage des fichiers images
        m=re.match(r"^(.*includegraphics[^{]*\{)([^}]+)(\}.*)$", l)
        if m: # associe l'ancien nom d'image avec une chaîne aléatoire
            n="img_"+hash(filePref+m.group(2))
            images[m.group(2)]=n
            l=m.group(1)+n+m.group(3)+"\n"
        m=re.match(r"^(.*figeps[^{]*\{)([^}]+)(\}.*)$", l)
        if m: # associe l'ancien nom d'image avec une chaîne aléatoire
            n="img_"+hash(filePref+m.group(2))
            images[m.group(2)]=n
            l=m.group(1)+n+m.group(3)+"\n"
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
        with open(os.path.join(root,"decoupe",filePref,"%02d.tex" %i), "w")\
             as outfile:
            for l in q:
                outfile.write(l)
        i=i+1
    for imname in images:
        ## enregistre les images en les renommant
        imgfiles=[i for i in os.listdir(root) if i.startswith(imname)]
        for i in imgfiles:
            r, ext= os.path.splitext(i)
            newfile=os.path.join(root,"decoupe",filePref,images[imname]+ext)
            copyfile(os.path.join(root,i), newfile)
    return newdir

def collecte(indir, outdir="collection"):
    """
    collecte les fichiers contenus dans un répertoire, les renomme au passage
    avec un préfixe aléatoire, et le suffixe .tex
    @param indir un répertoire, qui est censé contenir uniquement des
    fichiers .tex, encodés en UTF-8
    @param outdir un répertoire cible, par défaut : "collection"
    """
    archivables=[]
    for f in os.listdir(indir):
        if f.startswith("img_"):
            # c'est une image, recopiée sans modification
            copyfile(os.path.join(indir,f),os.path.join(outdir,f))
            archivables.append(f)
        else:
            continue
    for f in os.listdir(indir):
        if f.startswith("img_"):
            continue # rien pour les images
        else:
            contents=open(os.path.join(indir,f),"rb").read()
            h=hash(contents)
            g="%s.tex" %h
            copyfile(os.path.join(indir,f),os.path.join(outdir,g))
            wd=os.getcwd()
            with tarfile.open(os.path.join(outdir,"%s.tgz") %h, "w:gz") as tgz:
                os.chdir(indir)
                for a in archivables:
                    m=re.match(r"img_([0-9a-f]*)", a)
                    if m and m.group(1).encode("ascii") in contents:
                        ## on n'archive l'image que si elle est citée dans
                        ## le fichier .tex
                        tgz.add(a)
                tgz.add(f)
            os.chdir(wd)
    return

                
if __name__=="__main__":
    d=(findTexFiles('.'))
    os.makedirs("collection", exist_ok=True)
    for k in d:
        for f in d[k]:
            collecte(decoupe(k,f))
    print ("Créé le répertoire collection")
            
