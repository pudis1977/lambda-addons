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

import urllib,urllib2,re,os,threading,datetime,time,base64,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
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
        global action
        params = {}
        splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
        for param in splitparams:
            if (len(param) > 0):
                splitparam = param.split('=')
                key = splitparam[0]
                try:    value = splitparam[1].encode("utf-8")
                except: value = splitparam[1]
                params[key] = value

        try:        action = urllib.unquote_plus(params["action"])
        except:     action = None
        try:        channel = urllib.unquote_plus(params["channel"])
        except:     channel = None

        if action == None:                          channels().get()
        elif action == 'dialog':                    channels().dialog()
        elif action == 'epg_menu':                  contextMenu().epg(channel)
        elif action == 'refresh':                   index().container_refresh()
        elif action == 'play':                      resolver().run(channel)

        xbmcplugin.setContent(int(sys.argv[1]), 'Episodes')
        xbmcplugin.setPluginFanart(int(sys.argv[1]), addonFanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return

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

class player(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)

    def run(self, name, title, url, image, epg):
        meta = {'Label': title, 'Title': title, 'Studio': name, 'Duration': '1440', 'Plot': epg}

        item = xbmcgui.ListItem(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo( type="Video", infoLabels = meta )

        xbmc.PlayList(xbmc.PLAYLIST_VIDEO).clear()
        xbmc.Player().play(url, item)

    def onPlayBackStarted(self):
        return

    def onPlayBackEnded(self):
        return

    def onPlayBackStopped(self):
        return

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

    def dialogList(self, dialogList):
        selectList = []
        playerList = []
        for i in dialogList:
            try:
                name, epg = i['name'], i['epg']
                if getSetting(name) == "false": raise Exception()
                title = epg.split('\n')[0].split('-', 1)[-1].rsplit('[', 1)[0].strip()
                if title == name: title = language(30403).encode("utf-8")
                label = "[B]%s[/B] - %s" % (name.encode("utf-8"), title)
                playerList.append({'name': name, 'title': title, 'epg': epg})
                selectList.append(label)
            except:
                pass

        select = index().selectDialog(selectList)
        if not select > -1: return

        name = playerList[select]['name']
        title = playerList[select]['title']
        epg = playerList[select]['epg']
        url = resolver().run(name)
        if url is None: return
        meta = {'Label': title, 'Title': title, 'Studio': name, 'Duration': '1440', 'Plot': epg}
        image = '%s/%s.png' % (addonLogos, re.sub('\s[(]\d{1}[)]','', name))

        item = xbmcgui.ListItem(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo( type="Video", infoLabels= meta )
        #item.setProperty("IsPlayable", "true")
        xbmc.Player().play(url, item)

    def channelList(self, channelList):
        count = 0
        total = len(channelList)
        for i in channelList:
            try:
                name, epg = i['name'], i['epg']
                if getSetting(name) == "false": raise Exception()
                sysname = urllib.quote_plus(name.replace(' ','_'))

                u = '%s?action=play&channel=%s&t=%s' % (sys.argv[0], sysname, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                meta = {'Label': name, 'Title': name, 'Studio': name, 'Duration': '1440', 'Plot': epg}

                image = '%s/%s.png' % (addonLogos, re.sub('\s[(]\d{1}[)]','', name))
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=epg_menu&channel=%s)' % (sys.argv[0], sysname)))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=refresh)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
                item.setInfo( type="Video", infoLabels = meta )
                #item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

class contextMenu:
    def epg(self, channel):
        try:
            epgList = []
            channel = channel.replace('_',' ')
            channel = re.sub('\s[(]\d{1}[)]','', channel)

            now = datetime.datetime.now()
            now = '%04d' % now.year + '%02d' % now.month + '%02d' % now.day + '%02d' % now.hour + '%02d' % now.minute + '%02d' % now.second

            file = open(addonEPG,'r')
            read = file.read()
            file.close()
            programmes = re.compile('(<programme.+?</programme>)').findall(read)
        except:
            return
        for programme in programmes:
            try:
                match = common.parseDOM(programme, "programme", ret="channel")[0]
                if not channel == match: raise Exception()

                start = common.parseDOM(programme, "programme", ret="start")[0]
                start = re.split('\s+', start)[0]
                stop = common.parseDOM(programme, "programme", ret="stop")[0]
                stop = re.split('\s+', stop)[0]
                if not (int(start) <= int(now) <= int(stop) or int(start) >= int(now)): raise Exception()

                start = datetime.datetime(*time.strptime(start, "%Y%m%d%H%M%S")[:6])
                title = common.parseDOM(programme, "title")[0]
                title = common.replaceHTMLCodes(title)
                if channel == title : title = language(30403).encode("utf-8")
                epg = "%s    %s" % (str(start), title)
                epgList.append(epg)
            except:
                pass

        select = index().selectDialog(epgList, header='%s - %s' % (language(30402).encode("utf-8"), channel))
        return

class channels:
    def __init__(self):
        self.list = []
        self.epg = {}
        if not (os.path.isfile(addonEPG) and index().getProperty("htv_Service_Running") == ''):
            index().infoDialog(language(30301).encode("utf-8"))

    def get(self):
        self.list = self.channel_list()
        index().channelList(self.list)

    def dialog(self):
        self.list = self.channel_list()
        index().dialogList(self.list)

    def channel_list(self):
        try:
            self.epg_list()

            file = open(addonChannels,'r')
            result = file.read()
            file.close()
            channels = common.parseDOM(result, "channel", attrs = { "active": "True" })
        except:
            return

        for channel in channels:
            try:
                name = common.parseDOM(channel, "name")[0]

                type = common.parseDOM(channel, "type")[0]

                url = common.parseDOM(channel, "url")[0]
                url = common.replaceHTMLCodes(url)

                try: type2 = common.parseDOM(channel, "type2")[0]
                except: type2 = "False"

                try: url2 = common.parseDOM(channel, "url2")[0]
                except: url2 = "False"
                url2 = common.replaceHTMLCodes(url2)



                epg = common.parseDOM(channel, "epg")[0]
                try: epg = self.epg[re.sub('\s[(]\d{1}[)]','', name)]
                except: epg = "[B][%s] - %s[/B]\n%s" % (language(30361), name, language(int(epg)))
                epg = common.replaceHTMLCodes(epg)

                self.list.append({'name': name, 'epg': epg, 'url': url, 'type': type, 'url2': url2, 'type2': type2})
            except:
                pass

        return self.list

    def epg_list(self):
        try:
            now = datetime.datetime.now()
            now = '%04d' % now.year + '%02d' % now.month + '%02d' % now.day + '%02d' % now.hour + '%02d' % now.minute + '%02d' % now.second

            file = open(addonEPG,'r')
            read = file.read()
            file.close()
            programmes = re.compile('(<programme.+?</programme>)').findall(read)
        except:
            return

        for programme in programmes:
            try:
                start = re.compile('start="(.+?)"').findall(programme)[0]
                start = re.split('\s+', start)[0]

                stop = re.compile('stop="(.+?)"').findall(programme)[0]
                stop = re.split('\s+', stop)[0]
                if not int(start) <= int(now) <= int(stop): raise Exception()

                channel = common.parseDOM(programme, "programme", ret="channel")[0]

                title = common.parseDOM(programme, "title")[0]
                title = common.replaceHTMLCodes(title).encode('utf-8')

                desc = common.parseDOM(programme, "desc")[0]
                desc = common.replaceHTMLCodes(desc).encode('utf-8')

                epg = "[B][%s] - %s[/B]\n%s" % ('ÔÙÑÁ'.decode('iso-8859-7').encode('utf-8'), title, desc)

                self.epg.update({channel: epg})
            except:
                pass

class resolver:
    def run(self, channel):
        try:
            data = channels().channel_list()
            channel = channel.replace('_',' ')

            i = [x for x in data if channel == x['name']]
            name, epg, url, type, url2, type2 = i[0]['name'], i[0]['epg'], i[0]['url'], i[0]['type'], i[0]['url2'], i[0]['type2']
            image = '%s/%s.png' % (addonLogos, name)

            playerDict = {
                ''                  : self.direct,
                'http'              : self.http,
                'hls'               : self.hls,
                'visionip'          : self.visionip,
                'skai'              : self.skai,
                'madtv'             : self.madtv,
                'streamago'         : self.streamago,
                'viiideo'           : self.viiideo,
                'dailymotion'       : self.dailymotion,
                'livestream_new'    : self.livestream_new,
                'livestream'        : self.livestream,
                'ustream'           : self.ustream,
                'veetle'            : self.veetle
            }

            dialog = xbmcgui.DialogProgress()
            dialog.create(addonName.encode("utf-8"), language(30341).encode("utf-8"))
            dialog.update(0)

            url = playerDict[type](url)
            if url is None and not type2 == "False": url = playerDict[type2](url2)
            if url is None: url = fallback

            dialog.close()

            if not xbmc.getInfoLabel('ListItem.Plot') == '' : epg = xbmc.getInfoLabel('ListItem.Plot')
            title = epg.split('\n')[0].split('-', 1)[-1].rsplit('[', 1)[0].strip()

            player().run(name, title, url, image, epg)
            return url
        except:
            index().infoDialog(language(30302).encode("utf-8"))
            return

    def direct(self, url):
        return url

    def http(self, url):
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            response.close()
            response = response.info()
            return url
        except:
            return

    def hls(self, url):
        try:
            result = getUrl(url).result
            if "EXTM3U" in result: return url
        except:
            return

    def visionip(self, url):
        try:
            root = 'http://tvnetwork.new.visionip.tv/Hellenic_TV'
            result = getUrl(root, close=False).result
            result = getUrl(url).result
            result = common.parseDOM(result, "entry")[0]
            streamer = common.parseDOM(result, "param", ret="value")[0]
            playPath = common.parseDOM(result, "ref", ret="href")[0]
            url = '%s/%s live=1 timeout=10' % (streamer, playPath)
            return url
        except:
            return

    def skai(self, url):
        try:
            root = 'http://www.skai.gr/ajax.aspx?m=NewModules.LookupMultimedia&mmid=/Root/TVLive'
            result = getUrl(root).result
            url = common.parseDOM(result, "File")[0]
            url = url.split('[')[-1].split(']')[0]
            url = 'http://www.youtube.com/watch?v=%s' % url

            result = getUrl(url).result
            url = re.compile('"hlsvp": "(.+?)"').findall(result)[0]
            url = urllib.unquote(url).replace('\\/', '/')
            return url
        except:
            return

    def madtv(self, url):
        try:
            result = getUrl(url, timeout=30).result
            url = common.parseDOM(result, "iframe", ret="src")
            url = [i for i in url if 'apps.' in i][0]
            if not url.startswith('http://'): url = url.replace('//', 'http://') 

            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src")[0]
            url = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            url = 'http://www.youtube.com/watch?v=%s' % url

            result = getUrl(url).result
            url = re.compile('"hlsvp": "(.+?)"').findall(result)[0]
            url = urllib.unquote(url).replace('\\/', '/')
            return url
        except:
            return

    def viiideo(self, url):
        try:
            result = getUrl(url).result
            url = re.compile("ipadUrl.+?'http://(.+?)/playlist[.]m3u8'").findall(result)[0]
            url = 'rtmp://%s live=1 timeout=10' % url
            return url
        except:
            return

    def dailymotion(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('"flashvars".+?value="(.+?)"').findall(result)[0]
            url = urllib.unquote(url).decode('utf-8').replace('\\/', '/')
            quality = None
            try: quality = re.compile('"ldURL":"(.+?)"').findall(url)[0]
            except: pass
            try: quality = re.compile('"sdURL":"(.+?)"').findall(url)[0]
            except: pass
            try: quality = re.compile('"hqURL":"(.+?)"').findall(url)[0]
            except: pass
            quality += '&redirect=0'
            url = getUrl(quality).result
            url = '%s live=1 timeout=10' % url
            return url
        except:
            return

    def livestream_new(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('"m3u8_url":"(.+?)"').findall(result)[0]
            result = getUrl(url).result
            url = re.compile('(http://.+)').findall(result)[0]
            return url
        except:
            return

    def livestream(self, url):
        try:
            name = url.split("/")[-1]
            url = 'http://x%sx.api.channel.livestream.com/3.0/getstream.json' % name
            result = getUrl(url).result
            isLive = str(result.find('isLive":true'))
            if isLive == '-1': return
            url = re.compile('"httpUrl".+?"(.+?)"').findall(result)[0]
            return url
        except:
            return

    def streamago(self, url):
        try:
            result = getUrl(url + '/xml/').result
            url = common.parseDOM(result, "path_rtsp")[0]
            url = url.split('[')[-1].split(']')[0]
            return url
        except:
            return

    def ustream(self, url):
        try:
            try:
                result = getUrl(url).result
                id = re.compile('ustream.tv/embed/(.+?)"').findall(result)[0]
            except:
                id = url.split("/embed/")[-1]
            #url = 'http://iphone-streaming.ustream.tv/uhls/%s/streams/live/iphone/playlist.m3u8' % id
            url = 'http://sjc-uhls-proxy-beta01.ustream.tv/watch/playlist.m3u8?cid=%s' % id
            for i in range(1, 51):
                result = getUrl(url).result
                if "EXT-X-STREAM-INF" in result: return url
                if not "EXTM3U" in result: return
            return
        except:
            return

    def veetle(self, url):
        try:
            xbmc.executebuiltin('RunScript(%s)' % akamaiProxy)
            name = url.split("#")[-1]
            url = 'http://www.veetle.com/index.php/channel/ajaxStreamLocation/%s/flash' % name
            result = getUrl(url).result
            try: import json
            except: import simplejson as json
            url = json.loads(result)
            import base64
            url = base64.encodestring(url['payload']).replace('\n', '')
            url = 'http://127.0.0.1:64653/veetle/%s' % url
            return url
        except:
            return

main()