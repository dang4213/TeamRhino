import requests
import json
import re

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
		res = requests.post('http://127.0.0.1:5000/TeamRhino/add', \
				   json=testjson)

		print res.text

		res = requests.get('http://127.0.0.1:5000/TeamRhino/stopwords')
		print res.text
	except:
		print "API request failed"
