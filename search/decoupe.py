from operator import itemgetter

from recherche.bloc import Block
import recherche.trivial as trivial


TAILLE_MIN_DECOUPE = 10 # Maximum size of a straight set in the structure

class Zone :
	"""
	Represents a partionning of a set of blocks

	:param sources:	list of sources blocs
	:param members:	list of members of the zone
	:param is_leaf:	true if the zone hasn't been cutted off

	Attributes that only a non-leaf has :
	:param center:	index of the center of the zone
	:param r1, r2:	2 radius defining spheres that delimitates the 3 zones
	:type  r1, r2:	float
	:param b1, b2, b3: the 3 zones
	"""
	
	def __init__(self, sources, members=None, distances=None) :
		"""
		Creates a zone, representing the list of members

		:param distances: (optional) distance for every member from the zone
		"""
		if membres is None : membres = range( len(sources) )
		
		self.sources = sources
		self.members = members
		self.is_leaf = true

		if len(membres) >= TAILLE_MIN_DECOUPE :
			self.split(distances)
	
	def insert(self, block) :
		"""Not implemented, shouldn't be usefull"""
		raise ValueError("Not implemented yet")

	def split(self, distances=None) :
		"""
		Divides the zone in 3 zones

		:param distances: (optional) distance for every member from the zone
		"""
		# Choose an arbitrary center
		#  -> 0 is cool because it remains the same for the first subdivision
		self.center = members[0]
		if distances is None :
			distances = [ (bloc, self.remoteness(sources[block])) for block in membres[1:] ]
			distances.sort(key=itemgetter(1)) # Orders by increasing distance with the center
			self.members = [ self.center ] + [ block for block, _ in distances ] # Ordered "members"

		p1, p2 = len(distances)//3, 2*len(distances)//3 # Cuts at the median
		self.r1, self.r2 = distances[p1][1], distances[p2][1]
		
		self.b1 = Zone(sources, self.membres[:p1], distances[:p2])
		self.b2 = Zone(sources, self.membres[p1:p2])
		self.b3 = Zone(sources, self.membres[p2:])

	def remoteness(self, block) :
		"""Returns distance of the block from the center"""
		return Block.dist(block, self.sources[self.center])
	
	def candidates(self, block) :
		"""Returns the list of potentials blocks close to ``block``"""
		if self.is_leaf :
			return list(self.membres)
		elif self.remoteness(bloc) < self.r1 :
			return self.b1.candidates(bloc) + self.b2.candidates(bloc)
		elif self.remoteness(bloc) > self.r2 :
			return self.b1.candidates(bloc) + self.b2.candidates(bloc) + self.b3.candidates(bloc)
		else :
			return self.b2.candidates(bloc) + self.b3.candidates(bloc)
	
	def search(self, bloc) :
		i = trivial.search(self.sources, bloc, self.candidates(bloc))
		return self.sources[i]
