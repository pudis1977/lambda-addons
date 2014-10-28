# -*- coding: utf-8 -*-

'''
    Simply Player XBMC Addon
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

import urllib,urllib2,re,os,threading,datetime,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
from operator import itemgetter
try:    import CommonFunctions
except: import commonfunctionsdummy as CommonFunctions
from metahandler import metahandlers
from metahandler import metacontainers


language            = xbmcaddon.Addon().getLocalizedString
setSetting          = xbmcaddon.Addon().setSetting
getSetting          = xbmcaddon.Addon().getSetting
addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")
addonDesc           = language(30450).encode("utf-8")
addonIcon           = os.path.join(addonPath,'icon.png')
addonFanart         = os.path.join(addonPath,'fanart.jpg')
addonArt            = os.path.join(addonPath,'resources/art')
addonDownloads      = os.path.join(addonPath,'resources/art/Downloads.png')
addonPages          = os.path.join(addonPath,'resources/art/Pages.png')
addonGenres         = os.path.join(addonPath,'resources/art/Genres.png')
addonNext           = os.path.join(addonPath,'resources/art/Next.png')
dataPath            = xbmc.translatePath('special://profile/addon_data/%s' % (addonId))
viewData            = os.path.join(dataPath,'views.cfg')
favData             = os.path.join(dataPath,'favourites.cfg')
favData2            = os.path.join(dataPath,'favourites2.cfg')
subData             = os.path.join(dataPath,'subscriptions.cfg')
metaget             = metahandlers.MetaData(preparezip=False)
common              = CommonFunctions
action              = None


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
        try:        imdb = urllib.unquote_plus(params["imdb"])
        except:     imdb = None
        try:        genre = urllib.unquote_plus(params["genre"])
        except:     genre = None
        try:        plot = urllib.unquote_plus(params["plot"])
        except:     plot = None
        try:        show = urllib.unquote_plus(params["show"])
        except:     show = None
        try:        season = urllib.unquote_plus(params["season"])
        except:     season = None
        try:        episode = urllib.unquote_plus(params["episode"])
        except:     episode = None

        if action == None:                          root().get()
        elif action == 'root_movies':               root().movies()
        elif action == 'root_shows':                root().shows()
        elif action == 'root_favourites':           root().favourites()
        elif action == 'root_search':               root().search()
        elif action == 'item_play':                 contextMenu().item_play()
        elif action == 'item_random_play':          contextMenu().item_random_play()
        elif action == 'item_queue':                contextMenu().item_queue()
        elif action == 'item_play_from_here':       contextMenu().item_play_from_here(url)
        elif action == 'favourite_add':             contextMenu().favourite_add(favData, name, url, image, imdb)
        elif action == 'favourite_from_search':     contextMenu().favourite_from_search(favData, name, url, image, imdb)
        elif action == 'favourite_delete':          contextMenu().favourite_delete(favData, name, url)
        elif action == 'favourite_moveUp':          contextMenu().favourite_moveUp(favData, name, url)
        elif action == 'favourite_moveDown':        contextMenu().favourite_moveDown(favData, name, url)
        elif action == 'favourite_add2':            contextMenu().favourite_add(favData2, name, url, image, imdb)
        elif action == 'favourite_from_search2':    contextMenu().favourite_from_search(favData2, name, url, image, imdb)
        elif action == 'favourite_delete2':         contextMenu().favourite_delete(favData2, name, url)
        elif action == 'favourite_moveUp2':         contextMenu().favourite_moveUp(favData2, name, url)
        elif action == 'favourite_moveDown2':       contextMenu().favourite_moveDown(favData2, name, url)
        elif action == 'subscription_add':          contextMenu().subscription_add(name, url, image, imdb)
        elif action == 'subscription_delete':       contextMenu().subscription_delete(name, url)
        elif action == 'subscriptions_update':      contextMenu().subscriptions_update()
        elif action == 'subscriptions_service':     contextMenu().subscriptions_update(silent=True)
        elif action == 'subscriptions_clean':       contextMenu().subscriptions_clean()
        elif action == 'playlist_open':             contextMenu().playlist_open()
        elif action == 'settings_open':             contextMenu().settings_open()
        elif action == 'addon_home':                contextMenu().addon_home()
        elif action == 'view_movies':               contextMenu().view('movies')
        elif action == 'view_tvshows':              contextMenu().view('tvshows')
        elif action == 'view_seasons':              contextMenu().view('seasons')
        elif action == 'view_episodes':             contextMenu().view('episodes')
        elif action == 'metadata_movies':           contextMenu().metadata('movie', name, url, imdb, '', '')
        elif action == 'metadata_tvshows':          contextMenu().metadata('tvshow', name, url, imdb, '', '')
        elif action == 'metadata_seasons':          contextMenu().metadata('season', '', '', imdb, season, '')
        elif action == 'metadata_episodes':         contextMenu().metadata('episode', '', '', imdb, season, episode)
        elif action == 'playcount_movies':          contextMenu().playcount('movie', imdb, '', '')
        elif action == 'playcount_tvshows':         contextMenu().playcount('tvshow', imdb, '', '')
        elif action == 'playcount_seasons':         contextMenu().playcount('season', imdb, season, '')
        elif action == 'playcount_episodes':        contextMenu().playcount('episode', imdb, season, episode)
        elif action == 'library':                   contextMenu().library(name, url)
        elif action == 'library2':                  contextMenu().library2(name, url)
        elif action == 'download':                  contextMenu().download(name, url)
        elif action == 'trailer':                   contextMenu().trailer(name, url)
        elif action == 'movies_favourites':         favourites().movies()
        elif action == 'shows_favourites':          favourites().shows()
        elif action == 'shows_subscriptions':       subscriptions().shows()
        elif action == 'movies':                    movies().simplymovies(url)
        elif action == 'movies_title':              movies().simplymovies_title()
        elif action == 'movies_views':              movies().simplymovies_views()
        elif action == 'movies_rating':             movies().simplymovies_rating()
        elif action == 'movies_release':            movies().simplymovies_release()
        elif action == 'movies_search':             movies().simplymovies_search(query)
        elif action == 'shows':                     shows().simplymovies(url)
        elif action == 'shows_title':               shows().simplymovies_title()
        elif action == 'shows_views':               shows().simplymovies_views()
        elif action == 'shows_rating':              shows().simplymovies_rating()
        elif action == 'shows_search':              shows().simplymovies_search(query)
        elif action == 'seasons':                   seasons().simplymovies(url, image, imdb, genre, plot, show)
        elif action == 'episodes':                  episodes().simplymovies(name, url, image, imdb, genre, plot, show)
        elif action == 'pages_movies':              pages().simplymovies_movies()
        elif action == 'pages_shows':               pages().simplymovies_shows()
        elif action == 'genres_movies':             genres().simplymovies_movies()
        elif action == 'genres_shows':              genres().simplymovies_shows()
        elif action == 'play':                      resolver().run(url, name)

        if action is None:
            pass
        elif action.startswith('movies'):
            xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            index().container_view('movies', {'skin.confluence' : 500})
        elif action.startswith('shows'):
            xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
            index().container_view('tvshows', {'skin.confluence' : 500})
        elif action.startswith('seasons'):
            xbmcplugin.setContent(int(sys.argv[1]), 'seasons')
            index().container_view('seasons', {'skin.confluence' : 500})
        elif action.startswith('episodes'):
            xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
            index().container_view('episodes', {'skin.confluence' : 504})
        xbmcplugin.setPluginFanart(int(sys.argv[1]), addonFanart)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        return

class getUrl(object):
    def __init__(self, url, fetch=True, close=True, cookie=False, mobile=False, proxy=None, post=None, referer=None):
        if not proxy is None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if cookie == True:
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
        response = urllib2.urlopen(request, timeout=10)
        if fetch == True:
            result = response.read()
        else:
            result = response.geturl()
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
        self.property = addonName+'player_status'
        xbmc.Player.__init__(self)

    def status(self):
        getProperty = index().getProperty(self.property)
        index().clearProperty(self.property)
        if not xbmc.getInfoLabel('Container.FolderPath') == '': return
        if getProperty == 'true': return True
        return

    def run(self, name, url):
        if xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]):
            item = xbmcgui.ListItem(path=url)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        else:
            try: season = re.compile('S(\d{3})E\d*').findall(name)[-1]
            except: season = None
            try: season = re.compile('S(\d{2})E\d*').findall(name)[-1]
            except: season = None
            try: episode = re.compile('S%sE(\d*)' % (season)).findall(name)[-1]
            except: episode = None
            try: year = re.compile('[(](\d{4})[)]').findall(name)[-1]
            except: year = None
            try:
                if not (season is None and episode is None):
                	show = name.replace('S%sE%s' % (season, episode), '').strip()
                	season, episode = '%01d' % int(season), '%01d' % int(episode)
                	imdb = metaget.get_meta('tvshow', show)['imdb_id']
                	imdb = re.sub("[^0-9]", "", imdb)
                	meta = metaget.get_episode_meta('', imdb, season, episode)
                	meta.update({'tvshowtitle': show})
                	poster = meta['cover_url']
                elif not year is None:
                	title = name.replace('(%s)' % year, '').strip()
                	meta = metaget.get_meta('movie', title ,year=year ,overlay=6)
                	poster = meta['cover_url']
                else: raise Exception()
            except:
            	meta = {'label' : name, 'title' : name}
            	poster = ''
            item = xbmcgui.ListItem(path=url, iconImage="DefaultVideo.png", thumbnailImage=poster)
            item.setInfo( type="Video", infoLabels= meta )
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

        for i in range(1, 21):
            try: self.totalTime = self.getTotalTime()
            except: self.totalTime = 0
            if not self.totalTime == 0: continue
            xbmc.sleep(1000)
        if self.totalTime == 0: return

        subtitles().get(name)

        self.season = str(xbmc.getInfoLabel('VideoPlayer.season'))
        self.episode = str(xbmc.getInfoLabel('VideoPlayer.episode'))
        if self.season == '' or self.episode == '':
            self.content = 'movie'
            self.imdb = metaget.get_meta('movie', xbmc.getInfoLabel('VideoPlayer.title') ,year=str(xbmc.getInfoLabel('VideoPlayer.year')))['imdb_id']
            self.imdb = re.sub("[^0-9]", "", self.imdb)
        else:
            self.content = 'episode'
            self.imdb = metaget.get_meta('tvshow', xbmc.getInfoLabel('VideoPlayer.tvshowtitle'))['imdb_id']
            self.imdb = re.sub("[^0-9]", "", self.imdb)

        while True:
            try: self.currentTime = self.getTime()
            except: break
            xbmc.sleep(1000)

    def onPlayBackEnded(self):
        if xbmc.getInfoLabel('Container.FolderPath') == '': index().setProperty(self.property, 'true')
        if not self.currentTime / self.totalTime >= .9: return
        metaget.change_watched(self.content, '', self.imdb, season=self.season, episode=self.episode, year='', watched='')
        index().container_refresh()

    def onPlayBackStopped(self):
        index().clearProperty(self.property)

class subtitles:
    def get(self, name):
        subs = getSetting("subs")
        if subs == '1': self.greek(name)

    def greek(self, name):
        try:
            import shutil, zipfile, time
            sub_tmp = os.path.join(dataPath,'sub_tmp')
            sub_tmp2 = os.path.join(sub_tmp, "subs")
            sub_stream = os.path.join(dataPath,'sub_stream')
            sub_file = os.path.join(sub_tmp, 'sub_tmp.zip')
            try: os.makedirs(dataPath)
            except: pass
            try: os.remove(sub_tmp)
            except: pass
            try: shutil.rmtree(sub_tmp)
            except: pass
            try: os.makedirs(sub_tmp)
            except: pass
            try: os.remove(sub_stream)
            except: pass
            try: shutil.rmtree(sub_stream)
            except: pass
            try: os.makedirs(sub_stream)
            except: pass

            subtitles = []
            query = ''.join(e for e in name if e.isalnum() or e == ' ')
            query = urllib.quote_plus(query)
            url = 'http://www.greeksubtitles.info/search.php?name=' + query
            result = getUrl(url).result
            result = result.decode('iso-8859-7').encode('utf-8')
            result = result.lower().replace('"',"'")
            match = "get_greek_subtitles[.]php[?]id=(.+?)'.+?%s.+?<"
            quality = ['bluray', 'brrip', 'bdrip', 'dvdrip', 'hdtv']
            for q in quality:
                subtitles += re.compile(match % q).findall(result)
            if subtitles == []: raise Exception()
            for subtitle in subtitles:
                url = 'http://www.findsubtitles.eu/getp.php?id=' + subtitle
                response = urllib.urlopen(url)
                content = response.read()
                response.close()
                if content[:4] == 'PK': break

            file = open(sub_file, 'wb')
            file.write(content)
            file.close()
            file = zipfile.ZipFile(sub_file, 'r')
            file.extractall(sub_tmp)
            file.close()
            files = os.listdir(sub_tmp2)
            if files == []: raise Exception()
            file = [i for i in files if i.endswith('.srt') or i.endswith('.sub')]
            if file == []:
                pack = [i for i in files if i.endswith('.zip') or i.endswith('.rar')]
                pack = os.path.join(sub_tmp2, pack[0])
                xbmc.executebuiltin('Extract("%s","%s")' % (pack, sub_tmp2))
                time.sleep(1)
            files = os.listdir(sub_tmp2)
            file = [i for i in files if i.endswith('.srt') or i.endswith('.sub')][0]
            copy = os.path.join(sub_tmp2, file)
            shutil.copy(copy, sub_stream)
            try: shutil.rmtree(sub_tmp)
            except: pass
            file = os.path.join(sub_stream, file)
            if not os.path.isfile(file): raise Exception()

            xbmc.Player().setSubtitles(file)
        except:
            try: shutil.rmtree(sub_tmp)
            except: pass
            try: shutil.rmtree(sub_stream)
            except: pass
            index().infoDialog(language(30316).encode("utf-8"), name)
            return

class index:
    def infoDialog(self, str, header=addonName):
        xbmc.executebuiltin("Notification(%s,%s, 3000, %s)" % (header, str, addonIcon))

    def okDialog(self, str1, str2, header=addonName):
        xbmcgui.Dialog().ok(header, str1, str2)

    def selectDialog(self, list, header=addonName):
        select = xbmcgui.Dialog().select(header, list)
        return select

    def yesnoDialog(self, str1, str2, header=addonName):
        answer = xbmcgui.Dialog().yesno(header, str1, str2)
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
        if not xbmcvfs.exists(subData):
            file = xbmcvfs.File(subData, 'w')
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
        total = len(rootList)
        for i in rootList:
            try:
                name = language(i['name']).encode("utf-8")
                image = '%s/%s' % (addonArt, i['image'])
                action = i['action']
                u = '%s?action=%s' % (sys.argv[0], action)

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems([], replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def pageList(self, pageList):
        total = len(pageList)
        for i in pageList:
            try:
                name, url, image = i['name'], i['url'], i['image']
                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)

                if action.endswith('movies'):
                    u = '%s?action=movies&url=%s' % (sys.argv[0], sysurl)
                elif action.endswith('shows'):
                    u = '%s?action=shows&url=%s' % (sys.argv[0], sysurl)

                item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
                item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
                item.setProperty("Fanart_Image", addonFanart)
                item.addContextMenuItems([], replaceItems=False)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def nextList(self, next):
        if next == '': return
        name, url, image = language(30361).encode("utf-8"), next, addonNext
        sysurl = urllib.quote_plus(url)

        if action.startswith('movies'):
            u = '%s?action=movies&url=%s' % (sys.argv[0], sysurl)
        elif action.startswith('shows'):
            u = '%s?action=shows&url=%s' % (sys.argv[0], sysurl)

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def downloadList(self):
        u = getSetting("downloads")
        if u == '': return
        name, image = language(30363).encode("utf-8"), addonDownloads

        item = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=image)
        item.setInfo( type="Video", infoLabels={ "Label": name, "Title": name, "Plot": addonDesc } )
        item.setProperty("Fanart_Image", addonFanart)
        item.addContextMenuItems([], replaceItems=False)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

    def movieList(self, movieList):
        file = xbmcvfs.File(favData)
        favRead = file.read()
        file.close()

        total = len(movieList)
        for i in movieList:
            try:
                name, url, image, imdb, genre, plot = i['name'], i['url'], i['image'], i['imdb'], i['genre'], i['plot']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '      
                try: year = re.compile('[(](\d{4})[)]').findall(name)[-1]
                except: year = ' '
                title = name.replace('(%s)' % year, '').strip()

                sysname, sysurl, sysimage, sysimdb, systitle = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(imdb), urllib.quote_plus(title)
                u = '%s?action=play&name=%s&url=%s&t=%s' % (sys.argv[0], sysname, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

                if getSetting("meta") == 'true':
                    if action == 'movies_favourites':
                        meta = metaget.get_meta('movie', title ,imdb_id=imdb)
                    else:
                        meta = metaget.get_meta('movie', title ,year=year)
                    playcountMenu = language(30407).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb = urllib.quote_plus(re.sub("[^0-9]", "", meta['imdb_id']))
                    trailer, poster = urllib.quote_plus(meta['trailer_url']), meta['cover_url']
                    if trailer == '': trailer = sysurl
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'year': year, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                    trailer, poster = sysurl, image
                if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                cm.append((language(30412).encode("utf-8"), 'Action(Info)'))
                if action == 'movies_favourites':
                    if getSetting("meta") == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_movies&name=%s&url=%s&imdb=%s)' % (sys.argv[0], systitle, sysurl, metaimdb)))
                    if getSetting("meta") == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_movies&imdb=%s)' % (sys.argv[0], metaimdb)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action == 'movies_search':
                    cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, trailer)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_from_search&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                else:
                    cm.append((language(30416).encode("utf-8"), 'RunPlugin(%s?action=trailer&name=%s&url=%s)' % (sys.argv[0], sysname, trailer)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30428).encode("utf-8"), 'RunPlugin(%s?action=view_movies)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("art(poster)", poster)
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=False)
            except:
                pass

    def showList(self, showList):
        file = xbmcvfs.File(favData2)
        favRead = file.read()
        file.close()
        file = xbmcvfs.File(subData)
        subRead = file.read()
        file.close()

        total = len(showList)
        for i in showList:
            try:
                name, url, image, imdb, genre, plot = i['name'], i['url'], i['image'], i['imdb'], i['genre'], i['plot']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '
                title = name

                sysname, sysurl, sysimage, sysimdb, sysgenre, sysplot, systitle = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(imdb), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(title)
                u = '%s?action=seasons&url=%s&image=%s&imdb=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysurl, sysimage, sysimdb, sysgenre, sysplot, sysname)

                if getSetting("meta") == 'true':
                    meta = metaget.get_meta('tvshow', title, imdb_id=imdb)
                    playcountMenu = language(30407).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metayear = urllib.quote_plus(str(meta['year']))
                    metaimdb = urllib.quote_plus(re.sub("[^0-9]", "", meta['imdb_id']))
                    poster, banner = meta['cover_url'], meta['banner_url']
                    if banner == '': banner = poster
                    if banner == '': banner = image
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'tvshowtitle': title, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                    poster, banner = image, image
                if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                meta.update({'art(banner)': banner, 'art(poster)': poster})

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))
                if action == 'shows_favourites':
                    if getSetting("meta") == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_tvshows&name=%s&url=%s&imdb=%s)' % (sys.argv[0], systitle, sysurl, metaimdb)))
                    if getSetting("meta") == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_tvshows&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=subscription_add&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=subscription_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library2&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30419).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveUp2&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30420).encode("utf-8"), 'RunPlugin(%s?action=favourite_moveDown2&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30421).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete2&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                elif action == 'shows_subscriptions':
                    if getSetting("meta") == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_tvshows&name=%s&url=%s&imdb=%s)' % (sys.argv[0], systitle, sysurl, metaimdb)))
                    if getSetting("meta") == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_tvshows&imdb=%s)' % (sys.argv[0], metaimdb)))
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=subscription_add&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=subscription_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30425).encode("utf-8"), 'RunPlugin(%s?action=subscriptions_update)' % (sys.argv[0])))
                    cm.append((language(30426).encode("utf-8"), 'RunPlugin(%s?action=subscriptions_clean)' % (sys.argv[0])))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add2&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete2&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                elif action == 'shows_search':
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=subscription_add&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=subscription_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library2&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_from_search2&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))
                else:
                    if not '"%s"' % url in subRead: cm.append((language(30423).encode("utf-8"), 'RunPlugin(%s?action=subscription_add&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    else: cm.append((language(30424).encode("utf-8"), 'RunPlugin(%s?action=subscription_delete&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30422).encode("utf-8"), 'RunPlugin(%s?action=library2&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    if not '"%s"' % url in favRead: cm.append((language(30417).encode("utf-8"), 'RunPlugin(%s?action=favourite_add2&name=%s&imdb=%s&url=%s&image=%s)' % (sys.argv[0], sysname, sysimdb, sysurl, sysimage)))
                    else: cm.append((language(30418).encode("utf-8"), 'RunPlugin(%s?action=favourite_delete2&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                    cm.append((language(30429).encode("utf-8"), 'RunPlugin(%s?action=view_tvshows)' % (sys.argv[0])))
                    cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                    cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                    cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def seasonList(self, seasonList):
        try:
            imdb, genre, plot, show = seasonList[0]['imdb'], seasonList[0]['genre'], seasonList[0]['plot'], seasonList[0]['show']
            if plot == '': plot = addonDesc
            if genre == '': genre = ' '

            if getSetting("meta") == 'true':
                seasons = []
                for i in seasonList: seasons.append(i['season'])
                season_meta = metaget.get_seasons(show, imdb, seasons)
                meta = metaget.get_meta('tvshow', show, imdb_id=imdb)
                banner = meta['banner_url']
            else:
                meta = {'tvshowtitle': show, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                banner = ''
            if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                fanart = meta['backdrop_url']
                if fanart == '': fanart = addonFanart
            else:
                fanart = addonFanart
        except:
            return

        total = len(seasonList)
        for i in range(0, int(total)):
            try:
                name, url, image = seasonList[i]['name'], seasonList[i]['url'], seasonList[i]['image']
                sysname, sysurl, sysimage, sysimdb, sysgenre, sysplot, sysshow = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image), urllib.quote_plus(imdb), urllib.quote_plus(genre), urllib.quote_plus(plot), urllib.quote_plus(show)
                u = '%s?action=episodes&name=%s&url=%s&image=%s&imdb=%s&genre=%s&plot=%s&show=%s' % (sys.argv[0], sysname, sysurl, sysimage, sysimdb, sysgenre, sysplot, sysshow)

                if getSetting("meta") == 'true':
                    meta.update({'playcount': season_meta[i]['playcount'], 'overlay': season_meta[i]['overlay']})
                    poster = season_meta[i]['cover_url']
                    playcountMenu = language(30407).encode("utf-8")
                    if season_meta[i]['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb, metaseason = urllib.quote_plus(re.sub("[^0-9]", "", str(season_meta[i]['imdb_id']))), urllib.quote_plus(str(season_meta[i]['season']))
                    if poster == '': poster = image
                    if banner == '': banner = poster
                    if banner == '': banner = image
                else:
                    poster, banner = image, image

                meta.update({'label': name, 'title': name, 'art(season.banner)': banner, 'art(season.poster': poster})

                cm = []
                cm.append((language(30401).encode("utf-8"), 'RunPlugin(%s?action=item_play)' % (sys.argv[0])))
                cm.append((language(30404).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30413).encode("utf-8"), 'Action(Info)'))
                if getSetting("meta") == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_seasons&imdb=%s&season=%s)' % (sys.argv[0], metaimdb, metaseason)))
                if getSetting("meta") == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_seasons&imdb=%s&season=%s)' % (sys.argv[0], metaimdb, metaseason)))
                cm.append((language(30430).encode("utf-8"), 'RunPlugin(%s?action=view_seasons)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=poster)
                item.setInfo( type="Video", infoLabels = meta )
                item.setProperty("IsPlayable", "true")
                item.setProperty("Video", "true")
                item.setProperty("Fanart_Image", fanart)
                item.addContextMenuItems(cm, replaceItems=True)
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,totalItems=total,isFolder=True)
            except:
                pass

    def episodeList(self, episodeList):
        total = len(episodeList)
        for i in episodeList:
            try:
                name, url, image, imdb, genre, plot = i['name'], i['url'], i['image'], i['imdb'], i['genre'], i['plot']
                title, show, season, episode = i['title'], i['show'], i['season'], i['episode']
                if plot == '': plot = addonDesc
                if genre == '': genre = ' '

                sysname, sysurl, sysimage = urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(image)
                u = '%s?action=play&name=%s&url=%s&t=%s' % (sys.argv[0], sysname, sysurl, datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

                if getSetting("meta") == 'true':
                    if imdb == '0': imdb = metaget.get_meta('tvshow', show)['imdb_id']
                    imdb = re.sub("[^0-9]", "", imdb)
                    meta = metaget.get_episode_meta(title, imdb, season, episode)
                    meta.update({'tvshowtitle': show})
                    playcountMenu = language(30407).encode("utf-8")
                    if meta['overlay'] == 6: playcountMenu = language(30408).encode("utf-8")
                    metaimdb, metaseason, metaepisode = urllib.quote_plus(re.sub("[^0-9]", "", str(meta['imdb_id']))), urllib.quote_plus(str(meta['season'])), urllib.quote_plus(str(meta['episode']))
                    label = str(meta['season']) + 'x' + '%02d' % int(meta['episode']) + ' . ' + meta['title']
                    poster = meta['cover_url']
                    if poster == '': poster = image
                else:
                    meta = {'label': title, 'title': title, 'tvshowtitle': show, 'season': season, 'episode': episode, 'imdb_id' : imdb, 'genre' : genre, 'plot': plot}
                    label = season + 'x' + '%02d' % int(episode) + ' . ' + title
                    poster = image
                if getSetting("meta") == 'true' and getSetting("fanart") == 'true':
                    fanart = meta['backdrop_url']
                    if fanart == '': fanart = addonFanart
                else:
                    fanart = addonFanart

                cm = []
                cm.append((language(30405).encode("utf-8"), 'RunPlugin(%s?action=item_queue)' % (sys.argv[0])))
                cm.append((language(30406).encode("utf-8"), 'RunPlugin(%s?action=download&name=%s&url=%s)' % (sys.argv[0], sysname, sysurl)))
                cm.append((language(30403).encode("utf-8"), 'RunPlugin(%s?action=item_play_from_here&url=%s)' % (sys.argv[0], sysurl)))
                cm.append((language(30414).encode("utf-8"), 'Action(Info)'))
                if getSetting("meta") == 'true': cm.append((language(30415).encode("utf-8"), 'RunPlugin(%s?action=metadata_episodes&imdb=%s&season=%s&episode=%s)' % (sys.argv[0], metaimdb, metaseason, metaepisode)))
                if getSetting("meta") == 'true': cm.append((playcountMenu, 'RunPlugin(%s?action=playcount_episodes&imdb=%s&season=%s&episode=%s)' % (sys.argv[0], metaimdb, metaseason, metaepisode)))
                cm.append((language(30431).encode("utf-8"), 'RunPlugin(%s?action=view_episodes)' % (sys.argv[0])))
                cm.append((language(30409).encode("utf-8"), 'RunPlugin(%s?action=settings_open)' % (sys.argv[0])))
                cm.append((language(30410).encode("utf-8"), 'RunPlugin(%s?action=playlist_open)' % (sys.argv[0])))
                cm.append((language(30411).encode("utf-8"), 'RunPlugin(%s?action=addon_home)' % (sys.argv[0])))

                item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
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
        import urlparse
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        playlist.unshuffle()
        total = xbmc.getInfoLabel('Container.NumItems')
        for i in range(0, int(total)):
            i = str(i)
            label = xbmc.getInfoLabel('ListItemNoWrap(%s).Label' % i)
            if label == '': break

            path = xbmc.getInfoLabel('ListItemNoWrap(%s).FileNameAndPath' % i)
            query = urlparse.urlparse(path.replace(sys.argv[0],'')).query
            name, url = urlparse.parse_qs(query)['name'][0], urlparse.parse_qs(query)['url'][0]
            sysname, sysurl = urllib.quote_plus(name), urllib.quote_plus(url)
            u = '%s?action=play&name=%s&url=%s' % (sys.argv[0], sysname, sysurl)

            meta = {'label' : xbmc.getInfoLabel('ListItemNoWrap(%s).title' % i), 'title' : xbmc.getInfoLabel('ListItemNoWrap(%s).title' % i), 'tvshowtitle': xbmc.getInfoLabel('ListItemNoWrap(%s).tvshowtitle' % i), 'imdb_id' : xbmc.getInfoLabel('ListItemNoWrap(%s).imdb_id' % i), 'season' : xbmc.getInfoLabel('ListItemNoWrap(%s).season' % i), 'episode' : xbmc.getInfoLabel('ListItemNoWrap(%s).episode' % i), 'writer' : xbmc.getInfoLabel('ListItemNoWrap(%s).writer' % i), 'director' : xbmc.getInfoLabel('ListItemNoWrap(%s).director' % i), 'rating' : xbmc.getInfoLabel('ListItemNoWrap(%s).rating' % i), 'duration' : xbmc.getInfoLabel('ListItemNoWrap(%s).duration' % i), 'plot' : xbmc.getInfoLabel('ListItemNoWrap(%s).plot' % i), 'premiered' : xbmc.getInfoLabel('ListItemNoWrap(%s).premiered' % i), 'genre' : xbmc.getInfoLabel('ListItemNoWrap(%s).genre' % i)}
            poster, fanart = xbmc.getInfoLabel('ListItemNoWrap(%s).icon' % i), xbmc.getInfoLabel('ListItemNoWrap(%s).Property(Fanart_Image)' % i)

            item = xbmcgui.ListItem(label, iconImage="DefaultVideo.png", thumbnailImage=poster)
            item.setInfo( type="Video", infoLabels= meta )
            item.setProperty("IsPlayable", "true")
            item.setProperty("Video", "true")
            item.setProperty("Fanart_Image", fanart)
            playlist.add(u, item)
        xbmc.Player().play(playlist)
        subtitles().get(name)

    def playlist_open(self):
        xbmc.executebuiltin('ActivateWindow(VideoPlaylist)')

    def settings_open(self):
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % (addonId))

    def addon_home(self):
        xbmc.executebuiltin('Container.Update(plugin://%s/,replace)' % (addonId))

    def view(self, content):
        try:
            skin = xbmc.getSkinDir()
            if xbmcvfs.exists(xbmc.translatePath('special://xbmc/addons/%s/addon.xml' % (skin))):
                xml = xbmc.translatePath('special://xbmc/addons/%s/addon.xml' % (skin))
            elif xbmcvfs.exists(xbmc.translatePath('special://home/addons/%s/addon.xml' % (skin))):
                xml = xbmc.translatePath('special://home/addons/%s/addon.xml' % (skin))
            else:
                return
            file = xbmcvfs.File(xml)
            read = file.read().replace('\n','')
            file.close()
            src = os.path.dirname(xml) + '/'
            try:
                src += re.compile('defaultresolution="(.+?)"').findall(read)[0] + '/'
            except:
                src += re.compile('<res.+?folder="(.+?)"').findall(read)[0] + '/'
            src += 'MyVideoNav.xml'
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

    def favourite_add(self, data, name, url, image, imdb):
        try:
            index().container_refresh()
            file = open(data, 'a+')
            file.write('"%s"|"%s"|"%s"|"%s"\n' % (name, imdb, url, image))
            #file.write('"%s"|"%s"|"%s"\n' % (name, url, image))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_from_search(self, data, name, url, image, imdb):
        try:
            file = xbmcvfs.File(data)
            read = file.read()
            file.close()
            if url in read:
                index().infoDialog(language(30307).encode("utf-8"), name)
                return
            file = open(data, 'a+')
            file.write('"%s"|"%s"|"%s"|"%s"\n' % (name, imdb, url, image))
            #file.write('"%s"|"%s"|"%s"\n' % (name, url, image))
            file.close()
            index().infoDialog(language(30303).encode("utf-8"), name)
        except:
            return

    def favourite_delete(self, data, name, url):
        try:
            index().container_refresh()
            file = xbmcvfs.File(data)
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
            file = xbmcvfs.File(data)
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
            file = xbmcvfs.File(data)
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

    def subscription_add(self, name, url, image, imdb):
        try:
            status = metaget.get_meta('tvshow', name, imdb_id=imdb)['status']
            if status == 'Ended':
            	yes = index().yesnoDialog(language(30347).encode("utf-8"), language(30348).encode("utf-8"))
            	if not yes: return
            file = open(subData, 'a+')
            file.write('"%s"|"%s"|"%s"|"%s"\n' % (name, imdb, url, image))
            file.close()
            self.library2(name, url, silent=True)
            index().container_refresh()
            index().infoDialog(language(30312).encode("utf-8"), name)
        except:
            return

    def subscription_delete(self, name, url, silent=False):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
            list = re.compile('(".+?\n)').findall(read.replace(line, ''))
            file = open(subData, 'w')
            for line in list: file.write(line)
            file.close()
            if silent == False:
                index().container_refresh()
                index().infoDialog(language(30313).encode("utf-8"), name)
        except:
            return

    def subscriptions_update(self, silent=False):
        try:
            if getSetting("subscriptions_update") == 'true' and getSetting("subscriptions_clean") == 'true':
                self.subscriptions_clean(silent=True)
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
            match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
            for name, imdb, url, image in match:
                if xbmc.abortRequested == True: sys.exit()
                self.library2(name, url, silent=True)
            if getSetting("subscriptions_update") == 'true' and getSetting("subscriptions_updatelibrary") == 'true':
                xbmc.executebuiltin('UpdateLibrary(video)')
            if silent == False:
                index().infoDialog(language(30314).encode("utf-8"))
        except:
            return

    def subscriptions_clean(self, silent=False):
        try:
            file = xbmcvfs.File(subData)
            read = file.read()
            file.close()
            match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
            for name, imdb, url, image in match:
            	status = metaget.get_meta('tvshow', name, imdb_id=imdb)['status']
            	if status == 'Ended':
            	    self.subscription_delete(name, url, silent=True)
            if silent == False:
                index().container_refresh()
                index().infoDialog(language(30315).encode("utf-8"))
        except:
            return

    def metadata(self, content, name, url, imdb, season, episode):
        try:
            list = []
            if content == 'movie' or content == 'tvshow':
                if content == 'movie':
                    search = metaget.search_movies(name)
                elif content == 'tvshow':
                    search = []
                    result = metahandlers.TheTVDB().get_matching_shows(name)
                    for i in result: search.append({'tvdb_id': i[0], 'title': i[1], 'imdb_id': i[2]})
                for i in search:
                    label = i['title']
                    if 'year' in i: label += ' (%s)' % i['year']
                    list.append(label)
                select = index().selectDialog(list, language(30364).encode("utf-8"))
                if select > -1:
                    if content == 'movie':
                        new_imdb = metaget.get_meta('movie', search[select]['title'] ,year=search[select]['year'])['imdb_id']
                    elif content == 'tvshow':
                        new_imdb = search[select]['imdb_id']
                    new_imdb = re.sub("[^0-9]", "", new_imdb)
                    sources = []
                    try: sources.append(favData)
                    except: pass
                    try: sources.append(favData2)
                    except: pass
                    try: sources.append(subData)
                    except: pass
                    if sources == []: raise Exception()
                    for source in sources:
                        try:
                            file = xbmcvfs.File(source)
                            read = file.read()
                            file.close()
                            line = [x for x in re.compile('(".+?)\n').findall(read) if '"%s"' % url in x][0]
                            line2 = line.replace('"0"', '"%s"' % new_imdb).replace('"%s"' % imdb, '"%s"' % new_imdb)
                            file = open(source, 'w')
                            file.write(read.replace(line, line2))
                            file.close()
                        except:
                            pass
                    metaget.update_meta(content, '', imdb, year='')
                    index().container_refresh()
            elif content == 'season':
                metaget.update_episode_meta('', imdb, season, episode)
                index().container_refresh()
            elif content == 'episode':
                metaget.update_season('', imdb, season)
                index().container_refresh()
        except:
            return

    def playcount(self, content, imdb, season, episode):
        try:
            metaget.change_watched(content, '', imdb, season=season, episode=episode, year='', watched='')
            index().container_refresh()
        except:
            return

    def library(self, name, url, silent=False):
        try:
            library = getSetting("movie_library")
            library = xbmc.translatePath(library)
            sysname, sysurl = urllib.quote_plus(name), urllib.quote_plus(url)
            content = '%s?action=play&name=%s&url=%s' % (sys.argv[0], sysname, sysurl)
            enc_name = name.translate(None, '\/:*?"<>|')
            folder = os.path.join(library, enc_name)
            stream = os.path.join(folder, enc_name + '.strm')
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(library)
            xbmcvfs.mkdir(folder)
            file = xbmcvfs.File(stream, 'w')
            file.write(content)
            file.close()
            if silent == False:
                index().infoDialog(language(30311).encode("utf-8"), name)
        except:
            return

    def library2(self, name, url, silent=False):
        try:
            library = getSetting("tv_library")
            library = xbmc.translatePath(library)
            show = name
            enc_show = show.translate(None, '\/:*?"<>|')
            folder = os.path.join(library, enc_show)
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(library)
            xbmcvfs.mkdir(folder)
            seasonUrl = url
            seasonList = seasons().simplymovies_list(url, ' ', ' ', ' ', ' ', show)
            for i in seasonList:
                season = i['name']
                enc_season = season.translate(None, '\/:*?"<>|')
                seasonDir = os.path.join(folder, enc_season)
                xbmcvfs.mkdir(seasonDir)
                episodeList = episodes().simplymovies_list(season, seasonUrl, ' ', ' ', ' ', ' ', show)
                for i in episodeList:
                    name, url = i['name'], i['url']
                    sysname, sysurl = urllib.quote_plus(name), urllib.quote_plus(url)
                    content = '%s?action=play&name=%s&url=%s' % (sys.argv[0], sysname, sysurl)
                    enc_name = name.translate(None, '\/:*?"<>|')
                    stream = os.path.join(seasonDir, enc_name + '.strm')
                    file = xbmcvfs.File(stream, 'w')
                    file.write(content)
                    file.close()
            if silent == False:
                index().infoDialog(language(30311).encode("utf-8"), show)
        except:
            return

    def download(self, name, url):
        try:
            download = getSetting("downloads")
            download = xbmc.translatePath(download)
            if download == '':
            	yes = index().yesnoDialog(language(30341).encode("utf-8"), language(30342).encode("utf-8"))
            	if yes: contextMenu().settings_open()
            	return
            xbmcvfs.mkdir(dataPath)
            xbmcvfs.mkdir(download)

            property = (addonName+name)+'download'
            url = resolver().run(url, name, play=False)
            if url is None: return
            ext = os.path.splitext(url)[1][1:].strip().lower()
            enc_name = name.translate(None, '\/:*?"<>|')
            stream = os.path.join(download, enc_name + '.' + ext)
            temp = stream + '.tmp'

            if xbmcvfs.exists(stream):
            	yes = index().yesnoDialog(language(30343).encode("utf-8"), language(30344).encode("utf-8"), name)
            	if yes:
            	    xbmcvfs.delete(stream)
            	    xbmcvfs.delete(temp)
            	else:
            	    return
            if xbmcvfs.exists(temp):
            	if index().getProperty(property) == 'open':
            	    yes = index().yesnoDialog(language(30345).encode("utf-8"), language(30346).encode("utf-8"), name)
            	    if yes: index().setProperty(property, 'cancel')
            	    return
            	else:
            	    xbmcvfs.delete(temp)

            count = 0
            CHUNK = 16 * 1024
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
            response = urllib2.urlopen(request, timeout=10)
            size = response.info()["Content-Length"]

            file = xbmcvfs.File(temp, 'w')
            index().setProperty(property, 'open')
            index().infoDialog(language(30308).encode("utf-8"), name)
            while True:
            	chunk = response.read(CHUNK)
            	if not chunk: break
            	if index().getProperty(property) == 'cancel': raise Exception()
            	if xbmc.abortRequested == True: raise Exception()
            	part = xbmcvfs.File(temp)
            	quota = int(100 * float(part.size())/float(size))
            	part.close()
            	if not count == quota and count in [0,10,20,30,40,50,60,70,80,90]:
            		index().infoDialog(language(30309).encode("utf-8") + str(count) + '%', name)
            	file.write(chunk)
            	count = quota
            response.close()
            file.close()

            index().clearProperty(property)
            xbmcvfs.rename(temp, stream)
            index().infoDialog(language(30310).encode("utf-8"), name)
        except:
            file.close()
            index().clearProperty(property)
            xbmcvfs.delete(temp)
            sys.exit()
            return

    def trailer(self, name, url):
        url = resolver().trailer(name, url)
        if url is None: return
        item = xbmcgui.ListItem(path=url)
        item.setProperty("IsPlayable", "true")
        xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(url, item)

class subscriptions:
    def __init__(self):
        self.list = []

    def shows(self):
        file = xbmcvfs.File(subData)
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, imdb, url, image in match:
            self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': ' ', 'plot': ' '})
        index().showList(self.list)

class favourites:
    def __init__(self):
        self.list = []

    def movies(self):
        file = xbmcvfs.File(favData)
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, imdb, url, image in match:
            self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': ' ', 'plot': ' '})
        index().movieList(self.list)

    def shows(self):
        file = xbmcvfs.File(favData2)
        read = file.read()
        file.close()
        match = re.compile('"(.+?)"[|]"(.+?)"[|]"(.+?)"[|]"(.+?)"').findall(read)
        for name, imdb, url, image in match:
            self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': ' ', 'plot': ' '})
        index().showList(self.list)

class root:
    def get(self):
        rootList = []
        rootList.append({'name': 30501, 'image': 'Movies.png', 'action': 'root_movies'})
        rootList.append({'name': 30502, 'image': 'TVShows.png', 'action': 'root_shows'})
        rootList.append({'name': 30503, 'image': 'Favourites.png', 'action': 'root_favourites'})
        rootList.append({'name': 30504, 'image': 'Search.png', 'action': 'root_search'})
        index().rootList(rootList)
        index().downloadList()

    def movies(self):
        rootList = []
        rootList.append({'name': 30521, 'image': 'Title.png', 'action': 'movies_title'})
        rootList.append({'name': 30522, 'image': 'Views.png', 'action': 'movies_views'})
        rootList.append({'name': 30523, 'image': 'Rating.png', 'action': 'movies_rating'})
        rootList.append({'name': 30524, 'image': 'Release.png', 'action': 'movies_release'})
        rootList.append({'name': 30525, 'image': 'Pages.png', 'action': 'pages_movies'})
        rootList.append({'name': 30526, 'image': 'Genres.png', 'action': 'genres_movies'})
        rootList.append({'name': 30527, 'image': 'Favourites.png', 'action': 'movies_favourites'})
        rootList.append({'name': 30528, 'image': 'Search.png', 'action': 'movies_search'})
        index().rootList(rootList)

    def shows(self):
        rootList = []
        rootList.append({'name': 30541, 'image': 'Title.png', 'action': 'shows_title'})
        rootList.append({'name': 30542, 'image': 'Views.png', 'action': 'shows_views'})
        rootList.append({'name': 30543, 'image': 'Rating.png', 'action': 'shows_rating'})
        rootList.append({'name': 30544, 'image': 'Pages.png', 'action': 'pages_shows'})
        rootList.append({'name': 30545, 'image': 'Genres.png', 'action': 'genres_shows'})
        rootList.append({'name': 30546, 'image': 'Favourites.png', 'action': 'shows_favourites'})
        rootList.append({'name': 30547, 'image': 'Subscriptions.png', 'action': 'shows_subscriptions'})
        rootList.append({'name': 30548, 'image': 'Search.png', 'action': 'shows_search'})
        index().rootList(rootList)

    def favourites(self):
        rootList = []
        rootList.append({'name': 30561, 'image': 'Movies.png', 'action': 'movies_favourites'})
        rootList.append({'name': 30562, 'image': 'TVShows.png', 'action': 'shows_favourites'})
        index().rootList(rootList)

    def search(self):
        rootList = []
        rootList.append({'name': 30581, 'image': 'Movies.png', 'action': 'movies_search'})
        rootList.append({'name': 30582, 'image': 'TVShows.png', 'action': 'shows_search'})
        index().rootList(rootList)

class link:
    def __init__(self):
        self.simplymovies_base = 'http://simplymovies.net'
        self.simplymovies_movieroot = 'http://simplymovies.net/loadMore.php'
        self.simplymovies_movietitle = 'table=movies&orderBy=title&limit=40&lastRecord=0'
        self.simplymovies_movieviews = 'table=movies&orderBy=views+DESC&limit=100&lastRecord=0'
        self.simplymovies_movierating = 'table=movies&orderBy=rating+DESC&limit=100&lastRecord=0'
        self.simplymovies_movierelease = 'table=movies&orderBy=releaseDate+DESC&limit=100&lastRecord=0'
        self.simplymovies_moviesearch = 'http://simplymovies.net/index.php?sort=rating&searchTerm='
        self.simplymovies_tvshowroot = 'http://simplymovies.net/loadMoreTvShows.php'
        self.simplymovies_tvshowtitle = 'table=tv_shows&orderBy=title&limit=40&lastRecord=0'
        self.simplymovies_tvshowviews = 'table=tv_shows&orderBy=views+DESC&limit=100&lastRecord=0'
        self.simplymovies_tvshowrating = 'table=tv_shows&orderBy=rating+DESC&limit=100&lastRecord=0'
        self.simplymovies_tvshowsearch = 'http://simplymovies.net/tv_shows.php?sort=rating&searchTerm='
        self.simplymovies_moviegenre = "table=movies&orderBy=rating+DESC&limit=40&where=1+%26%26+genres+LIKE+'%25"
        self.simplymovies_moviegenre2 = "%25'&lastRecord=0"
        self.simplymovies_tvshowgenre = "table=tv_shows&orderBy=rating+DESC&limit=40&where=1+%26%26+genres+LIKE+'%25"
        self.simplymovies_tvshowgenre2 = "%25'&lastRecord=0"

        self.youtube_base = 'http://www.youtube.com'
        self.youtube_search = 'http://gdata.youtube.com/feeds/api/videos?q='
        self.youtube_watch = 'http://www.youtube.com/watch?v=%s'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

class pages:
    def __init__(self):
        self.list = []

    def simplymovies_movies(self):
        count = 1
        for i in range(0, 100 * 40, 40):
            name = '%s %s' % ('Page', str(count))
            name = name.encode('utf-8')
            url = link().simplymovies_movietitle.rsplit('=', 1)[0] + '=' + str(i)
            url = url.encode('utf-8')
            image = addonPages.encode('utf-8')
            self.list.append({'name': name, 'url': url, 'image': image})
            count = count + 1

        index().pageList(self.list)

    def simplymovies_shows(self):
        count = 1
        for i in range(0, 20 * 40, 40):
            name = '%s %s' % ('Page', str(count))
            name = name.encode('utf-8')
            url = link().simplymovies_tvshowtitle.rsplit('=', 1)[0] + '=' + str(i)
            url = url.encode('utf-8')
            image = addonPages.encode('utf-8')
            self.list.append({'name': name, 'url': url, 'image': image})
            count = count + 1

        index().pageList(self.list)

class genres:
    def __init__(self):
        self.list = []

    def simplymovies_movies(self):
        self.list = self.simplymovies_list('movies')
        index().pageList(self.list)

    def simplymovies_shows(self):
        self.list = self.simplymovies_list('tvshows')
        index().pageList(self.list)

    def simplymovies_list(self, content):
        try:
            result = getUrl(link().simplymovies_base).result
            if content == 'movies':
                result = common.parseDOM(result, "form", attrs = { "id": "moviesForm" })[0]
            else:
                result = common.parseDOM(result, "form", attrs = { "id": "tv_showsForm" })[0]

            genres = common.parseDOM(result, "select", attrs = { "name": "genre" })[0]
            genres = re.compile('(<option.+?</option>)').findall(genres)
        except:
            return
        for genre in genres:
            try:
                name = common.parseDOM(genre, "option")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                if content == 'movies':
                    url = link().simplymovies_moviegenre + name + link().simplymovies_moviegenre2
                else:
                    url = link().simplymovies_tvshowgenre + name + link().simplymovies_tvshowgenre2
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = addonGenres.encode('utf-8')
                if not name == '':
                    self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list

class movies:
    def __init__(self):
        self.list = []

    def simplymovies(self, url):
        self.list = self.simplymovies_list(url)
        index().movieList(self.list)
        index().nextList(self.list[0]['next'])

    def simplymovies_title(self):
        self.list = self.simplymovies_list(link().simplymovies_movietitle)
        index().movieList(self.list)
        index().nextList(self.list[0]['next'])

    def simplymovies_views(self):
        self.list = self.simplymovies_list(link().simplymovies_movieviews)
        index().movieList(self.list)

    def simplymovies_rating(self):
        self.list = self.simplymovies_list(link().simplymovies_movierating)
        index().movieList(self.list)

    def simplymovies_release(self):
        self.list = self.simplymovies_list(link().simplymovies_movierelease)
        index().movieList(self.list)

    def simplymovies_search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = None#query
        if not (self.query is None or self.query == ''):
            self.query = link().simplymovies_moviesearch + urllib.quote_plus(self.query.replace(' ', '-'))
            self.list = self.simplymovies_list('', self.query)
            index().movieList(self.list)

    def simplymovies_list(self, post, url=None):
        try:
            if url is None: url = link().simplymovies_movieroot
            result = getUrl(url, post=post).result
            movies = common.parseDOM(result, "div", attrs = { "class": "movieInfoHolder" })
        except:
            return
        try:
            next = '%s=%s' % (post.rsplit('=', 1)[0], int(post.split("=")[-1])+40)
        except:
            next = ''
        for movie in movies:
            try:
                title = common.parseDOM(movie, "h3")[0]
                year = common.parseDOM(movie, "p", attrs = { "class": "overlayMovieRelease" })[0]
                year = re.sub("[^0-9]", "", year.rsplit(' ', 1)[-1])
                name = '%s (%s)' % (title, year)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(movie, "a", ret="href")[0]
                url = '%s/%s' % (link().simplymovies_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(movie, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                try: imdb = common.parseDOM(movie, "a", ret="href", attrs = { "class": "imdbPageLink" })[0]
                except: imdb = '0'
                imdb = re.sub("[^0-9]", "", imdb.rsplit('/tt', 1)[-1])
                imdb = imdb.encode('utf-8')
                try: genre = common.parseDOM(movie, "p", attrs = { "class": "overlayMovieGenres" })[0]
                except: genre = ''
                genre = genre.rsplit(',', 1)[0].replace(',', ' /')
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')
                try: plot = common.parseDOM(movie, "p", attrs = { "class": "overlayMovieDescription" })[0]
                except: plot = ''
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'next': next})
            except:
                pass

        return self.list

class shows:
    def __init__(self):
        self.list = []

    def simplymovies(self, url):
        self.list = self.simplymovies_list(url)
        index().showList(self.list)
        index().nextList(self.list[0]['next'])

    def simplymovies_title(self):
        self.list = self.simplymovies_list(link().simplymovies_tvshowtitle)
        index().showList(self.list)
        index().nextList(self.list[0]['next'])

    def simplymovies_views(self):
        self.list = self.simplymovies_list(link().simplymovies_tvshowviews)
        index().showList(self.list)

    def simplymovies_rating(self):
        self.list = self.simplymovies_list(link().simplymovies_tvshowrating)
        index().showList(self.list)

    def simplymovies_search(self, query=None):
        if query is None:
            self.query = common.getUserInput(language(30362).encode("utf-8"), '')
        else:
            self.query = None#query
        if not (self.query is None or self.query == ''):
            self.query = link().simplymovies_tvshowsearch + urllib.quote_plus(self.query.replace(' ', '-'))
            self.list = self.simplymovies_list('', self.query)
            index().showList(self.list)

    def simplymovies_list(self, post, url=None):
        try:
            if url is None: url = link().simplymovies_tvshowroot
            result = getUrl(url, post=post).result
            shows = common.parseDOM(result, "div", attrs = { "class": "movieInfoHolder" })
        except:
            return
        try:
            next = '%s=%s' % (post.rsplit('=', 1)[0], int(post.split("=")[-1])+40)
        except:
            next = ''
        for show in shows:
            try:
                name = common.parseDOM(show, "h3")[0]
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(show, "a", ret="href")[0]
                url = '%s/%s' % (link().simplymovies_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                image = common.parseDOM(show, "img", ret="src")[0]
                image = common.replaceHTMLCodes(image)
                image = image.encode('utf-8')
                try: imdb = common.parseDOM(show, "a", ret="href", attrs = { "class": "imdbPageLink" })[0]
                except: imdb = '0'
                imdb = re.sub("[^0-9]", "", imdb.rsplit('/tt', 1)[-1])
                imdb = imdb.encode('utf-8')
                try: genre = common.parseDOM(show, "p", attrs = { "class": "overlayMovieGenres" })[0]
                except: genre = ''
                genre = genre.rsplit(',', 1)[0].replace(',', ' /')
                genre = common.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')
                try: plot = common.parseDOM(show, "p", attrs = { "class": "overlayMovieDescription" })[0]
                except: plot = ''
                plot = common.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'next': next})
            except:
                pass

        return self.list

class seasons:
    def __init__(self):
        self.list = []

    def simplymovies(self, url, image, imdb, genre, plot, show):
        self.list = self.simplymovies_list(url, image, imdb, genre, plot, show)
        index().seasonList(self.list)

    def simplymovies_list(self, url, image, imdb, genre, plot, show):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "id": "main" })[0]
            seasons = common.parseDOM(result, "h3")
        except:
            return
        for season in seasons:
            try:
                name = common.replaceHTMLCodes(season)
                name = name.encode('utf-8')
                num = re.sub("[^0-9]", "", name.rsplit(' ', 1)[-1])
                num = num.encode('utf-8')
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'show': show, 'season': num})
            except:
                pass

        return self.list

class episodes:
    def __init__(self):
        self.list = []

    def simplymovies(self, name, url, image, imdb, genre, plot, show):
        self.list = self.simplymovies_list(name, url, image, imdb, genre, plot, show)
        index().episodeList(self.list)

    def simplymovies_list(self, name, url, image, imdb, genre, plot, show):
        try:
            result = getUrl(url).result
            result = common.parseDOM(result, "div", attrs = { "id": "main" })[0]
            season = re.sub("[^0-9]", "", name.split(" ")[-1])
            season = season.encode('utf-8')
            episodes = result.split("<h3>%s" % name)[-1].split("<h3>")[0]
            episodes = common.parseDOM(episodes, "p")
        except:
            return
        for episode in episodes:
            try:
                label = common.parseDOM(episode, "a")[0]
                try: title = label.split(":", 1)[1].strip()
                except: title = label
                title = common.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                num = re.sub("[^0-9]", "", label.split(":")[0])
                num = num.encode('utf-8')
                name = show + ' S' + '%02d' % int(season) + 'E' + '%02d' % int(num)
                name = common.replaceHTMLCodes(name)
                name = name.encode('utf-8')
                url = common.parseDOM(episode, "a", ret="href")[0]
                url = '%s/%s' % (link().simplymovies_base, url)
                url = common.replaceHTMLCodes(url)
                url = url.encode('utf-8')
                self.list.append({'name': name, 'url': url, 'image': image, 'imdb': imdb, 'genre': genre, 'plot': plot, 'title': title, 'show': show, 'season': season, 'episode': num})
            except:
                pass

        return self.list

class resolver:
    def run(self, url, name=None, play=True):
        try:
            if player().status() is True: return
            url = self.simplymovies(url)
            if url is None: raise Exception()

            if play == False: return url
            player().run(name, url)
            return url
        except:
            index().infoDialog(language(30317).encode("utf-8"))
            return

    def simplymovies(self, url):
        try:
            result = getUrl(url).result
            url = common.parseDOM(result, "iframe", ret="src", attrs = { "class": "videoPlayerIframe" })[0]
            result = getUrl(url).result
            var = common.parseDOM(result, "param", ret="value", attrs = { "name": "flashvars" })[0]
            var = common.replaceHTMLCodes(var)
            url = None
            try: url = re.compile('url240=(.+?)&').findall(var)[0]
            except: pass
            try: url = re.compile('url360=(.+?)&').findall(var)[0]
            except: pass
            try: url = re.compile('url480=(.+?)&').findall(var)[0]
            except: pass
            if getSetting("quality") == 'true' or url is None:
                try: url = re.compile('url720=(.+?)&').findall(var)[0]
                except: pass
            return url
        except:
            return

    def trailer(self, name, url):
        try:
            if not url.startswith('http://'):
                url = link().youtube_watch % url
                url = self.youtube(url)
            else:
                try:
                    result = getUrl(url).result
                    url = re.compile('"http://www.youtube.com/embed/(.+?)"').findall(result)[0]
                    url = url.split("?")[0].split("&")[0]
                    url = link().youtube_watch % url
                    url = self.youtube(url)
                except:
                    url = link().youtube_search + name + ' trailer'
                    url = self.youtube_search(url)
            if url is None: return
            return url
        except:
            return

    def youtube_search(self, url):
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
                url = link().youtube_watch % url
                url = self.youtube(url)
                if not url is None: return url
        except:
            return

    def youtube(self, url):
        try:
            if index().addon_status('plugin.video.youtube') is None:
                index().okDialog(language(30321).encode("utf-8"), language(30322).encode("utf-8"))
                return
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            state, reason = None, None
            result = getUrl(link().youtube_info % id).result
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = getUrl(link().youtube_watch % id).result
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return


main()