import requests
import re
import json
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

endpoint = "https://in.bookmyshow.com"

def checkCinemaAndInformUsers(movieName, cinemaNames, cinemaNameToSearchFor):
    cinemasToInformFor = []
    if cinemaNameToSearchFor is None:
        print "Matching all cinenmas!"
        cinemasToInformFor = cinemaNames
    else:
        print "Shortlisting cinemas with regex " + cinemaNameToSearchFor
        regex = re.compile(cinemaNameToSearchFor, flags=re.IGNORECASE)
        for cinema in cinemaNames:
            if regex.search(cinema):
                print "Cinema match ! " + cinema
                cinemasToInformFor.append(cinema)
            else:
                print "Not matching:" + cinema

    if len(cinemasToInformFor) == 0:
        print "No cinemas found for this movie that match the required pattern!!"
        return

    print "Sending mail for movie - " + movieName + ", cinemaName = " " ".join(cinemasToInformFor)

    message = Mail(
        from_email='chindii@abhinavsingh.co.in',
        to_emails=['abhinav.singh21093@gmail.com','abhinav7525@gmail.com'],
        subject='Tickets available for ' + movieName,
        html_content='<strong>Hey! Movie ticket are available for movie ' +movieName+' with cinema ' + " ".join(cinemasToInformFor) + ' </strong>')
    try:
        sg = SendGridAPIClient('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')
        response = {}#sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def findAllEventCodes(movieName,movieCode):
    movieCodes = [movieCode]
    detailsPage = endpoint + "/national-capital-region-ncr/movies/" + movieName + "/" + movieCode;
    req = requests.get(detailsPage)
    req._content
    regex = re.compile("eventLangDimensionMap\s=\sJSON.parse.*\)")
    eventCodeRawJsons = regex.findall(req._content)
    if len(eventCodeRawJsons) > 0:
        rawJson = eventCodeRawJsons[0][36:-2]
        j = json.loads(rawJson)
        for key in j:
            for code in j[key]:
                movieCodes.append(code)
    return movieCodes



def getCinemas(url):
    req = requests.get(endpoint + url)
    #print req
    #print req.__dict__
    regex = re.compile('\n\s*data-name=".*"')
    raw_cinemas = regex.findall(req._content)
    cinemas = []
    for raw_cinema in raw_cinemas:
        cinemas.append(raw_cinema[37:-1])
    return cinemas;


def crawl(movieName, movieCode, cinemaName=None):
    eventCodes = findAllEventCodes(movieName, movieCode)
    for eventCode in eventCodes:
        showsPage = "https://in.bookmyshow.com/buytickets/" + movieName + "-national-capital-region-ncr/movie-ncr-" + eventCode + "-MT"
        req = requests.get(showsPage, allow_redirects=False)
        if req.status_code == 302 or re.status_code == 301:
            redirectLocation = req.headers['Location']
            if("buytickets" in redirectLocation):
                print "ticketsAreAvailable!! for " + movieName + " with movieCode " + movieCode
                cinemas = getCinemas(redirectLocation)
                checkCinemaAndInformUsers(movieName, cinemas, cinemaName)

crawl("avengers-endgame","ET00090482", "Paytm")
