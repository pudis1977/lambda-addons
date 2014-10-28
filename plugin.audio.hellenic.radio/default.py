# -*- coding: utf-8 -*-

'''
    Hellenic Radio XBMC Addon
    Copyright (C) 2013 lambda

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
addonDesc           = language(30450).encode("utf-8")
addonRadios         = os.path.join(addonPath,'radios.xml')
addonIcon           = os.path.join(addonPath,'icon.png')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
addonArt            = os.path.join(addonPath,'resources/art')
addonLogos          = os.path.join(addonPath,'resources/logos')
addonSlideshow      = os.path.join(addonPath,'resources/slideshow')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
favData             = os.path.join(dataPath,'favourites.cfg')


class main:
    def __init__(self):
        global action
        index().container_data()
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
        try:        radio = urllib.unquote_plus(params["radio"])
        except:     radio = None
        try:        area = urllib.unquote_plus(params["area"])
        except:     area = None

        if action == None:                          root().get()
        elif action == 'favourite_add':             contextMenu().favourite_add(favData, radio, area)
        elif action == 'favourite_delete':          contextMenu().favourite_delete(favData, radio, area)
        elif action == 'favourite_moveUp':          contextMenu().favourite_moveUp(favData, radio, area)
        elif action == 'favourite_moveDown':        contextMenu().favourite_moveDown(favData, radio, area)
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'view_radios':               contextMenu().view('radios')
        elif action == 'radios_favourites':         favourites().radios()
        elif action	== 'radios_all':                radios().all()
        elif action	== 'radios_international':      radios().international()
        elif action	== 'radios_eclectic':           radios().eclectic()
        elif action	== 'radios_rock':               radios().rock()
        elif action	== 'radios_greek':              radios().greek()
        elif action	== 'radios_laika':              radios().laika()
        elif action	== 'radios_sports':             radios().sports()
        elif action	== 'radios_news':               radios().news()
        elif action	== 'radios_religious':          radios().religious()
        elif action	== 'radios_traditional':        radios().traditional()
        elif action	== 'radios_attica':             radios().attica()
        elif action	== 'radios_salonica':           radios().salonica()
        elif action	== 'radios_internet':           radios().internet()
        elif action	== 'radios_aegean':             radios().aegean()
        elif action	== 'radios_epirus':             radios().epirus()
        elif action	== 'radios_thessaly':           radios().thessaly()
        elif action	== 'radios_thrace':             radios().thrace()
        elif action	== 'radios_ionian':             radios().ionian()
        elif action	== 'radios_crete':              radios().crete()
        elif action	== 'radios_cyprus':             radios().cyprus()
        elif action	== 'radios_macedonia':          radios().macedonia()
        elif action	== 'radios_peloponnese':        radios().peloponnese()
        elif action	== 'radios_centralgreece':      radios().centralgreece()
        elif action == 'play':                      resolver().run(radio, area)

        if action is None or action.startswith('root'):
            xbmcplugin.setContent(int(sys.argv[1]), 'albums')
        elif action.startswith('radios'):
            xbmcplugin.setContent(int(sys.argv[1]), 'albums')
            index().container_view('radios', {'skin.confluence' : 500})
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

    def run(self, name, band, genre, area, desc, url, image):
        meta = {'Label': name, 'Title': name, 'Album': name, 'Artist': band, 'Genre': genre, 'Duration': '1440', 'Comment': desc}

        item = xbmcgui.ListItem(path=url, iconImage=image, thumbnailImage=image)
        item.setInfo( type="Video", infoLabels = { "title": "" } )
        item.setInfo( type="Music", infoLabels = meta )
        item.setProperty("Album_Label", area)
        item.setProperty("Album_Description", desc)

        xbmc.PlayList(xbmc.PLAYLIST_MUSIC).clear()
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

    def container_data(self):
        if not os.path.exists(dataPath):
            os.makedirs(dataPath)
        if not os.path.isfile(favData):
            file = open(favData, 'w')
            file.write('')
            file.close()
        if not os.path.isfile(viewData):
            file = open(viewData, 'w')
            file.write('')
            file.close()

    def container_view(self, content, viewDict):
        try:
            skin = xbmc.getSkinDir()
            file = xbmcvfs.File(viewData)
            read = file.read().replace('\n','')
            file.close()
            view = re.compile('"%s"[|]"%s"[|]"(.+?)"' % (skin, content)).findall(read)[0]
            xbmc.executebuiltin('Container.SetViewMode(%s)' % str(view))
        except:
            try:
                id = str(viewDict[skin])
                xbmc.executebuiltin('Container.SetViewMode(%s)' % id)
            except:
                pass

    def rootList(self, rootList):
        count = 0
        total = len(rootList)
        for i in rootList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Music", infoLabels={ "Label": name, "Title": name, 'Album': name, 'Artist': addonName } )
                item.setProperty("Album_Description", addonDesc)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems([], replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def radioList(self, radioList):
        file = xbmcvfs.File(favData)
        favRead = file.read()
        file.close()

        count = 0
        total = len(radioList)
        for i in radioList:
            try:
                name, band, genre, area, desc, url = i['name'], i['band'], i['genre'], i['area'], i['desc'], i['url']
                sysname, sysarea = urllib.quote_plus(name.replace(' ','_')), urllib.quote_plus(area.replace(' ','_'))

                u = '%s?action=play&radio=%s&area=%s&t=%s' % (sys.argv[0], sysname, sysarea, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))
                meta = {'Label': name, 'Title': name, 'Album': name, 'Artist': band, 'Genre': genre, 'Duration': '1440', 'Comment': desc}

                image = '%s/%s/%s.png' % (addonLogos, area, name)
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1

                cm = []
                if action == 'radios_favourites':
                    if getSetting("fav_sort") == '3': cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&radio=%s&area=%s)' % (sys.argv[0], sysname, sysarea)))
                    if getSetting("fav_sort") == '3': cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&radio=%s&area=%s)' % (sys.argv[0], sysname, sysarea)))
                    cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&radio=%s&area=%s)' % (sys.argv[0], sysname, sysarea)))
                else:
                    if not '"%s"|"%s"' % (name, area) in favRead: cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&radio=%s&area=%s)' % (sys.argv[0], sysname, sysarea)))
                    else: cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&radio=%s&area=%s)' % (sys.argv[0], sysname, sysarea)))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=view_radios)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
                item.setInfo( type="Music", infoLabels = meta )
                #item.setProperty("IsPlayable", "true")
                item.setProperty( "Music", "true" )
                item.setProperty("Album_Label", area)
                item.setProperty("Album_Description", desc)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

class contextMenu:
    def view(self, content):
        try:
            skin = xbmc.getSkinDir()
            skinPath = xbmc.translatePath('special://skin/')
            xml = os.path.join(skinPath,'addon.xml')
            file = xbmcvfs.File(xml)
            read = file.read().replace('\n','')
            file.close()
            try: src = re.compile('defaultresolution="(.+?)"').findall(read)[0]
            except: src = re.compile('<res.+?folder="(.+?)"').findall(read)[0]
            src = os.path.join(skinPath, src)
            if xbmcgui.getCurrentWindowId() == 10501: src = os.path.join(src, 'MyMusicSongs.xml')
            else: src = os.path.join(src, 'MyMusicNav.xml')
            file = xbmcvfs.File(src)
            read = file.read().replace('\n','')
            file.close()
            views = re.compile('<views>(.+?)</views>').findall(read)[0]
            views = [int(x) for x in views.split(',')]
            for view in views:
                label = xbmc.getInfoLabel('Control.GetLabel(%s)' % (view))
                if not (label == '' or label is None): break
            file = xbmcvfs.File(viewData)
            read = file.read()
            file.close()
            file = open(viewData, 'w')
            for line in re.compile('(".+?\n)').findall(read):
                if not line.startswith('"%s"|"%s"|"' % (skin, content)): file.write(line)
            file.write('"%s"|"%s"|"%s"\n' % (skin, content, str(view)))
            file.close()
            viewName = xbmc.getInfoLabel('Container.Viewmode')
            index().infoDialog('%s%s%s' % (language(30301).encode("utf-8"), viewName, language(30302).encode("utf-8")))
        except:
            return

    def favourite_add(self, data, name, url):
        try:
            name, url = name.replace('_',' '), url.replace('_',' ')
            index().container_refresh()
            file = open(data, 'a+')
            file.write('"%s"|"%s"\n' % (name, url))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, data, name, url):
        try:
            name, url = name.replace('_',' '), url.replace('_',' ')
            index().container_refresh()
            file = open(data,'r')
            read = file.read()
            file.close()
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"|"%s"' % (name, url) in x][0]
            list = re.compile('(".+?\n)').findall(read.replace(line, ''))
            file = open(data, 'w')
            for line in list: file.write(line)
            file.close()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def favourite_moveUp(self, data, name, url):
        try:
            name, url = name.replace('_',' '), url.replace('_',' ')
            index().container_refresh()
            file = open(data,'r')
            read = file.read()
            file.close()
            list = re.compile('(".+?)\n').findall(read)
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"|"%s"' % (name, url) in x][0]
            i = list.index(line)
            if i == 0 : return
            list[i], list[i-1] = list[i-1], list[i]
            file = open(data, 'w')
            for line in list: file.write('%s\n' % (line))
            file.close()
            index().infoDialog(language(30305).encode("utf-8"), name)
        except:
            return

    def favourite_moveDown(self, data, name, url):
        try:
            name, url = name.replace('_',' '), url.replace('_',' ')
            index().container_refresh()
            file = open(data,'r')
            read = file.read()
            file.close()
            list = re.compile('(".+?)\n').findall(read)
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"|"%s"' % (name, url) in x][0]
            i = list.index(line)
            if i+1 == len(list): return
            list[i], list[i+1] = list[i+1], list[i]
            file = open(data, 'w')
            for line in list: file.write('%s\n' % (line))
            file.close()
            index().infoDialog(language(30306).encode("utf-8"), name)
        except:
            return

class favourites:
    def __init__(self):
        self.list = radios().radio_list()

    def radios(self):
        filter = []
        file = open(favData,'r')
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"').findall(read)
        for name, area in match:
            filter += [i for i in self.list if name == i['name'] and area == i['area']]

        if getSetting("fav_sort") == '0':
            filter = sorted(filter, key=itemgetter('name'))
        elif getSetting("fav_sort") == '1':
            sortDict = {'International': 1, 'Eclectic': 2, 'Rock': 3, 'Greek': 4, 'Laika': 5, 'Sports': 6, 'News': 7, 'Religious': 8, 'Traditional': 9}
            for i in range(len(filter)): filter[i]['sort'] = sortDict[filter[i]['genre']]
            filter = sorted(filter, key=itemgetter('name'))
            filter = sorted(filter, key=itemgetter('sort'))
        elif getSetting("fav_sort") == '2':
            sortDict = {'Attica': 1, 'Salonica': 2, 'Internet': 3, 'Aegean': 4, 'Epirus': 5, 'Thessaly': 6, 'Thrace': 7, 'Ionian': 8, 'Crete': 9, 'Cyprus': 10, 'Macedonia': 11, 'Peloponnese': 12, 'Central Greece': 13}
            for i in range(len(filter)): filter[i]['sort'] = sortDict[filter[i]['area']]
            filter = sorted(filter, key=itemgetter('name'))
            filter = sorted(filter, key=itemgetter('sort'))

        index().radioList(filter)

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': '01.png', 'action': 'radios_favourites'})
        rootList.append({'name': 30502, 'image': '02.png', 'action': 'radios_all'})
        rootList.append({'name': 30521, 'image': '03.png', 'action': 'radios_international'})
        rootList.append({'name': 30522, 'image': '04.png', 'action': 'radios_eclectic'})
        rootList.append({'name': 30523, 'image': '05.png', 'action': 'radios_rock'})
        rootList.append({'name': 30524, 'image': '06.png', 'action': 'radios_greek'})
        rootList.append({'name': 30525, 'image': '07.png', 'action': 'radios_laika'})
        rootList.append({'name': 30526, 'image': '08.png', 'action': 'radios_sports'})
        rootList.append({'name': 30527, 'image': '09.png', 'action': 'radios_news'})
        rootList.append({'name': 30528, 'image': '10.png', 'action': 'radios_religious'})
        rootList.append({'name': 30529, 'image': '11.png', 'action': 'radios_traditional'})
        rootList.append({'name': 30541, 'image': '12.png', 'action': 'radios_attica'})
        rootList.append({'name': 30542, 'image': '13.png', 'action': 'radios_salonica'})
        rootList.append({'name': 30543, 'image': '14.png', 'action': 'radios_internet'})
        rootList.append({'name': 30544, 'image': '15.png', 'action': 'radios_aegean'})
        rootList.append({'name': 30545, 'image': '16.png', 'action': 'radios_epirus'})
        rootList.append({'name': 30546, 'image': '17.png', 'action': 'radios_thessaly'})
        rootList.append({'name': 30547, 'image': '18.png', 'action': 'radios_thrace'})
        rootList.append({'name': 30548, 'image': '19.png', 'action': 'radios_ionian'})
        rootList.append({'name': 30549, 'image': '20.png', 'action': 'radios_crete'})
        rootList.append({'name': 30550, 'image': '21.png', 'action': 'radios_cyprus'})
        rootList.append({'name': 30551, 'image': '22.png', 'action': 'radios_macedonia'})
        rootList.append({'name': 30552, 'image': '23.png', 'action': 'radios_peloponnese'})
        rootList.append({'name': 30553, 'image': '24.png', 'action': 'radios_centralgreece'})
        index().rootList(rootList)

class radios:
    def __init__(self):
        self.list = []

    def all(self):
        filter = self.radio_list()
        index().radioList(filter)

    def international(self):
        filter = [i for i in self.radio_list() if i['genre'] == 'International']
        index().radioList(filter)

    def eclectic(self):
        filter = [i for i in self.radio_list() if i['genre'] == 'Eclectic']
        index().radioList(filter)

    def rock(self):
        filter = [i for i in self.radio_list() if i['genre'] == 'Rock']
        index().radioList(filter)

    def greek(self):
        filter = [i for i in self.radio_list() if i['genre'] == 'Greek']
        index().radioList(filter)

    def laika(self):
        filter = [i for i in self.radio_list() if i['genre'] == 'Laika']
        index().radioList(filter)

    def sports(self):
        filter = [i for i in self.radio_list() if i['genre'] == 'Sports']
        index().radioList(filter)

    def news(self):
        filter = [i for i in self.radio_list() if i['genre'] == 'News']
        index().radioList(filter)

    def religious(self):
        filter = [i for i in self.radio_list() if i['genre'] == 'Religious']
        index().radioList(filter)

    def traditional(self):
        filter = [i for i in self.radio_list() if i['genre'] == 'Traditional']
        index().radioList(filter)

    def attica(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Attica']
        index().radioList(filter)

    def salonica(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Salonica']
        index().radioList(filter)

    def internet(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Internet']
        index().radioList(filter)

    def aegean(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Aegean']
        index().radioList(filter)

    def epirus(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Epirus']
        index().radioList(filter)

    def thessaly(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Thessaly']
        index().radioList(filter)

    def thrace(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Thrace']
        index().radioList(filter)

    def ionian(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Ionian']
        index().radioList(filter)

    def crete(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Crete']
        index().radioList(filter)

    def cyprus(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Cyprus']
        index().radioList(filter)

    def macedonia(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Macedonia']
        index().radioList(filter)

    def peloponnese(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Peloponnese']
        index().radioList(filter)

    def centralgreece(self):
        filter = [i for i in self.radio_list() if i['area'] == 'Central Greece']
        index().radioList(filter)

    def radio_list(self):
        descDict = {
            ''                  : '',
            'International'     : language(30451).encode("utf-8"),
            'Eclectic'          : language(30452).encode("utf-8"),
            'Rock'              : language(30453).encode("utf-8"),
            'Greek'             : language(30454).encode("utf-8"),
            'Laika'             : language(30455).encode("utf-8"),
            'Sports'            : language(30456).encode("utf-8"),
            'News'              : language(30457).encode("utf-8"),
            'Religious'         : language(30458).encode("utf-8"),
            'Traditional'       : language(30459).encode("utf-8")
            }

        try:
            file = open(addonRadios,'r')
            result = file.read()
            file.close()

            radios = common.parseDOM(result, "radio", attrs = { "active": "True" })
        except:
            return

        for radio in radios:
            try:
                name = common.parseDOM(radio, "name")[0]

                band = common.parseDOM(radio, "band")[0]

                genre = common.parseDOM(radio, "genre")[0]

                area = common.parseDOM(radio, "area")[0]

                desc = descDict[genre]
                desc = common.replaceHTMLCodes(desc)

                url = common.parseDOM(radio, "url")[0]
                url = common.replaceHTMLCodes(url)

                self.list.append({'name': name, 'band': band, 'genre': genre, 'area': area, 'desc': desc, 'url': url})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('name'))
        return self.list

class resolver:
    def run(self, radio, area):
        try:
            list = radios().radio_list()
            name = radio.replace('_',' ')
            area = area.replace('_',' ')

            i = [x for x in list if name == x['name'] and area == x['area']]
            name, band, genre, area, desc, url = i[0]['name'], i[0]['band'], i[0]['genre'], i[0]['area'], i[0]['desc'], i[0]['url']
            image = '%s/%s/%s.png' % (addonLogos, area, name)

            if url.startswith('http://iphone-streaming.ustream.tv'): url = self.ustream(url)
            elif url.startswith('http://www.mad.tv'): url = self.madtv(url)

            if url is None: raise Exception()

            player().run(name, band, genre, area, desc, url, image)
            return url
        except:
            index().infoDialog(language(30317).encode("utf-8"))
            return


    def madtv(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return
            result = getUrl(url).result
            url = re.compile('.*src="(.+?/youtube/.+?)"').findall(result)[0]
            if url.startswith('//'): url = 'http:' + url

            result = getUrl(url).result
            url = re.compile('/embed/(.+?)"').findall(result)[0]
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url

            return url
        except:
            return

    def ustream(self, url):
        try:
            for i in range(1, 51):
                result = getUrl(url).result
                if "EXT-X-STREAM-INF" in result: return url
                if not "EXTM3U" in result: return
        except:
            return

main()