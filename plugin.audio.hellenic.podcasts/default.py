# -*- coding: utf-8 -*-

'''
    Hellenic Podcasts XBMC Addon
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
try:    import StorageServer
except: import storageserverdummy as StorageServer


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
cache               = StorageServer.StorageServer(addonFullId,1).cacheFunction
cache2              = StorageServer.StorageServer(addonFullId,24).cacheFunction
cache3              = StorageServer.StorageServer(addonFullId,720).cacheFunction
addonIcon           = os.path.join(addonPath,'icon.png')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
addonArt            = os.path.join(addonPath,'resources/art')
addonREAL           = os.path.join(addonPath,'resources/art/REAL.png')
addonSKAI           = os.path.join(addonPath,'resources/art/SKAI.png')
addonALPHA          = os.path.join(addonPath,'resources/art/ALPHA.png')
addonSlideshow      = os.path.join(addonPath,'resources/slideshow')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')


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
        try:        name = urllib.unquote_plus(params["name"])
        except:     name = None
        try:        url = urllib.unquote_plus(params["url"])
        except:     url = None
        try:        image = urllib.unquote_plus(params["image"])
        except:     image = None
        try:        date = urllib.unquote_plus(params["date"])
        except:     date = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        plot = urllib.unquote_plus(params["plot"])
        except:     plot = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None

        if action == None:                                 root().get()
        elif action == 'item_play':                        contextMenu().item_play()
        elif action == 'item_random_play':                 contextMenu().item_random_play()
        elif action == 'item_queue':                       contextMenu().item_queue()
        elif action == 'playlist_open':                    contextMenu().playlist_open()
        elif action == 'settings_open':                    contextMenu().settings_open()
        elif action == 'addon_home':                       contextMenu().addon_home()
        elif action == 'view_shows':                       contextMenu().view('shows')
        elif action == 'view_episodes':                    contextMenu().view('episodes')
        elif action == 'shows_real':                       real().shows()
        elif action == 'shows_skai':                       skai().shows()
        elif action == 'shows_alpha':                      alpha().shows()
        elif action == 'episodes':                         episodes().get(name, url, image, genre, plot, show)
        elif action == 'episodesparts':                    episodeparts().get(name, url, image, date, genre, plot, title, show)
        elif action == 'play':                             resolver().run(url)

        if action is None:
            pass
        elif action.startswith('shows'):
            xbmcplugin.setContent(int(sys.argv[1]), 'albums')
            index().container_view('shows', {'skin.confluence' : 506})
        elif action.startswith('episodes'):
            xbmcplugin.setContent(int(sys.argv[1]), 'albums')
            index().container_view('episodes', {'skin.confluence' : 506})
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

    def run(self, url):
        item = xbmcgui.ListItem(path=url.split(' playpath=')[0])
        item.setProperty('PlayPath', url.split(' playpath=')[-1]) 
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

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
        if not xbmcvfs.exists(dataPath):
            xbmcvfs.mkdir(dataPath)
        if not xbmcvfs.exists(viewData):
            file = xbmcvfs.File(viewData, 'w')
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

                cm = []

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Music", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def showList(self, showList):
        if showList == None: return

        count = 0
        total = len(showList)
        for i in showList:
            try:
                name, url, image, genre, plot = i['name'], i['url'], i['image'], i['genre'], i['plot']
                if image == '': image = addonFanart
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '

                sysname, sysurl, sysimage, sysgenre, sysplot, sysshow = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(name)
                u = '%s?action=episodes&name=%s&url=%s&image=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysgenre, sysplot, sysshow)
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1
                try: fanart = i['fanart']
                except: pass

                meta = {'label': name, 'title': name, 'album': name, 'genre' : genre, 'plot': plot}

                cm = []
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=view_shows)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Music", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Music", "true")
                item.setProperty("Album_Label", name)
                item.setProperty("Album_Description", plot)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def episodeList(self, episodeList):
        if episodeList == None: return

        count = 0
        total = len(episodeList)
        for i in episodeList:
            try:
                name, url, image, date, genre, plot, title, show = i['name'], i['url'], i['image'], i['date'], i['genre'], i['plot'], i['title'], i['show']
                if show == '': show = addonName
                if image == '': image = addonFanart
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '
                if date == '': date = ' '

                sysurl = urllib.quote_plus(url)
                u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1
                try: fanart = i['fanart']
                except: pass

                meta = {'label': name, 'title': name, 'album' : name, 'artist': show, 'genre': genre, 'comment': plot}

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Music", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Music", "true")
                item.setProperty("Album_Label", show)
                item.setProperty("Album_Description", plot)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

    def episodepartList(self, episodepartList):
        if episodepartList == None: return

        count = 0
        total = len(episodepartList)
        for i in episodepartList:
            try:
                name, url, image, date, genre, plot, title, show = i['name'], i['url'], i['image'], i['date'], i['genre'], i['plot'], i['title'], i['show']
                if show == '': show = addonName
                if image == '': image = addonFanart
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '
                if date == '': date = ' '

                sysurl = urllib.quote_plus(url)

                sysname, sysurl, sysimage, sysdate, sysgenre, sysplot, systitle, sysshow = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(date), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(title), urllib.quote_plus(show)

                u = '%s?action=episodesparts&name=%s&url=%s&image=%s&date=%s&genre=%s&plot=%s&title=%s&show=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysdate, sysgenre, sysplot, systitle, sysshow)

                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1
                try: fanart = i['fanart']
                except: pass

                meta = {'label': name, 'title': name, 'album' : name, 'artist': show, 'genre': genre, 'comment': plot}

                cm = []
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Music", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Music", "true")
                item.setProperty("Album_Label", show)
                item.setProperty("Album_Description", plot)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

class contextMenu:
    def item_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def item_random_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.shuffle()
        xbmc.Player().play(playlist)

    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(MusicPlaylist)')

    def settings_open(self):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % (addonId))

    def addon_home(self):
        xbmc.executebuiltin('Container.Update(plugin://%s/,replace)' % (addonId))

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

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'REAL.png', 'action': 'shows_real'})
        rootList.append({'name': 30502, 'image': 'SKAI.png', 'action': 'shows_skai'})
        rootList.append({'name': 30503, 'image': 'ALPHA.png', 'action': 'shows_alpha'})
        index().rootList(rootList)

class episodes:
    def get(self, name, url, image, genre, plot, show):
        if url.startswith(real().base_link):
            self.list = real().episodes_list(name, url, image, genre, plot, show)
            index().episodepartList(self.list)
        elif url.startswith(skai().base_link):
            self.list = skai().episodes_list(name, url, image, genre, plot, show)
            index().episodeList(self.list)
        elif url.startswith(alpha().base_link):
            self.list = alpha().episodes_list(name, url, image, genre, plot, show)
            index().episodeList(self.list)

class episodeparts:
    def get(self, name, url, image, date, genre, plot, title, show):
        self.list = real().episodepart_list(name, url, image, date, genre, plot, title, show)
        index().episodeList(self.list)

class resolver:
    def run(self, url):
        try:
            if url.startswith(alpha().base_link): url = alpha().resolve(url)

            if url is None: raise Exception()
            player().run(url)
            return url
        except:
            print 'No stream available' #delete in xbmc!
            return #delete in xbmc!
            index().infoDialog(language(30303).encode("utf-8"))
            return


class real:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.real.gr'
        self.shows_link = 'http://www.real.gr/default.aspx?page=radioathens&catID=50'
        self.added_link = 'http://www.real.gr/?Page=category&catID=50'

    def shows(self):
        #self.list = self.shows_list()
        self.list = cache2(self.shows_list)
        index().showList(self.list)

    def shows_list(self):
        try:
            result = getUrl(self.shows_link).result
            result = common.parseDOM(result, "div", attrs = { "class": "middle-container" })[0]
            result = common.parseDOM(result, "tbody")[0]
            shows = common.parseDOM(result, "td", attrs = { "style": ".+?" })
            shows += common.parseDOM(result, "td")
        except:
            return

        for show in shows:
            try:
                url = common.parseDOM(show, "a", ret="href")[0]
                if not 'catID=' in url: raise Exception()
                url = '%s/%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = addonREAL.encode('utf-8')

                self.list.append({'name': url, 'url': url, 'image': image, 'genre': 'Greek', 'plot': ''})
            except:
                pass

        for i in range(len(self.list)):
            try:
                result = getUrl(self.list[i]['url']).result
                name = common.parseDOM(result, "title")[0]
                name = name.split(' - ', 1)[-1]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                self.list[i]['name'] = name
            except:
                pass

        self.list = [{'name': 'Πρόσφατα'.decode('iso-8859-7').encode('utf-8'), 'url': self.added_link, 'image': addonREAL.encode('utf-8'), 'genre': 'Greek', 'plot': ''}] + self.list

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            redirects = [url + '&getPaging=true&curPage=1', url + '&getPaging=true&curPage=2', url + '&getPaging=true&curPage=3']

            count = 0
            threads = []
            result = ''
            for redirect in redirects:
                self.data.append('')
                threads.append(Thread(self.thread, redirect, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "div", attrs = { "class": "category_article_gridview" })
        except:
        	return

        for episode in episodes:
            try:
                match = common.parseDOM(episode, "a", attrs = { "class": ".+?article.+?" })[0]
                match = re.findall('(\d+)[/](\d+)[/](\d+) (.+)', match, re.I)[0]

                title = match[3]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                date = '%s-%s-%s' % ('%04d' % int(match[2]), '%02d' % int(match[1]), '%02d' % int(match[0]))

                name = '%s (%s)' % (match[3], date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href", attrs = { "class": ".+?article.+?" })[0]
                url = '%s/%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': date, 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def episodepart_list(self, name, url, image, date, genre, plot, title, show):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "class": "article_pure_text" })[0]
            parts = common.parseDOM(result, "a", ret="href")
        except:
            return

        count = 0
        for url in parts:
            try:
                count = count + 1
                title = '%s (%s)' % (name, str(count))

                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': title, 'url': url, 'image': image, 'date': date, 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class skai:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.skai.gr'
        self.shows_link = 'http://www.skai.gr/Ajax.aspx?m=Skai.TV.ProgramListView&la=0&Type=Radio&Day=%s'
        self.episodes_link = 'http://www.skai.gr/Ajax.aspx?m=Skai.Player.ItemView&type=Radio&cid=6&alid=%s'

    def shows(self):
        #self.list = self.shows_list()
        self.list = cache2(self.shows_list)
        index().showList(self.list)

    def shows_list(self):
        try:
            url = []
            d = datetime.datetime.utcnow()
            for i in range(0, 7):
                url.append(self.shows_link % d.strftime("%d.%m.%Y"))
                d = d - datetime.timedelta(hours=24)
            url = url[::-1]

            threads = []
            result = ''
            for i in range(0, 7):
                self.data.append('')
                showsUrl = url[i]
                threads.append(Thread(self.thread, showsUrl, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            shows = common.parseDOM(result, "Show", attrs = { "TVonly": "0" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "Show")[0]
                name = name.split('[')[-1].split(']')[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "Link")[0]
                url = url.split('[')[-1].split(']')[0]
                url = '%s%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "ShowImage")[0]
                image = image.split('[')[-1].split(']')[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                plot = common.parseDOM(show, "Description")[0]
                plot = plot.split('[')[-1].split(']')[0]
                plot = plot.replace('<br>','').replace('</br>','').replace('\n','').split('<')[0].strip()
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                if image in str(self.list): raise Exception()
                if not 'mmid=' in url: raise Exception()

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': plot})
            except:
                pass

        for i in range(len(self.list)): self.list[i]['image'] = addonSKAI.encode('utf-8')
        self.list = sorted(self.list, key=itemgetter('name'))
        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "li", ret="id", attrs = { "class": "active_sub" })[0]

            threads = []
            result = ''
            for i in range(1, 3):
                self.data.append('')
                episodesUrl = self.episodes_link % url + '&Page=%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, i-1))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "Item")
        except:
        	return

        for episode in episodes:
            try:
                title = common.parseDOM(episode, "Title")[0]
                title = title.split('[')[-1].split(']')[0]

                date = common.parseDOM(episode, "Date")[0]
                date = date.split('[')[-1].split(']')[0]
                date = date.split('T')[0]

                name = '%s (%s)' % (title, date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "File")[0]
                url = url.split('[')[-1].split(']')[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "Photo1")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': addonSKAI.encode('utf-8'), 'date': date, 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class alpha:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.alpha989.com'
        self.shows_link = 'http://www.alpha989.com/MediaList.aspx?a_id=1335'
        self.shows_link2 = 'http://www.alpha989.com/MediaList.aspx?a_id=1335&prodId=%s'

    def shows(self):
        #self.list = self.shows_list()
        self.list = cache2(self.shows_list)
        index().showList(self.list)

    def shows_list(self):
        try:
            result = getUrl(self.shows_link).result
            result = common.parseDOM(result, "select", attrs = { "id": ".+?lstProducers" })[0]
            shows = re.compile('(<option.+?</option>)').findall(result)
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "option")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "option", ret="value")[0]
                if not url.isdigit() or url == '0': raise Exception()
                url = self.shows_link2 % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = addonALPHA.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': ''})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('name'))
        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            redirects = [url + '&p=1', url + '&p=2', url + '&p=3']

            count = 0
            threads = []
            result = ''
            for redirect in redirects:
                self.data.append('')
                threads.append(Thread(self.thread, redirect, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "div", attrs = { "id": ".+?_divMedia_.+?" })
        except:
        	return

        for episode in episodes:
            try:
                title = common.parseDOM(episode, "b")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                date = episode.split(">")[-1].strip().split(" ")[-1]
                date = re.findall('(\d+)[/](\d+)[/](\d+)', date, re.I)[0]
                date = '%s-%s-%s' % ('%04d' % int(date[2]), '%02d' % int(date[1]), '%02d' % int(date[0]))

                name = '%s (%s)' % (common.parseDOM(episode, "b")[0], date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[0]
                url = '%s/%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': date, 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result

            try:
                result = common.parseDOM(result, "div", attrs = { "class": "playNow" })[0]
            except:
                pass
            try:
                result = common.parseDOM(result, "div", attrs = { "class": "mainContent" })[0]
            except:
                pass

            rtmp = re.compile("streamer:.+?'(.+?)'").findall(result)[0]
            playpath = re.compile("file:.+?'(.+?)'").findall(result)[0]
            if not 'mp3:' in playpath: playpath = 'mp3:' + playpath

            url = '%s playpath=%s' % (rtmp, playpath)
            return url
        except:
            return

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return


main()