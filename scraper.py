import requests, schedule, time, os, random
from bs4 import BeautifulSoup
from twilio.rest import TwilioRestClient

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

def parseSouthWest(htmlText):
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
	if int(lowestOutBoundFare) < 200 or int(lowestInBoundFare) < 200:
		message = "Cheapest outbound flight: $"+lowestOutBoundFare+ ", "\
				"Cheapest inbound flight: $"+lowestInBoundFare
		twilio(message)
		
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
	parse(r.text)
	
def twilio(message):
	ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
	AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
	client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
	message = client.sms.messages.create(to="+16105859087",
                                     from_="+14846854493",
                                     body=message)


times = [1,2,3,4,5]		 
schedule.every(random.choice(times)).minutes.do(scrapeSouthWest)							 
#times = ['22:00','23:00','00:00','01:00','02:00']			 
#schedule.every().day.at(random.choice(times)).do(scrapeSouthWest)

while 1:
   schedule.run_pending()
   time.sleep(1)									
