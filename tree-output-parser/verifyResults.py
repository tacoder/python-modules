import json
from pprint import pprint
import Queue
from guessit import guessit
from fuzzywuzzy import fuzz
import re

scount = 0
fcount = 0

def describeMovie(movie):
    print "MovieFullpath",movie["movie"]["fullpath"]
    print "MovieExtractedName", movie["nameMatched"]
    print "MatchesCount",len(movie["finalResult"])
    i = 0
    for result in movie["finalResult"]:
        i+=1
        print "  Result#",i
        print "    imdb Name:",result["title"]
        print "    imdb kind:", result["kind"]
        print "    imdb year:", result["year"]
        print "    imdb rating:", result["rating"]
        print "    imdb id",result["id"]
    print "==============================="
    print ""

def normaliseString(string):
    return re.sub('[\W]+',' ', string )

def score(a, b):
     return fuzz.WRatio(normaliseString(a),normaliseString(b))

def verifyCorrectMatch(movie):
    return 100
    matchScore = score(movie['nameMatched'], movie['finalResult'][0]["title"])
    if matchScore < 80:
            print "Possible non-match (based on file name!, score=",matchScore,")", describeMovie(movie)
            return False;
    else:
        return True;

def traverse(data):
    global scount
    global fcount
    for movie in data:
        matchedMoviesCount = len(movie["finalResult"])
        if matchedMoviesCount == 0:
            print "No Movie found for movie", describeMovie(movie)
            fcount +=1
        if matchedMoviesCount > 1:
            print "More than one movies found for movie", describeMovie(movie)
            fcount +=1
        if matchedMoviesCount == 1:
            if verifyCorrectMatch(movie):
                scount +=1
            else:
                fcount +=1

def processFile(fileName):
	with open(fileName) as f:
	    data = json.load(f)
	    traverse(data)

processFile('data/movies-imdb-data-filtered.json')

print "Deemed Accuracy: ",((scount*100)/(scount+fcount))," (",scount,"/",(scount+fcount),")"

