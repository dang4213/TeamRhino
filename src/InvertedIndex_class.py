from sets import Set
import json

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
		self.stopwords = {}
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
		if not self.verifyJSON(document):
			return "Incorrect submission format"
		# return document['documentMetadata']['documentID']

		for tokeninfo in document['tokens']:
			if tokeninfo['token'] in self.indexstore:
				self.updateIndex(tokeninfo['token'], document)
			else:
				self.indexstore[tokeninfo['token']] = \
				self.createStore(document['documentMetadata'], \
								 len(tokeninfo['locations'])
								)

		# t = json.dumps([store['token'] for store in document['tokens']])
		# return "Add Successful \n %s" %(''.join(t))
		return "Add Successful"

	"""
	createStore

	params:
		- metadata: info about the document in which a token was found 
	"""
	def createStore(self, metadata, numOccurences):
		return [numOccurences, metadata]

	"""
	updateIndex

	params:
		- token: string
		- metadata: metadata to update a token 
	"""
	def updateIndex(self, token, metadata):
		if metadata['documentID'] in self.indexstore[token]:

		return None

	"""
	getStopwords

	- returns a json list of the 50 most frequently occuring words
	"""
	def getStopwords(self):
		
		return None

	def verifyJSON(self, document):
		if not 'documentMetadata' in document:
			return False
		if not 'tokens' in document:
			return False
		return True


# index = InvertedIndex()
# index.addMetadata({'documentID': '1'})

