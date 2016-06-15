# Effectue quelques tests sur les différentes méthodes de recherches qui ont été implémentées

from bloc import Bloc

NB_DESTINATIONS = 500                   # Le nombre de blocs destinations
NB_SOURCES = (NB_DESTINATIONS // 4) * 8 # 8 transformations appliquées à des blocs 8 fois plus petits

destinations = [ Bloc() for i in range(NB_DESTINATIONS) ]
sources = [ Bloc() for i in range(NB_SOURCES) ]

distances = [ Bloc.distance(d, s) for d in destinations for s in sources ]
print("La plus grande distance est : ", max(distances))
print("La plus petite distance est : ", min(distances))
print("La distance moyenne est ", sum(distances) / len(distances))

## Algorithme trivial

import trivial

Bloc.comparaisons = 0
match = trivial.match(destinations, sources)

print()
print("L'algorithme trivial demande ", Bloc.comparaisons, " comparaisons")

distances = [ Bloc.distance(destinations[d], sources[s]) for (d, s) in match ]
print("La plus grande distance est : ", max(distances))
print("La plus petite distance est : ", min(distances))
print("La distance moyenne est ", sum(distances) / len(distances), " (optimal)")

## Par découpe de l'espace

from decoupe import Zone

Bloc.comparaisons = 0
arbre = Zone(sources)

print()
print("Construire l'arbre de répartition demande ", Bloc.comparaisons, " comparaisons")

a_match = []
for i in range(len(destinations)) :
    s = arbre.chercher(destinations[i])
    a_match.append((i, s))
    
print("Cette méthode demande au total ", Bloc.comparaisons, " comparaisons")

distances = [ Bloc.distance(destinations[d], sources[s]) for (d, s) in a_match ]
print("La plus grande distance est : ", max(distances))
print("La plus petite distance est : ", min(distances))
print("La distance moyenne est ", sum(distances) / len(distances))


## Construction d'un graphe

from graphe import Graphe

Bloc.comparaisons = 0
G = Graphe(sources)

print()
print("Construire le graphe demande ", Bloc.comparaisons, " comparaisons")

g_match = []
for i in range(len(destinations)) :
    s = G.chercher(destinations[i])
    g_match.append((i, s))
    
print("Cette méthode demande au total ", Bloc.comparaisons, " comparaisons")
distances = [ Bloc.distance(destinations[d], sources[s]) for (d, s) in g_match ]
print("La plus grande distance est : ", max(distances))
print("La plus petite distance est : ", min(distances))
print("La distance moyenne est ", sum(distances) / len(distances))
