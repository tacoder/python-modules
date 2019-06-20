import json
import os
from guessit import guessit
import imdb
from imdb import IMDb
from difflib import SequenceMatcher

LEAST_PROBABLE_MOVIE_SIZE=300*1000*1000
mediaFileFormats = ['webm','mkv','flv','flv','vob','ogv','ogg','drc','gif','gifv','mng','avi','MTS','M2TS','mov','qt','wmv','yuv','rm','rmvb','asf','amv','mp4','m4p','m4v','mpg','mp2','mpeg','mpe','mpv','mpg','mpeg','m2v','m4v','svi','3gp','3g2','mxf','roq','nsv','flv','f4v','f4p','f4a','f4b']
exclusionPaths = ['./DATA/Series/']

def score(a, b):
    return SequenceMatcher(None, a, b).ratio()

def filterByYear(movieData, imdbResultSet):
    if not 'year' in movieData:
        return imdbResultSet;
    else:
        filteredData = []
        for imdbResult in imdbResultSet:
            if movieData['year'] == imdbResult.data['year']:
                filteredData.append(imdbResult)
        return filteredData

def filterByNameBestMatch(movieData, imdbResultSet):
    if len(imdbResultSet) is 0:
        return imdbResultSet
    ratedData = imdbResultSet.sort(key=lambda x: score(x.data['title'], movieData['title']),reverse=True);
    highestRating =score(imdbResultSet[0].data['title'], movieData['title'])
    filteredData = []
    for imdbResult in imdbResultSet:
        if(score(imdbResult.data['title'], movieData['title'])):
            filteredData.append(imdbResult)
    return filteredData

def getBestMatch(movieData, imdbResultSet):
    imdbResultSet = filterByYear(movieData, imdbResultSet)
    imdbResultSet = filterByNameBestMatch(movieData, imdbResultSet)
    return imdbResultSet

def fetchImdb(guessItOutput):
    title = guessItOutput['title']
    print("Searching imdb for title: " + title)
    # Create the object that will be used to access the IMDb's database.
    ia = imdb.IMDb()
    # Search for a movie (get a list of Movie objects).
    s_result = ia.search_movie(title)
    print("Imdb output")
    for movie in s_result:
        print(movie)
        #print movie.__dict__
    filteredResults = getBestMatch(guessItOutput, s_result)
    print "filteredResults:"
    for result in filteredResults:
        print result
        print result.__dict__
    if len(filteredResults) > 1:
        print "UNABLE TO FIND A MATCH"


def processFile(fileName):
    with open(fileName) as f:
        for fullFilePath in f.readlines():
            print(fullFilePath);
            gi = guessit(os.path.basename(fullFilePath))
            #print "guessit output ", gi
            fetchImdb(gi)

ia = IMDb()
print(ia.get_movie_infoset())

processFile('data/possibleMovies.txt')