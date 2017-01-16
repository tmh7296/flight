import requests, time, os, random, re
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient

ORIGIN_AIRPORT = os.environ.get('ORIGIN_AIRPORT')
DEST_AIRPORT = os.environ.get('DEST_AIRPORT')
LEAVE_DATE = os.environ.get('LEAVE_DATE')
RETURN_DATE = os.environ.get('RETURN_DATE')
NUM_TICKETS = os.environ.get('NUM_TICKETS')
MY_NUMBER = os.environ.get('MY_NUMBER')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')
ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

def main():
	outBoundSpirit, inBoundSpirit = scrapeSpirit()
	outBoundSouthWest, inBoundSouthWest = scrapeSouthWest()
	if (outBoundSpirit + inBoundSpirit) < (outBoundSouthWest + inBoundSouthWest):
		lowestOutBoundFare = outBoundSpirit
		lowestInBoundFare = inBoundSpirit
		airline = "Spirit"
	else:
		lowestOutBoundFare = outBoundSouthWest
		lowestInBoundFare = inBoundSouthWest
		airline = "SouthWest"
	if float(lowestOutBoundFare) < 150 or float(lowestInBoundFare) < 150:
	message = "Cheapest outbound flight ("+ airline +"): $"+lowestOutBoundFare+ ", "\
			"Cheapest inbound flight ("+ airline +"): $"+lowestInBoundFare+ 
	twilio(message, MY_NUMBER)
	
def parseSouthWest(htmlText):
	try:
		print("parsing")
		page = BeautifulSoup(htmlText, 'html.parser')
		priceString = '<span class="currency_symbol">$</span>'
		directionString = 'id="In'
		flights = page.find_all('div', {'class':'product_info'})
		inBoundPrice = []
		outBoundPrice = []
		for flight in flights:
			flight = str(flight)
			index = flight.find(priceString)
			if index != -1:
				newIndex = index + len(priceString)
				price = ""
				while flight[newIndex].isdigit():
					price += flight[newIndex]
					newIndex += 1
				if flight.find(directionString) != -1:
					inBoundPrice.append(price)
				else:
					outBoundPrice.append(price)
			else:
				pass
		lowestOutBoundFare = (min(outBoundPrice))
		lowestInBoundFare = (min(inBoundPrice))
		return lowestOutBoundFare, lowestInBoundFare
	except Exception as e:
		message = e
		twilio(message, "16105859087")
		#twilio("Something's fucked, man: " + message)

def parseSpirit(htmlText):
	try:
		page = BeautifulSoup(htmlText, 'html.parser')
		chunks = page.find_all('div', {'class':'standardFare'})
		flights = []
		inBoundPrices = []
		outBoundPrices = []
		for el in chunks:
			el = str(el)
			if "Market1" in el:
				price = ''
				priceString = '<em class="emPrice">'
				index = el.find(priceString) + len(priceString) + 1
				while el[index].isdigit() or el[index] == ".":
					price += el[index].strip("$")
					index += 1
				inBoundPrices.append(price)
			elif "Market2" in el:
				price = ''
				priceString = '<em class="emPrice">'
				index = el.find(priceString) + len(priceString) + 1
				while el[index].isdigit() or el[index] == ".":
					price += el[index].strip("$")
					index += 1
				outBoundPrices.append(price)
		return min(outBoundPrices), min(inBoundPrices)
	except Exception as e:
		message = e
		twilio(message, "16105859087")
		
def twilio(message, number):
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	message = client.messages.create(to=number, from_=TWILIO_NUMBER,
                                     body=message)

def scrape(url, payload):
	r = requests.post(url, data=payload)
	return r.text

def scrapeSouthWest():
	payload = {
		'returnAirport':'',
		'twoWayTrip':'true',
		'fareType':'DOLLARS',
		'originAirport':ORIGIN_AIRPORT,
		'destinationAirport':DEST_AIRPORT,
		'outboundDateString':LEAVE_DATE,
		'returnDateString':RETURN_DATE,
		'adultPassengerCount':NUM_TICKETS,
		'seniorPassengerCount':'0',
		'promoCode':'',
		'submitButton':'true'
	}
	url = "https://www.southwest.com/flight/search-flight.html"
	html = scrape(url, payload)
	return parseSouthWest(html)


	
def scrapeSpirit():
    payload = {
        'HiddenGuid':'907493d4-0e96-4d08-a623-87a5c8ca91b4',
        'birthdates':'2/2/2004,6/16/2007',
        'lapoption':'0,0',
        'awardFSNumber':'',
        'bookingType':'F',
        'hotelOnlyInput':'',
        'autoCompleteValueHidden':'',
        'tripType':'roundTrip',
        'from':ORIGIN_AIRPORT,
        'to':DEST_AIRPORT,
        'departDate':LEAVE_DATE,
        'departDateDisplay':LEAVE_DATE,
        'returnDate':RETURN_DATE,
        'returnDateDisplay':RETURN_DATE,
        'carPickUpTime':'16',
        'carDropOffTime':'16',
        'ADT':NUM_TICKETS,
        'CHD':'2',
        'INF':'0'
    }
	url = "https://www.spirit.com/Default.aspx?action=search"
	html = scrape(url, payload)
	return parseSpirit(html)

scrapeSouthWest()