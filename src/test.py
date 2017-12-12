import requests
import json
import re
from os import listdir
from os.path import isfile, join

def cleanDocument(contents):
	contents = re.sub('<script.+</script>', ' ', contents)
	contents = re.sub('<[^<>]+>', ' ', contents)
	contents = re.sub('&.+;', ' ', contents)
	contents = re.sub("\d+", ' ', contents)
	contents = re.sub("(,|\.|:|;|!|\(|\)|\?)", '', contents)
	contents = re.sub("(--|-)", ' ', contents).split()
	return contents

def createTestJSON(words, filename):
	word_locations = {}
	for index, word in enumerate(words):
		if word in word_locations:
			word_locations[word].append(index)
		else:
			word_locations[word] = [index]

	testjson = {
		'documentMetadata': {
			'documentID': filename,
			'wordCount': len(word_locations)
		},
		'tokens': [{'token': token, 'ngramSize': len(token),
					'locations': word_locations[token]} for token in word_locations.keys()]}
	return testjson


files = [file for file in listdir("./testfiles") if isfile(join("./testfiles", file))]

for filename in files:
	with open("./testfiles/" + files[0]) as file:
		contents = file.read().replace('\n', ' ')

	contents = cleanDocument(contents)
	words = [word for word in contents
	         if re.search('[a-zA-z]', word)]

	testjson = createTestJSON(words, files[0])

	try:
		print "hello"
		res = requests.post('http://127.0.0.1:5000/TeamRhino/add', \
				   json=testjson)
		print "yup"
	except:
		print "API request failed"

	print res



# test_metadata1 = {
# 	'documentMetadata': {
# 		'documentID': 'testfile',
# 		'wordCount': 50,
# 	},
# 	'tokens': [
# 		{
# 			'token': 'hello',
# 			'ngramSize': 5,
# 			'locations': [1,2,3,4]
# 		},
# 		{
# 			'token': 'world',
# 			'ngramSize': 5,
# 			'locations': [5,6,7,8]
# 		},
# 		{
# 			'token': 'what a day',
# 			'ngramSize': 11,
# 			'locations': [9,10,11,12]
# 		},
# 	]
# }

# test_metadata2 = {
# 	'documentMetadata': {
# 		'documentID': 'testfile',
# 		'wordCount': 50,
# 	},
# 	'tokens': [
# 		{
# 			'token': 'yeah',
# 			'ngramSize': 5,
# 			'locations': [1,2,3,4]
# 		},
# 		{
# 			'token': 'okay',
# 			'ngramSize': 5,
# 			'locations': [5,6,7,8]
# 		},
# 		{
# 			'token': "it's snowing",
# 			'ngramSize': 11,
# 			'locations': [9,10,11,12]
# 		},
# 		{
# 			'token': 'hello',
# 			'ngramSize': 5,
# 			'locations': [1,2,3,4,15]
# 		},
# 	]
# }

# test_search1 = {'tokens': ['hello', 'yeah', 'world']}

# # Test for rpi server
# # res = requests.post('http://teamrhino.cs.rpi.edu:5000/TeamRhino/add', \
# # 				   json=test_metadata)

# res = requests.post('http://127.0.0.1:5000/TeamRhino/add',\
# 					json = test_metadata1)

# print 'response from server:', res.text

# res = requests.post('http://127.0.0.1:5000/TeamRhino/add',\
# 					json = test_metadata2)

# print 'response from server:', res.text

# res = requests.get('http://127.0.0.1:5000/TeamRhino/stopwords')

# print 'response from server:', res.text

# res = requests.post('http://127.0.0.1:5000/TeamRhino/tokens',\
# 					json = test_search1)

# print 'response from server:', res.text
