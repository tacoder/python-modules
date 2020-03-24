#!/bin/python
import json

from pip._vendor.distlib.compat import raw_input


def yes_or_no(question):
    reply = str(raw_input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return yes_or_no("Uhhhh... please enter ")

with open("data/movies-imdb-data-filtered.json", 'r') as f:
    moviesJson = json.load(f)

# moviesJson = json.loads("finalResult5.json")

def notSoGoodMovie(movieData):
	if movieData['genres'] and  'Comedy' in movieData['genres'] and 'Romance' not in movieData['genres']:
		if movieData['rating'] is not None  and movieData['rating'] < 3:
			return True
	else:
		if movieData['rating'] is not None  and movieData['rating'] < 7:
			return True;
	return False

finaldata = {}
finaldata['delete'] = []
finaldata['keep'] = []
finaldata['undecided'] = []
finaldata['duplicate'] = []

for movie in moviesJson:
	if len(movie['finalResult']) != 1:
		# print "No data for file: " , movie['movie']['fullpath'].encode('utf-8')
		finaldata['undecided'].append(movie)
		continue
	movieData = movie['finalResult'][0]
	if notSoGoodMovie(movieData):
		# print "You can delete: " , movie['movie']['fullpath'].encode('utf-8')
		finaldata['delete'].append(movie)
	else :
		# print "You cannot delete this mf!", movie['movie']['fullpath'].encode('utf-8')
		finaldata['keep'].append(movie)


def printMovie(movie):
	print(movie['movie']['fullpath'])


def detectDuplicatesAndMoveToDelete(finaldata):
	moviesFound = {}
	stillKeep = []
	delete = []
	for movie in finaldata['keep']:
		print("Total:", len(moviesFound.keys()), ", keep:", len(stillKeep), ", delete:", len(delete), " undecided:", len(finaldata['undecided']))
		id_ = movie['finalResult'][0]['id']
		if id_ in moviesFound:
			print("=================")
			print("=================")
			print("Duplicate found - ",id_)
			printMovie(movie)
			print("Original - ")
			printMovie(moviesFound[id_])
			if(yes_or_no("Does this look like a possible duplicate?")):
				print("Removing!")
				delete.append(movie)
			else:
				print("Not removing")
				moviesFound[id_] = movie
				stillKeep.append(movie)
		else:
			moviesFound[id_] = movie
			stillKeep.append(movie)
	finaldata['keep'] = stillKeep
	finaldata['duplicate'] = delete


def allResultsAreNotSoGood(movie):
	atLeastOneResultIsGood = False
	if(len(movie['finalResult']) == 0):
		return False;
	for result in movie["finalResult"]:
		if not notSoGoodMovie(result):
			atLeastOneResultIsGood = True
	return not atLeastOneResultIsGood

preDeterminedIds = ["0264464","0172495","0113277", "0319061"]
alwaysUnknownIds = ["0988045","0375679"]

def preDetermineConditionOrInvalid(movie):
	index  =0
	for result in movie["finalResult"]:
		index += 1
		if(result['id'] in preDeterminedIds):
			print ("pre determined, choosing - ", index)
			return index
		if(result['id'] in alwaysUnknownIds):
			print("always stays xero")
			return 0
	return -1
0


def allResultsAreGood(movie):
	if (len(movie['finalResult']) == 0):
		return False;
	allGood = True
	for result in movie["finalResult"]:
		if notSoGoodMovie(result):
			allGood = False
	return allGood


def decideUndecided(finaldata):
	stillUndecided = []
	keeping = []
	deleting = []
	for movie in finaldata['undecided']:
		print(", keep:", len(keeping), ", undecided:", len(stillUndecided), " delted:", len(finaldata['delete']))
		print ("Undecided movie:", movie['movie']['fullpath'], " found : ", len(movie["finalResult"]), " results")
		printMovie(movie)
		print("Decide for yourselves:")
		i=0
		for result in movie["finalResult"]:
			i += 1
			print "  Result#", i
			printMovieResults(result)
			# "    imdb Name:", result["title"]
			# print "    imdb kind:", result["kind"]
			# print "    imdb year:", result["year"]
			# print "    imdb rating:", result["rating"]
			# print "    imdb id", result["id"]
			# print "==============================="
			# print ""
		if (allResultsAreNotSoGood(movie)):
			print "Moving this movie to delted queue, as all possible resutls are not so good"
			deleting.append(movie)
			# finaldata['delete'].append(movie)
			continue
		if(allResultsAreGood(movie)):
			print "Moving this movie to keep queue, as all possible resutls are so good"
			movie["finalResult"] = [movie["finalResult"][0]]
			keeping.append(movie)
			continue
		choice = preDetermineConditionOrInvalid(movie)
		if (len(movie["finalResult"]) == 0):
			choice = 0
		while choice < 0 or choice > len(movie["finalResult"]):
			try:
				choice = int(raw_input("Enter your choico!(0 for none):"))
			except Exception:
				pass
		if choice == 0:
			stillUndecided.append(movie)
		else:
			movie["finalResult"] = [movie["finalResult"][choice-1]]
			keeping.append(movie)
	finaldata['undecided'] = stillUndecided
	finaldata['keep'].extend(keeping)
	finaldata['delete'].extend(deleting)




def printMovieResults(result):
	print "    imdb Name:", result["title"]
	print "    imdb kind:", result["kind"]
	print "    imdb year:", result["year"]
	print "    imdb rating:", result["rating"]
	print "    imdb id", result["id"]
	print "==============================="
	print ""


decideUndecided(finaldata)
# detectDuplicatesAndMoveToDelete(finaldata)
f = open("data/imdb-final-final-date.json", "w")
f.write(json.dumps(finaldata))
f.close()

print("Summary!!!!!!")
print("Total movies - ", len(finaldata['delete']) + len(finaldata['keep']) + len(finaldata['undecided']) )
print("Deletable movies - ")
print("count = ", len(finaldata['delete']))
print("size = ", sum([x['movie']["size"] for x in finaldata['delete']]))
print("keep mo - ")
print("count = ", len(finaldata['keep']))
print("size = ", sum([x['movie']["size"] for x in finaldata['keep']]))
print("undecided mo - ")
print("count = ", len(finaldata['undecided']))
print("size = ", sum([x['movie']["size"] for x in finaldata['undecided']]))
print("duplicate mo - ")
print("count = ", len(finaldata['duplicate']))
print("size = ", sum([x['movie']["size"] for x in finaldata['duplicate']]))
