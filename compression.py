# -*- coding: utf-8 -*

from math import ceil
import numpy as np
from PIL import Image
from tqdm import *

from recherche.bloc import Bloc
from recherche.graphe import Graphe
import couleur

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
            retour.append( image[taille*i:taille*(i+1), taille*j:taille*(j+1)].copy().astype(int) )
    return retour

def recomposer(taille, decoupe, dim) :
    largeur, hauteur = dim
    nb_c = largeur // taille
    nb_l = hauteur // taille
    lignes = [ np.concatenate(decoupe[nb_c*i:nb_c*(i+1)], axis=1) for i in range(nb_l) ]
    return np.concatenate(lignes)

def recherche_ifs(param, image, text='Compression') :
    # Retourne l'ifs représentant l'image (nvdg)

    destinations = decouper(param['taille_petit'], image)
    destinations = [ Bloc(bloc) for bloc in destinations ]

    sources = decouper(param['taille_petit']*2, image)
    [ couleur.normaliser(param['methode_couleur'], bloc) for bloc in sources ]
    sources = [ Bloc(bloc) for bloc in sources ]
    sources = [ bloc.transformer(transfo) for bloc in sources for transfo in range(8) ]

    G = Graphe(sources, text + ' (1/2)')
    match = []
    for i in tqdm(range(len(destinations)), text+' (2/2)') :
        col = couleur.normaliser(param['methode_couleur'], destinations[i].data)
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
    [ couleur.normaliser(param['methode_couleur'], bloc) for bloc in sources ]
    sources = [ Bloc(bloc) for bloc in sources ]

    destinations = []
    for col, s in ifs :
        i, transfo = s // 8, s % 8
        destinations.append(sources[i].transformer(transfo).data)
        couleur.reproduire(param['methode_couleur'], col, destinations[-1])

    return recomposer(param['taille_petit'], destinations, (len(image[0]), len(image)))

def compresser(fichier, params) :
    img = Image.open(fichier)
    l, h, p = np.array(img).shape

    couche = [ np.array(img)[:,:,i] for i in range(3) ]
    couche.append(np.array(img)[:,:,3] if p == 4 else np.zeros((l,h), dtype=int))

    if params['couleur'] is None :
        params['couleur'] = not np.all(couche[0] == couche[1])
    if params['transparence'] is None :
        params['transparence'] = not np.all(couche[3] == couche[3][0,0])

    ifs = []
    if params['couleur'] :
        for i in range(3) :
            col = ['Rouge', 'Vert  ', 'Bleu  ']
            ifs.append( recherche_ifs(params, couche[i], col[i]) )
    else :
        ifs.append( recherche_ifs(params, couche[0], 'NVDG ') )
    if params['transparence'] :
        ifs.append( recherche_ifs(params, couche[3], 'Alpha') )

    return ((l,h), ifs, params)

def decompresser(ifs) :
    l, h = ifs[0]
    image = []
    for couche in ifs[1] :
        I = np.zeros((l,h), dtype=int)
        for i in tqdm(range(10), 'Decompression') :
            I = appliquer_ifs(ifs[2], couche, I)
            savegrey(str(i)+'.png', I)
        image.append(I)

    if len(image) == 2 : image = [ image[0], image[0], image[0], image[1] ]
    if len(image) > 1 :
        image = [ [ [ image[i][x][y] for i in range(len(image)) ] for y in range(len(image[0][0])) ] for x in range(len(image[0])) ]
    if len(image) == 1 : image = image[0]

    img = Image.fromarray( np.array(image).astype(np.uint8) )
    img.save('debug.png')


parametres = {
    'taille_petit' : 4, # la taille des petits blocs
    'methode_couleur' : couleur.representation.etaler,
    'transparence' : None,
    'couleur' : None
}

ifs = compresser('LennaC.png', parametres)
decompresser(ifs)

print(Bloc.comparaisons, 'comparaisons')
