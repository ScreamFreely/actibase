import requests, re, datetime
from lxml import html

from pupa.scrape import Scraper
from pupa.scrape import Event


class HennepinEventScraper(Scraper):
	datetime = datetime.datetime
	format = '%B %d, %Y %I:%M %p'

	def run_board_mts(board_mtgs):
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
	        print('{0} {1}'.format(info[1], real_date))

	        if len(list(clinks))>0:
	            for i,l in clinks:
	                j = "<a href=\"" + l + "\" target=_blank>" + i + "</a>"
	                print(j)

	def run_cmt_mts(cmt_mtgs):
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
	        print('{0} {1}'.format(info[1], real_date))    
	        enotes = []

	        if len(list(clinks))>0:
	            for i,l in clinks:
	                j = "<a href=\"" + l + "\" target=_blank>" + i + "</a>"
	                print(j)            

	def run_auth_mts(auth_mtgs):
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
	        print('{0} {1}'.format(info[1], real_date))
	        enotes = []

	        if len(list(clinks))>0:
	            for i,l in clinks:
	                j = "<a href=\"" + l + "\" target=_blank>" + i + "</a>"
	                print(j)


    def scrape(self):
        today = datetime.today()
		year = today.year

		for x in range(0,4):
		    month = today.month + x
		    while month >= 12:
		        if x == 0:
		            print('new month ', month)
		            root = requests.get('https://board.co.hennepin.mn.us/hcmeetview/Default.aspx?year={0}&month={1}'.format(year, month))
		            base = html.fromstring(root.text)
		        else:
		            root = requests.get('https://board.co.hennepin.mn.us/hcmeetview/Default.aspx?year={0}&month={1}'.format(year, x))
		            base = html.fromstring(root.text)
		    else:
		        print('new month ', month)
		        root = requests.get('https://board.co.hennepin.mn.us/hcmeetview/Default.aspx?year={0}&month={1}'.format(year, month))
		        base = html.fromstring(root.text)

		    board_mtgs = base.xpath('.//*[@id="tblBoardMeetings"]/tr')
		    cmt_mtgs = base.xpath('.//*[@id="tblCommitteeMeetings"]/tr')
		    auth_mtgs = base.xpath('.//*[@id="tblAuthorityMeetings"]/tr')

		    run_board_mts(board_mtgs)
		    run_cmt_mts(cmt_mtgs)
		    run_auth_mts(auth_mtgs)
