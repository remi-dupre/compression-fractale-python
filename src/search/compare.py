# Effectue quelques tests sur les différentes méthodes de recherches qui ont été implémentées

from block import Block
from search import methods


def test_random(nb_destinations=500) :
    """Process tests on randomly generated blocs"""
    nb_sources = (nb_destinations // 4) * 8    # 8 transformations applied to blocks 8 times smallers

    # Generate blocks
    destinations = [Block() for i in range(nb_destinations)]
    sources = [Block() for i in range(nb_sources)]

    # General statistics on blocks
    distances = [Block.dist(d, s) for d in destinations for s in sources]
    print("La plus grande distance est : ", max(distances))
    print("La plus petite distance est : ", min(distances))
    print("La distance moyenne est ", sum(distances) / len(distances))
    print()

    # Statistics on each structure
    for Structure in methods :
        print("##### ", Structure.__name__, " #####")

        Block.comparaisons = 0
        stock = Structure(sources)

        match = []
        for i in range(len(destinations)) :
            s = stock.search(destinations[i])
            match.append((destinations[i], sources[s]))

        print("Demande ", Block.comparaisons, " comparaisons")

        distances = [Block.dist(d, s) for (d, s) in match]
        print("La plus grande distance est : ", max(distances))
        print("La plus petite distance est : ", min(distances))
        print("La distance moyenne est ", sum(distances) / len(distances))
        print()
