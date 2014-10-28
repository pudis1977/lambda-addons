# -*- coding: utf-8 -*-

'''
    Hellenic Movies XBMC Addon
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
addonSlideshow      = os.path.join(addonPath,'resources/slideshow')
addonPages          = os.path.join(addonPath,'resources/art/Pages.png')
addonGenres         = os.path.join(addonPath,'resources/art/Genres.png')
addonYears          = os.path.join(addonPath,'resources/art/Years.png')
addonNext           = os.path.join(addonPath,'resources/art/Next.png')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
favData             = os.path.join(dataPath,'favourites3.cfg')


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
        try:        query = urllib.unquote_plus(params["query"])
        except:     query = None
        try:        title = urllib.unquote_plus(params["title"])
        except:     title = None
        try:        year = urllib.unquote_plus(params["year"])
        except:     year = None
        try:        imdb = urllib.unquote_plus(params["imdb"])
        except:     imdb = None

        if action == None:                          root().get()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'addon_home':                contextMenu().addon_home()
        elif action == 'view_movies':               contextMenu().view('movies')
        elif action == 'favourite_add':             contextMenu().favourite_add(favData, name, url, image)
        elif action == 'favourite_from_search':     contextMenu().favourite_from_search(favData, name, url, image)
        elif action == 'favourite_delete':          contextMenu().favourite_delete(favData, name, url)
        elif action == 'favourite_moveUp':          contextMenu().favourite_moveUp(favData, name, url)
        elif action == 'favourite_moveDown':        contextMenu().favourite_moveDown(favData, name, url)
        elif action == 'movies':                    movies().get(url)
        elif action == 'movies_added':              movies().cinegreece_added()
        elif action == 'movies_favourites':         favourites().movies()
        elif action == 'movies_search':             search().cinegreece(query)
        elif action == 'pages_movies':              pages().cinegreece()
        elif action == 'genres_movies':             genres().cinegreece()
        elif action == 'years_movies':              years().cinegreece()
        elif action == 'play':                      resolver().run(url, name)

        if action is None:
            pass
        elif action.startswith('movies'):
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            index().container_view('movies', {'skin.confluence' : 500})
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
        item = xbmcgui.ListItem(path=url)
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
        if not xbmcvfs.exists(favData):
            file = xbmcvfs.File(favData, 'w')
            file.write('')
            file.close()
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
                if action == 'movies_favourites': cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                if action == 'movies_favourites': cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def pageList(self, pageList):
        count = 0
        total = len(pageList)
        for i in pageList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=movies&url=%s' % (sys.argv[0], sysurl)
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems([], replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def nextList(self, nextList):
        try: next = nextList[0]['next']
        except: return
        if next == '': return
        name, url, image = language(30361).encode("utf-8"), next, addonNext
        sysurl = urllib.quote_plus(url)

        u = '%s?action=movies&url=%s' % (sys.argv[0], sysurl)

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def movieList(self, movieList):
        if movieList == None: return

        file = xbmcvfs.File(favData)
        favRead = file.read()
        file.close()

        count = 0
        total = len(movieList)
        for i in movieList:
            try:
                name, url, image, title, genre, plot = i['name'], i['url'], i['image'], i['title'], i['genre'], i['plot']
                if image == '': image = addonFanart
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '

                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=play&url=%s&name=%s' % (sys.argv[0], sysurl, sysname)
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1
                try: fanart = i['fanart']
                except: pass

                meta = {'label': title, 'title': title, 'genre' : genre, 'plot': plot}

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))

                if action == 'movies_favourites':
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    if getSetting("fav_sort") == '2': cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if getSetting("fav_sort") == '2': cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30425).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action == 'movies_search':
                    cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_from_search&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                else:
                    if not '"%s"' % url in favRead: cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                    else: cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

class contextMenu:
    def item_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.unshuffle()
        xbmc.Player().play(playlist)

    def item_random_play(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.executebuiltin('Action(Queue)')
        playlist.shuffle()
        xbmc.Player().play(playlist)

    def item_queue(self):
        xbmc.executebuiltin('Action(Queue)')

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

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
            src = os.path.join(src, 'MyVideoNav.xml')
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

    def favourite_add(self, data, name, url, image):
        try:
            index().container_refresh()
            file = open(data, 'a+')
            file.write('"%s"|"0"|"%s"|"%s"\n' % (name, url, image))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_from_search(self, data, name, url, image):
        try:
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            if url in read:
                index().infoDialog(language(30307).encode("utf-8"), name)
                return
            file = open(data, 'a+')
            file.write('"%s"|"0"|"%s"|"%s"\n' % (name, url, image))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, data, name, url):
        try:
            index().container_refresh()
            file = open(data,'r')
            read = file.read()
            file.close()
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
            list = re.compile('(".+?\n)').findall(read.replace(line, ''))
            file = open(data, 'w')
            for line in list: file.write(line)
            file.close()
            index().infoDialog(language(30304).encode("utf-8"), name)
        except:
            return

    def favourite_moveUp(self, data, name, url):
        try:
            index().container_refresh()
            file = open(data,'r')
            read = file.read()
            file.close()
            list = re.compile('(".+?)\n').findall(read)
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
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
            index().container_refresh()
            file = open(data,'r')
            read = file.read()
            file.close()
            list = re.compile('(".+?)\n').findall(read)
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
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
        self.list = []

    def movies(self):
        file = xbmcvfs.File(favData)
        read = file.read()
        file.close()

        match = re.compile('"(.+?)"[|]".+?"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, url, image in match:
            try: year = re.compile('[(](\d{4})[)]').findall(name)[-1]
            except: year = '0'
            title = name.replace('(%s)' % year, '').strip()
            self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': '0', 'genre': 'Greek', 'plot': ''})

        if getSetting("fav_sort") == '0':
            self.list = sorted(self.list, key=itemgetter('title'))
        elif getSetting("fav_sort") == '1':
            self.list = sorted(self.list, key=itemgetter('title'))[::-1]
            self.list = sorted(self.list, key=itemgetter('year'))[::-1]

        index().movieList(self.list)

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'Pages.png', 'action': 'pages_movies'})
        rootList.append({'name': 30502, 'image': 'Genres.png', 'action': 'genres_movies'})
        rootList.append({'name': 30503, 'image': 'Years.png', 'action': 'years_movies'})
        rootList.append({'name': 30504, 'image': 'Added.png', 'action': 'movies_added'})
        rootList.append({'name': 30505, 'image': 'Favourites.png', 'action': 'movies_favourites'})
        rootList.append({'name': 30506, 'image': 'Search.png', 'action': 'movies_search'})
        index().rootList(rootList)

class link:
    def __init__(self):
        self.cinegreece_base = 'http://www.cinegreece.com'
        self.cinegreece_page = 'http://www.cinegreece.com/p/blog-page.html'
        self.cinegreece_added = 'http://www.cinegreece.com/search/label/%CE%95%CE%BB%CE%BB%CE%B7%CE%BD%CE%B9%CE%BA%CE%AD%CF%82%20%CE%A4%CE%B1%CE%B9%CE%BD%CE%AF%CE%B5%CF%82'
        self.google_search = 'https://encrypted.google.com/search?as_q=%s'
        self.greekmovies_base = 'http://greek-movies.com'

class pages:
    def __init__(self):
        self.list = []

    def cinegreece(self):
        #self.list = self.cinegreece_list()
        self.list = cache3(self.cinegreece_list)
        index().pageList(self.list)

    def cinegreece_list(self):
        try:
            result = getUrl(link().cinegreece_page).result
            result = common.parseDOM(result, "div", attrs = { "itemprop": "articleBody" })[0]
            pages = common.parseDOM(result, "span", attrs = { "class": "buttona" })
        except:
            return

        for page in pages:
            try:
                name = common.parseDOM(page, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(page, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = addonPages.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class genres:
    def __init__(self):
        self.list = []

    def cinegreece(self):
        #self.list = self.cinegreece_list()
        self.list = cache3(self.cinegreece_list)
        index().pageList(self.list)

    def cinegreece_list(self):
        try:
            result = getUrl(link().cinegreece_page).result
            result = common.parseDOM(result, "div", attrs = { "itemprop": "articleBody" })[0]
            genres = common.parseDOM(result, "span", attrs = { "class": "buttond" })
        except:
            return

        for genre in genres:
            try:
                name = common.parseDOM(genre, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(genre, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = addonGenres.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class years:
    def __init__(self):
        self.list = []

    def cinegreece(self):
        #self.list = self.cinegreece_list()
        self.list = cache2(self.cinegreece_list)
        index().pageList(self.list)

    def cinegreece_list(self):
        try:
            result = getUrl(link().cinegreece_page).result
            result = common.parseDOM(result, "div", attrs = { "itemprop": "articleBody" })[0]
            years = common.parseDOM(result, "span", attrs = { "class": "button" })
        except:
            return

        for year in years:
            try:
                name = common.parseDOM(year, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(year, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = addonYears.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class search:
    def __init__(self):
        self.list = []

    def cinegreece(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query is None or self.query == ''):
            self.cinegreece_list()
            index().movieList(self.list)

    def cinegreece_list(self):
        try:
            searchUrl = link().google_search % urllib.quote_plus(self.query) + '&as_sitesearch=cinegreece.com'
            result = getUrl(searchUrl).result
            search = re.compile('cinegreece.com/(.+?/.+?[.]html)').findall(result)
            search = uniqueList(search).list

            threads = []
            for url in search:
                url = common.replaceHTMLCodes(url)
                url = '%s/%s' % (link().cinegreece_base, url)
                url = url.encode('utf-8')
                threads.append(Thread(self.cinegreece_list2, url))
            [i.start() for i in threads]
            [i.join() for i in threads]
        except:
            pass

    def cinegreece_list2(self, url): 
        try:
            result = getUrl(url).result
            if not "/%CE%95%CE%BB%CE%BB%CE%B7%CE%BD%CE%B9%CE%BA%CE%AD%CF%82%20%CE%A4%CE%B1%CE%B9%CE%BD%CE%AF%CE%B5%CF%82" in result: raise Exception()

            name = common.parseDOM(result, "h3")[0]
            name = name.replace('[','(').replace(']',')').strip()
            match = re.findall('(.+?)[(](\d{4})[)]', name)[0]
            name = common.replaceHTMLCodes(name)
            name = name.encode('utf-8')

            title = match[0].strip()
            if title.endswith('(Ο)'.decode('iso-8859-7')): title = 'Ο '.decode('iso-8859-7') + title.replace('(Ο)'.decode('iso-8859-7'), '').strip()
            elif title.endswith('(Η)'.decode('iso-8859-7')): title = 'Η '.decode('iso-8859-7') + title.replace('(Η)'.decode('iso-8859-7'), '').strip()
            elif title.endswith('(Το)'.decode('iso-8859-7')): title = 'Το '.decode('iso-8859-7') + title.replace('(Το)'.decode('iso-8859-7'), '').strip()
            elif title.endswith('(Οι)'.decode('iso-8859-7')): title = 'Οι '.decode('iso-8859-7') + title.replace('(Οι)'.decode('iso-8859-7'), '').strip()
            elif title.endswith('(Τα)'.decode('iso-8859-7')): title = 'Τα '.decode('iso-8859-7') + title.replace('(Τα)'.decode('iso-8859-7'), '').strip()
            title = common.replaceHTMLCodes(title)
            title = title.encode('utf-8')

            year = match[-1].strip()
            year = re.sub('[^0-9]', '', year)
            year = year.encode('utf-8')

            image = common.parseDOM(result, "div", attrs = { "class": "separator" })[0]
            image = common.parseDOM(image, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')

            self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': '0', 'genre': 'Greek', 'plot': ''})
        except:
            pass

class movies:
    def __init__(self):
        self.list = []

    def get(self, url):
        #self.list = self.cinegreece_list(url)
        self.list = cache(self.cinegreece_list, url)
        index().movieList(self.list)
        index().nextList(self.list)

    def cinegreece_added(self):
        #self.list = self.cinegreece_list2(link().cinegreece_added)
        self.list = cache(self.cinegreece_list2, link().cinegreece_added)
        index().movieList(self.list)

    def cinegreece_list(self, url):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "itemprop": "articleBody" })[0]
            movies = re.compile('(<a.+?</a>)').findall(result)
            movies = uniqueList(movies).list
        except:
            return

        try:
            next = common.parseDOM(result, "span", attrs = { "class": "buttonb" })[-1]
            exception = common.parseDOM(next, "a", ret="href")[0]
            if '171' in common.parseDOM(next, "a")[0]: raise Exception()
            next = common.parseDOM(next, "a", ret="href")[0]
        except:
            next = ''

        for movie in movies:
            try:
                title = common.parseDOM(movie, "img", ret="title")[0]
                if title.endswith('(Ο)'.decode('iso-8859-7')): title = 'Ο '.decode('iso-8859-7') + title.replace('(Ο)'.decode('iso-8859-7'), '').strip()
                elif title.endswith('(Η)'.decode('iso-8859-7')): title = 'Η '.decode('iso-8859-7') + title.replace('(Η)'.decode('iso-8859-7'), '').strip()
                elif title.endswith('(Το)'.decode('iso-8859-7')): title = 'Το '.decode('iso-8859-7') + title.replace('(Το)'.decode('iso-8859-7'), '').strip()
                elif title.endswith('(Οι)'.decode('iso-8859-7')): title = 'Οι '.decode('iso-8859-7') + title.replace('(Οι)'.decode('iso-8859-7'), '').strip()
                elif title.endswith('(Τα)'.decode('iso-8859-7')): title = 'Τα '.decode('iso-8859-7') + title.replace('(Τα)'.decode('iso-8859-7'), '').strip()
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                url = common.parseDOM(movie, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.replace(url.split("/")[2], link().cinegreece_base.split("//")[-1])
                url = url.encode('utf-8')

                year = url.split("/")[-1].split("-")[-1].split(".")[0].split("_")[0]
                year = re.sub('[^0-9]', '', year)
                year = year.encode('utf-8')

                if not year == '': name = '%s (%s)' % (title, year)
                else: name = title

                image = common.parseDOM(movie, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': '0', 'genre': 'Greek', 'plot': '', 'next': next})
            except:
                pass

        return self.list

    def cinegreece_list2(self, url):
        try:
            result = getUrl(url).result
            movies = common.parseDOM(result, "div", attrs = { "class": "post-outer" })
            movies = uniqueList(movies).list
        except:
            return

        for movie in movies:
            try:
                name = common.parseDOM(movie, "h3")[0]
                name = common.parseDOM(name, "a")[0]
                name = name.replace('[','(').replace(']',')').strip()
                match = re.findall('(.+?)[(](\d{4})[)]', name)[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                title = match[0].strip()
                if title.endswith('(Ο)'.decode('iso-8859-7')): title = 'Ο '.decode('iso-8859-7') + title.replace('(Ο)'.decode('iso-8859-7'), '').strip()
                elif title.endswith('(Η)'.decode('iso-8859-7')): title = 'Η '.decode('iso-8859-7') + title.replace('(Η)'.decode('iso-8859-7'), '').strip()
                elif title.endswith('(Το)'.decode('iso-8859-7')): title = 'Το '.decode('iso-8859-7') + title.replace('(Το)'.decode('iso-8859-7'), '').strip()
                elif title.endswith('(Οι)'.decode('iso-8859-7')): title = 'Οι '.decode('iso-8859-7') + title.replace('(Οι)'.decode('iso-8859-7'), '').strip()
                elif title.endswith('(Τα)'.decode('iso-8859-7')): title = 'Τα '.decode('iso-8859-7') + title.replace('(Τα)'.decode('iso-8859-7'), '').strip()
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = match[-1].strip()
                year = re.sub('[^0-9]', '', year)
                year = year.encode('utf-8')

                url = common.parseDOM(movie, "h3")[0]
                url = common.parseDOM(url, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.replace(url.split("/")[2], link().cinegreece_base.split("//")[-1])
                url = url.encode('utf-8')

                image = common.parseDOM(movie, "div", attrs = { "class": "separator" })[0]
                image = common.parseDOM(image, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'title': title, 'year': year, 'imdb': '0', 'genre': 'Greek', 'plot': '', 'next': next})
            except:
                pass

        return self.list

class resolver:
    def run(self, url, name):
        try:
            url = self.cinegreece(url)
            if url is None: url = self.greekmovies(name)

            if url is None: raise Exception()
            player().run(url)
            return url
        except:
            index().infoDialog(language(30308).encode("utf-8"))
            return

    def cinegreece(self, url):
        try:
            result = getUrl(url).result
        except:
            return

        try:
            url = common.parseDOM(result, "div", attrs = { "id": "panel" })[0]
            url = common.parseDOM(url, "iframe", ret="src")[0]
            url = common.replaceHTMLCodes(url)
            if url.startswith('//'): url = '%s%s' % ('http:', url)
            if 'youtube.com' in url: url = self.youtube(url)
            else: url = self.urlresolver(url)
            return url
        except:
            pass

        try:
            body = common.parseDOM(result, "div", attrs = { "itemprop": "articleBody" })[0]
            url = common.parseDOM(body, "a", ret="onclick")
            url += common.parseDOM(body, "button", ret="onclick")
            url = re.compile("'(.+?)'").findall(url[0])[0]
            url = common.replaceHTMLCodes(url)
            if url.startswith('//'): url = '%s%s' % ('http:', url)
            if 'youtube.com' in url: url = self.youtube(url)
            else: url = self.urlresolver(url)
            return url
        except:
            pass

    def greekmovies(self, name):
        try:
            query = link().google_search % urllib.quote_plus(name) + '&as_sitesearch=greek-movies.com'

            result = getUrl(query).result
            url = re.compile('greek-movies.com/(movies.php[?]m=\d*)').findall(result)[0]
            url = '%s/%s' % (link().greekmovies_base, url)
            url = common.replaceHTMLCodes(url)

            result = getUrl(url).result
            result = re.compile('"(view.php[?]v=.+?)".+?><b>(.+?)</b>').findall(result)
            match = [i[0] for i in result if i[1] == 'youtube']
            match = ['%s/%s' % (link().greekmovies_base, i) for i in match]
            match = uniqueList(match).list

            for i in match[:5]:
                try:
                    result = getUrl(i).result
                    url = common.parseDOM(result, "button", ret="OnClick")[0]
                    url = self.youtube(url.split("'")[1])
                    if not url == None: return url
                except:
                    pass
        except:
            return

    def youtube(self, url):
        try:
            watch_link = 'http://www.youtube.com/watch?v=%s'
            info_link = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return

            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            state, reason = None, None
            result = getUrl(info_link % id).result
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = getUrl(watch_link % id).result
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return

    def urlresolver(self, url):
        try:
            import urlresolver
            host = urlresolver.HostedMediaFile(url)
            if host: resolver = urlresolver.resolve(url)
            if not resolver.startswith('http://'): return
            if not resolver == url: return resolver
        except:
            return

main()