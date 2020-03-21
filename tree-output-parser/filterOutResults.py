import json
from dateutil import parser

# Entry of type:
#
def hasRating(movie):
    return "rating" in movie and movie["rating"] is not None


def isOlderThanFile(movieResult, entry):
    # try:
    fileDate = parser.parse(entry['time'])
    resultDate = parser.parse((str(movieResult['year'])))
    isOlder = resultDate < fileDate
    # if isOlder:
    #     print(resultDate)
    #     print(fileDate)
    #     print("Too old!")
    return isOlder
    # except Exception:
    #     raise Exception
    #     # print("Soething went wrong")
    #     return True


def doesNotContainTVinTitle(movieResult):
    return not "(TV)" in movieResult['title']


def validMovieResult(movieResult, entry):
    return  hasRating(movieResult) and isOlderThanFile(movieResult, entry) and doesNotContainTVinTitle(movieResult)
        # return movieResult

def filteroutInvalidResults(finalResults, entry):
    filteredMovies = [movie for movie in finalResults if validMovieResult(movie, entry)]
    if len (filteredMovies) == 0:
        return finalResults
    else :
        return filteredMovies

def filterMovies(movieEntry):
    movieEntry["finalResult"] = filteroutInvalidResults(movieEntry["finalResult"], movieEntry['movie'])
    return movieEntry
    
def filterOut(data):
    return [filterMovies(x) for x in data]

def processFile(fileName):
    with open(fileName) as f:
        data = json.load(f)
        fileredOutData = filterOut(data)
        print(json.dumps(fileredOutData))

processFile('data/movies-imdb-data.json')
