# -*- coding: utf-8 -*-

'''
    Hellenic Toons XBMC Addon
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
movieDatabase       = os.path.join(addonPath,'resources/db/movies.xml')
showDatabase        = os.path.join(addonPath,'resources/db/tvshows.xml')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
favData             = os.path.join(dataPath,'favourites5.cfg')
favData2            = os.path.join(dataPath,'favourites6.cfg')


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
        try:        size = urllib.unquote_plus(params["size"])
        except:     size = None

        if action == None:                                 root().get()
        elif action == 'item_play':                        contextMenu().item_play()
        elif action == 'item_random_play':                 contextMenu().item_random_play()
        elif action == 'item_queue':                       contextMenu().item_queue()
        elif action == 'item_play_from_here':              contextMenu().item_play_from_here(url)
        elif action == 'playlist_open':                    contextMenu().playlist_open()
        elif action == 'settings_open':                    contextMenu().settings_open()
        elif action == 'addon_home':                       contextMenu().addon_home()
        elif action == 'view_movies':                      contextMenu().view('movies')
        elif action == 'view_tvshows':                     contextMenu().view('tvshows')
        elif action == 'view_episodes':                    contextMenu().view('episodes')
        elif action == 'favourite_add':                    contextMenu().favourite_add(favData, name, url, image)
        elif action == 'favourite_delete':                 contextMenu().favourite_delete(favData, name, url)
        elif action == 'favourite_moveUp':                 contextMenu().favourite_moveUp(favData, name, url)
        elif action == 'favourite_moveDown':               contextMenu().favourite_moveDown(favData, name, url)
        elif action == 'favourite2_add':                   contextMenu().favourite_add(favData2, name, url, image)
        elif action == 'favourite2_delete':                contextMenu().favourite_delete(favData2, name, url)
        elif action == 'favourite2_moveUp':                contextMenu().favourite_moveUp(favData2, name, url)
        elif action == 'favourite2_moveDown':              contextMenu().favourite_moveDown(favData2, name, url)
        elif action == 'root_favourites':                  root().favourites()
        elif action == 'movies_favourites':                favourites().movies()
        elif action == 'shows_favourites':                 favourites().shows()
        elif action == 'movies':                           database().movies()
        elif action == 'movies_dubbed':                    database().movies_dubbed()
        elif action == 'shows':                            database().shows()
        elif action == 'shows_classics':                   youtube().classics()
        elif action == 'shows_songs':                      youtube().songs()
        elif action == 'episodes':                         episodes().get(name, url, image, genre, plot, show)
        elif action == 'play':                             resolver().run(url, size)

        if action is None:
            pass
        elif action.startswith('movies'):
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            index().container_view('movies', {'skin.confluence' : 500})
        elif action.startswith('shows'):
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            index().container_view('tvshows', {'skin.confluence' : 500})
        elif action.startswith('episodes'):
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            index().container_view('episodes', {'skin.confluence' : 504})
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

class cryptUrl:
    def __init__(self):
        self.key = 'dhflqoxm'

    def encode(self, str):
        enc = []
        for i in range(len(str)):
            key_c = self.key[i % len(self.key)]
            enc_c = chr((ord(str[i]) + ord(key_c)) % 256)
            enc.append(enc_c)
        return base64.urlsafe_b64encode("".join(enc))

    def decode(self, str):
        dec = []
        str = base64.urlsafe_b64decode(str)
        for i in range(len(str)):
            key_c = self.key[i % len(self.key)]
            dec_c = chr((256 + ord(str[i]) - ord(key_c)) % 256)
            dec.append(dec_c)
        return "".join(dec)

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
        if not xbmcvfs.exists(favData2):
            file = xbmcvfs.File(favData2, 'w')
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
                if action.startswith('episodes'): cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                if action.startswith('episodes'): cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def movieList(self, movieList):
        if movieList == None: return

        file = xbmcvfs.File(favData)
        favRead = file.read()
        file.close()

        count = 0
        total = len(movieList)
        for i in movieList:
            try:
                name, url, image, title, genre, plot, size = i['name'], i['url'], i['image'], i['title'], i['genre'], i['plot'], i['size']
                if image == '': image = addonFanart
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '

                sysname, sysurl, sysimage, syssize = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(size)
                u = '%s?action=play&url=%s&size=%s' % (sys.argv[0], sysurl, syssize)
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
                    if getSetting("fav_sort") == '1': cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if getSetting("fav_sort") == '1': cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30425).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
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

    def showList(self, showList):
        if showList == None: return

        file = xbmcvfs.File(favData2)
        favRead = file.read()
        file.close()

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

                meta = {'label': name, 'title': name, 'tvshowtitle': name, 'genre' : genre, 'plot': plot}

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                if action == 'shows_favourites':
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    if getSetting("fav_sort") == '1': cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=favourite2_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if getSetting("fav_sort") == '1': cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=favourite2_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30425).encode("utf-8"), 'RunPlugin(%s?action=favourite2_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                else:
                    if not '"%s"' % url in favRead: cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite2_add&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                    else: cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=favourite2_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
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
                name, url, image, date, genre, plot, title, show, size = i['name'], i['url'], i['image'], i['date'], i['genre'], i['plot'], i['title'], i['show'], i['size']
                if show == '': show = addonName
                if image == '': image = addonFanart
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '
                if date == '': date = ' '

                sysurl, syssize = urllib.quote_plus(url), urllib.quote_plus(size)
                u = '%s?action=play&url=%s&size=%s' % (sys.argv[0], sysurl, syssize)
                fanart = '%s/%s.jpg' % (addonSlideshow, str(count)[-1])
                count = count + 1
                try: fanart = i['fanart']
                except: pass

                meta = {'label': title, 'title': title, 'studio': show, 'premiered': date, 'genre': genre, 'plot': plot}

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_play_from_here&url=%s)' % (sys.argv[0], sysurl)))
                cm.append((language(30412).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
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

    def item_play_from_here(self, url):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.unshuffle()
        total = xbmc.getInfoLabel('Container.NumItems')
        for i in range(0, int(total)):
            i = str(i)
            label = xbmc.getInfoLabel('ListItemNoWrap(%s).Label' % i)
            if label == '': break

            params = {}
            path = xbmc.getInfoLabel('ListItemNoWrap(%s).FileNameAndPath' % i)
            path = urllib.quote_plus(path).replace('+%26+', '+&+')
            query = path.split('%3F', 1)[-1].split('%26')
            for i in query: params[urllib.unquote_plus(i).split('=')[0]] = urllib.unquote_plus(i).split('=')[1]
            sysurl = urllib.quote_plus(params["url"])
            u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)

            meta = {'title': xbmc.getInfoLabel('ListItemNoWrap(%s).title' % i), 'tvshowtitle': xbmc.getInfoLabel('ListItemNoWrap(%s).tvshowtitle' % i), 'season': xbmc.getInfoLabel('ListItemNoWrap(%s).season' % i), 'episode': xbmc.getInfoLabel('ListItemNoWrap(%s).episode' % i), 'writer': xbmc.getInfoLabel('ListItemNoWrap(%s).writer' % i), 'director': xbmc.getInfoLabel('ListItemNoWrap(%s).director' % i), 'rating': xbmc.getInfoLabel('ListItemNoWrap(%s).rating' % i), 'duration': xbmc.getInfoLabel('ListItemNoWrap(%s).duration' % i), 'premiered': xbmc.getInfoLabel('ListItemNoWrap(%s).premiered' % i), 'plot': xbmc.getInfoLabel('ListItemNoWrap(%s).plot' % i)}
            poster, fanart = xbmc.getInfoLabel('ListItemNoWrap(%s).icon' % i), xbmc.getInfoLabel('ListItemNoWrap(%s).Property(Fanart_Image)' % i)

            item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
            item.setInfo( type="Video", infoLabels= meta )
            item.setProperty("IsPlayable", "true")
            item.setProperty("Video", "true")
            item.setProperty("Fanart_Image", fanart)
            playlist.add(u, item)
        xbmc.Player().play(playlist)

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
            file.write('"%s"|"%s"|"%s"\n' % (name, url, image))
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
        file = open(favData, 'r')
        read = file.read()
        file.close()
        file = open(movieDatabase, 'r')
        db = file.read()
        file.close()
        db = common.parseDOM(db, "movie")
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, url, image in match:
            try: size = [common.parseDOM(i, "size")[0] for i in db if common.replaceHTMLCodes(common.parseDOM(i, "base")[0]) == url][0]
            except: size= '0'
            movieDict = {'name': name, 'url': url, 'image': image, 'title': name, 'genre': 'Greek', 'plot': '', 'size': size}
            try: movieDict.update({'fanart': [common.parseDOM(i, "fanart")[0] for i in db if common.replaceHTMLCodes(common.parseDOM(i, "base")[0]) == url][0]})
            except: pass
            self.list.append(movieDict)

        if getSetting("fav_sort") == '0':
            self.list = sorted(self.list, key=itemgetter('name'))

        index().movieList(self.list)

    def shows(self):
        file = open(favData2, 'r')
        read = file.read()
        file.close()
        file = open(showDatabase, 'r')
        db = file.read()
        file.close()
        db = common.parseDOM(db, "show")
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, url, image in match:
            showDict = {'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': ''}
            try: showDict.update({'fanart': [common.parseDOM(i, "fanart")[0] for i in db if common.replaceHTMLCodes(common.parseDOM(i, "base")[0]) == url][0]})
            except: pass
            self.list.append(showDict)

        if getSetting("fav_sort") == '0':
            self.list = sorted(self.list, key=itemgetter('name'))

        index().showList(self.list)

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'Movies.png', 'action': 'movies'})
        rootList.append({'name': 30502, 'image': 'TV Shows.png', 'action': 'shows'})
        rootList.append({'name': 30503, 'image': 'Dubbed.png', 'action': 'movies_dubbed'})
        rootList.append({'name': 30504, 'image': 'Favourites.png', 'action': 'root_favourites'})
        rootList.append({'name': 30505, 'image': 'Classics.png', 'action': 'shows_classics'})
        rootList.append({'name': 30506, 'image': 'Songs.png', 'action': 'shows_songs'})
        index().rootList(rootList)

    def favourites(self):
        rootList = []
        rootList.append({'name': 30521, 'image': 'Movies.png', 'action': 'movies_favourites'})
        rootList.append({'name': 30522, 'image': 'TV Shows.png', 'action': 'shows_favourites'})
        index().rootList(rootList)

class episodes:
    def get(self, name, url, image, genre, plot, show):
        if url.startswith(database().shows_link):
            self.list = database().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(youtube().api_link):
            self.list = youtube().episodes_list(name, url, image, genre, plot, show)
            for i in range(len(self.list)): self.list[i]['size'] = '0'
        index().episodeList(self.list)

class resolver:
    def run(self, url, size):
        try:
            if url.startswith(database().movies_link): url = database().resolve(url)

            if url.startswith(youtube().base_link): url = youtube().resolve(url)
            else: url = self.urlresolver(url)

            if not size == '0' and not 'firedrive.com' in url:
                if not size == self.size(url): raise Exception()

            if url is None: raise Exception()
            player().run(url)
            return url
        except:
            index().infoDialog(language(30307).encode("utf-8"))
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

    def size(self, url):
        try:
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0')
            response = urllib2.urlopen(request, timeout=30)
            size = response.info()["Content-Length"]
            return size
        except:
            return


class database:
    def __init__(self):
        self.list = []
        self.data = []
        self.movies_link = 'http://www.themoviedb.org'
        self.shows_link = 'http://thetvdb.com'

    def movies(self):
        self.list = self.movies_list()
        index().movieList(self.list)

    def movies_dubbed(self):
        self.list = self.movies_list()
        self.list = [i for i in self.list if i['lang'] == 'el']
        index().movieList(self.list)

    def shows(self):
        self.list = self.shows_list()
        index().showList(self.list)

    def movies_list(self):
        try:
            file = open(movieDatabase,'r')
            result = file.read()
            file.close()
            movies = common.parseDOM(result, "movie")
        except:
            return

        for movie in movies:
            try:
                name = common.parseDOM(movie, "name")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(movie, "base")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(movie, "poster")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                fanart = common.parseDOM(movie, "fanart")[0]
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                lang = common.parseDOM(movie, "language")[0]
                lang = common.replaceHTMLCodes(lang)
                lang = lang.encode('utf-8')

                size = common.parseDOM(movie, "size")[0]
                size = common.replaceHTMLCodes(size)
                size = size.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'title': name, 'genre': 'Greek', 'plot': '', 'fanart': fanart, 'size': size, 'lang': lang})
            except:
                pass

        return self.list

    def shows_list(self):
        try:
            file = open(showDatabase,'r')
            result = file.read()
            file.close()
            shows = common.parseDOM(result, "show")
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "name")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "base")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "poster")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                fanart = common.parseDOM(show, "fanart")[0]
                fanart = common.replaceHTMLCodes(fanart)
                fanart = fanart.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': '', 'fanart': fanart})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            file = open(showDatabase,'r')
            result = file.read()
            file.close()
            result = common.parseDOM(result, "show")
            result = [i for i in result if common.replaceHTMLCodes(common.parseDOM(i, "base")[0]) == url][0]

            fanart = common.parseDOM(result, "fanart")[0]
            fanart = common.replaceHTMLCodes(fanart)
            fanart = fanart.encode('utf-8')

            count = 1
            episodes = common.parseDOM(result, "episode")
        except:
        	return

        for episode in episodes:
            try:
                name = 'Επεισόδιο '.decode('iso-8859-7') + str(count)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "url")[0]
                url = cryptUrl().decode(url.encode('utf-8'))
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                size = common.parseDOM(episode, "size")[0]
                size = common.replaceHTMLCodes(size)
                size = size.encode('utf-8')

                count = count + 1

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show, 'fanart': fanart, 'size': size})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            file = open(movieDatabase,'r')
            result = file.read()
            file.close()
            result = common.parseDOM(result, "movie")
            result = [i for i in result if common.replaceHTMLCodes(common.parseDOM(i, "base")[0]) == url][0]

            url = common.parseDOM(result, "url")[0]
            url = cryptUrl().decode(url.encode('utf-8'))
            url = common.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except:
            return

class youtube:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.youtube.com'
        self.api_link = 'http://gdata.youtube.com'
        self.playlists_link = 'http://gdata.youtube.com/feeds/api/users/%s/playlists'
        self.playlist_link = 'http://gdata.youtube.com/feeds/api/playlists/%s'
        self.search_link = 'http://gdata.youtube.com/feeds/api/videos?q='
        self.watch_link = 'http://www.youtube.com/watch?v=%s'
        self.info_link = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

    def classics(self):
        #self.list = self.classics_parse()
        self.list = cache(self.classics_parse)
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

    def classics_parse(self):
        self.list = self.shows_list('GreekTvCartoon', [], [])
        self.list = self.shows_list('GreekTvCartoons', [], [])
        self.list = self.shows_list('GreekCartoonClassics', [], [])
        self.list = self.shows_list('ToonsFromThePast', [], ['PLStChvmvfcLCTv__R0DdRG95E0DC-wQik'])
        self.list = self.shows_list('lilithvii', ['PL3420AA02720B05E5', 'PL147140D5904AFBE4', 'PLF191388E07E9E127', 'PL8F5C47492E11C109', 'PLAD759EE008F12C43', 'PLC3C3861A770162F5', 'PL0C994DFD3BCDAEDB', 'PLE3470893493CF5A8', 'PLD2C2707D06DA58DC', 'PL724AA3356D663CED', 'PLC34BCF01941BAC02'], [])
        self.list = self.shows_list('Michaletosjr', [], [])
        self.list = self.shows_list('GPITRAL5', [], [])
        return self.list

    def songs(self):
        #self.list = self.songs_parse()
        self.list = cache(self.songs_parse)
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

    def songs_parse(self):
        self.list = self.shows_list('sapiensgr2', [], ['PLB3126415BC8BCDE3'])
        self.list = self.shows_list('Aviosys', ['PL9E9CD72ED3715FEA', 'PL35F8EE4D9D188A0C', 'PLEC7CC64E658C1D7E'], [])
        return self.list

    def shows_list(self, channel, include, exclude):
        try:
            count = 0
            threads = []
            result = ''
            for i in range(1, 250, 25):
                self.data.append('')
                showsUrl = self.playlists_link % channel + '?max-results=25&start-index=%s' % str(i)
                threads.append(Thread(self.thread, showsUrl, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            shows = common.parseDOM(result, "entry")
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "id")[0]
                url = self.playlist_link % url.split("/")[-1]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "media:thumbnail", ret="url")[0]
                image = image.replace(image.split("/")[-1], '0.jpg')
                image = image.encode('utf-8')

                if image.endswith("/00000000000/0.jpg"): raise Exception() #empty playlist
                if not include == [] and not any(url.endswith(i) for i in include): raise Exception()
                if any(url.endswith(i) for i in exclude): raise Exception()

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': ''})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            count = 0
            threads = []
            result = ''
            for i in range(1, 250, 25):
                self.data.append('')
                episodesUrl = url + '?max-results=25&start-index=%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "entry")
        except:
        	return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "title")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "media:player", ret="url")[0]
                url = url.split("&amp;")[0].split("=")[-1]
                url = self.watch_link % url
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "media:thumbnail", ret="url")[0]
                image = image.replace(image.split("/")[-1], '0.jpg')
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve_search(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return

            query = url.split("?q=")[-1].split("/")[-1].split("?")[0]
            url = url.replace(query, urllib.quote_plus(query))
            result = getUrl(url).result
            result = common.parseDOM(result, "entry")
            result = common.parseDOM(result, "id")

            for url in result[:5]:
                url = url.split("/")[-1]
                url = self.watch_link % url
                url = self.resolve(url)
                if not url is None: return url
        except:
            return

    def resolve(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            state, reason = None, None
            result = getUrl(self.info_link % id).result
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = getUrl(self.watch_link % id).result
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
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