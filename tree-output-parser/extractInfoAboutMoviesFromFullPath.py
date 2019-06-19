import json
import os
from guessit import guessit
import imdb
from imdb import IMDb

LEAST_PROBABLE_MOVIE_SIZE=300*1000*1000
mediaFileFormats = ['webm','mkv','flv','flv','vob','ogv','ogg','drc','gif','gifv','mng','avi','MTS','M2TS','mov','qt','wmv','yuv','rm','rmvb','asf','amv','mp4','m4p','m4v','mpg','mp2','mpeg','mpe','mpv','mpg','mpeg','m2v','m4v','svi','3gp','3g2','mxf','roq','nsv','flv','f4v','f4p','f4a','f4b']
exclusionPaths = ['./DATA/Series/']

def fetchImdb(title):
    print("Searching imdb for title: " + title)
    # Create the object that will be used to access the IMDb's database.
    ia = imdb.IMDb()
    # Search for a movie (get a list of Movie objects).
    s_result = ia.search_movie(title)
    for movie in s_result:
        print(movie.data)
        print(movie.__dict__)

def processFile(fileName):
    with open(fileName) as f:
        for fullFilePath in f.readlines():
            print(fullFilePath);
            gi = guessit(os.path.basename(fullFilePath))
            fetchImdb(gi['title'])

ia = IMDb()
print(ia.get_movie_infoset())

processFile('possibleMovies.txt')
