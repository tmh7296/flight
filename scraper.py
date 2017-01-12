import requests, time, os, random
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient

def parseSouthWest(htmlText):
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
	if int(lowestOutBoundFare) < 150 or int(lowestInBoundFare) < 150:
		message = "Cheapest outbound flight: $"+lowestOutBoundFare+ ", "\
				"Cheapest inbound flight: $"+lowestInBoundFare
		twilio(message)
	
def twilio(message):
	ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
	AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	message = client.messages.create(to="+16105859087",
                                     from_="+14846854493",
                                     body=message)

def scrapeSouthWest():
	payload = {
		'returnAirport':'',
		'twoWayTrip':'true',
		'fareType':'DOLLARS',
		'originAirport':'BOS',
		'destinationAirport':'PDX',
		'outboundDateString':'05/31/2017',
		'returnDateString':'06/02/2017',
		'adultPassengerCount':'1',
		'seniorPassengerCount':'0',
		'promoCode':'',
		'submitButton':'true'
	}
	r = requests.post("https://www.southwest.com/flight/search-flight.html", data=payload)
	parseSouthWest(r.text)

scrapeSouthWest()