import json
import os
from pprint import pprint
import Queue
from guessit import guessit

LEAST_PROBABLE_MOVIE_SIZE=300*1000*1000
mediaFileFormats = ['webm','mkv','flv','flv','vob','ogv','ogg','drc','gif','gifv','mng','avi','MTS','M2TS','mov','qt','wmv','yuv','rm','rmvb','asf','amv','mp4','m4p','m4v','mpg','mp2','mpeg','mpe','mpv','mpg','mpeg','m2v','m4v','svi','3gp','3g2','mxf','roq','nsv','flv','f4v','f4p','f4a','f4b']
exclusionPaths = ['./DATA/Series/']

def processFile(fileName):
    with open(fileName) as f:
        for fullFilePath in f.readlines():
            print("begin")
            print(fullFilePath)
            print("end")
            print(guessit(os.path.basename(fullFilePath))['title'])

processFile('possibleMovies.txt')