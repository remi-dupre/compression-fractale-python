# Effectue quelques tests sur les différentes méthodes de recherches qui ont été implémentées

from block import Block

from search.graph import Graph
from search.separate import Zone
from search.trivial import Exaustive

NB_DESTINATIONS = 1000					# Le nombre de blocks destinations
NB_SOURCES = (NB_DESTINATIONS // 4) * 8	# 8 transformations appliquées à des blocks 8 fois plus petits

destinations = [ Block() for i in range(NB_DESTINATIONS) ]
sources = [ Block() for i in range(NB_SOURCES) ]

distances = [ Block.dist(d, s) for d in destinations for s in sources ]
print("La plus grande distance est : ", max(distances))
print("La plus petite distance est : ", min(distances))
print("La distance moyenne est ", sum(distances) / len(distances))
print()

## Algorithme trivial

methods = [Exaustive, Graph, Zone]

for Structure in methods :
	print("##### ", Structure.__name__, " #####")

	Block.comparaisons = 0
	stock = Structure(sources)

	match = []
	for i in range(len(destinations)) :
		s = stock.search(destinations[i])
		match.append((destinations[i], s))

	print("Demande ", Block.comparaisons, " comparaisons")

	distances = [ Block.dist(d, s) for (d, s) in match ]
	print("La plus grande distance est : ", max(distances))
	print("La plus petite distance est : ", min(distances))
	print("La distance moyenne est ", sum(distances) / len(distances))
	print()
