import requests
import json
import re
from os import listdir
from os.path import isfile, join

"""
cleanDocument

- params:
    - contents: string of file contents

- removes any script tags, html tags, special chars, and punctuation

return: list of strings
"""
def cleanDocument(contents):

    contents = re.sub('<script.+</script>', ' ', contents)
    contents = re.sub('<[^<>]+>', ' ', contents)
    contents = re.sub('&.+;', ' ', contents)
    contents = re.sub("\d+", ' ', contents)
    contents = re.sub("(,|\.|:|;|!|\(|\)|\?)", '', contents)
    contents = re.sub("(--|-)", ' ', contents).split()
    return contents

"""
getLocations

- params:
    - words: list of strings

- iterates over an enumerated list of strings, adding the current index
  to a hashmap noting the various indexes of each string

return: hashmap
"""
def getLocations(words):

    word_locations = {}
    for index, word in enumerate(words):
        if word in word_locations:
            word_locations[word].append(index)
        else:
            word_locations[word] = [index]
    return word_locations

"""
createTestJSON

- params:
    - words: list of strings
    - filename: string

- create a JSON object with the given file name
- sets the locations of each string to their found indexes

return: JSON object
"""
def createTestJSON(words, filename):

    locations = getLocations(words)

    testjson = {
        'documentMetadata': {
            'documentID': filename,
            'wordCount': len(locations)
        },
        'tokens': [{'token': token, 'ngramSize': len(token),
                    'locations': locations[token]}
                   for token in locations.keys()]}
    return testjson

"""
testAPI

- params: none

- browses the testfiles directory for all files
- creates a JSON object for each file
- sends the JSON to our add api and then requests
  the first ten unique words and the stopwords

return: none
"""
def testAPI():
    files = [file for file in listdir("./testfiles")
             if isfile(join("./testfiles", file))]

    for filename in files:
        with open("./testfiles/" + files[0]) as file:
            contents = file.read().replace('\n', ' ')

        contents = cleanDocument(contents)
        words = [word for word in contents if re.search('[a-zA-z]', word)]

        testjson = createTestJSON(words, files[0])

        try:
            res = requests.post('http://127.0.0.1:5000/TeamRhino/add',
                                json=testjson)
            print res.text

            testjson = {'tokens': [word for word in words[:10]]}
            res = requests.get('http://127.0.0.1:5000/TeamRhino/tokens',
                               json=testjson)
            print res.text

            res = requests.get('http://127.0.0.1:5000/TeamRhino/stopwords')
            print res.text
        except:
            print "API request failed"

testAPI()
