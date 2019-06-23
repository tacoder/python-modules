# -*- coding: utf-8 -*-

import sys
import json
import os
from guessit import guessit
import imdb
from imdb import IMDb
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import threading
import concurrent.futures
import re
import socket
socket.setdefaulttimeout(5)

LEAST_PROBABLE_MOVIE_SIZE=300*1000*1000
mediaFileFormats = ['webm','mkv','flv','flv','vob','ogv','ogg','drc','gif','gifv','mng','avi','MTS','M2TS','mov','qt','wmv','yuv','rm','rmvb','asf','amv','mp4','m4p','m4v','mpg','mp2','mpeg','mpe','mpv','mpg','mpeg','m2v','m4v','svi','3gp','3g2','mxf','roq','nsv','flv','f4v','f4p','f4a','f4b']
exclusionPaths = ['./DATA/Series/', './laptop backup/Shalini']
undesirableKinds = ['episode', 'video game', 'tv movie', 'short']
desirableKinds = []
cache = {}
results = []    

debug=False

def outputImdbResults(prefix, imdbResultSet):
    print(prefix)
    print(": [")
    for imdbResult in imdbResultSet:
        # if 'title' in imdbResult:
        #     print("'", imdbResult.data['title'], "', ")
        # else:
            print(imdbResult.data)
    print("]")

def normaliseString(string):
    return re.sub('[\W]+',' ', string )

def score(a, b):
    if debug:
        print("normalised ", a , " to ", normaliseString(a))
        print("normalised ", b , " to ", normaliseString(b))
        print("Ratio is: ", fuzz.ratio(normaliseString(a),normaliseString(b)))
    return fuzz.ratio(normaliseString(a),normaliseString(b))
    # return SequenceMatcher(None, b, a).ratio()

def isDesirable(imdbResult):
    # if imdbResult.data['kind'] == 'episode':
    if 'kind' not in imdbResult.data:
        print("kind not avaiable for movie ", imdbResult, " data for the same is: ", imdbResult.data)
        return true # We don't know the kind, so just let it thorough!
    kind = imdbResult.data['kind']
    isDesirable = kind not in undesirableKinds
    if isDesirable:
        if kind not in desirableKinds:
            desirableKinds.append(kind)
    else :
        if debug:
            print("Undesirable kind " , imdbResult ,"data",imdbResult.data)
    return isDesirable

def removeUndesirableResults(imdbResultSet):
    desirables = [x for x in imdbResultSet if isDesirable(x)]
    return desirables

def filterByYear(movieData, imdbResultSet):
    if not 'year' in movieData:
        return imdbResultSet;
    else:
        filteredData = []
        for imdbResult in imdbResultSet:
            if not 'year' in imdbResult:
                continue
            if movieData['year'] == imdbResult.data['year']:
                filteredData.append(imdbResult)
        return filteredData

def filterByNameBestMatch(movieData, imdbResultSet):
    if len(imdbResultSet) is 0:
        return imdbResultSet
    ratedData = imdbResultSet.sort(key=lambda x: score(x.data['title'], movieData['title']),reverse=True);
    highestScore =score(imdbResultSet[0].data['title'], movieData['title'])
    filteredData = []
    for imdbResult in imdbResultSet:
        if(score(imdbResult.data['title'], movieData['title']) == highestScore):
            filteredData.append(imdbResult)
    return filteredData

def ifEpisodeRemoveMovies(movieData, imdbResultSet):
    # print(movieData['type'])
    if movieData['type'] == "episode":
        # print("i am here!")
        # for imdbResult in imdbResultSet:
        #     print(imdbResult)
        #     print(imdbResult.data)
        #     print("kind: ",imdbResult.data['kind'])
        #     print("Tru eof rnoew : ", "movie" not in imdbResult.data['kind'])
        return [x for x in imdbResultSet if "movie" not in x.data['kind'] ]
    else :
        return imdbResultSet

def getBestMatch(movieData, imdbResultSet):
    imdbResultSet = removeUndesirableResults(imdbResultSet);
    if debug:
        outputImdbResults("Afterop:removeUndesirableResults Matches are: ", imdbResultSet)
    imdbResultSet = filterByYear(movieData, imdbResultSet)
    if debug:
        outputImdbResults("Afterop:filterByYear Matches are: ", imdbResultSet)
    imdbResultSet = filterByNameBestMatch(movieData, imdbResultSet)
    if debug:
        outputImdbResults("Afterop:filterByNameBestMatch Matches are: ", imdbResultSet)
    imdbResultSet = ifEpisodeRemoveMovies(movieData, imdbResultSet)
    if debug:
        outputImdbResults("Afterop:ifEpisodeRemoveMovies Matches are: ", imdbResultSet)
    return imdbResultSet

