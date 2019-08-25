# IMPORT needed libraries

import re, os
import datetime

from pprint import pprint as ppr

from time import sleep
from pprint import pprint as ppr
from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException

from xvfbwrapper import Xvfb

import requests
from lxml import html

# Set initial variables for City, etc
city_url = 'http://www.duluthmn.gov'
council_url = 'http://www.duluthmn.gov/city-council/city-councilors'
calendar_url = 'https://duluthmn.gov/event-calendar/'
DATE_FORMAT = '%B %d, %Y %I:%M%p'
DATE_FORMAT_ALT = '%B %d, %Y %I:%M %p'

# Setting up routine processes
def get_base(site):
	s = requests.get(site)
	b = html.fromstring(s.text)
	return b

# Initiate virtual display
start_cmd = "Xvfb :91 && export DISPLAY=:91 &"
xvfb = Xvfb()

# Start the virtual display
os.system(start_cmd)
xvfb.start()
print("started Xvfb")

# Initiate and start the Browser
br = wd.Chrome()

# Go to specified URL
br.get(calendar_url)
sleep(3)
collectedRows = []
# Changing to List style view
br.find_elements_by_xpath('.//*/a[@id="ContentPlaceHolder1_ctl03_WebCalendar_4_btnCalendarViewList"]')[0].click()
# Get the rows in the table of events 
def getRows(br):
	rows = br.find_elements_by_xpath('.//*/div[@id="pnlCalendar"]/div/div/table/tbody/tr/td[@class="tblListCalendarEventCell"]/span')
	numOfRows = len(rows)-1
	return rows, numOfRows


# Set a variable to the number of rows in the table
# numOfRows = len(rows)-1
# print(numOfRows)

# Create empty list to collect event data


# PROCESS FOR FOLLOWING FOR LOOP
"""
0) cycle through a range of integers equal to numOfRows
1) create new dictionary
2) Refresh the rows variable
3) Set 'row' equal to the next row
4) Add 'title' to our dictionary
5) 'TRY' to get more event info
6) 'Click' on the row in question
7) Get Event date
8) Event Info
9) Close the pop-up window
10) Append new dictionary to list collectedRows
11) if that doesn't work --- let us know why
12) if a pop-up failed to close, try closing it
"""

def getInfo(rows, numOfRows, br):
	for n in range(0,numOfRows):
		print("\n\n ++++++ \n\n")
		nR = {}
		rows = br.find_elements_by_xpath('.//*/div[@id="pnlCalendar"]/div/div/table/tbody/tr/td[@class="tblListCalendarEventCell"]/span')
		row = rows[n]
		nR['title'] = row.text
		row.click()
		sleep(3)
		dateInfo = br.find_elements_by_xpath('.//*/div[@id="ContentPlaceHolder1_ctl03_WebCalendar_4_upPopUp"]/table/tbody/tr/td')[0].text
		dateInfo = dateInfo.split("\n")
		dateTime = dateInfo[1] + ' '+ dateInfo[2]
		nR['dateTime'] = datetime.strptime(dateTime.split('-')[0], DATE_FORMAT)
		print(nR)
		moreInfo = dateInfo[3:-7]
		n = 0
		loc = False
		site = False
		nR['moreInfo'] = []
		nR['eventLocation'] = []
		for mi in moreInfo:
			if site == True:
				nR['website'] = mi
				continue
			elif loc == False and not mi == 'Location:':
				nR['moreInfo'].append(mi)
				continue
			elif mi == 'Location:':
				loc = True
				continue
			elif mi == 'Website:':
				loc = False
				site = True
				continue
			elif loc == True:
				nR['eventLocation'].append(mi)
				continue
			else:
				print('oops')
		nR['eventLocation'] = (' ').join(nR['eventLocation'])
		nR['moreInfo'] = ('\n').join(nR['moreInfo'])
		# for di in dateInfo:
		# 	print(di)
		# 	print()
		br.find_elements_by_xpath('.//*/button[@title="Close"]')[0].click()
		sleep(3)
		collectedRows.append(nR)



for x in range(0,3):
	rows, numOfRows = getRows(br)
	getInfo(rows, numOfRows, br)
	nextBtn = br.find_elements_by_xpath('.//*/i[@class="fas fa-angle-double-right"]')[0]
	nextBtn.click()
	print('\n\n New New coming soon \n\n')
	print(len(collectedRows))
	sleep(3)





os.system('pkill Xvfb')
# xvfb.stop()
ppr(collectedRows)


