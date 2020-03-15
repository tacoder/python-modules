#!/bin/python
import json

with open("finalResult5.json", 'r') as f:
    moviesJson = json.load(f)

# moviesJson = json.loads("finalResult5.json")

def notSoGoodMovie(movieData):
	if movieData['genres'] and  'Comedy' in movieData['genres'] and 'Romance' not in movieData['genres']:
		if movieData['rating'] is not None  and movieData['rating'] < 3:
			return True
	else:
		if movieData['rating'] is not None  and movieData['rating'] < 7:
			return True;
	return False

for movie in moviesJson:
	if len(movie['finalResult']) == 0:
		print "No data for file: " , movie['fullFilePath']
		continue
	movieData = movie['finalResult'][0]
	if notSoGoodMovie(movieData):
		print "You can delete: " , movie['fullFilePath']
	else :
		print "You cannot delete this mf!", movie['fullFilePath']
