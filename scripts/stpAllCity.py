import sys
import os
import django
import re
sys.path.append('/websrv/digisnaxx.com/DigiSnaxx/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'DigiSnaxx.settings'
django.setup()


import requests
import datetime
from pprint import pprint as ppr

from lxml import html
from selenium import webdriver 

from digilegislature.models import *

"""
https://www.stpaul.gov/calendar/2016-12?field_department_tid=741

https://www.stpaul.gov/calendar/2016-12
"""

root = requests.get("https://www.stpaul.gov/calendar?field_department_tid=All&field_calendar_item_type_value=All")
base = html.fromstring(root.text)
items = base.xpath('.//*/div[@class="view-content"]/div')
format = "%A %B %d, %Y - %I:%M %p"
format2 = "%A %B %d, %Y - "
meetings = []

for i in items:
    if len(i.xpath('.//*/span[@class="date-display-single"]/text()')) > 0:
        d = {}
        d['date'] = i.xpath('.//*/span[@class="date-display-single"]/text()')[0]
        d['info'] = i.xpath('.//*/span[@class="field-content"]/a/text()')[0]
        d['link'] = i.xpath('.//*/span[@class="field-content"]/a/@href')[0]
        meetings.append(d)

for m in meetings:
    m['link'] = "https://www.stpaul.gov" + m['link']

for m in meetings:
    ppr(m['info'])
    r = requests.get(m['link'])
    b = html.fromstring(r.text)
    exists = b.xpath('.//div[@class="node-content clearfix"]')
    if len(exists)>0:
        date = exists[0].xpath('.//*/span[@class="date-display-single"]/text()')
        loc1 = exists[0].xpath('.//*/div[@class="thoroughfare"]/text()')
        loc2 = exists[0].xpath('.//*/div[@class="premise"]/text()')
#        links = exists[0].xpath('.//*/a/@href')
#        link_names = exists[0].xpath('.//*/a/text()')
        if len(loc1) > 0:
            m['location'] = loc1[0] 
	    if len(loc2) > 0:
	        m['location'] = m['location'] + " " + loc2[0]
        else:
            m['location'] = 'N/A'
        if ":" in date[0]:
            date = datetime.strptime(date[0], format)
	else:
            date = datetime.strptime(date[0], format2)
        m['date'] = date
        ppr(m)

        event, created = Events.objects.get_or_create(title=m['info'],
                                                      url=m['link'], 
                                                      time=m['date'], 
                                                      calendar='St Paul'
        )
        event.address = m['location']
        event.save()


print('START NEXT PULL')

r = requests.get("https://stpaul.legistar.com/Calendar.aspx")
b = html.fromstring(r.text)
eas = b.xpath('.//*/table[@class="rgMasterTable"]/*/tr')

for e in eas:
    print('GET EVENTS')
    date_format = '%m/%d/%Y %I:%M %p'
    name = e.xpath('.//td[1]/*/a/*/text()')
    date = e.xpath('.//td[2]/*/text()')
    time = e.xpath('.//td[4]/*/span/*/text()')
    loc = e.xpath('.//td[5]/*/text()')
    details = e.xpath('.//td[6]/*/a/@href')
    agenda = e.xpath('.//td[7]/*/*/a/@href')
    if len(date) > 0:
        print('CHECK DATE')
        name = name[0]
        if len(details) > 0:
            deets_link = 'https://stpaul.legistar.com/' + details[0]
        if len(agenda) > 0:
            agenda_link = 'https://stpaul.legistar.com/' + agenda[0]
        dt = date[0] + ' ' + time[0]
        rdt = datetime.strptime(dt, date_format)
        try:
            ev = Events.objects.get(calendar="St Paul", time=rdt, title__startswith=name)
            if len(details) > 0 and len(agenda) > 0:
                note = '{0}\n <a href="{1}" target="_blank"><h3>Meeting Details</h3></a> <a href="{2}" target="_blank"><h3>PDF Agenda</h3></a>'.format(loc[0], deets_link, agenda_link)
                
                ev.notes = note
                ev.save()
            elif len(details) > 0 and not len(agenda) >0:
                note = '{0}\n<a href="{1}" target="_blank"><h3>Meeting Details</h3></a>'.format(loc[0], deets_link)
                ev.notes = note
                ev.save()
            else:
                note = '{0}'.format(loc[0])
                ev.notes = note
                ev.save()
        except:
            pass
