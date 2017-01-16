import requests, time, os, random
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient

def parseSouthWest(htmlText):
	try:
		print("parsing")
		page = BeautifulSoup(htmlText, 'html.parser')
		print(str(page))
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
	except Exception as e:
		message = e
		print(message)
		twilio("Something's fucked, man: " + str(message))
	
def twilio(message):
	ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
	AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	message = client.messages.create(to=os.environ.get('MY_NUMBER'),
                                     from_=os.environ.get('TWILIO_NUMBER'),
                                     body=message)

def scrapeSouthWest():
	payload = {
		'returnAirport':'',
		'twoWayTrip':'true',
		'fareType':'DOLLARS',
		'originAirport':os.environ.get('ORIGIN_AIRPORT'),
		'destinationAirport':os.environ.get('DEST_AIRPORT'),
		'outboundDateString':os.environ.get('LEAVE_DATE'),
		'returnDateString':os.environ.get('RETURN_DATE'),
		'adultPassengerCount':os.environ.get('NUM_TICKETS'),
		'seniorPassengerCount':'0',
		'promoCode':'',
		'submitButton':'true'
	}
	r = requests.post("https://www.southwest.com/flight/search-flight.html", data=payload)
	parseSouthWest(r.text)

scrapeSouthWest()