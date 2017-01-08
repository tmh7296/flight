import requests
from bs4 import BeautifulSoup

def parse(htmlText):
	page = BeautifulSoup(htmlText, 'html.parser')
	priceString = '<span class="currency_symbol">$</span>'
	directionString = 'id="In'
	flights = page.find_all('div', {'class':'product_info'})
	inBoundPrice = []
	outBoundPrice = []
	for flight in flights:
		flight = str(flight)
		index = flight.find(priceString)
		newIndex = index + len(priceString)
		price = ""
		while flight[newIndex].isdigit():
			price += flight[newIndex]
			newIndex += 1
		if flight.find(directionString) != -1:
			inBoundPrice.append(price)
		else:
			outBoundPrice.append(price)
	print("The cheapest outbound flight is: $"+ str(min(outBoundPrice)))
	print("The cheapest inbound flight is: $"+ str(min(inBoundPrice)))	
		
def scrape():
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
	#print(r.text)
	parse(r.text)
	
scrape()
