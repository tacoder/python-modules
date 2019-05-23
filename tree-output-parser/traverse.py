import json

LEAST_PROBABLE_MOVIE_SIZE=300*1000*1000
mediaFileFormats = ['webm','mkv','flv','flv','vob','ogv','ogg','drc','gif','gifv','mng','avi','MTS','M2TS','mov','qt','wmv','yuv','rm','rmvb','asf','amv','mp4','m4p','m4v','mpg','mp2','mpeg','mpe','mpv','mpg','mpeg','m2v','m4v','svi','3gp','3g2','mxf','roq','nsv','flv','f4v','f4p','f4a','f4b']
exclusionPaths = ['./DATA/Series/']

def isExcluded(fullPath):
	for path in exclusionPaths:
		if path in fullPath:
			return True
		else:
			return False

def isMedia(filename):
	extension = filename.split('.')[-1]
	return extension in mediaFileFormats


def performActionOnFile(entry):
	#print("Got file to process !!!")
	#print(entry)
	fullPath = entry['name']
	size = entry['size']
	#print("Extention is " + extension)
	if isMedia(fullPath) and not isExcluded(fullPath) and size > LEAST_PROBABLE_MOVIE_SIZE:
		print(fullPath.encode("utf-8"))

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


processFile('HDDJsonTreeWithAggregationSize.json')