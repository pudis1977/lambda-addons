# -*- coding: utf-8 -*-

'''
    Football Today XBMC Addon
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
addonNext           = os.path.join(addonPath,'resources/art/Next.png')
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

        if action == None:                          root().get()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'item_play_from_here':       contextMenu().item_play_from_here(url)
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'addon_home':                contextMenu().addon_home()
        elif action == 'view_videos':               contextMenu().view('videos')
        elif action == 'videos':                    videos().get(url)
        elif action == 'videos_games':              videos().root('games')
        elif action == 'videos_premierleague':      videos().root('premierleague')
        elif action == 'videos_laliga':             videos().root('laliga')
        elif action == 'videos_bundesliga':         videos().root('bundesliga')
        elif action == 'videos_seriea':             videos().root('seriea')
        elif action == 'videos_ligue1':             videos().root('ligue1')
        elif action == 'videos_eredivisie':         videos().root('eredivisie')
        elif action == 'videos_primeiraliga':       videos().root('primeiraliga')
        elif action == 'videos_uefachampionleague': videos().root('uefachampionleague')
        elif action == 'videos_uefaeuropaleague':   videos().root('uefaeuropaleague')
        elif action == 'videos_copalibertadores':   videos().root('copalibertadores')
        elif action == 'videos_highlights':         videos().root2('highlights')
        elif action == 'videos_search':             videos().search(query)
        elif action == 'videos_parts':              videoparts().get(name, url, image, date, genre, plot, title, show)
        elif action == 'play':                      resolver().run(url)

        if action == None:
            pass
        elif action.startswith('videos'):
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            index().container_view('videos', {'skin.confluence' : 504})
        xbmcplugin.setPluginFanart(int(sys.argv[1]), addonFanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='10'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
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
        total = len(rootList)
        for i in rootList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)

                cm = []

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def nextList(self, nextList):
        try: next = nextList[0]['next']
        except: return
        if next == '': return
        name, url, image = language(30361).encode("utf-8"), next, addonNext
        sysurl = urllib.quote_plus(url)

        u = '%s?action=videos&url=%s' % (sys.argv[0], sysurl)

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def videoList(self, videoList):
        if videoList == None: return

        total = len(videoList)
        for i in videoList:
            try:
                name, url, image, date, genre, plot, title, show = i['name'], i['url'], i['image'], i['date'], i['genre'], i['plot'], i['title'], i['show']
                if show == '': show = addonName
                if image == '': image = addonFanart
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '
                if date == '': date = ' '

                sysname, sysurl, sysimage, sysdate, sysgenre, sysplot, systitle, sysshow = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(date), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(title), urllib.quote_plus(show)
                u = '%s?action=videos_parts&name=%s&url=%s&image=%s&date=%s&genre=%s&plot=%s&title=%s&show=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysdate, sysgenre, sysplot, systitle, sysshow)

                meta = {'label': title, 'title': title, 'studio': show, 'premiered': date, 'genre': genre, 'plot': plot}

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=view_videos)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def videopartList(self, videopartList):
        if videopartList == None: return

        total = len(videopartList)
        for i in videopartList:
            try:
                name, url, image, date, genre, plot, title, show = i['name'], i['url'], i['image'], i['date'], i['genre'], i['plot'], i['title'], i['show']
                if show == '': show = addonName
                if image == '': image = addonFanart
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '
                if date == '': date = ' '

                sysurl = urllib.quote_plus(url)
                u = '%s?action=play&url=%s' % (sys.argv[0], sysurl)

                meta = {'label': title, 'title': title, 'studio': show, 'premiered': date, 'genre': genre, 'plot': plot}

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_play_from_here&url=%s)' % (sys.argv[0], sysurl)))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=view_videos)' % (sys.argv[0])))
                cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", addonFanart)
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
            u = '%s?action=play&url=%s' % (sys.argv[0], params["url"])

            meta = {'title': xbmc.getInfoLabel('ListItemNoWrap(%s).title' % i), 'studio': xbmc.getInfoLabel('ListItemNoWrap(%s).studio' % i), 'writer': xbmc.getInfoLabel('ListItemNoWrap(%s).writer' % i), 'director': xbmc.getInfoLabel('ListItemNoWrap(%s).director' % i), 'rating': xbmc.getInfoLabel('ListItemNoWrap(%s).rating' % i), 'duration': xbmc.getInfoLabel('ListItemNoWrap(%s).duration' % i), 'premiered': xbmc.getInfoLabel('ListItemNoWrap(%s).premiered' % i), 'plot': xbmc.getInfoLabel('ListItemNoWrap(%s).plot' % i)}
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
                if not (label == '' or label == None): break
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
        rootList.append({'name': 30501, 'image': 'Games.png', 'action': 'videos_games'})
        rootList.append({'name': 30502, 'image': 'Highlights.png', 'action': 'videos_highlights'})
        rootList.append({'name': 30503, 'image': 'Search.png', 'action': 'videos_search'})
        rootList.append({'name': 30504, 'image': 'Premier League.png', 'action': 'videos_premierleague'})
        rootList.append({'name': 30505, 'image': 'La Liga.png', 'action': 'videos_laliga'})
        rootList.append({'name': 30506, 'image': 'Bundesliga.png', 'action': 'videos_bundesliga'})
        rootList.append({'name': 30507, 'image': 'Serie A.png', 'action': 'videos_seriea'})
        rootList.append({'name': 30508, 'image': 'Ligue 1.png', 'action': 'videos_ligue1'})
        rootList.append({'name': 30509, 'image': 'Eredivisie.png', 'action': 'videos_eredivisie'})
        rootList.append({'name': 30510, 'image': 'Primeira Liga.png', 'action': 'videos_primeiraliga'})
        rootList.append({'name': 30511, 'image': 'UEFA Champions League.png', 'action': 'videos_uefachampionleague'})
        rootList.append({'name': 30512, 'image': 'UEFA Europa League.png', 'action': 'videos_uefaeuropaleague'})
        rootList.append({'name': 30513, 'image': 'Copa Libertadores.png', 'action': 'videos_copalibertadores'})
        index().rootList(rootList)

class link:
    def __init__(self):
        self.lfv_base = 'http://livefootballvideo.com'
        self.lfv_search = 'http://www.google.com/cse?cx=partner-pub-9069051203647610:8413886168&sa=Search&ie=UTF-8&nojs=1&ref=livefootballvideo.com/&q=%s'
        self.lfv_games = 'http://livefootballvideo.com/fullmatch'
        self.lfv_highlights = 'http://livefootballvideo.com/highlights'
        self.lfv_premierleague = 'http://livefootballvideo.com/competitions/premier-league'
        self.lfv_laliga = 'http://livefootballvideo.com/competitions/la-liga'
        self.lfv_bundesliga = 'http://livefootballvideo.com/competitions/bundesliga'
        self.lfv_seriea = 'http://livefootballvideo.com/competitions/serie-a'
        self.lfv_ligue1 = 'http://livefootballvideo.com/competitions/ligue-1'
        self.lfv_eredivisie = 'http://livefootballvideo.com/competitions/eredivisie'
        self.lfv_primeiraliga = 'http://livefootballvideo.com/competitions/primeira-liga'
        self.lfv_uefachampionleague = 'http://livefootballvideo.com/competitions/uefa-champions-league'
        self.lfv_uefaeuropaleague = 'http://livefootballvideo.com/competitions/uefa-europa-league'
        self.lfv_copalibertadores = 'http://livefootballvideo.com/competitions/copa-libertadores'

class videos:
    def __init__(self):
        self.list = []

    def root(self, url):
        if url == 'games': url = link().lfv_games
        elif url == 'premierleague': url = link().lfv_premierleague
        elif url == 'laliga': url = link().lfv_laliga
        elif url == 'bundesliga': url = link().lfv_bundesliga
        elif url == 'seriea': url = link().lfv_seriea
        elif url == 'ligue1': url = link().lfv_ligue1
        elif url == 'eredivisie': url = link().lfv_eredivisie
        elif url == 'primeiraliga': url = link().lfv_primeiraliga
        elif url == 'uefachampionleague': url = link().lfv_uefachampionleague
        elif url == 'uefaeuropaleague': url = link().lfv_uefaeuropaleague
        elif url == 'copalibertadores': url = link().lfv_copalibertadores

        self.list = self.lfv_list(url)
        #self.list = cache(self.lfv_list, url)
        index().videoList(self.list)
        index().nextList(self.list)

    def root2(self, url):
        if url == 'highlights': url = link().lfv_highlights

        self.list = self.lfv_list2(url)
        #self.list = cache(self.lfv_list2, url)
        index().videoList(self.list)
        index().nextList(self.list)

    def get(self, url):
        if '/highlights/' in url:
            #self.list = self.lfv_list2(url)
            self.list = cache(self.lfv_list2, url)
        else:
            #self.list = self.lfv_list(url)
            self.list = cache(self.lfv_list, url)
        index().videoList(self.list)
        index().nextList(self.list)

    def search(self, query=None):
        if query == None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = query
        if not (self.query == None or self.query == ''):
            self.query = link().lfv_search % urllib.quote_plus(self.query)
            self.list = self.lfv_list3(self.query)
            index().videoList(self.list)


    def lfv_list(self, url):
        try:
            result = getUrl(url, timeout='30').result
            result = re.sub('<li\s.+?>','<li>', result)
            videos = common.parseDOM(result, "li")
        except:
            return

        try:
            next = common.parseDOM(result, "div", attrs = { "class": "wp-pagenavi" })
            if len(next) > 1: next = next[1]
            else: next = next[0]
            next = common.parseDOM(next, "a", ret="href", attrs = { "class": "nextpostslink" })[0]
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for video in videos:
            try:
                title = common.parseDOM(video, "a", ret="title")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                date = common.parseDOM(video, "p")[-1]
                date = re.findall('(\d+)[/](\d+)[/](\d+)', date, re.I)[0]
                date = '%s-%s-%s' % ('%04d' % int(date[2]), '%02d' % int(date[0]), '%02d' % int(date[1]))

                name = '%s (%s)' % (title, date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(video, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(video, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': date, 'genre': 'Sports', 'plot': '', 'title': title, 'show': '', 'next': next})
            except:
                pass

        return self.list

    def lfv_list2(self, url):
        try:
            result = getUrl(url, timeout='30').result
            result = re.sub('<li\s.+?>','<li>', result)
            videos = common.parseDOM(result, "li")
        except:
            return

        try:
            next = common.parseDOM(result, "div", attrs = { "class": "wp-pagenavi" })
            if len(next) > 1: next = next[1]
            else: next = next[0]
            next = common.parseDOM(next, "a", ret="href", attrs = { "class": "nextpostslink" })[0]
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for video in videos:
            try:
                home = common.parseDOM(video, "div", attrs = { "class": "team.+?" })[0]
                home = home.split("&nbsp;")[0]
                away = common.parseDOM(video, "div", attrs = { "class": "team.+?" })[-1]
                away = away.split("&nbsp;")[-1]
                title = '%s vs %s' % (home, away)
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                date = common.parseDOM(video, "span", attrs = { "class": "starttime.+?" })[0]
                date = common.replaceHTMLCodes(date)
                date = date.encode('utf-8')

                name = '%s (%s)' % (title, date)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(video, "a", ret="href", attrs = { "class": "playvideo" })[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': '', 'date': date, 'genre': 'Sports', 'plot': '', 'title': title, 'show': '', 'next': next})
            except:
                pass

        return self.list

    def lfv_list3(self, url):
        try:
            result = getUrl(url, timeout='30').result
            videos = common.parseDOM(result, "h2")
        except:
            return
        for video in videos:
            try:
                name = common.parseDOM(video, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = re.sub('<b>|</b>|&\sAll\sGoals|\sDownload', '', name).strip()
                name = re.sub('\s\d+\s-\s\d+\s', ' vs ', name)
                name = name.encode('utf-8')

                url = common.parseDOM(video, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                if not ('/fullmatch/' in url or '/highlights/' in url): raise Exception()

                self.list.append({'name': name, 'url': url, 'image': '', 'date': '', 'genre': 'Sports', 'plot': '', 'title': name, 'show': '', 'next': ''})
            except:
                pass

        return self.list

class videoparts:
    def __init__(self):
        self.list = []

    def get(self, name, url, image, date, genre, plot, title, show):
        if '/highlights/' in url:
            #self.list = self.lfv_list2(name, url, image, date, genre, plot, title, show)
            self.list = cache(self.lfv_list2, name, url, image, date, genre, plot, title, show)
        else:
            #self.list = self.lfv_list(name, url, image, date, genre, plot, title, show)
            self.list = cache(self.lfv_list, name, url, image, date, genre, plot, title, show)

        index().videopartList(self.list)


    def lfv_list(self, name, url, image, date, genre, plot, title, show):
        try:
            result = getUrl(url, timeout='30').result
            result = result.replace('<object', '<iframe').replace(' data=', ' src=')
            result = common.parseDOM(result, "div", attrs = { "id": "fullvideo" })[0]
            videos = common.parseDOM(result, "div", attrs = { "class": "et-learn-more.+?" })
        except:
            return

        for video in videos:
            try:
                lang = common.parseDOM(video, "span")[0]
                lang = lang.split("-")[-1].strip()

                if 'proxy.link=lfv*' in video:
                    import GKDecrypter
                    parts = re.compile('proxy[.]link=lfv[*](.+?)&').findall(video)
                    parts = uniqueList(parts).list
                    parts = [GKDecrypter.decrypter(198,128).decrypt(i,base64.urlsafe_b64decode('Y0ZNSENPOUhQeHdXbkR4cWJQVlU='),'ECB').split('\0')[0] for i in parts]
                else:
                    video = video.replace('"//', '"http://')
                    parts = re.findall('"(http://.+?)"', video, re.I)
                    parts = [i for i in parts if any(i.startswith(x) for x in resolver().hostList)]

                count = 0
                for url in parts:
                    count = count + 1

                    name = '%s (%s) %s' % (title, str(count), lang)
                    name = common.replaceHTMLCodes(name)
                    name = name.encode('utf-8')

                    url = common.replaceHTMLCodes(url)
                    if url.startswith('//') : url = 'http:' + url
                    if not any(url.startswith(i) for i in resolver().hostList): continue
                    url = url.encode('utf-8')

                    self.list.append({'name': name, 'url': url, 'image': image, 'date': date, 'genre': genre, 'plot': plot, 'title': title, 'show': show})
            except:
                pass

        return self.list

    def lfv_list2(self, name, url, image, date, genre, plot, title, show):
        try:
            result = getUrl(url, timeout='30').result
            result = result.replace('"//', '"http://')

            result = re.findall('"(http://.+?)"', result, re.I)
            result = uniqueList(result).list

            videos = [i for i in result if any(i.startswith(x) for x in resolver().hostList)]
            videos = [i for i in videos if not i.endswith('.js')]
        except:
            return

        for video in videos:
            try:
                url = video
                url = common.replaceHTMLCodes(url)
                if url.startswith('//') : url = 'http:' + url
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': date, 'genre': genre, 'plot': plot, 'title': title, 'show': show})
            except:
                pass

        return self.list

class resolver:
    def __init__(self):
        self.vk_base = 'http://vk.com'
        self.dailymotion_base = 'http://www.dailymotion.com'
        self.facebook_base = 'http://www.facebook.com/video'
        self.playwire_base = 'http://cdn.playwire.com'
        self.youtube_base = 'http://www.youtube.com'
        self.rutube_base = 'http://rutube.ru'
        self.videa_base = 'http://videa.hu'
        self.sapo_base = 'http://videos.sapo.pt'
        self.hostList = self.host_list()

    def run(self, url):
        try:
            if url.startswith(self.vk_base): url = self.vk(url)
            elif url.startswith(self.dailymotion_base): url = self.dailymotion(url)
            elif url.startswith(self.facebook_base): url = self.facebook(url)
            elif url.startswith(self.playwire_base): url = self.playwire(url)
            elif url.startswith(self.youtube_base): url = self.youtube(url)
            elif url.startswith(self.rutube_base): url = self.rutube(url)
            elif url.startswith(self.videa_base): url = self.videa(url)
            elif url.startswith(self.sapo_base): url = self.sapo(url)

            if url == None: raise Exception()
            player().run(url)
            return url
        except:
            index().infoDialog(language(30303).encode("utf-8"))
            return

    def host_list(self):
        return [self.vk_base, self.dailymotion_base, self.facebook_base, self.playwire_base, self.youtube_base, self.rutube_base, self.videa_base, self.sapo_base]

    def vk(self, url):
        try:
            if not 'hash' in url: url = self.vk_private(url)

            url = url.replace('http://', 'https://')
            url = url.encode('utf-8')

            result = getUrl(url).result
            url = None
            try: url = re.compile('url240=(.+?)&').findall(result)[0]
            except: pass
            try: url = re.compile('url360=(.+?)&').findall(result)[0]
            except: pass
            try: url = re.compile('url480=(.+?)&').findall(result)[0]
            except: pass
            try: url = re.compile('url720=(.+?)&').findall(result)[0]
            except: pass

            return url
        except:
            return

    def vk_private(self, url):
        urln = 'http://livefootballvideo.com/player/vkru/plugins/plugins_vk.php'

        result = re.compile('\/video(.*)_(.*)').findall(url)[0]
        oid, vid = result[0], result[1]

        post = {'getacc':'true'}
        post = urllib.urlencode(post)
        result = getUrl(urln, post=post).result
        result = re.compile('u=(.*)&p=(.*)&').findall(result)[0]
        username, pwd = result[0], result[1]
        ipostfield = "pass=%s&email=%s&act=login&captcha_sid=&captcha_key=&role=al_frame&_origin=http://vk.com&expire=" % (pwd, username)

        post = {'icookie':'remixlang=3',
                'ipostfield':ipostfield,
				'ihttpheader':'true',
				'iagent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
				'isslverify':'true',
				'iheader':'true',
				'url':'https://login.vk.com/?act=login',
				'ipost':'true'}
        post = urllib.urlencode(post)
        result = getUrl(urln, post=post).result
        result = re.compile('Set-Cookie: h=(.*?)\;.*?\sSet-Cookie:\ss=(.*?);.*?\sSet-Cookie:\sl=(.*?);.*?\sSet-Cookie:\sp=(.*?);.*?\sLocation.*?hash=(.*)').findall(result)
        h, s, l, p, hash = result[0][0], result[0][1], result[0][2], result[0][3], result[0][4]
        icookiePost = "h=%s; s=%s; p=%s; l=%s; remixlang=3" % (h,s,p,l)
        if hash[len(hash)-1] == '\r': hash = hash[:-1]
        urlPost = 'http://vk.com/login.php?act=slogin&to=&s=%s&__q_hash=%s' % (s,hash)

        post = {'icookie':icookiePost,
				'iheader':'true',
				'url':urlPost,
				'ihttpheader':'true',
				'iagent':'	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        post = urllib.urlencode(post)
        result = getUrl(urln, post=post).result
        remixId = re.compile('remixsid=(.*?);').findall(result)[0]
        icookiePost = "remixlang=3; remixsid=%s" % (remixId)
        ipostFieldPost = "vid=%s&act=video_embed_box&al=1&oid=%s"	% (vid,oid)

        post = {'icookie':icookiePost,
				'ipostfield':ipostFieldPost,
				'ihttpheader':'true',
				'iagent':'	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
				'iheader':'true',
				'url':'http://vk.com/al_video.php'
				}
        post = urllib.urlencode(post)
        result = getUrl(urln, post=post).result
        url = re.compile('iframe src=&quot;(.*)";').findall(result)[0]
        return url

    def dailymotion(self, url):
        try:
            url = url.replace('dailymotion.com/video/', 'dailymotion.com/embed/video/')

            result = getUrl(url).result
            url = None
            try: url = re.compile('"stream_h264_ld_url":"(.+?)"').findall(result)[0]
            except: pass
            try: url = re.compile('"stream_h264_url":"(.+?)"').findall(result)[0]
            except: pass
            try: url = re.compile('"stream_h264_hq_url":"(.+?)"').findall(result)[0]
            except: pass
            try: url = re.compile('"stream_h264_hd_url":"(.+?)"').findall(result)[0]
            except: pass

            url = urllib.unquote(url).decode('utf-8').replace('\\/', '/')
            return url
        except:
            return

    def facebook(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('"params","(.+?)"').findall(result)[0]
            url = re.sub(r'\\(.)', r'\1', urllib.unquote_plus(url.decode('unicode_escape')))
            url = re.compile('_src":"(.+?)"').findall(url)[0]
            return url
        except:
            return

    def playwire(self, url):
        try:
            url = url.split("config=")[-1]
            result = getUrl(url).result
            url = re.compile('"src":"(.+?)"').findall(result)[0]
            return url
        except:
            return

    def youtube(self, url):
        try:
            url = url.split("?v=")[-1].split("/")[-1].split("?")[0]
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
            return url
        except:
            return

    def rutube(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('"m3u8": "(.+?)"').findall(result)[0]
            return url
        except:
            return

    def videa(self, url):
        try:
            url = url.rsplit("v=", 1)[-1].rsplit("-", 1)[-1]
            if url.startswith('http://'): raise Exception()
            url = 'http://videa.hu/flvplayer_get_video_xml.php?v=%s' % url

            result = getUrl(url).result
            url = re.compile('video_url="(.+?)"').findall(result)[0]
            if url.startswith('//'): url = 'http:' + url

            return url
        except:
            return

    def sapo(self, url):
        try:
            id = url.split("file=")[-1].split("sapo.pt/")[-1].split("/")[0]
            url = '%s/%s/rss2' % (self.sapo_base, id)

            result = getUrl(url).result
            url = common.parseDOM(result, "media:content", ret="url")[0]
            url = '%s%s/mov' % (url.split(id)[0], id)
            url = getUrl(url, output='geturl').result

            return url
        except:
            return

main()