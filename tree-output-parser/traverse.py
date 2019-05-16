import json
from pprint import pprint
import Queue

mediaFileFormats = ['md','webm','mkv','flv','flv','vob','ogv','ogg','drc','gif','gifv','mng','avi','MTS','M2TS','mov','qt','wmv','yuv','rm','rmvb','asf','amv','mp4','m4p','m4v','mpg','mp2','mpeg','mpe','mpv','mpg','mpeg','m2v','m4v','svi','3gp','3g2','mxf','roq','nsv','flv','f4v','f4p','f4a','f4b']

def performActionOnFile(entry):
	print("Got file to process !!!")
	print(entry)
	name = entry['name']
	extension = name.split('.')[-1]
	print("Extention is " + extension)
	if extension in mediaFileFormats:
		print("This is a medis !!!")

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


processFile('smallTreeWithAggregations.json')