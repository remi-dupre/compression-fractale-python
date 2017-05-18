import numpy as np

class Block :
	# Classe représentant un Block dans une image
	# Attributs :
	#  - data : les pixels du Block

	TAILLE = 8		 	# La taille des Blocks
	comparaisons = 0	# Nombre decomparaisons effectuées

	def __init__(self, data=None) :
		if data is None :
			# Le Block a un contenu aléatoire par défaut
			valeurs = np.random.random((Block.TAILLE, Block.TAILLE)) * 256
			self.data = np.array(valeurs, dtype=int)
		else :
			self.data = data

	def distance(A, B) :
		# Calcule la variance entre deux Blocks
		n = len(A.data)
		Block.comparaisons += 1

		D = A.data - B.data
		return np.sum(D**2)# // n**2 # - (np.sum(D)**2 // n**2) ) 

	def transformer(self, i) :
		# Retourne un Block auquel on a appliqué la transformation d'indice i
		retour = self.data[::2,::2].copy()
		if i > 3 :
			retour = np.flipud(retour)
			i -= 4
		retour = np.rot90(retour, i)
		return Block(retour)
