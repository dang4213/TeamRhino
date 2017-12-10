from sets import Set

"""
class InvertedIndex

params:
	- object

usage: index = InvertedIndex()

- creates an InvertedIndex with string tokens as keys and
  documentMetadata as values
- tokens are mapped to a set of metadata objects

"""
class InvertedIndex:

	def __init__(self):
		self.indexstore = {}

	"""
	addMetadata

	params:
		- document: parsed json object in the format:
			{
				documentMetadata: {
					documentID: string,
					wordCount: int,
					importantTokenRanges: [
						{
							fieldName: string,
							rangeStart: int,
							rangeEnd: int
						}
					]
				}
				tokens: [
					token: string,
					ngramSize: int,
					locations: [int]
				]
			}

	- adds a document and associated metadata to an invertedindex

	return: none
	"""
	def addMetadata(self, document):
		print "Hello!"
		for tokeninfo in document['tokens']:
			if tokeninfo['token'] in self.indexstore:
				self.updateIndex(tokeninfo['token'], document)
			else:
				self.updateIndex[tokeninfo['token']] = \
				self.createStore(document['documentMetadata'])

	"""
	createStore

	params:
		- metadata: info about the document in which a token was found 
	"""
	def createStore(self, metadata):
		return None

	"""
	updateIndex

	params:
		- token: string
		- metadata: metadata to update a token 
	"""
	def updateIndex(self, token, metadata):
		return None


# index = InvertedIndex()
# index.addMetadata({'documentID': '1'})

