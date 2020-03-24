#!/bin/python
import json

from pip._vendor.distlib.compat import raw_input

def printMovie(movie):
	print(movie['movie']['fullpath'])
	print("size in MB:", movie['movie']['size']/1000000)

def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply == '' or reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")


def toArray(moviesToKeepInput):
	return [int(i) for i in moviesToKeepInput.split(",")]


def validate(moviesToKeepIndexesArray, maxlen):
	for integer in moviesToKeepIndexesArray:
		if(integer <= 0 or integer>maxlen):
			return False
	return True


def detectDuplicatesAndMoveToDelete(finaldata):
	idToMovieMap = {}
	for movie in finaldata['keep']:
		id = movie['finalResult'][0]['id']
		if id not in idToMovieMap:
			idToMovieMap[id] = []
		idToMovieMap[id].append(movie);
	stillKeep = []
	delete = []
	progress = 0
	for id in idToMovieMap:
		progress += 1
		print "progress:(",progress,"/",len(idToMovieMap.keys()),")"
		movies = idToMovieMap[id]
		index = 0
		if(len(movies) == 1):
			stillKeep.append(movies[0])
			continue
		print("==========================")
		for movie in movies:
			index += 1
			print ("Movie#", index)
			printMovie(movie)
		largest = None
		largestSizeSoFar = 0
		index = 0
		for movie in movies:
			index += 1
			size = movie['movie']['size']
			if largestSizeSoFar < size:
				largestSizeSoFar = size
				largest = index
		print("Suggest - ", largest)
		moviesToKeepIndexesArray = [-1]
		while not validate(moviesToKeepIndexesArray, len(movies)):
			try:
				doConfirm = True
				moviesToKeepInput = raw_input("Which movies shall i keep, master? (0=all, -1=none) >")
				if moviesToKeepInput == '':
					moviesToKeepInput = str(largest)
					doConfirm = False
				moviesToKeepIndexesArray = toArray(moviesToKeepInput)
				if len(moviesToKeepIndexesArray) == 1:
					if moviesToKeepIndexesArray[0] == 0:
						moviesToKeepIndexesArray = range(1,len(movies)+1)
						break
					if(moviesToKeepIndexesArray[0] == -1):
						if yes_or_no("Delete all ?"):
							moviesToKeepIndexesArray = []
							break
						else:
							raise Exception
				if doConfirm:
					print "You have chosen : ", moviesToKeepIndexesArray
					if not yes_or_no("Please confirm!"):
						raise Exception
			except Exception:
				continue
		index = 0
		keptMovieNames = []
		deletedMovieNames = []
		for movie in movies:
			index+=1
			if index in moviesToKeepIndexesArray:
				keptMovieNames.append(movies[index-1]['nameMatched'])
				stillKeep.append(movies[index-1])
			else:
				deletedMovieNames.append(index)
				delete.append(movies[index-1])
		print('keps:' ,moviesToKeepIndexesArray)
		print('del-',deletedMovieNames)

	# moviesFound = {}
	# stillKeep = []
	# delete = []
	#
	#
	# for movie in finaldata['keep']:
	# 	print("Total:", len(moviesFound.keys()), ", keep:", len(stillKeep), ", delete:", len(delete), " undecided:", len(finaldata['undecided']))
	# 	id_ = movie['finalResult'][0]['id']
	# 	if id_ in moviesFound:
	# 		print("=================")
	# 		print("=================")
	# 		print("Duplicate found - ",id_)
	# 		printMovie(movie)
	# 		print("Original - ")
	# 		printMovie(moviesFound[id_])
	# 		if(yes_or_no("Does this look like a possible duplicate?")):
	# 			print("Removing!")
	# 			delete.append(movie)
	# 		else:
	# 			print("Not removing")
	# 			moviesFound[id_] = movie
	# 			stillKeep.append(movie)
	# 	else:
	# 		moviesFound[id_] = movie
	# 		stillKeep.append(movie)
	finaldata['keep'] = stillKeep
	finaldata['duplicate'] = delete

with open("data/imdb-final-final-date.json", 'r') as f:
    finaldata = json.load(f)

detectDuplicatesAndMoveToDelete(finaldata)






# detectDuplicatesAndMoveToDelete(finaldata)
f = open("data/imdb-final-final-deduplicated-date.json", "w")
f.write(json.dumps(finaldata))
f.close()

print("Summary!!!!!!")
print("Total movies - ", len(finaldata['delete']) + len(finaldata['keep']) + len(finaldata['undecided']) )
print("Deletable movies - ")
print("count = ", len(finaldata['delete']))
print("size = ", sum([x['movie']["size"] for x in finaldata['delete']])/1000000000)
print("keep mo - ")
print("count = ", len(finaldata['keep']))
print("size = ", sum([x['movie']["size"] for x in finaldata['keep']])/1000000000)
print("undecided mo - ")
print("count = ", len(finaldata['undecided']))
print("size = ", sum([x['movie']["size"] for x in finaldata['undecided']])/1000000000)
print("duplicate mo - ")
print("count = ", len(finaldata['duplicate']))
print("size = ", sum([x['movie']["size"] for x in finaldata['duplicate']])/1000000000)
