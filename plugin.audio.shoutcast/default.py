#/*
# *      Copyright (C) 2010 Team XBMC
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# */

import urllib2,string,xbmc,xbmcgui,xbmcplugin
from xml.dom import minidom
from urllib import quote_plus
import unicodedata

BASE_URL = 'http://yp.shoutcast.com/sbin/newxml.phtml'

__XBMC_Revision__ = xbmc.getInfoLabel('System.BuildVersion')

def INDEX():
  req = urllib2.Request(BASE_URL)
  response = urllib2.urlopen(req)
  link=response.read()
  response.close()
  for stat in minidom.parseString(link).firstChild.getElementsByTagName('genre'):
    name = stat.attributes["name"].value
    addDir(name)

def RESOLVE(id):
  url = "%s?genre=%s" % (BASE_URL, quote_plus(id),)
  req3 = urllib2.Request(url)
  response = urllib2.urlopen(req3)
  link = response.read()
  response.close()
  node = minidom.parseString(link).firstChild
  for stat in node.getElementsByTagName('station'):
    name = unicodedata.normalize('NFKD',stat.attributes["name"].value).encode('ascii','ignore')
    url = "%s?play=%s&tunein=%s" % (sys.argv[0], stat.attributes["id"].value,node.getElementsByTagName('tunein')[0].attributes["base"].value)
    addLink(name,url,stat.attributes["br"].value)

def PLAY(st_id, tunein):
  if __XBMC_Revision__.startswith("10.0"):
    url = "shout://yp.shoutcast.com%s?id=%s" %(tunein,st_id,)
  else:
    url = "http://yp.shoutcast.com%s?id=%s" %(tunein,st_id,)
  print "#### plugin.audio.shoutcast #### URL: %s" % url    
  xbmc.Player().play(url)

def addLink(name,url,size):
  ok=True
  liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage="")
  liz.setInfo( type="Video", infoLabels={ "Title": name ,"Size": int(size)} )
  liz.setProperty("IsPlayable","false");
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
  return ok

def get_params():
  param=[]
  paramstring=sys.argv[2]
  if len(paramstring)>=2:
    params=sys.argv[2]
    cleanedparams=params.replace('?','')
    if (params[len(params)-1]=='/'):
      params=params[0:len(params)-2]
    pairsofparams=cleanedparams.split('&')
    param={}
    for i in range(len(pairsofparams)):
      splitparams={}
      splitparams=pairsofparams[i].split('=')
      if (len(splitparams))==2:
        param[splitparams[0]]=splitparams[1]
  return param

def addDir(name):
  u = "%s?id=%s" % (sys.argv[0], name,)
  liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage="")
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
  return ok

params=get_params()
try:
  id = params["id"]
except:
  id = "0";
  pass
try:
  play = params["play"]
except:
  play = "0";
  pass  

iid = len(id);
iplay = len(play)

if iid > 1 :
  RESOLVE(id)
  xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL, label2Mask="%X" )
  xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_BITRATE, label2Mask="%X" )
  xbmcplugin.endOfDirectory(int(sys.argv[1]))
else:
  if iplay > 1:
    PLAY(play,params["tunein"] )
  else:  
    INDEX()
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


