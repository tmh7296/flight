from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from twilio.rest import Client
import requests, time, os, random


originAirport = os.environ.get("ORIGIN_AIRPORT")
destinationAirport = os.environ.get("DEST_AIRPORT")
outboundDateString = os.environ.get("LEAVE_DATE")
returnDateString = os.environ.get("RETURN_DATE")

def flightPage():
	chrome_options = Options()
	chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	chrome_options.add_argument("--disable-gpu")
	chrome_options.add_argument("--no-sandbox")
	driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
	driver.get("https://www.southwest.com/")
	departure_airport = WebDriverWait(driver,
                                 10).until(EC.element_to_be_clickable((By.ID,
                                                                      "air-city-departure")))
	arrival_airport = driver.find_element_by_id("air-city-arrival")
	departure_airport.send_keys(originAirport)
	arrival_airport.send_keys(destinationAirport)
	arrival_date = WebDriverWait(driver,
                                 10).until(EC.element_to_be_clickable((By.ID,
                                                                       "air-date-return")))
	departure_date = driver.find_element_by_id("air-date-departure")
	departure_date.click()
	departure_date.clear()
	departure_date.send_keys(outboundDateString)
	driver.find_element_by_tag_name("div").click()
	arrival_date.click()
	arrival_date.clear()
	arrival_date.send_keys(returnDateString)
	driver.find_element_by_id("jb-booking-form-submit-button").click()
	parseSouthWest(driver.page_source)

def parseSouthWest(htmlText):
	try:
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
		print("$" + str(lowestOutBoundFare))
		print("$" + str(lowestInBoundFare))
		if int(lowestOutBoundFare) < 1500 or int(lowestInBoundFare) < 1500:
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
	NUM = os.environ.get('MY_NUMBER')
	TWILIO_NUM = os.environ.get('TWILIO_NUMBER')
	client = Client(ACCOUNT_SID, AUTH_TOKEN)
	client.messages.create(to=NUM, from_=TWILIO_NUM, body=message)


flightPage()




