# -*- coding: utf-8 -*-

'''
    Extreme Sports XBMC Addon
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
        elif action == 'videos_all':                videos().root('all')
        elif action == 'videos_users':              videos().root('users')
        elif action == 'videos_mountainbike':       videos().root('mountainbike')
        elif action == 'videos_bmx':                videos().root('bmx')
        elif action == 'videos_skate':              videos().root('skate')
        elif action == 'videos_snowboard':          videos().root('snowboard')
        elif action == 'videos_freeski':            videos().root('freeski')
        elif action == 'videos_fmx':                videos().root('fmx')
        elif action == 'videos_mx':                 videos().root('mx')
        elif action == 'videos_surf':               videos().root('surf')
        elif action == 'videos_autosports':         videos().root('autosports')
        elif action == 'videos_kayak':              videos().root('kayak')
        elif action == 'videos_kite':               videos().root('kite')
        elif action == 'videos_outdoor':            videos().root('outdoor')
        elif action == 'videos_wake':               videos().root('wake')
        elif action == 'videos_windsurf':           videos().root('windsurf')
        elif action == 'play':                      resolver().run(url)

        if action is None:
            pass
        elif action.startswith('videos'):
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
        rootList.append({'name': 30501, 'image': 'All videos.png', 'action': 'videos_all'})
        if getSetting("user_videos") == 'true':
            rootList.append({'name': 30502, 'image': 'User videos.png', 'action': 'videos_users'})
        rootList.append({'name': 30503, 'image': 'MTB.png', 'action': 'videos_mountainbike'})
        rootList.append({'name': 30504, 'image': 'BMX.png', 'action': 'videos_bmx'})
        rootList.append({'name': 30505, 'image': 'Skate.png', 'action': 'videos_skate'})
        rootList.append({'name': 30506, 'image': 'Snowboard.png', 'action': 'videos_snowboard'})
        rootList.append({'name': 30507, 'image': 'Freeski.png', 'action': 'videos_freeski'})
        rootList.append({'name': 30508, 'image': 'FMX.png', 'action': 'videos_fmx'})
        rootList.append({'name': 30509, 'image': 'MX.png', 'action': 'videos_mx'})
        rootList.append({'name': 30510, 'image': 'Surf.png', 'action': 'videos_surf'})
        rootList.append({'name': 30511, 'image': 'Auto Sports.png', 'action': 'videos_autosports'})
        rootList.append({'name': 30512, 'image': 'Kayak.png', 'action': 'videos_kayak'})
        rootList.append({'name': 30513, 'image': 'Kitesurf.png', 'action': 'videos_kite'})
        rootList.append({'name': 30514, 'image': 'Outdoor.png', 'action': 'videos_outdoor'})
        rootList.append({'name': 30515, 'image': 'Wake.png', 'action': 'videos_wake'})
        rootList.append({'name': 30516, 'image': 'Windsurf.png', 'action': 'videos_windsurf'})
        index().rootList(rootList)

class link:
    def __init__(self):
        self.extreme_base = 'http://extreme.com'
        self.extreme_all = 'http://extreme.com/videos'
        self.extreme_users = 'http://extreme.com/user-videos'
        self.extreme_mountainbike = 'http://extreme.com/mountainbike'
        self.extreme_bmx = 'http://extreme.com/bmx'
        self.extreme_skate = 'http://extreme.com/skate'
        self.extreme_snowboard = 'http://extreme.com/snowboard'
        self.extreme_freeski = 'http://extreme.com/freeski'
        self.extreme_fmx = 'http://extreme.com/fmx'
        self.extreme_mx = 'http://extreme.com/mx'
        self.extreme_surf = 'http://extreme.com/surf'
        self.extreme_autosports = 'http://extreme.com/autosports'
        self.extreme_kayak = 'http://extreme.com/kayak'
        self.extreme_kite = 'http://extreme.com/kite'
        self.extreme_outdoor = 'http://extreme.com/outdoor'
        self.extreme_wake = 'http://extreme.com/wake'
        self.extreme_windsurf = 'http://extreme.com/windsurf'

class videos:
    def __init__(self):
        self.list = []

    def root(self, url):
        if url == 'all': url = link().extreme_all
        elif url == 'users': url = link().extreme_users
        elif url == 'mountainbike': url = link().extreme_mountainbike
        elif url == 'bmx': url = link().extreme_bmx
        elif url == 'skate': url = link().extreme_skate
        elif url == 'snowboard': url = link().extreme_snowboard
        elif url == 'freeski': url = link().extreme_freeski
        elif url == 'fmx': url = link().extreme_fmx
        elif url == 'mx': url = link().extreme_mx
        elif url == 'surf': url = link().extreme_surf
        elif url == 'autosports': url = link().extreme_autosports
        elif url == 'kayak': url = link().extreme_kayak
        elif url == 'kite': url = link().extreme_kite
        elif url == 'outdoor': url = link().extreme_outdoor
        elif url == 'wake': url = link().extreme_wake
        elif url == 'windsurf': url = link().extreme_windsurf

        self.list = self.extreme_list(url)
        #self.list = cache(self.extreme_list, url)
        index().videoList(self.list)
        index().nextList(self.list)

    def get(self, url):
        self.list = self.extreme_list(url)
        #self.list = cache(self.extreme_list, url)
        index().videoList(self.list)
        index().nextList(self.list)

    def extreme_list(self, url):
        try:
            result = getUrl(url).result
            result = result.replace('–', '-')

            videos = common.parseDOM(result, "div", attrs = { "class": "videos_list" })[0]
            videos = common.parseDOM(videos, "div", attrs = { "class": "video_cell" })
        except:
            return

        try:
            next = common.parseDOM(result, "a", ret="href", attrs = { "class": "next_btn" })[0]
            next = '%s%s' % (link().extreme_base, next)
            next = common.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for video in videos:
            try:
                name = common.parseDOM(video, "p", attrs = { "class": "link" })[0]
                name = common.parseDOM(name, "a")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = common.parseDOM(video, "p", attrs = { "class": "link" })[0]
                url = common.parseDOM(url, "a", ret="href")[0]
                url = '%s%s' % (link().extreme_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = common.parseDOM(video, "img", ret="src")[0]
                image = image.split("?")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                try: plot = common.parseDOM(video, "p", attrs = { "class": "description" })[0]
                except: plot = ''
                plot = plot.replace('\n', ' ')
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image, 'date': '', 'genre': 'Extreme Sports', 'plot': plot, 'title': name, 'show': '', 'next': next})
            except:
                pass

        return self.list

class resolver:
    def run(self, url):
        try:
            url = self.extreme(url)
            if url is None: raise Exception()
            player().run(url)
            return url
        except:
            index().infoDialog(language(30303).encode("utf-8"))
            return

    def extreme(self, url):
        try:
            r = getUrl(url).result
        except:
            return

        try:
            freecaster = re.compile('"levels":(\[{"file":.+?\])').findall(r)[0]

            result = json.loads(freecaster)
            url = None
            try: url = [i['file'] for i in result if i['width'] == '320'][0]
            except: pass
            try: url = [i['file'] for i in result if i['width'] == '640'][0]
            except: pass
            try: url = [i['file'] for i in result if i['width'] == '1280'][0]
            except: pass

            if url == None: raise Exception()
            return url
        except:
            pass

        try:
            result = r.replace('\/', '/').replace('youtube.com/watch', 'youtube.com/embed/')

            youtube = re.compile('youtube.com/embed/(.+?)"').findall(result)[0]
            youtube = youtube.split("?v=")[-1].split("/")[-1].split("?")[0]

            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtube
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return

            return url
        except:
            pass

        try:
            vimeo = re.compile('.*src="(http://.+?vimeo.com/.+?)"').findall(r)[0]
            vimeo = common.replaceHTMLCodes(vimeo)
            vimeo = vimeo.encode('utf-8')

            result = getUrl(vimeo).result
            url = re.compile('"url":"(.+?)"').findall(result)
            url = [i for i in url if 'token=' in i or 'token2=' in i][-1]

            return url
        except:
            pass


main()