# -*- coding: utf-8 -*-

'''
    Hellenic Player XBMC Addon
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
        elif action == 'item_play_from_here':              contextMenu().item_play_from_here(url)
        elif action == 'playlist_open':                    contextMenu().playlist_open()
        elif action == 'settings_open':                    contextMenu().settings_open()
        elif action == 'addon_home':                       contextMenu().addon_home()
        elif action == 'view_tvshows':                     contextMenu().view('tvshows')
        elif action == 'view_videos':                      contextMenu().view('videos')
        elif action == 'favourite_add':                    contextMenu().favourite_add(favData, name, url, image)
        elif action == 'favourite_delete':                 contextMenu().favourite_delete(favData, name, url)
        elif action == 'favourite_moveUp':                 contextMenu().favourite_moveUp(favData, name, url)
        elif action == 'favourite_moveDown':               contextMenu().favourite_moveDown(favData, name, url)
        elif action == 'root_shows':                       root().shows()
        elif action == 'root_archive':                     root().archives()
        elif action == 'root_news':                        root().news()
        elif action == 'root_sports':                      root().sports()
        elif action == 'root_music':                       root().music()
        elif action == 'item_live':                        item().live()
        elif action == 'shows_favourites':                 favourites().shows()
        elif action == 'shows_mega':                       mega().shows()
        elif action == 'shows_ant1':                       ant1().shows()
        elif action == 'shows_alpha':                      alpha().shows()
        elif action == 'shows_star':                       star().shows()
        elif action == 'shows_skai':                       skai().shows()
        elif action == 'shows_rik':                        cybc().shows()
        elif action == 'shows_sigma':                      sigma().shows()
        elif action == 'shows_youtube.madtv':              youtube().madtv()
        elif action == 'shows_cinegreece.mega':            cinegreece().mega()
        elif action == 'shows_cinegreece.ant1':            cinegreece().ant1()
        elif action == 'shows_cinegreece.alpha':           cinegreece().alpha()
        elif action == 'shows_cinegreece.star':            cinegreece().star()
        elif action == 'shows_cinegreece.ert':             cinegreece().ert()
        elif action == 'shows_cinegreece.rik':             cinegreece().rik()
        elif action == 'episodes_mega.news':               mega().news()
        elif action == 'episodes_ant1.news':               ant1().news()
        elif action == 'episodes_alpha.news':              alpha().news()
        elif action == 'episodes_star.news':               star().news()
        elif action == 'episodes_skai.news':               skai().news()
        elif action == 'episodes_cybc.news':               cybc().news()
        elif action == 'episodes_sigma.news':              sigma().news()
        elif action == 'episodes_youtube.enikos':          youtube().enikos()
        elif action == 'episodes_mega.sports':             mega().sports()
        elif action == 'episodes_ant1.sports':             ant1().sports()
        elif action == 'episodes_cybc.sports':             cybc().sports()
        elif action == 'episodes_novasports.news':         novasports().news()
        elif action == 'episodes_dailymotion.superleague': dailymotion().superleague()
        elif action == 'episodes_novasports.shows':        novasports().shows()
        elif action == 'episodes_dailymotion.superball':   dailymotion().superball()
        elif action == 'shows_youtube.madgreekz':          youtube().madgreekz()
        elif action == 'episodes_mtvhitlisthellas':        mtvchart().mtvhitlisthellas()
        elif action == 'episodes_rythmoshitlist':          rythmoschart().rythmoshitlist()
        elif action == 'episodes_mtvdancefloor':           mtvchart().mtvdancefloor()
        elif action == 'episodes_eurotop20':               mtvchart().eurotop20()
        elif action == 'episodes_usatop20':                mtvchart().usatop20()
        elif action == 'shows_skai.docs':                  skai().docs()
        elif action == 'episodes':                         episodes().get(name, url, image, genre, plot, show)
        elif action == 'play':                             resolver().run(url)

        if action is None:
            pass
        elif action.startswith('shows'):
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            index().container_view('tvshows', {'skin.confluence' : 500})
        elif action.startswith('episodes'):
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            index().container_view('videos', {'skin.confluence' : 504})
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
                if action.startswith('episodes'): cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                if action.startswith('episodes'): cm.append((language(30402).encode("utf-8"), 'RunPlugin(%s?action=item_random_play)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def itemList(self, itemList):
        total = len(itemList)
        for i in itemList:
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
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

    def showList(self, showList):
        if showList == None: return

        file = xbmcvfs.File(favData)
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
                if action.startswith('shows_cinegreece'):
                    if not '"%s"' % url in favRead: cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysurl, sysimage)))
                    else: cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                if action == 'shows_favourites':
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30407).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30408).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    if getSetting("fav_sort") == '1': cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if getSetting("fav_sort") == '1': cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30425).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                else:
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
            u = '%s?action=play&url=%s' % (sys.argv[0], params["url"])

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

    def shows(self):
        file = open(favData, 'r')
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]".+?"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, url, image in match:
            self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': ''})

        if getSetting("fav_sort") == '0':
            self.list = sorted(self.list, key=itemgetter('name'))

        index().showList(self.list)

class root:
    def get(self):
        rootList = []
        index().itemList([{'name': 30501, 'image': 'Live.png', 'action': 'item_live'}])
        rootList.append({'name': 30502, 'image': 'Networks.png', 'action': 'root_shows'})
        rootList.append({'name': 30503, 'image': 'Archives.png', 'action': 'root_archive'})
        rootList.append({'name': 30504, 'image': 'Favourites.png', 'action': 'shows_favourites'})
        rootList.append({'name': 30505, 'image': 'News.png', 'action': 'root_news'})
        rootList.append({'name': 30506, 'image': 'Sports.png', 'action': 'root_sports'})
        rootList.append({'name': 30507, 'image': 'Music.png', 'action': 'root_music'})
        rootList.append({'name': 30508, 'image': 'Documentaries.png', 'action': 'shows_skai.docs'})
        index().rootList(rootList)

    def shows(self):
        rootList = []
        rootList.append({'name': 30521, 'image': 'MEGA.png', 'action': 'shows_mega'})
        rootList.append({'name': 30522, 'image': 'ANT1.png', 'action': 'shows_ant1'})
        rootList.append({'name': 30523, 'image': 'ALPHA.png', 'action': 'shows_alpha'})
        rootList.append({'name': 30524, 'image': 'STAR.png', 'action': 'shows_star'})
        rootList.append({'name': 30525, 'image': 'SKAI.png', 'action': 'shows_skai'})
        rootList.append({'name': 30526, 'image': 'RIK.png', 'action': 'shows_rik'})
        rootList.append({'name': 30527, 'image': 'SIGMA.png', 'action': 'shows_sigma'})
        rootList.append({'name': 30528, 'image': 'MAD TV.png', 'action': 'shows_youtube.madtv'})
        index().rootList(rootList)

    def archives(self):
        rootList = []
        rootList.append({'name': 30541, 'image': 'MEGA.png', 'action': 'shows_cinegreece.mega'})
        rootList.append({'name': 30542, 'image': 'ANT1.png', 'action': 'shows_cinegreece.ant1'})
        rootList.append({'name': 30543, 'image': 'ALPHA.png', 'action': 'shows_cinegreece.alpha'})
        rootList.append({'name': 30544, 'image': 'STAR.png', 'action': 'shows_cinegreece.star'})
        rootList.append({'name': 30545, 'image': 'ERT.png', 'action': 'shows_cinegreece.ert'})
        rootList.append({'name': 30546, 'image': 'RIK.png', 'action': 'shows_cinegreece.rik'})
        index().rootList(rootList)

    def news(self):
        rootList = []
        rootList.append({'name': 30561, 'image': 'MEGA.png', 'action': 'episodes_mega.news'})
        rootList.append({'name': 30562, 'image': 'ANT1.png', 'action': 'episodes_ant1.news'})
        rootList.append({'name': 30563, 'image': 'ALPHA.png', 'action': 'episodes_alpha.news'})
        rootList.append({'name': 30564, 'image': 'STAR.png', 'action': 'episodes_star.news'})
        rootList.append({'name': 30565, 'image': 'SKAI.png', 'action': 'episodes_skai.news'})
        rootList.append({'name': 30566, 'image': 'RIK.png', 'action': 'episodes_cybc.news'})
        rootList.append({'name': 30567, 'image': 'SIGMA.png', 'action': 'episodes_sigma.news'})
        rootList.append({'name': 30568, 'image': 'ENIKOS.png', 'action': 'episodes_youtube.enikos'})
        index().rootList(rootList)

    def sports(self):
        rootList = []
        rootList.append({'name': 30581, 'image': 'MEGA.png', 'action': 'episodes_mega.sports'})
        rootList.append({'name': 30582, 'image': 'ANT1.png', 'action': 'episodes_ant1.sports'})
        rootList.append({'name': 30583, 'image': 'RIK.png', 'action': 'episodes_cybc.sports'})
        rootList.append({'name': 30584, 'image': 'Novasports.png', 'action': 'episodes_novasports.news'})
        rootList.append({'name': 30585, 'image': 'Super League.png', 'action': 'episodes_dailymotion.superleague'})
        rootList.append({'name': 30586, 'image': 'Novasports.png', 'action': 'episodes_novasports.shows'})
        rootList.append({'name': 30587, 'image': 'SuperBALL.png', 'action': 'episodes_dailymotion.superball'})
        index().rootList(rootList)

    def music(self):
        rootList = []
        rootList.append({'name': 30601, 'image': 'MAD Greekz.png', 'action': 'shows_youtube.madgreekz'})
        rootList.append({'name': 30602, 'image': 'MTV Hit List Hellas.png', 'action': 'episodes_mtvhitlisthellas'})
        rootList.append({'name': 30603, 'image': 'Rythmos Hit List.png', 'action': 'episodes_rythmoshitlist'})
        rootList.append({'name': 30604, 'image': 'MTV Dance Floor.png', 'action': 'episodes_mtvdancefloor'})
        rootList.append({'name': 30605, 'image': 'Euro Top 20.png', 'action': 'episodes_eurotop20'})
        rootList.append({'name': 30606, 'image': 'U.S. Top 20.png', 'action': 'episodes_usatop20'})
        index().rootList(rootList)

class item:
    def live(self):
        if index().addon_status('plugin.video.hellenic.tv') is None:
            index().okDialog(language(30323).encode("utf-8"), language(30324).encode("utf-8"))
            return
        xbmc.executebuiltin('RunPlugin(plugin://plugin.video.hellenic.tv/?action=dialog)')

class episodes:
    def get(self, name, url, image, genre, plot, show):
        if url.startswith(mega().feed_link):
            self.list = mega().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(mega().base_link):
            self.list = mega().episodes_list2(name, url, image, genre, plot, show)
        elif url.startswith(ant1().base_link):
            self.list = ant1().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(alpha().base_link):
            self.list = alpha().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(star().base_link):
            self.list = star().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(skai().base_link):
            self.list = skai().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(cybc().base_link):
            self.list = cybc().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(sigma().base_link):
            self.list = sigma().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(cinegreece().base_link):
            self.list = cinegreece().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(novasports().base_link):
            self.list = novasports().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(mtvchart().base_link):
            self.list = mtvchart().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(rythmoschart().base_link):
            self.list = rythmoschart().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(dailymotion().api_link):
            self.list = dailymotion().episodes_list(name, url, image, genre, plot, show)
        elif url.startswith(youtube().api_link):
            self.list = youtube().episodes_list(name, url, image, genre, plot, show)
        index().episodeList(self.list)

class resolver:
    def run(self, url):
        try:
            if url.startswith(mega().base_link): url = mega().resolve(url)
            elif url.startswith(ant1().base_link): url = ant1().resolve(url)
            elif url.startswith(alpha().base_link): url = alpha().resolve(url)
            elif url.startswith(cybc().base_link): url = cybc().resolve(url)
            elif url.startswith(sigma().base_link): url = sigma().resolve(url)
            elif url.startswith(novasports().base_link): url = novasports().resolve(url)
            elif url.startswith(dailymotion().base_link): url = dailymotion().resolve(url)
            elif url.startswith(youtube().search_link): url = youtube().resolve_search(url)
            elif url.startswith(youtube().base_link): url = youtube().resolve(url)

            if url is None: raise Exception()
            player().run(url)
            return url
        except:
            index().infoDialog(language(30307).encode("utf-8"))
            return


class mega:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.megatv.com'
        self.feed_link = 'http://megatv.feed.gr'
        self.media_link = 'http://media.megatv.com'
        self.shows_link = 'http://megatv.feed.gr/mobile/mobile.asp?pageid=816&catidlocal=32623&subidlocal=20933'
        self.episodes_link = 'http://megatv.feed.gr/mobile/mobile/ekpompiindex_29954.asp?pageid=816&catidlocal=%s'
        self.news_link = 'http://www.megatv.com/webtv/default.asp?catid=27377&catidlocal=27377'
        self.sports_link = 'http://www.megatv.com/webtv/default.asp?catid=27377&catidlocal=27387'

    def shows(self):
        #self.list = self.shows_list()
        self.list = cache(self.shows_list)
        index().showList(self.list)

    def news(self):
        name = 'MEGA GEGONOTA'
        self.list = self.episodes_list2(name, self.news_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def sports(self):
        name = 'MEGA SPORTS'
        self.list = self.episodes_list2(name, self.sports_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def shows_list(self):
        try:
            result = getUrl(self.shows_link, mobile=True).result
            shows = common.parseDOM(result, "li")
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "h1")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                tpl = common.parseDOM(show, "a", ret="data-tpl")[0]
                if not tpl == 'ekpompiindex': raise Exception()

                url = common.parseDOM(show, "a", ret="data-params")[0]
                url = self.episodes_link % url.split("catid=")[-1]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': '', 'genre': 'Greek', 'plot': ''})
            except:
                pass

        threads = []
        for i in range(0, len(self.list)): threads.append(Thread(self.shows_info, i))
        [i.start() for i in threads]
        [i.join() for i in threads]

        return self.list

    def shows_info(self, i):
        try:
            result = getUrl(self.list[i]['url'], mobile=True).result

            image = common.parseDOM(result, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')
            self.list[i].update({'image': image})
        except:
            pass

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url, mobile=True).result
            result = common.parseDOM(result, "section", attrs = { "class": "ekpompes.+?" })[0]
            episodes = common.parseDOM(result, "li")
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "h5")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="data-vUrl")[0]
                url = url.replace(',', '').split('/i/', 1)[-1].rsplit('.csmil', 1)[0]
                url = '%s/%s' % (self.media_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def episodes_list2(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            result = result.decode('iso-8859-7').encode('utf-8')

            v1 = '/megagegonota/'
            match = re.search("addPrototypeElement[(]'.+?','REST','(.+?)','(.+?)'.+?[)]", result)
            v2,v3 = match.groups()
            redirect = '%s%s%s?%s' % (self.base_link, v1, v2, v3)

            result = getUrl(redirect).result
            result = result.decode('iso-8859-7').encode('utf-8')
            result = common.parseDOM(result, "div", attrs = { "class": "rest" })[0]
            episodes = common.parseDOM(result, "li")
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "a")[1]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[0]
                url = url.split("catid=")[-1].replace("')",'')
                url = '%s/r.asp?catid=%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                if not image.startswith('http://'):
                    image = '%s%s%s' % (self.base_link, v1, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result
            url = re.compile('{file:"(%s/.+?)"' % self.media_link).findall(result)[0]
            return url
        except:
            return

class ant1:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.antenna.gr'
        self.img_link = 'http://www.antenna.gr/imgHandler/326'
        self.shows_link = 'http://www.antenna.gr/tv/doubleip/shows?version=3.0'
        self.episodes_link = 'http://www.antenna.gr/tv/doubleip/show?version=3.0&sid='
        self.episodes_link2 = 'http://www.antenna.gr/tv/doubleip/categories?version=3.0&howmany=100&cid='
        self.news_link = 'http://www.antenna.gr/tv/doubleip/show?version=3.0&sid=222903'
        self.sports_link = 'http://www.antenna.gr/tv/doubleip/categories?version=3.0&howmany=100&cid=3062'
        self.watch_link = 'http://www.antenna.gr/webtv/watch?cid=%s'
        self.info_link = 'http://www.antenna.gr/webtv/templates/data/player?cid=%s'

    def shows(self):
        #self.list = self.shows_list()
        self.list = cache(self.shows_list)
        index().showList(self.list)

    def news(self):
        name = 'ANT1 NEWS'
        self.list = self.episodes_list(name, self.news_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def sports(self):
        name = 'ANT1 SPORTS'
        self.list = self.episodes_list(name, self.sports_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def shows_list(self):
        try:
            self.list.append({'name': 'ANT1 NEWS', 'url': self.news_link, 'image': 'http://www.antenna.gr/imgHandler/326/5a7c9f1a-79b6-47e0-b8ac-304d4e84c591.jpg', 'genre': 'Greek', 'plot': 'ANT1 NEWS'})

            result = getUrl(self.shows_link, mobile=True).result
            shows = re.compile('({.+?})').findall(result)
        except:
            return

        for show in shows:
            try:
                i = json.loads(show)

                name = i['teasertitle'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                image = i['webpath'].strip()
                image = '%s/%s' % (self.img_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                url = i['id'].strip()
                url = self.episodes_link + url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                try: plot = i['teasertext'].strip()
                except: plot = ''
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': plot})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url, mobile=True).result

            if url.startswith(self.episodes_link):
                id = json.loads(result)
                id = id['feed']['show']['videolib']
                if url.endswith('sid=223077'): id = '3110'#EUROPA LEAGUE
                elif url.endswith('sid=318756'): id = '3246'#ΟΛΑ ΤΡΕΛΑ
                elif url.endswith('sid=314594'): id = '4542'#THE VOICE
            elif url.startswith(self.episodes_link2):
                id = ''

            if id == '':
                episodes = result.replace("'",'"').replace('"title"','"caption"').replace('"image"','"webpath"').replace('"trailer_contentid"','"contentid"')
                episodes = re.compile('({.+?})').findall(episodes)
            else:
                url = self.episodes_link2 + id
                episodes = getUrl(url, mobile=True).result
                episodes = re.compile('({.+?})').findall(episodes)
        except:
            return

        for episode in episodes:
            try:
                i = json.loads(episode)

                name = i['caption'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                image = i['webpath'].strip()
                image = '%s/%s' % (self.img_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                url = i['contentid'].strip()
                url = self.watch_link % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        id = url.split("?")[-1].split("cid=")[-1].split("&")[0]
        dataUrl = self.info_link % id
        pageUrl = self.watch_link % id
        swfUrl = 'http://www.antenna.gr/webtv/images/fbplayer.swf'

        try:
            result = getUrl(dataUrl).result
            rtmp = common.parseDOM(result, "FMS")[0]
            playpath = common.parseDOM(result, "appStream")[0]
            if playpath.endswith('/GR.flv'): raise Exception()
            url = '%s playpath=%s pageUrl=%s swfUrl=%s swfVfy=true timeout=10' % (rtmp, playpath, pageUrl, swfUrl)
            if playpath.startswith('http://'): url = playpath
            return url
        except:
            pass

        try:
            result = getUrl('http://9proxy.in/b.php?u=' + dataUrl, referer='http://9proxy.in').result
            rtmp = common.parseDOM(result, "FMS")[0]
            playpath = common.parseDOM(result, "appStream")[0]
            if playpath.endswith('/GR.flv'): raise Exception()
            url = '%s playpath=%s pageUrl=%s swfUrl=%s swfVfy=true timeout=10' % (rtmp, playpath, pageUrl, swfUrl)
            if playpath.startswith('http://'): url = playpath
            return url
        except:
            pass

        try:
            proxy = None
            proxy = '%s:%s' % (getSetting("proxy_ip"), getSetting("proxy_port"))
            if (getSetting("proxy_ip") == '' or getSetting("proxy_port") == ''): raise Exception()

            result = getUrl(dataUrl, proxy=proxy, timeout='30').result
            rtmp = common.parseDOM(result, "FMS")[0]
            playpath = common.parseDOM(result, "appStream")[0]
            if playpath.endswith('/GR.flv'): raise Exception()
            url = '%s playpath=%s pageUrl=%s swfUrl=%s swfVfy=true timeout=10' % (rtmp, playpath, pageUrl, swfUrl)
            if playpath.startswith('http://'): url = playpath
            return url
        except:
            yes = index().yesnoDialog(language(30341).encode("utf-8"), language(30342).encode("utf-8"))
            if yes: contextMenu().settings_open()

class alpha:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.alphatv.gr'
        self.shows_link = 'http://www.alphatv.gr/shows'
        self.shows_link2 = 'http://www.alphatv.gr/views/ajax?view_name=alpha_shows_category_view&view_display_id=page_3&view_path=shows&view_base_path=shows&page=%s'
        self.news_link = 'http://www.alphatv.gr/shows/informative/news'

    def shows(self):
        #self.list = self.shows_list()
        self.list = cache(self.shows_list)
        index().showList(self.list)

    def news(self):
        name = 'ALPHA NEWS'
        self.list = self.episodes_list(name, self.news_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def shows_list(self):
        try:
            result = getUrl(self.shows_link).result
            filter = common.parseDOM(result, "span", attrs = { "class": "field-content" })
            filter = common.parseDOM(filter, "a", ret="href")
            filter = uniqueList(filter).list

            threads = []
            result = ''
            for i in range(0, 5):
                self.data.append('')
                showsUrl = self.shows_link2 % str(i)
                threads.append(Thread(self.thread, showsUrl, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += json.loads(i)[1]['data']

            shows = common.parseDOM(result, "li")
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "span")[0]
                name = common.parseDOM(name, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "a", ret="href")[0]
                if not any(url == i for i in filter): raise Exception()
                url = '%s%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': ''})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            redirects = ['/webtv/shows?page=0', '/webtv/shows?page=1', '/webtv/shows?page=2', '/webtv/shows?page=3', '/webtv/episodes?page=0', '/webtv/episodes?page=1', '/webtv/episodes?page=2', '/webtv/episodes?page=3', '/webtv/news?page=0', '/webtv/news?page=1']
            base = url

            count = 0
            threads = []
            result = ''
            for redirect in redirects:
                self.data.append('')
                threads.append(Thread(self.thread, url + redirect, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "div", attrs = { "class": "views-field.+?" })
        except:
        	return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "img", ret="alt")[-1]
                if name == '': raise Exception()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[-1]
                url = '%s%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                if not url.startswith(base): raise Exception()
                if url in [i['url'] for i in self.list]: raise Exception()

                image = common.parseDOM(episode, "img", ret="src")[-1]
                if not image.startswith('http://'): image = '%s%s' % (self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result
            result = result.replace('\n','')

            try:
                url = re.compile("playlist:.+?file: '(.+?[.]m3u8)'").findall(result)[0]
                if "EXTM3U" in getUrl(url).result: return url
            except:
                pass

            url = re.compile('playlist:.+?"(rtmp[:].+?)"').findall(result)[0]
            url += ' timeout=10'
            return url
        except:
            return

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class star:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.star.gr'
        self.shows_link = 'http://www.star.gr/_layouts/handlers/tv/feeds.program.ashx?catTitle=hosts'
        self.episodes_link = 'http://www.star.gr/_layouts/handlers/tv/feeds.program.ashx?catTitle=%s&artId=%s'
        self.news_link = 'http://www.star.gr/_layouts/handlers/tv/feeds.program.ashx?catTitle=News&artId=9'
        self.watch_link = 'http://cdnapi.kaltura.com/p/21154092/sp/2115409200/playManifest/entryId/%s/flavorId/%s/format/url/protocol/http/a.mp4'
        self.enikos_link = 'http://gdata.youtube.com/feeds/api/users/enikoslive/uploads'

    def shows(self):
        #self.list = self.shows_list()
        self.list = cache(self.shows_list)
        index().showList(self.list)

    def news(self):
        name = 'STAR NEWS'
        image = 'http://www.star.gr/tv/PublishingImages/160913114342_2118.jpg'
        self.list = self.episodes_list(name, self.news_link, image, 'Greek', '', name)
        index().episodeList(self.list)

    def shows_list(self):
        try:
            result = getUrl(self.shows_link, mobile=True).result
            result = json.loads(result)
            shows = result['hosts']
        except:
            return

        for show in shows:
            try:
                name = show['Title'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                image = show['Image'].strip()
                image = '%s%s' % (self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                id = show['ProgramId']
                cat = show['ProgramCat'].strip()
                url = self.episodes_link % (cat, id)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                if url.endswith('artId=42'): url = self.enikos_link

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': ''})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url, mobile=True).result
            result = json.loads(result)

            try: plot = result['programme']['StoryLinePlain'].strip()
            except: plot = ''
            plot = common.replaceHTMLCodes(plot)
            plot = plot.encode('utf-8')

            episodes = result['videosprogram']
        except:
        	return

        for episode in episodes:
            try:
                name = episode['Title'].strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = episode['VideoID'].strip()
                url = self.watch_link % (url, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

class skai:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.skai.gr'
        self.shows_link = 'http://www.skai.gr/Ajax.aspx?m=Skai.TV.ProgramListView&la=0&Type=TV&Day=%s'
        self.episodes_link = 'http://www.skai.gr/Ajax.aspx?m=Skai.Player.ItemView&type=TV&cid=6&alid=%s'
        self.news_link = 'http://www.skai.gr/player/TV/?mmid=243980'

    def shows(self):
        #self.list = self.shows_list()
        self.list = cache(self.shows_list)
        index().showList(self.list)

    def news(self):
        name = 'SKAI NEWS'
        self.list = self.episodes_list(name, self.news_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def docs(self):
        self.list.append({'name': '1821', 'url': '212286', 'image': '103D3757BC656810AC691936864E49DC'})
        self.list.append({'name': '1821 .. Σήμερα', 'url': '212553', 'image': 'E3D27CCD6D665DDFCC3E1640D5BDA3A4'})
        self.list.append({'name': 'Βατοπαίδι...Όλη η Ιστορία', 'url': '222624', 'image': 'B2CC9280E741C03798070106B70D135C'})
        self.list.append({'name': 'Έλληνες του Πνεύματος και της Τέχνης', 'url': '237922', 'image': 'EBF431B4C010691F2C413AA88EFAB970'})
        self.list.append({'name': 'Ιαπωνία: 9 ριχτερ', 'url': '225869', 'image': '536726829DB3BCD79F48A8EFBB53D66E'})
        self.list.append({'name': 'Μάχες των Ελλήνων', 'url': '215411', 'image': 'DE9D8BABEB908FAD0F343AF3713EB8F4'})
        self.list.append({'name': 'Μάχες των Ελλήνων - Θεματική', 'url': '215434', 'image': 'DE9D8BABEB908FAD0F343AF3713EB8F4'})
        self.list.append({'name': 'Μεγάλοι Έλληνες', 'url': '240386', 'image': '726CDE5CBA10F5E8F7FA08D826D1DBDD'})
        self.list.append({'name': 'Μίκης Θεοδωράκης', 'url': '102819', 'image': '779D513A0FDDA7F61C2A9F3413F655EC'})
        self.list.append({'name': 'Ναυτίλος', 'url': '217362', 'image': 'B490C451013D93C9BAF99F2B343B2798'})
        self.list.append({'name': 'Ξεχασμένα Βαλκάνια', 'url': '226754', 'image': '50C20F6750CC31944937C60933D4B85A'})
        self.list.append({'name': 'Οι Δρόμοι της Ελιάς', 'url': '102527', 'image': '94B08523EB84D83CBD374A7F955091C9'})
        self.list.append({'name': 'Τα Παιδία Δεν Παίζει', 'url': '215848', 'image': 'E1C308853845C7ECD4B6F5B999D812DF'})

        for i in range(len(self.list)):
            self.list[i]['name'] = self.list[i]['name'].decode('iso-8859-7').encode('utf-8')
            self.list[i]['url'] = 'http://www.skai.gr/player/TV/?mmid=%s' % self.list[i]['url']
            self.list[i]['image'] = 'http://www.skai.gr/files/temp/%s.jpg' % self.list[i]['image']
            self.list[i]['genre'] = 'Greek'
            self.list[i]['plot'] = ''

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

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class cybc:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.cybc-media.com'
        self.shows_link = 'http://www.cybc-media.com/video/index.php?option=com_videoflow&task=categories&Itemid=102'
        self.news_link = 'http://www.cybc-media.com/video/index.php/video-on-demand?task=cats&cat=16'
        self.sports_link = 'http://www.cybc-media.com/video/index.php/video-on-demand?task=cats&cat=17'

    def shows(self):
        #self.list = self.shows_list()
        self.list = cache(self.shows_list)
        index().showList(self.list)

    def news(self):
        name = 'RIK NEWS'
        self.list = self.episodes_list(name, self.news_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def sports(self):
        name = 'RIK SPORTS'
        self.list = self.episodes_list(name, self.sports_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def shows_list(self):
        try:
            result = getUrl(self.shows_link).result
            result = result.replace(' = ', '=')
            shows = common.parseDOM(result, "td", attrs = { "class": "vfbox" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try: plot = common.parseDOM(show, "div", attrs = { "class": "vfmedia_details" })[0]
                except: plot = ''
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': plot})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            result = result.replace(' = ', '=')
            episodes = common.parseDOM(result, "td", attrs = { "class": "vfbox" })
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[0]
                url = '%s%s' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result
            result = result.replace('\n','')
            url = re.compile("'vfmediaspace'.+?'file'.+?'(.+?)'").findall(result)[0]
            return url
        except:
            return

class sigma:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.sigmatv.com'
        self.shows_link = 'http://www.sigmatv.com/shows'
        self.news_link = 'http://www.sigmatv.com/shows/tomes-sta-gegonota/episodes'

    def shows(self):
        #self.list = self.shows_list()
        self.list = cache(self.shows_list)
        index().showList(self.list)

    def news(self):
        name = 'SIGMA NEWS'
        self.list = self.episodes_list(name, self.news_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def shows_list(self):
        try:
            result = getUrl(self.shows_link).result
            shows = common.parseDOM(result, "div", attrs = { "class": "show_entry.+?" })
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "div", attrs = { "class": "body" })[0]
                name = common.parseDOM(name, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "a", ret="href")[0]
                filter = ['/uefa-champions-league', '/seirestainies', '/tilenouveles', '/alpha']
                if any(url.endswith(i) for i in filter): raise Exception()
                url = '%s/%s/episodes' % (self.base_link, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(show, "img", ret="src")[0]
                image = image.replace('/./', '')
                image = '%s/%s' % (self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try: plot = common.parseDOM(show, "div", attrs = { "style": "min.+?" })[-1]
                except: plot = ''
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': plot})
            except:
                pass

        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            count = 0
            threads = []
            result = ''
            for i in range(0, 100, 20):
                self.data.append('')
                episodesUrl = url + '/page/%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, count))
                count = count + 1
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += i

            episodes = common.parseDOM(result, "div", attrs = { "class": "entry .+?" })
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "img", ret="alt")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                if '/no-image' in image: raise Exception()
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result

            try: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/mp4" })[0]
            except: url = common.parseDOM(result, "source", ret="src", attrs = { "type": "video/flash" })[0]
            url = common.replaceHTMLCodes(url)

            url = getUrl(url, output='geturl').result
            return url
        except:
            return

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class cinegreece:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.cinegreece.com'
        self.mega_link = 'http://www.cinegreece.com/2012/05/mega.html'
        self.ant1_link = 'http://www.cinegreece.com/2012/05/ant1.html'
        self.alpha_link = 'http://www.cinegreece.com/2012/05/alpha.html'
        self.star_link = 'http://www.cinegreece.com/2012/05/star.html'
        self.ert_link = 'http://www.cinegreece.com/2012/05/ert.html'
        self.rik_link = 'http://www.cinegreece.com/2012/05/rik.html'

    def mega(self):
        #self.list = self.shows_list(self.mega_link)
        self.list = cache(self.shows_list, self.mega_link)
        index().showList(self.list)

    def ant1(self):
        #self.list = self.shows_list(self.ant1_link)
        self.list = cache(self.shows_list, self.ant1_link)
        index().showList(self.list)

    def alpha(self):
        #self.list = self.shows_list(self.alpha_link)
        self.list = cache(self.shows_list, self.alpha_link)
        index().showList(self.list)

    def star(self):
        #self.list = self.shows_list(self.star_link)
        self.list = cache(self.shows_list, self.star_link)
        index().showList(self.list)

    def ert(self):
        #self.list = self.shows_list(self.ert_link)
        self.list = cache(self.shows_list, self.ert_link)
        index().showList(self.list)

    def rik(self):
        #self.list = self.shows_list(self.rik_link)
        self.list = cache(self.shows_list, self.rik_link)
        index().showList(self.list)

    def shows_list(self, url):
        try:
            showsUrl = [url]
            for i in range(2, 5): showsUrl.append(url.replace('.html', 'p%s.html' % str(i)))

            threads = []
            result = ''
            for i in range(0, 4):
                self.data.append('')
                threads.append(Thread(self.thread, showsUrl[i], i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for data in self.data:
                try: result += common.parseDOM(data, "div", attrs = { "itemprop": "articleBody" })[0]
                except: pass

            shows = re.compile('(<a.+?</a>)').findall(result)
        except:
            return

        for show in shows:
            try:
                name = common.parseDOM(show, "img", ret="title")[0]
                if name.endswith('(Ο)'.decode('iso-8859-7')): name = 'Ο '.decode('iso-8859-7') + name.replace('(Ο)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Η)'.decode('iso-8859-7')): name = 'Η '.decode('iso-8859-7') + name.replace('(Η)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Το)'.decode('iso-8859-7')): name = 'Το '.decode('iso-8859-7') + name.replace('(Το)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Οι)'.decode('iso-8859-7')): name = 'Οι '.decode('iso-8859-7') + name.replace('(Οι)'.decode('iso-8859-7'), '').strip()
                elif name.endswith('(Τα)'.decode('iso-8859-7')): name = 'Τα '.decode('iso-8859-7') + name.replace('(Τα)'.decode('iso-8859-7'), '').strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(show, "a", ret="href")[0]
                url = common.replaceHTMLCodes(url)
                url = url.replace(url.split("/")[2], self.base_link.split("//")[-1])
                url = url.encode('utf-8')

                image = common.parseDOM(show, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'genre': 'Greek', 'plot': ''})
            except:
                pass

        self.list = sorted(self.list, key=itemgetter('name'))
        return self.list

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result

            image = common.parseDOM(result, "a", attrs = { "imageanchor": ".+?" })[0]
            image = common.parseDOM(image, "img", ret="src")[0]
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')

            episodes = re.compile('(<button.+?</button>)').findall(result)
            episodes = uniqueList(episodes).list
        except:
            return

        for episode in episodes:
            try:
                name = common.parseDOM(episode, "button")[0]
                try: name = common.parseDOM(name, "span")[0]
                except: pass
                if '#' in name: raise Exception()
                name = name.replace('&nbsp;&nbsp;&nbsp;','-').strip()
                name = 'Επεισόδιο '.decode('iso-8859-7') + name
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "button", ret="onclick")[0]
                url = re.compile("'(.+?)'").findall(url)[0]
                if url.startswith('popvid'):
                    url = common.parseDOM(result, "div", attrs = { "id": url })[0]
                    url = common.parseDOM(url, "embed", ret="src")[0]
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
        except:
            return

class novasports:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.novasports.gr'
        self.episodes_link = 'http://www.novasports.gr/LiveWebTV.aspx%s'
        self.series_link = 'http://www.novasports.gr/handlers/LiveWebTv/LiveWebTvMediaGallery.ashx?containerid=-1&mediafiletypeid=0&latest=true&isBroadcast=true&tabid=shows'
        self.news_link = 'http://www.novasports.gr/handlers/LiveWebTv/LiveWebTvMediaGallery.ashx?containerid=-1&mediafiletypeid=2&latest=true&tabid=categories'

    def shows(self):
        name = 'Novasports'
        self.list = self.episodes_list(name, self.series_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def news(self):
        name = 'Novasports News'
        self.list = self.episodes_list(name, self.news_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result
            result = json.loads(result)['HTML']
            episodes = common.parseDOM(result, "li")
        except:
            return

        for episode in episodes:
            try:
                title = common.parseDOM(episode, "a", ret="title")[0]
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                try:
                    name = common.parseDOM(episode, "a", ret="title")[0]
                    date = common.parseDOM(episode, "span", attrs = { "class": "date" })[0]
                    name = '%s (%s)' % (name, date.rsplit(',', 1)[0])
                except:
                    pass
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(episode, "a", ret="href")[0]
                url = self.episodes_link % url
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(episode, "img", ret="src")[0]
                image = '%s/%s' % (self.base_link, image)
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': title, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            result = getUrl(url).result
            url = re.compile("type: 'html5'.+?'file': '(.+?)'").findall(result)[0]
            return url
        except:
            return

class mtvchart:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.mtvgreece.gr'
        self.mtvhitlisthellas_link = 'http://www.mtvgreece.gr/hitlisthellas'
        self.mtvdancefloor_link = 'http://www.mtvgreece.gr/mtv-dance-flour-chart'
        self.eurotop20_link = 'http://www.mtvgreece.gr/mtv-euro-top-20'
        self.usatop20_link = 'http://www.mtvgreece.gr/mtv-usa-top-20'
        self.youtube_search = 'http://gdata.youtube.com/feeds/api/videos?q='

    def mtvhitlisthellas(self):
        name = 'MTV Hit List Hellas'
        self.list = self.episodes_list(name, self.mtvhitlisthellas_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def mtvdancefloor(self):
        name = 'MTV Dance Floor'
        self.list = self.episodes_list(name, self.mtvdancefloor_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def eurotop20(self):
        name = 'Euro Top 20'
        self.list = self.episodes_list(name, self.eurotop20_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def usatop20(self):
        name = 'U.S. Top 20'
        self.list = self.episodes_list(name, self.usatop20_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result

            image = '%s/%s_wide.png' % (addonArt, name)
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')

            episodes = common.parseDOM(result, "span", attrs = { "class": "artistRow" })
        except:
            return

        for episode in episodes:
            try:
                name = ' '.join(re.sub('<.+?>', '', episode).split()).strip()
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                show = common.parseDOM(result, "strong")[0]
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')

                query = ' '.join(re.sub('=|&|:|;|-|"|,|\'|\.|\?|\/', ' ', name).split())
                url = self.youtube_search + query + ' official'
                url = common.replaceHTMLCodes(url)

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

class rythmoschart:
    def __init__(self):
        self.list = []
        self.base_link = 'http://www.rythmosfm.gr'
        self.top20_link = 'http://www.rythmosfm.gr/community/top20/'
        self.youtube_search = 'http://gdata.youtube.com/feeds/api/videos?q='

    def rythmoshitlist(self):
        name = 'Rythmos Hit List'
        self.list = self.episodes_list(name, self.top20_link, '', 'Greek', '', name)
        index().episodeList(self.list)

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            result = getUrl(url).result

            image = '%s/%s_wide.png' % (addonArt, name)
            image = common.replaceHTMLCodes(image)
            image = image.encode('utf-8')

            episodes = common.parseDOM(result, "span", attrs = { "class": "toptitle" })
        except:
            return

        for episode in episodes:
            try:
                name = episode
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                show = episode.rsplit('-', 1)[-1].strip()
                show = common.replaceHTMLCodes(show)
                show = show.encode('utf-8')

                query = ' '.join(re.sub('=|&|:|;|-|"|,|\'|\.|\?|\/', ' ', name).split())
                url = self.youtube_search + query + ' official'
                url = common.replaceHTMLCodes(url)

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

class dailymotion:
    def __init__(self):
        self.list = []
        self.data = []
        self.base_link = 'http://www.dailymotion.com'
        self.api_link = 'https://api.dailymotion.com'
        self.playlist_link = 'https://api.dailymotion.com/user/%s/videos?fields=description,duration,id,owner.username,taken_time,thumbnail_large_url,title,views_total&sort=recent&family_filter=1'
        self.watch_link = 'http://www.dailymotion.com/video/%s'
        self.info_link = 'http://www.dailymotion.com/embed/video/%s'

    def superleague(self):
        name = 'Super League'
        channel = 'greeksuperleague'
        url = self.playlist_link % channel
        self.list = self.episodes_list(name, url, '', 'Greek', '', name)
        index().episodeList(self.list)

    def superball(self):
        name = 'Super Ball'
        channel = 'Super-Ball'
        url = self.playlist_link % channel
        self.list = self.episodes_list(name, url, '', 'Greek', '', name)
        index().episodeList(self.list)

    def episodes_list(self, name, url, image, genre, plot, show):
        try:
            threads = []
            result = []
            for i in range(1, 3):
                self.data.append('')
                episodesUrl = url + '&limit=100&page=%s' % str(i)
                threads.append(Thread(self.thread, episodesUrl, i-1))
            [i.start() for i in threads]
            [i.join() for i in threads]
            for i in self.data: result += json.loads(i)['list']

            episodes = result
        except:
        	return

        for episode in episodes:
            try:
                name = episode['title']
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = episode['id']
                url = self.watch_link % url
                url = url.encode('utf-8')

                image = episode['thumbnail_large_url']
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': genre, 'plot': plot, 'title': name, 'show': show})
            except:
                pass

        return self.list

    def resolve(self, url):
        try:
            id = url.split("/")[-1].split("?")[0]
            result = getUrl(self.info_link % id).result

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
            url = getUrl(url, output='geturl').result
            return url
        except:
            return

    def thread(self, url, i):
        try:
            result = getUrl(url).result
            self.data[i] = result
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
        self.enikos_link = 'http://gdata.youtube.com/feeds/api/users/enikosgr/uploads'

    def madtv(self):
        channel = 'MADTVGREECE'
        exclude = ["PL1RY_6CEqdtnxJYgudDydiG4fKVoQouHf", "PL1RY_6CEqdtlu30q6SyuNe6Tk5IYjAiks", "PLE4B3F6B7F753D97C", "PL85C952EA930B9E90", "PL04B2C2D8B304BA48", "PL46B9D152167BA727"]
        #self.list = self.shows_list(channel, [], exclude)
        self.list = cache(self.shows_list, channel, [], exclude)
        index().showList(self.list)

    def madgreekz(self):
        channel = 'madtvgreekz'
        exclude = ["PL20iPi-qHKiz1wJCqvbvy5ffrtWT1VcVF", "PL20iPi-qHKiyWnRbBdnSF7RlDdAePiKzj", "PL20iPi-qHKiyZGlOs5DTElzAK_YNCDJn0", "PL20iPi-qHKiwyRhqqmOnbDvPSUgRzzxgq"]
        #self.list = self.shows_list(channel, [], exclude)
        self.list = cache(self.shows_list, channel, [], exclude)
        self.list = sorted(self.list, key=itemgetter('name'))
        index().showList(self.list)

    def enikos(self):
        name = 'ENIKOS'
        self.list = self.episodes_list(name, self.enikos_link, '', 'Greek', '', name)
        index().episodeList(self.list[:100])

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