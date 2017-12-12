import requests
import json

test_metadata1 = {
    'documentMetadata': {
        'documentID': 'testfile',
        'wordCount': 50
    },
    'tokens': [
        {
            'token': 'hello',
            'ngramSize': 5,
            'locations': [1, 2, 3, 4]
        },
        {
            'token': 'world',
            'ngramSize': 5,
            'locations': [5, 6, 7, 8]
        },
        {
            'token': 'what a day',
            'ngramSize': 11,
            'locations': [9, 10, 11, 12]
        },
    ]
}

test_metadata2 = {
    'documentMetadata': {
        'documentID': 'testfile',
        'wordCount': 50
    },
    'tokens': [
        {
            'token': 'yeah',
            'ngramSize': 5,
            'locations': [1, 2, 3, 4]
        },
        {
            'token': 'okay',
            'ngramSize': 5,
            'locations': [5, 6, 7, 8]
        },
        {
            'token': "it's snowing",
            'ngramSize': 11,
            'locations': [9, 10, 11, 12]
        },
        {
            'token': 'hello',
            'ngramSize': 5,
            'locations': [1, 2, 3, 4, 15]
        },
    ]
}

test_search1 = {'tokens': ['hello', 'yeah', 'world']}


res = requests.post('http://127.0.0.1:5000/TeamRhino/add',
                    json=test_metadata1)
print res.text

print 'response from server:', res.text

res = requests.post('http://127.0.0.1:5000/TeamRhino/add',
                    json=test_metadata2)

print 'response from server:', res.text

res = requests.get('http://127.0.0.1:5000/TeamRhino/stopwords')

print 'response from server:', res.text

res = requests.post('http://127.0.0.1:5000/TeamRhino/tokens',
                    json=test_search1)

print 'response from server:', res.text
