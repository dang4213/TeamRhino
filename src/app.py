from flask import Flask, jsonify, request, abort
from InvertedIndex_class import InvertedIndex

app = Flask(__name__)

tokenIndex = InvertedIndex()

@app.route("/TeamRhino/add", methods=['GET', 'POST'])
def add_ngrams():
	if not request.json:
		abort(400)
	tokenIndex.addMetadata(request.json)
	return "Add successful!"


@app.route("/TeamRhino/stopwords", methods=['GET'])
def get_stopwords():
	return "List of stopwords"

@app.route("/TeamRhino/tokens", methods=['GET', 'POST'])
def get_token_metadata():
	return "Documents associated with searched tokens"

@app.route("/TeamRhino")
def homepage():
	return "Welcome to team Rhino's Indexing page"

if __name__ =='__main__':
	app.run(debug=True, host="0.0.0.0")

