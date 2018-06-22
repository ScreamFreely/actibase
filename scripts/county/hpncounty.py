import sys
import os
import django

#sys.path.append('/websrv/digisnaxx.com/DigiSnaxx/')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'DigiSnaxx.settings'
#django.setup()

from lxml import html
import requests, re
from datetime import datetime


#from digilegislature.models import *


root = requests.get('https://board.co.hennepin.mn.us/hcmeetview/Default.aspx?year=2016&month=12')
base = html.fromstring(root.text)

board_mtgs = base.xpath('.//*[@id="tblBoardMeetings"]/tr')
cmt_mtgs = base.xpath('.//*[@id="tblCommitteeMeetings"]/tr')
auth_mtgs = base.xpath('.//*[@id="tblAuthorityMeetings"]/tr')


format = '%B %d, %Y %I:%M %p'

for b in board_mtgs[1:]:
    info = b.xpath('.//td/text()')
    link_text = b.xpath('.//td/a/text()')
    links = b.xpath('.//td/a/@href')
    nlinks = []
    date = info[0] + ' 1:30 pm'
    real_date = datetime.strptime(date, format)
    for l in links:
        l = l[22:-2]
        nlinks.append(l)
    clinks = zip(link_text, nlinks)
    enotes = []
#    event, created = Events.objects.get_or_create(title=info[1],
#                                                  time=real_date,
#                                                  calendar="Hennepin County")
    if len(clinks)>0:
        for i,l in clinks:
            j = "<a href=\"" + l + "\" target=_blank>" + i + "</a>"
#            enotes.append(j)
#        event.notes = " ".join(enotes)
#        event.save()



for c in cmt_mtgs[1:]:
    info = c.xpath('.//td/text()')
    link_text = c.xpath('.//td/a/text()')
    links = c.xpath('.//td/a/@href')
    nlinks = []
    date = info[0] + ' 1:30 pm'
    real_date = datetime.strptime(date, format)
    for l in links:
        l = l[22:-2]
        nlinks.append(l)
    clinks = zip(link_text, nlinks)
    enotes = []
#    event, created = Events.objects.get_or_create(title=info[1],
#                                                  time=real_date,
#                                                  calendar="Hennepin County")
    if len(clinks)>0:
        for i,l in clinks:
            j = "<a href=\"" + l + "\" target=_blank>" + i + "</a>"
#            enotes.append(j)
#        event.notes = " ".join(enotes)
#        event.save()


    
for a in auth_mtgs[1:]:
    info = a.xpath('.//td/text()')
    link_text = a.xpath('.//td/a/text()')
    links = a.xpath('.//td/a/@href')
    nlinks = []
    date = info[0] + ' 1:30 pm'
    real_date = datetime.strptime(date, format)
    for l in links:
        l = l[22:-2]
        nlinks.append(l)
    clinks = zip(link_text, nlinks)
    enotes = []
#    event, created = Events.objects.get_or_create(title=info[1],
#                                                  time=real_date,
#                                                  calendar="Hennepin County")
    if len(clinks)>0:
        for i,l in clinks:
            j = "<a href=\"" + l + "\" target=_blank>" + i + "</a>"
#            enotes.append(j)
#        event.notes = " ".join(enotes)
#        event.save()


