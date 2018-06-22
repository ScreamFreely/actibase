import requests, re, datetime
from lxml import html


broot = requests.get('https://www.hennepin.us/your-government#leadership')
base = html.fromstring(broot.text)
grids = base.xpath('.//*[@class="module-grid"]/article')
for g in grids:
    c = {}
    c['link'] =  g.xpath('.//*/@href')[0]
    if not c['link'].startswith('http'):
        c['link'] = 'https://www.hennepin.us' + c['link']
    name = g.xpath('.//h1/text()')[0]
    print('printedlink:', c['link'])
    if 'hennepinattorney.org' in c['link']:
        print('pass this attn')
        continue

    if 'hennepinsheriff.org' in c['link']:
        print('pass this shrf')
        continue
    
    clink = c['link']
    cr = requests.get(c['link'])
    cb = html.fromstring(cr.text)
    cbase = cb.xpath('.//*[@class="street-address"]')[0]
    blocks = cbase.xpath('.//*[@class="contactBlock"]')
    for bl in blocks:
        bname = bl.xpath('.//h3/text()')[0]
        email = bl.xpath('.//*/@href')[0].replace('mailto:', '')
        phone = bl.xpath('.//p/text()')[0].replace('Phone: ', '')
        text = bl.xpath('.//p/text()')
        if ',' in bname:
            bname = bname.split(',')
            aname = bname[0]
            position = bname[1]
            print('{0}: {1}'.format(position, aname))
            print('{0} {1}'.format(email, phone))
        else:
            bname = bname.replace('Commissioner', '').strip()
            print('{0}*'.format(bname))
            print('{0}, {1}'.format(email, phone))
            nclink = clink.split('/')[-1:][0][0]
            print(nclink)
    print('\n Next Block \n\n')


"""
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

"""