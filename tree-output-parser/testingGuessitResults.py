import json

from guessit import guessit


def searchMovies(movies):
    for movie in movies:
        fullpath = movie['fullpath']
        gi = guessit(fullpath)
        print "===================="
        print "filepath:",fullpath.encode('utf-8')
        print "Guessed name:", gi['title'].encode('utf-8')

def traverse(data):
    searchMovies(data["movies"])


def processFile(fileName):
    with open(fileName) as f:
        data = json.load(f)
        traverse(data)

processFile('data/movies-data-grouped.json')