# for n in range(0,5):
# 	print("\n\n ++++++ \n\n")
# 	nR = {}
# 	rows = br.find_elements_by_xpath('.//*/div[@id="pnlCalendar"]/div/div/table/tbody/tr/td[@class="tblListCalendarEventCell"]/span')
# 	row = rows[n]
# 	nR['title'] = row.text
# 	print(nR)
# 	# base = html.fromstring(br.page_source)
# 	# print('first run\n', nR, dir(row))
# 	try:
# 		# print(dir(row))
# 		row.click()
# 		sleep(1)
# 		print('end sleep')
# 		dateInfo = br.find_elements_by_xpath('.//*/div[@id="ContentPlaceHolder1_ctl03_WebCalendar_4_upPopUp"]/table/tbody/tr/td/p')[0].text
# 		# print(dateInfo)
# 		eventInfo = br.find_elements_by_xpath('.//*/div[@id="ContentPlaceHolder1_ctl03_WebCalendar_4_upPopUp"]/table/tbody/tr/td/table/tbody/tr/td')[0].text
# 		# print(eventInfo)
# 		eventInfo = eventInfo.split("\n")
# 		len(eventInfo)
# 		for di in eventInfo:
# 			print(di)
# 			print()
		# nR['datetime'] = br.find_elements_by_xpath('.//*/div[@id="ContentPlaceHolder1_ctl03_WebCalendar_4_upPopUp"]/table/tbody/tr/td/p')[0].text
		# nR['paragraph'] = br.find_elements_by_xpath('.//*/div[@id="ContentPlaceHolder1_ctl03_WebCalendar_4_upPopUp"]/table/tbody/tr/td/table/tbody/tr/td/div')[0].text
		# nR['datetime'] = br.find_elements_by_xpath('.//*/div[@id="ContentPlaceHolder1_ctl03_WebCalendar_4_upPopUp"]/table/tbody/tr/td/p')[0].text
		# print(nR)
		# ppr(nR['paragraph'][0].text)
	# 	br.find_elements_by_xpath('.//*/button[@title="Close"]')[0].click()
	# 	collectedRows.append(nR)
	# 	pass
	# except:
	# 	print('oops')
	# 	dateInfo = br.find_elements_by_xpath('.//*/div[@id="ContentPlaceHolder1_ctl03_WebCalendar_4_upPopUp"]/table/tbody/tr/td')[0].text
	# 	# print(len(dateInfo))
	# 	# print(dateInfo)
	# 	dateInfo = dateInfo.split("\n")
	# 	len(dateInfo)
	# 	for di in dateInfo:
	# 		print(di)
	# 		print()
	# 	try:
	# 		br.find_elements_by_xpath('.//*/button[@title="Close"]')[0].click()
	# 	except:
	# 		pass



# Move to next month
# nextBtn = br.find_elements_by_xpath('.//*/i[@class="fas fa-angle-double-right"]')[0]

# for r in rows[:5]:
# 	print(type(r))
# 	r.click()
# 	sleep(3)
# 	print('end sleep')
# 	event = br.find_elements_by_xpath('.//*/div[@id="ContentPlaceHolder1_ctl03_WebCalendar_4_upPopUp"]')
# 	print(event)
# 	br.find_elements_by_xpath('.//*/button[@title="Close"]')[0].click()
# 	rows = br.find_elements_by_xpath('.//*/div[@id="pnlCalendar"]/div/div/table/tbody/tr/td[@class="tblListCalendarEventCell"]/span')



# print(rows)

# xvfb.stop()

# os.system('pkill Xvfb')

# base = get_base(calendar_url)
# rows = base.xpath()
# events = calendar.xpath('.//*/tr[@class="tblListCalendarHeader"]')
# print(events)

# for row in rows:
# 	row.

# council = get_base(council_url)
# members = council.xpath('.//*/div[@id="divPageContent"]/*[@id="divRight"]/ul/li')
# for m in members:
# 	name = m.xpath('.//a/text()')[0]
# 	link = m.xpath('.//a/@href')[0]
# 	mlink = city_url+link
# 	print(name, mlink)
# 	member = get_base(mlink)
# 	info = member.xpath('.//*/div[@id="divPageContent"]/*[@id="divCenter"]/p/span/text()')
# 	text = member.xpath('.//*/div[@id="divPageContent"]/*[@id="divCenter"]/p/span/span/text()')
# 	email = member.xpath('.//*/div[@id="divPageContent"]/*[@id="divCenter"]/p/span/a/text()')
# 	links = member.xpath('.//*/div[@id="divPageContent"]/*[@id="divCenter"]/p/span/span/span/a')
# 	mlinks = member.xpath('.//*/div[@id="divPageContent"]/*[@id="divCenter"]/p/a/text()')
# 	# ppr(info)
# 	if len(email)>0:
# 		ppr(email[0])
# 	else:
# 		ppr(mlinks[0])
# 	# ppr(text)
# 	# ppr(links)
# 	# ppr(mlinks)
# 	print('+++ \n\n +++')