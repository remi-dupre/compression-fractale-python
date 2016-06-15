# -*- coding: utf-8 -*

from math import ceil
import numpy as np
from PIL import Image
from tqdm import *

from recherche.bloc import Bloc
from recherche.graphe import Graphe
import couleur

lenna = Image.open('Lenna.png')
lenvdg = np.array(lenna)[:,:,0].astype(int)

parametres = {
    'taille_petit' : 8, # la taille des petits blocs
    'couleur' : couleur.representation.etaler
}

def savegrey(str, img) :
    # img = np.array([[(c,c,c) for c in L] for L in img])
    img = Image.fromarray(img.astype(np.uint8))
    img.save(str)

def decouper(taille, image) :
    # Retourne un liste de blocs découpés de l'image (nvdg)
    # Il faut que la taille divise les dimensions de l'image
    retour = []
    l, h = image.shape
    nl, nh = ceil(l/taille), ceil(h/taille)
    for i in range(nl) :
        for j in range(nh) :
            retour.append( image[taille*i:taille*(i+1), taille*j:taille*(j+1)].copy() )
    return retour

def recomposer(taille, decoupe, dim) :
    largeur, hauteur = dim
    nb_c = largeur // taille
    nb_l = hauteur // taille
    lignes = [ np.concatenate(decoupe[nb_c*i:nb_c*(i+1)], axis=1) for i in range(nb_l) ]
    return np.concatenate(lignes)

def recherche_ifs(param, image) :
    # Retourne l'ifs représentant l'image (nvdg)

    print('Decoupe de l\'image')
    destinations = decouper(param['taille_petit'], image)
    destinations = [ Bloc(bloc) for bloc in destinations ]

    sources = decouper(param['taille_petit']*2, image)
    [ couleur.normaliser(param['couleur'], bloc) for bloc in sources ]
    sources = [ Bloc(bloc) for bloc in sources ]

    print('Application des transformations a ', len(sources), 'blocs')
    sources = [ bloc.transformer(transfo) for bloc in sources for transfo in range(8) ]

    print('Construction du graphe de ', len(sources), 'noeuds')
    G = Graphe(sources)
    print('Recherche pour ', len(destinations), ' blocs')
    match = []
    for i in tqdm(range(len(destinations)), 'Correspondances') :
        col = couleur.normaliser(param['couleur'], destinations[i].data)
        s = G.chercher(destinations[i])
        correspondance = (col, s) # couleur, source
        match.append(correspondance)
        if i < 200 :
            savegrey("test/" + str(i) + "d.png", destinations[i].data)
            savegrey("test/" + str(i) + "s.png", sources[match[i][1]].data)
    return match

def appliquer_ifs(param, ifs, image) :
    # Applique un ifs à une image (nvdg)
    taille = param['taille_petit']
    sources = decouper(taille*2, image)
    [ couleur.normaliser(param['couleur'], bloc) for bloc in sources ]
    sources = [ Bloc(bloc) for bloc in sources ]

    destinations = []
    for col, s in ifs :
        i, transfo = s // 8, s % 8
        destinations.append(sources[i].transformer(transfo).data)
        couleur.reproduire(param['couleur'], col, destinations[-1])

    return recomposer(param['taille_petit'], destinations, (len(image[0]), len(image)))

ifs = recherche_ifs(parametres, lenvdg)

import simplejson
f = open('debug.txt', 'w')
f.write(str(ifs))
f.close()

R = appliquer_ifs(parametres, ifs, lenvdg)
# R = appliquer_ifs(parametres, ifs, R)
savegrey("triche.png", R)
print(lenvdg.dtype)

R = np.zeros(lenvdg.shape, dtype=np.uint8)
for _ in tqdm(range(10), 'Decompression') :
    R = appliquer_ifs(parametres, ifs, R)
savegrey("debug.png", R)
