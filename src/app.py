from flask import Flask, jsonify, request, abort
from InvertedIndex_class import InvertedIndex
import time

app = Flask(__name__)

tokenIndex = InvertedIndex()

@app.route("/TeamRhino/add", methods=['GET', 'POST'])
def add_tokens():
	t = time.time()
	if not request.json:
		abort(400)
	return tokenIndex.addMetadata(request.json, t)

@app.route("/TeamRhino/stopwords", methods=['GET'])
def get_stopwords():
	# return tokenIndex.getStopwords()
	return jsonify(["the", "of", "to", "a", "and", "in", "said", "for", "that", "was",
			"on", "he", "is", "with", "at", "by", "it", "from", "as", "be",
			"were", "an", "have", "his", "but", "has", "are", "not", "who",
			"they"])

@app.route("/TeamRhino/tokens", methods=['GET', 'POST'])
def get_token_metadata():
	return tokenIndex.searchToken(request.json)

@app.route("/TeamRhino")
def homepage():
	return "Welcome to team Rhino's Indexing page"

if __name__ =='__main__':
	app.run(debug=True)
	# app.run(debug=True, host="0.0.0.0")
