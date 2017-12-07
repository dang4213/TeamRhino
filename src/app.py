from flask import Flask, jsonify, request, abort

app = Flask(__name__)


tokenIndex = {}

@app.route("/add", methods=['GET', 'POST'])
def add_ngrams():
	if not request.json:
		abort(400)
	for token in request.json['tokens']:
		if tokenIndex[token]:
			tokenIndex[token].append(request.json['documentMetadata']['documentID'])
		else:
			tokenIndex[token] = [request.json['documentMetadata']['documentID']]
	return "Add successful!"


@app.route("/")
def homepage():
	return "Welcome to team Rhino's Indexing page"

if __name__ =='__main__':
	app.run(debug=True, host="0.0.0.0")
	# app.run(host="0.0.0.0")

