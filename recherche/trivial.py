# Ce fichier contient les fonctions de recherche exhaustive
# Le résultat par cette méthode donne donc les meilleurs approximations possibles et une complexité maximale.

from recherche.bloc import Bloc

def match(destinations, sources) :
	# Effectue la recherche des blocs proches de façon exhaustive
	# Entrée :
	#  - destinations : liste des blocs destination (pour lesquels on cherche)
	#  - sources : liste des blocs source (parmi lequels on cherche)
	# Sortie : une liste du doublets (d, s)
	#  - où 'd' est l'indice d'un bloc destination
	#  - s est l'indice du bloc source le plus proche
	
	retour = []
	for d in range(len(destinations)) :
		dest = destinations[d]
		retour.append( (d, chercher(sources, dest)) )
	return retour

def chercher_min(sources, bloc, membres=None) :
	# Retourne le bloc source le plus proche
	# Entrées :
	#  - sources : liste des blocs source parmis lesquels chercher
	#  - bloc : le bloc qu'on cherche à approcher
	#  - membres (falcutatif) : les indices à considérer dans 'sources'
	# Sortie :
	#  - l'indice du bloc source proche
	#  - la distance de ce bloc
	if membres is None : membres = range(len(sources))
	
	distance = float('inf')
	proche = membres[0]
	for s in membres :
		nv_dist = Bloc.distance(sources[s], bloc)
		if nv_dist < distance :
			distance = nv_dist
			proche = s
	return proche, distance

def chercher(sources, bloc, membres=None) :
	# Pareil que chercher_dist mais sans retourner la distance
	r, _ = chercher_min(sources, bloc, membres)
	return r