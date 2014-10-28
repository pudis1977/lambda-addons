# -*- coding: utf-8 -*-

'''
    Hellenic TV XBMC Addon
    Copyright (C) 2014 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib,urllib2,re,os,threading,datetime,time,xbmc,xbmcplugin,xbmcgui,xbmcaddon
from operator import itemgetter
try:    import json
except: import simplejson as json
try:    import CommonFunctions
except: import commonfunctionsdummy as CommonFunctions


action              = None
common              = CommonFunctions
language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonFullId         = addonName + addonVersion
addonIcon           = os.path.join(addonPath,'icon.png')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
addonEPG            = os.path.join(addonPath,'xmltv.xml')
addonChannels       = os.path.join(addonPath,'channels.xml')
addonLogos          = os.path.join(addonPath,'resources/logos')
addonSlideshow      = os.path.join(addonPath,'resources/slideshow')
addonStrings        = os.path.join(addonPath,'resources/language/Greek/strings.xml')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
fallback            = os.path.join(addonPath,'resources/fallback/fallback.mp4')
akamaiProxy         = os.path.join(addonPath,'akamaisecurehd.py')


class main:
    def __init__(self):
        while (not xbmc.abortRequested):
            epg()
            count = 60
            while (not xbmc.abortRequested) and count > 0:
                count -= 1
                time.sleep(1)

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post is None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0')
        if not referer is None:
            request.add_header('Referer', referer)
        if not cookie is None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

class uniqueList(object):
    def __init__(self, list):
        uniqueSet = set()
        uniqueList = []
        for n in list:
            if n not in uniqueSet:
                uniqueSet.add(n)
                uniqueList.append(n)
        self.list = uniqueList

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)

class index:
    def infoDialog(self, str, header=addonName):
        try: xbmcgui.Dialog().notification(header, str, addonIcon, 3000, sound=False)
        except: xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, addonIcon))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName, str3='', str4=''):
        answer = xbmcgui.Dialog().yesno(header, str1, str2, '', str4, str3)
        return answer

    def getProperty(self, str):
        property = xbmcgui.Window(10000).getProperty(str)
        return property

    def setProperty(self, str1, str2):
        xbmcgui.Window(10000).setProperty(str1, str2)

    def clearProperty(self, str):
        xbmcgui.Window(10000).clearProperty(str)

    def addon_status(self, id):
        check = xbmcaddon.Addon(id=id).getAddonInfo("name")
        if not check == addonName: return True

    def container_refresh(self):
        xbmc.executebuiltin("Container.Refresh")

class epg:
    def __init__(self):
        if xbmc.abortRequested == True: sys.exit()
        try:
            t1 = datetime.datetime.utcfromtimestamp(os.path.getmtime(addonEPG))
            t2 = datetime.datetime.utcnow()
            update = abs(t2 - t1) > datetime.timedelta(hours=24)
            if update is False: return
        except:
            pass
        if index().getProperty('htv_Service_Running') == 'true': return
        index().setProperty('htv_Service_Running', 'true')

        self.xmltv = ''
        self.get_dates()
        self.get_channels()
        threads = []
        threads.append(Thread(self.ote_data))
        [i.start() for i in threads]
        [i.join() for i in threads]
        self.xmltv_creator()

        index().clearProperty('htv_Service_Running')

    def get_dates(self):
        if xbmc.abortRequested == True: sys.exit()
        try:
            self.dates = []
            now = self.greek_datetime()
            today = datetime.date(now.year, now.month, now.day)
            for i in range(0, 3):
                d = today + datetime.timedelta(days=i)
                self.dates.append(str(d))
        except:
            return

    def get_channels(self):
        if xbmc.abortRequested == True: sys.exit()
        try:
            self.channels = []
            self.dummyData = {}
            file = open(addonChannels,'r')
            channels = file.read()
            file.close()
            file = open(addonStrings,'r')
            strings = file.read()
            file.close()
            channels = common.parseDOM(channels, "channel", attrs = { "active": "True" })
        except:
            return
        for channel in channels:
            try:
                epg = common.parseDOM(channel, "epg")[0]
                epg = common.parseDOM(strings, "string", attrs = { "id": epg })[0]
                channel = common.parseDOM(channel, "name")[0]
                self.channels.append(channel)
                self.dummyData.update({channel: epg})
            except:
                pass

    def ote_data(self):
        if xbmc.abortRequested == True: sys.exit()
        threads = []
        self.oteData = []
        for date in self.dates:
            date = date.replace('-','')
            url = 'http://otetv.ote.gr/otetv_program/ProgramListServlet?t=sat&d=%s' % date
            threads.append(Thread(self.ote_data2, date, url))
        [i.start() for i in threads]
        [i.join() for i in threads]

    def ote_data2(self, date, url):
        if xbmc.abortRequested == True: sys.exit()
        try:
            result = getUrl(url).result
            self.oteData.append({'date': date, 'value': result})
        except:
            return

    def ote_programme(self, channel, id):
        if xbmc.abortRequested == True: sys.exit()
        programmes = []
        programmeList = []

        for data in self.oteData:
            try:
                date = data["date"]
                data = data["value"]
                data = json.loads(data)
                data = data["titles"][id]
                data = data.iteritems()
                [programmes.append({'date': date, 'value': value}) for key, value in data]
            except:
                pass

        for programme in programmes:
            try:
                date = programme["date"]
                programme = programme["value"]
                start = programme["start"].replace(':','')
                start = date + str('%04d' % int(start)) + '00'
                start = self.start_processor(start)
                title = programme["title"]
                title = self.title_prettify(title)
                subtitle = programme["category"]
                desc = programme["desc"].split("<br/>")[-1]
                desc = self.desc_prettify(desc)
                programmeList.append({'start': start, 'title': title, 'desc': desc})
            except:
                pass

        self.programme_creator(channel, programmeList)

    def tvc_data(self, id):
        if xbmc.abortRequested == True: sys.exit()
        threads = []
        self.tvcData = []
        for date in self.dates:
            date = date.replace('-','')
            url = 'http://www.tvcontrol.gr/json/events/channel_%s_0.json?d=%s000000' % (id, date)
            threads.append(Thread(self.tvc_data2, date, url))
        [i.start() for i in threads]
        [i.join() for i in threads]

    def tvc_data2(self, date, url):
        if xbmc.abortRequested == True: sys.exit()
        try:
            result = getUrl(url).result
            self.tvcData.append({'date': date, 'value': result})
        except:
            return

    def tvc_programme(self, channel, id):
        if xbmc.abortRequested == True: sys.exit()
        self.tvc_data(id)
        self.tvcData = sorted(self.tvcData, key=itemgetter('date'))
        programmes = []
        programmeList = []

        for data in self.tvcData:
            try:
                date = data["date"]
                d = json.loads(data["value"])
                data = []
                for i in range(0, len(d)): data += d[i]["events"]
                [programmes.append({'date': date, 'value': value}) for value in data]
            except:
                pass

        for programme in programmes:
            try:
                date = programme["date"]
                programme = programme["value"]
                start = programme["event_time"].replace(':','')
                start = date + str('%04d' % int(start)) + '00'
                start = self.start_processor(start)
                title = programme["constructed_titlegr"]
                title = self.title_prettify(title)
                descDict = {'1': '¡ËÎÁÙÈÍ‹', '3': '≈È‰ﬁÛÂÈÚ', '4': 'ÕÙÔÍÈÏ·ÌÙ›Ò', '5': '–·È‰ÈÍ‹', '6': '‘·ÈÌﬂ·', '8': '”ÂÈÒ‹', '10': 'ÿı˜·„˘„ﬂ·'}
                desc = programme["main_genre_id"]
                try: desc = descDict[desc].decode('iso-8859-7')
                except: desc = descDict['10'].decode('iso-8859-7')
                programmeList.append({'start': start, 'title': title, 'desc': desc})
            except:
                pass

        self.programme_creator(channel, programmeList)

    def dummy_programme(self, channel):
        if xbmc.abortRequested == True: sys.exit()
        programmeList = []
        desc = self.dummyData[channel]
        self.get_titleDict()

        for date in self.dates:
            for i in range(0, 2400, 1200):
                start = date.replace('-','') + '%04d' % i + '00'
                start = self.start_processor(start)
                try: title = self.titleDict[channel]
                except: title = channel
                programmeList.append({'start': start, 'title': title, 'desc': desc})

        self.programme_creator(channel, programmeList)

    def greek_datetime(self):
        if xbmc.abortRequested == True: sys.exit()
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours = 2)
        d = datetime.datetime(dt.year, 4, 1)
        dston = d - datetime.timedelta(days=d.weekday() + 1)
        d = datetime.datetime(dt.year, 11, 1)
        dstoff = d - datetime.timedelta(days=d.weekday() + 1)
        if dston <=  dt < dstoff:
            return dt + datetime.timedelta(hours = 1)
        else:
            return dt

    def start_processor(self, start):
        if xbmc.abortRequested == True: sys.exit()
        dt1 = self.greek_datetime()
        dt2 = datetime.datetime.now()
        dt3 = datetime.datetime.utcnow()
        dt1 = datetime.datetime(dt1.year, dt1.month, dt1.day, dt1.hour)
        dt2 = datetime.datetime(dt2.year, dt2.month, dt2.day, dt2.hour)
        dt3 = datetime.datetime(dt3.year, dt3.month, dt3.day, dt3.hour)
        start = datetime.datetime(*time.strptime(start, "%Y%m%d%H%M%S")[:6])
        if dt2 >= dt1 :
            dtd = (dt2 - dt1).seconds/60/60
            tz = (dt1 - dt3).seconds/60/60
            tz = ' +' + '%02d' % (dtd + tz) + '00'
            start = start + datetime.timedelta(hours = int(dtd))
        else:
            dtd = (dt1 - dt2).seconds/60/60
            tz = (dt1 - dt3).seconds/60/60
            tz = ' -' + '%02d' % (dtd - tz) + '00'
            start = start - datetime.timedelta(hours = int(dtd))
        start = '%04d' % start.year + '%02d' % start.month + '%02d' % start.day + '%02d' % start.hour + '%02d' % start.minute + '%02d' % start.second + tz
        return start

    def title_prettify(self, title):
        if xbmc.abortRequested == True: sys.exit()
        acuteDict = {u'\u0386': u'\u0391', u'\u0388': u'\u0395', u'\u0389': u'\u0397', u'\u038A': u'\u0399', u'\u038C': u'\u039F', u'\u038E': u'\u03A5', u'\u038F': u'\u03A9', u'\u0390': u'\u03AA', u'\u03B0': u'\u03AB'}
        title = common.replaceHTMLCodes(title)
        title = title.strip().upper()
        for key in acuteDict:
            title = title.replace(key, acuteDict[key])
        return title

    def desc_prettify(self, desc):
        if xbmc.abortRequested == True: sys.exit()
        desc = common.replaceHTMLCodes(desc)
        desc = desc.strip()
        return desc

    def xml_attrib(self, str):
        if xbmc.abortRequested == True: sys.exit()
        str = str.replace("&", "&amp;")
        str = str.replace("'", "&apos;")
        str = str.replace("\"", "&quot;")
        str = str.replace("<", "&lt;")
        str = str.replace(">", "&gt;")
        return str

    def programme_creator(self, channel, list):
        if xbmc.abortRequested == True: sys.exit()
        list = sorted(list, key=itemgetter('start'))
        for i in range(0, len(list)):
            start = list[i]['start']
            try: stop = list[i+1]['start']
            except: stop = list[i]['start']
            title = list[i]['title']
            desc = list[i]['desc']
            channel, title, desc = self.xml_attrib(channel), self.xml_attrib(title), self.xml_attrib(desc)
            self.xmltv += '<programme channel="%s" start="%s" stop="%s">\n' % (channel, start, stop)
            self.xmltv += '<title lang="el">%s</title>\n' % (title)
            self.xmltv += '<desc>%s</desc>\n' % (desc)
            self.xmltv += '</programme>\n'

    def xmltv_creator(self):
        if xbmc.abortRequested == True: sys.exit()
        self.xmltv += '<tv>\n'
        for channel in self.channels:
            channel = self.xml_attrib(channel)
            self.xmltv += '<channel id="%s">\n' % (channel)
            self.xmltv += '<display-name>%s</display-name>\n' % (channel)
            self.xmltv += '<icon src="%s/%s.png"/>\n' % (addonLogos, channel)
            self.xmltv += '<stream>plugin://plugin.video.hellenic.tv/?action=play&amp;channel=%s</stream>\n' % (channel.replace(' ','_'))
            self.xmltv += '</channel>\n'

        self.get_channelDict()
        for channel in self.channels:
            try: self.channelDict[channel]
            except: self.dummy_programme(channel)
        self.xmltv += '</tv>'

        try: os.remove(addonEPG)
        except: pass
        file = open(addonEPG, 'w')
        file.write(self.xmltv.replace('\n','').encode('utf8'))
        file.close()

    def get_channelDict(self):
        self.channelDict = {
            'MEGA'                      : self.ote_programme("MEGA", "90"),
            'ANT1'                      : self.ote_programme("ANT1", "150"),
            'STAR'                      : self.ote_programme("STAR", "98"),
            'ALPHA'                     : self.ote_programme("ALPHA", "132"),
            'SKAI'                      : self.ote_programme("SKAI", "120"),
            'MACEDONIA TV'              : self.ote_programme("MACEDONIA TV", "152"),
            'NERIT'                     : self.ote_programme("NERIT", "593"),
            'BOYLH TV'                  : self.ote_programme("BOYLH TV", "119"),
            'EURONEWS'                  : self.ote_programme("EURONEWS", "19"),
            #'NICKELODEON'              : self.ote_programme("NICKELODEON", "117"),
            #'MTV'                      : self.ote_programme("MTV", "121"),
            'MAD TV'                    : self.ote_programme("MAD TV", "144"),
            'KONTRA CHANNEL'            : self.ote_programme("KONTRA CHANNEL", "44"),
            'EXTRA 3'                   : self.ote_programme("EXTRA 3", "135"),
            'ART CHANNEL'              : self.ote_programme("ART CHANNEL", "156"),
            #'ZOOM'                     : self.ote_programme("ZOOM", "157"),
            'BLUE SKY'                  : self.ote_programme("BLUE SKY", "153"),
            #'CHANNEL 9'                : self.ote_programme("CHANNEL 9", "163"),
            #'SBC TV'                   : self.ote_programme("SBC TV", "136"),
            'TV 100'                    : self.ote_programme("TV 100", "137"),
            '4E TV'                     : self.ote_programme("4E TV", "133"),
            #'STAR KENTRIKIS ELLADOS'    : self.ote_programme("STAR KENTRIKIS ELLADOS", "139"),
            'EPIRUS TV1'                : self.ote_programme("EPIRUS TV1", "145"),
            'CORFU CHANNEL'             : self.ote_programme("CORFU CHANNEL", "166"),
            'BEST TV'                   : self.ote_programme("BEST TV", "165"),
            'KRITI TV'                  : self.ote_programme("KRITI TV", "138"),
            'TV AIGAIO'                 : self.ote_programme("TV AIGAIO", "164"),
            'DIKTYO TV'                 : self.ote_programme("DIKTYO TV", "146"),
            'DELTA TV'                  : self.ote_programme("DELTA TV", "147"),

            'E TV'                      : self.tvc_programme("E TV", "326"),
            'ACTION 24'                 : self.tvc_programme("ACTION 24", "189"),
            'MEGA CYPRUS'               : self.tvc_programme("MEGA CYPRUS", "306"),
            'ANT1 CYPRUS'               : self.tvc_programme("ANT1 CYPRUS", "258"),
            'SIGMA'                     : self.tvc_programme("SIGMA", "305"),
            #'TV PLUS'                  : self.tvc_programme("TV PLUS", "289"),
            #'EXTRA TV'                 : self.tvc_programme("EXTRA TV", "290"),
            'CAPITAL'                   : self.tvc_programme("CAPITAL", "282"),
            'RIK SAT'                   : self.tvc_programme("RIK SAT", "83")
        }

    def get_titleDict(self):
        self.titleDict = {
            'RIK SAT'                   : 'ƒœ—’÷œ—… œ —… '.decode('iso-8859-7'),
            'NICKELODEON+'              : '–¡…ƒ… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7'),
            'MUSIC TV'                  : 'Ãœ’”… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7'),
            'GREEK CINEMA'              : '≈ÀÀ«Õ… « ‘¡…Õ…¡'.decode('iso-8859-7'),
            'CY SPORTS'                 : '¡»À«‘… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7'),
            'ODIE TV'                   : '…––œƒ—œÃ…≈”'.decode('iso-8859-7'),
            'SMILE TV'                  : '–¡…ƒ… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7'),
            'GNOMI TV'                  : 'Ãœ’”… œ –—œ√—¡ÃÃ¡'.decode('iso-8859-7')
        }


main()