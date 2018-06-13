import sys
import os
import django

sys.path.append('/websrv/digisnaxx.com/DigiSnaxx/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'DigiSnaxx.settings'
django.setup()

from lxml import html
import requests, re, datetime
from xvfbwrapper import Xvfb
from pprint import pprint as ppr

from selenium import webdriver as wd

from digilegislature.models import *

r = requests.get("https://www.threeriversparks.org/about/board-commissioners/meeting-calendar.aspx")
b = html.fromstring(r.text)

mtgs = b.xpath('.//*/table[@class="table_data"]/*/tr')

f1 = '%b %d, %Y %I:%M %p'
f2 = '%B %d, %Y %I:%M %p'

def get_date(dt, f1, f2):
    if "." in dt:
        if 'Sept' in dt:
            new_dt = datetime.strptime(dt.replace(".", "").replace("Sept", "Sep"), f1)
            return new_dt
        new_dt = datetime.strptime(dt.replace(".", ""), f1)
        return new_dt
    else:
        new_dt = datetime.strptime(dt, f2)
        return new_dt

for m in mtgs:
    info = []
    cells = m.xpath('./td')
    for c in cells:
        i = c.xpath('.//text()')
        info.append(i)
    if not len(info)>0:
        continue
    date = info[0][0].replace("*", "")
    time = info[1]
    mtype = info[2]
    info = info[3]
    if len(time) == 2:
        e1_time = date + ', 2017 ' + time[0]
        e2_time = date + ', 2017 ' + time[1]
        rd1 = get_date(e1_time, f1, f2)
        rd2 = get_date(e2_time, f1, f2)
        t1_mtg = mtype[0]
        t2_mtg = mtype[1]
        event1, created = Events.objects.get_or_create(title=t1_mtg,
                                                      time=rd1,
                                                      calendar="Three Rivers Park Council")
        event2, created = Events.objects.get_or_create(title=t2_mtg,
                                                      time=rd2,
                                                      calendar="Three Rivers Park Council")
        continue
    dtime = date + ', 2017 ' + time[0]
    real_date = get_date(dtime, f1, f2)
    event, created = Events.objects.get_or_create(title=mtype[0],
                                                  time=real_date,
                                                  calendar="Three Rivers Park Council")
    if len(info)>0:
        event.notes = info
        event.save()

