#!/usr/bin/env python

import os, sys
import pylab
import urllib2
import BeautifulSoup as bs
import re, glob
import datetime

##########################
def parsey(u):
    data = []
#    ll = u.read().split('\n')
    ll = u.read()
    st = ''
    for l in ll:
        if l in ['\n', '\t']:
            continue
        st += l

    ll = st.split('/div>')
    for l in ll:
#        print '****************'
#        print l
        l = l.replace('&#039;','')       
#        l = l.replace('<strong>','')
#        l = l.replace('</strong>','')
        m = re.search('<div.+\"show\"(.+)', l)
        if m:
#            print '****************'
#            print m.group(1)
            sh = m.group(1)
            mm = re.search('">(.+)</a', sh)
            try:
                sh = mm.group(1)
            except AttributeError:
                pass
            
        m = re.search('<div.+\"episode\"(.+)', l)
        if m:
#            print '****************'
#            print l, m.group(1)
            ep = m.group(1)
            mm = re.search('>(.+?)<span', ep)
            try:
#                print ep
                ep = mm.group(1)
            except AttributeError:
                pass

            mm = re.search('href.+>(.+?)</a>', ep)
            if mm:
                ep = mm.group(1)

        m = re.search('<div.+\"ratings\"(.+)', l)
        if m:
#            print '****************'
#            print l, m.group(1)
            rat = m.group(1)
            mm = re.search('Rating:</strong>(.+?)</li', rat)
            try:
#                print rat
                rat = mm.group(1)
            except:
                print l, '||||', rat

            ep = ep.replace('<','')
            ep = ep.replace('>','')
            ep = ep.replace('\"','')
            ep = ep.replace(';','')
            ep = ep.replace('\r','')
            ep = ep.replace(',',' ')
            ep = ep.replace('.','')

            if 'span' in ep and 'font' in ep and 'Repeat' in ep:
                ep = 'Repeat'
            elif 'span' in ep and 'font' in ep and 'New' in ep:
                ep = 'New'

            sh = sh.replace('.','')
            sh = sh.replace(',','')

            if len(ep)<=1:
                ep = 'None'

            if 'Viewers:' in rat:
                rat = -1
            elif 'Share:' in rat:
                rat = -1
            print 'xxx', sh, '|', ep, '|', rat, len(ep)
            data.append([sh, ep, float(rat)])
    return data

##########################
def getDate(yr, mn, day, base='tvRatingsFiles'):
    ifile = '%s/%04d_%02d_%02d.html' % (base, yr, mn, day)
    if os.path.exists(ifile):
        return open(ifile)
    else:
        url = 'http://www.tvtango.com/listings/%4d/%02d/%02d' % (yr, mn, day)
        u = urllib2.urlopen(url)
        fh = open(ifile,'w')
        fh.write(u.read())
        fh.close()
        u.close()
        return open(ifile)
    


##########################
if __name__=='__main__':
    
    ofp = open('scrapeTvRatings_1.csv', 'w')
    ofp.write('sh,ep,rat,yr,mn,day,dayofweek,iday,isbb\n')
    bdate = datetime.date(1985, 10, 19)
    edate = datetime.date(2014, 3, 31)
    
#    bdate = datetime.date(2009, 11, 1)
#    edate = datetime.date(2009, 11, 1)

    ib = bdate.toordinal()
    ie = edate.toordinal()
    
    for i in range(ib, ie+1):
        dd = datetime.date.fromordinal(i)
        yr = dd.year
        mn = dd.month
        day = dd.day
        print yr, mn, day
        if mn<10 or (mn==11 and day>5) or mn>11:
#            continue
            pass
        u = getDate(yr, mn, day)
        p = parsey(u)
        u.close()
        for ip in p:
            if 'world' in ip[0].lower() and 'series' in ip[0].lower():
                isbb = 1
            elif 'NLCS' in ip[0]:
                isbb = 1
            elif 'ALCS' in ip[0]:
                isbb = 1
            elif 'MLB' in ip[0]:
                isbb = 1
            elif 'football' in ip[0].lower():
                isbb = 2
            elif 'super bowl' in ip[0].lower():
                isbb = 2
            elif 'AFC ' in ip[0]:
                isbb = 2
            elif 'NFC ' in ip[0]:
                isbb = 2
            elif 'BCS ' in ip[0]:
                isbb = 2
            elif 'NFL ' in ip[0]:
                isbb = 2
            else:
                isbb = 0
            print ip, dd.weekday(), isbb
            ofp.write('%s,%s,%.1f,%d,%d,%d,%d,%d,%d\n' \
                          % (ip[0], ip[1], ip[2], 
                             dd.year, dd.month, dd.day, 
                             dd.weekday(), i, isbb))
    ofp.close()

#http://www.tvtango.com/listings/1985/10/19