def fetchImdb(guessItOutput):
    title = guessItOutput['title']
    if title in cache:
        print("Serving from cache for title: " + title)
        return cache[title]
    print("Searching imdb for title: " + title)
    # Create the object that will be used to access the IMDb's database.
    ia = imdb.IMDb()
    # Search for a movie (get a list of Movie objects).
    s_result = ia.search_movie(title)
    if debug:
        print("Imdb returned: " , len(s_result) ,  " Results")
        for movie in s_result:
            print(movie)
            print(movie.__dict__)
    filteredResults = getBestMatch(guessItOutput, s_result)
    if debug:
        print("we filtered it to " ,len(filteredResults)," Results")
        print("filteredResults:")
        for result in filteredResults:
            print(result)
            print(result.__dict__)
        if len(filteredResults) is not 1:
            print("UNABLE TO FIND A+ MATCH")
            outputImdbResults("Filtered results", filteredResults)
            print("Filtered Results: ", filteredResults)
            outputImdbResults("imdb resturnde", s_result)
            print("imdb returned: ", s_result)
    result = {}
    result['filteredResults'] = filteredResults
    result['imdbResults'] = s_result
    cache[title] = result
    return result

def doEverything(fullFilePath):
    if debug:
        print(fullFilePath);
    gi = guessit(os.path.basename(fullFilePath))
    if debug:
        print("guessit output ", gi)
    while True:
        try:
            fetchImdbResult = fetchImdb(gi)
        except:
            continue
        break
    result = {}
    result['fullFilePath'] = fullFilePath
    result['imdbResult'] = fetchImdbResult['imdbResults']
    result['finalResult'] = fetchImdbResult['filteredResults']
    result['guessItResult'] = gi
    results.append(result)
    if debug: 
        print(result)

def printFullResult(result):
    print("Result.fullFilePath", result['fullFilePath'])
    print("Result.guessItResult", result['guessItResult'])
    print("Title chosen by guessIt: ", result['guessItResult']['title'])
    print("Result.finalResult (len=", len(result['finalResult']))
    for imdbResult in result['finalResult']:
        print(imdbResult, imdbResult.data)
    # print("Result.imdbResult (len=", len(result['imdbResult']))
    # for imdbResult in result['imdbResult']:
    #     print(imdbResult, imdbResult.data)

def printPartialResult(result):
    print("===================================")
    print("Result.fullFilePath", result['fullFilePath'])
    # print("Result.guessItResult", result['guessItResult'])
    print("Title: ", result['guessItResult']['title'])
    # print("Result.finalResult")
    for imdbResult in result['finalResult']:
        print(imdbResult, imdbResult.data)

def processFile(fileName):
    threads = []
    lines = []
    with open(fileName) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(doEverything, lines)
        executor.shutdown(wait=True)
    print("================+FETCHIGNB DBES!!============")
    successResults = []
    for result in results:
        if len(result['finalResult']) == 1:
            successResults.append(result)
        else:
            print("Failed to find movie for: ")
            printFullResult(result)
    print("================================================")
    print("================================================")
    print("================================================")
    for successResult in successResults:
        print("Successfully found resiult for: ")
        printPartialResult(successResult)
    print("================================================")
    print("SUmmary: ")
    print("Found results for : ", len(successResults), "titles. ")
    print("Failed to find results for : ", len(results) - len(successResults), "titles. ")
    print("Desirable kinds foinr : ", desirableKinds)

ia = IMDb()
print(ia.get_movie_infoset())

processFile('data/possibleMovies.txt')

# debug=True
# fileName="./torrents/completed/Fargo.Season.2.720p.BluRay.x264.ShAaNiG/Fargo.S02E08.720p.BluRay.x264.ShAaNiG.mkv"
# fileName= "./DATA/Movies/new ones/Crazy.Stupid.Love.2011.720p.BrRip.x264.YIFY.mp4"
# fileName="./DATA/Movies/English/Watched Normal Resolution/Crash [Eng] [2005].avi"
./DATA/Movies/Movies/12 Angry Men.avi
./DATA/Movies/Movies/Due Date.avi #can remove video moviue
./DATA/Movies/Movies/Collateral.mkv
./DATA/Movies/Movies/The Aviator (2004).mkv
./DATA/Movies/new ones/16.wishes.2010.hdtv.xvid-momentum.avi
./New folder (2)/movies/Fatal Attraction [1987] [IMDB_6.8]/FatalAttraction_DVDRip.avi
# doEverything(fileName)
# debug=True
