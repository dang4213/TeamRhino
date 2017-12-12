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
        self.documentMetadataStore = {}
        self.documentTokenStore = {}

    """
    addMetadata

    params:
        - document: parsed json object in the format:
          (borrowed from Team Y's specs)
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
                    {
                        token: string,
                        ngramSize: int,
                        locations: [int]
                    }
                ]
            }

    - adds a document and associated metadata to an invertedindex

    return: none
    """
    def addMetadata(self, document, timestamp):
        if not self.verifyJSON(document):
            return "Incorrect submission format"

        self.handleDocument(document['documentMetadata'],
                            str(document['documentMetadata']['documentID']),
                            timestamp)

        self.handleTokens(document['tokens'],
                          str(document['documentMetadata']['documentID']))

        self.checkDeletions({token['token'] for token in document['tokens']},
                            str(document['documentMetadata']['documentID']))

        return "Add Successful | indexed the following tokens:\
                \n%s" % (' \n'.join([t['token'] for t in document['tokens']]))

    """
    handleDocument

    params:
        - metadata: json:
        - timestamp: float

    - adds/updates a document to an index
    """
    def handleDocument(self, metadata, docid, timestamp):
        metadata['pageLastIndexed'] = timestamp
        self.documentMetadataStore[docid] = metadata

    """
    handleTokens

    params:
        - tokens, list of strings
        - docid, string

    - iterates over tokens and adds/updates tokens to an index
    - if a token is already associated to a docid,
      then the token is updated
    """
    def handleTokens(self, tokens, docid):
        for info in tokens:
            if info['token'] in self.indexstore:
                self.updateToken(info['token'], info['locations'], docid)
            else:
                self.indexstore[info['token']] = \
                    self.createStore(info['locations'], docid)


   

    """
    checkDeletions

    params:
        - tokens: set of strings
        - docid: string

    - iterates over the current self.documentTokenStore and compares vs
      tokens
    - any non present tokens are updated (docid removed)

    return: none
    """
    def checkDeletions(self, tokens, docid):
        if docid not in self.documentTokenStore:
            self.documentTokenStore[docid] = tokens

        else:
            for token in self.documentTokenStore[docid]:
                if token not in tokens:
                    print token
                    del self.indexstore[token][1][docid]
                    if len(self.indexstore[token][1]) == 0:
                        del self.indexstore[token]
            self.documentTokenStore[docid] = tokens

    """
    createStore

    params:
        - metadata: info about the document in which a token was found

    return: list of word occurences and the first document metadata
            associated
    """
    def createStore(self, occurences, docid):
        return [len(occurences), {str(docid): occurences}]

    """
    updateIndex

    params:
        - token: string
        - metadata: metadata to update a token

    - updates the overall count and associated document IDs for a token
    """
    def updateToken(self, token, occurences, docid):
        if docid in self.indexstore[token][1]:
            self.updateStore(token, occurences, docid)
        else:
            self.indexstore[token][1][str(docid)] = occurences
            self.indexstore[token][0] += len(occurences)
        return None

    """
    updateStore

    params:
        - token: string
        - occurences: list of ints
        - docid: string

    - removes the previous doc_count from a token's overall count
    - adds the updated doc_count
    """
    def updateStore(self, token, occurences, docid):
        self.indexstore[token][0] -= len(self.indexstore[token][1][docid])
        self.indexstore[token][0] += len(occurences)
        self.indexstore[token][1][docid] = occurences
        return None
    """
    getStopwords

    - returns a json list of the 50 (or all words)
      most frequently occuring words

    return: json list
    """
    def getStopwords(self):
        stopwords = sorted(self.indexstore.iteritems(),
                           key=lambda(key, value): value[0], reverse=True)
        return json.dumps([token[0] for token in stopwords[:50]])

    """
    searchToken

    - returns a json object in the format (borrowed from Team Y's specs):
        {
          returnCode: int,
          error: string,
          documents: [
            {
              documentID: string,
              wordCount: int,
              pageLastIndexed: datetime,
              importantTokenRanges: [
                {
                  fieldName: string,
                  rangeStart: int,
                  rangeEnd: int
                }
              ]
            }
          ],
          tokens: [
            {
                token: string,
                ngramSize: int,
                documentOccurences: [
                  {
                    documentID: string,
                    locations: [int]
                  }
                ]
            }
          ]
        }

    - json object has
        - `tokens`: a list of tokens and associated document stats
        - returnCode: int, indicated the status of retrieval
        - error: description of error if present
        - documents: metadata concerning documents associated for the
                     returned tokens

    """
    def searchToken(self, tokens):
        search = {'returnCode': 0, 'error': "", 'documents': [], 'tokens': []}

        docs = set()

        for token in tokens['tokens']:
            docinfo = self.findDocs(token)
            if docinfo:
                indexinfo = {'token': token, 'ngramSize': len(token),
                             'documentOccurences': docinfo}
                search['tokens'].append(indexinfo)
                for document in docinfo:
                    docs.add(document.keys()[0])

        for doc in docs:
            search['documents'].append(self.documentMetadataStore[doc])
        return json.dumps(search)

    """
    verifyJSON

    params:
        - document: json object

    - confirms that the POSTed json contains documentMetadata and tokens

    return: boolean, True if valid json else False
    """
    def verifyJSON(self, document):
        if 'documentMetadata' not in document:
            return False
        if 'tokens' not in document:
            return False
        return True

    """
    findDocs

    params:
        - token: string

    - finds the associated documents for a given token

    return: list of dict of documentID and token locations
    """
    def findDocs(self, token):
        if token not in self.indexstore:
            return False
        ret = []
        for doc in self.indexstore[token][1:]:
            ret.append(doc)
        return ret
