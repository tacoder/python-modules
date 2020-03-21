import json
from pprint import pprint
import Queue
from guessit import guessit

#LEAST_PROBABLE_MOVIE_SIZE=300*1000*1000

# Algorithm Calibration
LEAST_PROBABLE_MOVIE_SIZE=135184583

mediaFileFormats = ['webm','mkv','flv','flv','vob','ogv','ogg','drc','gif','gifv','mng','avi','MTS','M2TS','mov','qt','wmv','yuv','rm','rmvb','asf','amv','mp4','m4p','m4v','mpg','mp2','mpeg','mpe','mpv','mpg','mpeg','m2v','m4v','svi','3gp','3g2','mxf','roq','nsv','flv','f4v','f4p','f4a','f4b','divx','ogm','DAT','VOB']

exclusionPaths = ['./DATA/Series/']

result = {"movies":[],"smallmovies":[],"others":[]}

def isExcluded(fullPath):
	for path in exclusionPaths:
		if path in fullPath:
			return True
		else:
			return False

def isMedia(filename):
	extension = filename.split('.')[-1]
        return extension.upper() in (formats.upper() for formats in mediaFileFormats)
	#return extension in mediaFileFormats


def performActionOnFile(entry):
	#print("Got file to process !!!")
	#print(entry)
	fullPath = entry['name']
	size = entry['size']
        time = entry['time']
	#print("Extention is " + extension)
        if isMedia(fullPath) and not isExcluded(fullPath):
            if size > LEAST_PROBABLE_MOVIE_SIZE:
                result["movies"].append( {"size":size,"fullpath":fullPath, "time":time})
            else:
                result["smallmovies"].append( {"size":size,"fullpath":fullPath, "time":time})
        else:
            result["others"].append( {"size":size,"fullpath":fullPath, "time":time})

def traverse(data):
    q = Queue.Queue()
    q.put(data)
    while not q.empty():
        folder = q.get()
        for entry in folder:
            # print("Entry!")
            # print(entry)
            # print(entry['type'])
            type = entry['type']
            if type == 'directory':
            	q.put(entry['contents'])
            elif type == 'file':
            	performActionOnFile(entry)

def processFile(fileName):
	with open(fileName) as f:
	    data = json.load(f)
	    traverse(data)
            summarize()
            order()

def order():
    result["others"].sort(key=lambda x: x["size"], reverse=True)
    result["movies"].sort(key=lambda x: x["size"], reverse=True)
    result["smallmovies"].sort(key=lambda x: x["size"], reverse=True)

def summarize():
    result["summary"]={}
    nmovies = 0
    moviesize = 0
    for movie in result["movies"]:
        nmovies += 1;
        moviesize += movie["size"]
    result["summary"]["movies"] = {}
    result["summary"]["movies"]["count"]=nmovies
    result["summary"]["movies"]["size"]=moviesize

    nothers = 0
    othersize = 0
    for others in result["others"]:
        nothers += 1
        othersize += others["size"]
    result["summary"]["others"] = {}
    result["summary"]["others"]["count"]=nothers
    result["summary"]["others"]["size"]=othersize

    nsmovies = 0
    smallmoviessize = 0
    for movie in result["smallmovies"]:
         nsmovies += 1;
         smallmoviessize += movie["size"]
    result["summary"]["smallmovies"] = {}
    result["summary"]["smallmovies"]["count"]=nsmovies
    result["summary"]["smallmovies"]["size"]=smallmoviessize


processFile('data/Movies-tree.json')
print(json.dumps(result));

