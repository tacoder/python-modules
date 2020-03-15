# JSON IMDbPY class wrapper
# Goal:  wraps IMDB class data function to provide fully complaint json
# author: james , rubino <at> gmail , com
# note: contains wrapper and randomized test cases

from random import randint as r
import json
import imdb
ia = imdb.IMDb()

#movie = ia.get_movie(r(1,2300000))
#i#company = ia.get_company(r(1,2756))
person = ia.get_person(r(1,4116000))


def identify(DataObj):
     idoc = {}
     if type(DataObj) == imdb.Person.Person:
         tag = 'nm'
     if type(DataObj) == imdb.Movie.Movie:
         tag = 'tt'
     if type(DataObj) == imdb.Company.Company:
         tag = 'co'
     ID = DataObj.getID()
     idoc['_id'] = tag+ID
     idoc['id_'] = ID
     return idoc


def convert(DataObj):
    document = {}
    document.update(identify(DataObj))

    classes = (
    imdb.Person.Person,
    imdb.Movie.Movie,
    imdb.Company.Company )


    for key in DataObj.keys():
        if type(DataObj[key]) is list:
            values = DataObj[key]

            if len(values) == 0:
                continue

            sample = values[0]

            if type(sample) in classes:
                val = map(lambda x: x.data, values)
                for x in val:
                    n = val.index(x)
                    x.update(identify(values[n]))
                    document[key] = val

            if len(values) is 1 and type(values[0]) not in classes:
                document[key] = values[0]

            if len(values) is 1 and type(values[0]) in classes:
                data = values[0].data
                data.update(identify(values[0]))

                document[key] = [data]

            if type(sample) in (unicode, str):
                document[key] = DataObj[key]



        else:
            #print key
            document[key] = DataObj[key]

    return document


print "Test Person Conversion"
pk = person.keys()
print "Keys in Person Object:\t", len(pk)
pc = convert(person)
print "Keys in Converted Object:\t", len(pk)
print json.dumps(person)
print set(pk) - set(pc.keys())

print "\n"*2

print "Test Company Conversion"
ck = company.keys()
print "Keys in Company Object:\t", len(ck)
cc = convert(company)
print "Keys in Converted Object:t\t", len(cc.keys())
print set(ck) - set(cc.keys())

print "\n"*2

print "Test Movie Conversion: "
mk = movie.keys()
print "Keys in Movie Object:\t", len(mk)
mc = convert(movie)
print "Keys in Converted Object:\t", len(mc.keys())
print set(mk) - set(mc.keys())

