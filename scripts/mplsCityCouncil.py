import sys
import os
import django
from pprint import pprint as ppr

sys.path.append('/websrv/digisnaxx.com/DigiSnaxx/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'DigiSnaxx.settings'
django.setup()

from lxml import html
import requests, re
from datetime import datetime


from digilegislature.models import *


root = requests.get('http://apps.ci.minneapolis.mn.us/CalendarApp/Ex_CalendarRSS.aspx?linkurl=http://www.ci.minneapolis.mn.us/government/calendars.asp&datebook=City%20Council%20Date%20Book&type=rss')
base = html.fromstring(root.text)


items = base.xpath('.//*/item')

date_format = '%m/%d/%y %I:%M %p'


for i in items:
    title = i.xpath('.//title/text()')
    desc = i.xpath('.//description/text()')
    place = i.xpath('.//comments/text()')
    link = i.xpath('.//guid/text()')
    tit = title[0].strip()
    num = re.search('\d', tit).start()
    date = title[0][num:].strip()
    real_date = datetime.strptime(date, date_format)
    title = title[0][:num].strip()
    loc = place[0].strip()
    url = link[0]
    event, created = Events.objects.get_or_create(title=title,
                                                  url=url,
                                                  time=real_date,
                                                  calendar="Minneapolis")
    ppr(event)

event_agendas = []

r = requests.get('http://www.ci.minneapolis.mn.us/meetings/all/index.htm')
b = html.fromstring(r.text)
eas = b.xpath('.//*/table[@id="schedule"]/*/tr')

for e in eas:
    date_format = '%b. %d, %Y %I:%M %p'
    agenda = e.xpath('.//td[1]/a/@href')
    name = e.xpath('.//td[1]/a/text()')
    date = e.xpath('.//td[@class="date"]/text()')
    time = e.xpath('.//td[@class="time"]/text()')
    if len(date) > 0:
        name = name[0].split(' ')
        dt = date[0] + ' ' + time[0]
        rdt = datetime.strptime(dt, date_format)
        try:
            ev = Events.objects.get(calendar="Minneapolis", time=rdt, title__startswith=name[0])
            note = '<a href="{0}" target="_blank"><h3>Agenda</h3></a>'.format(agenda[0])
            ev.notes = note
            ev.save()
        except:
            pass


