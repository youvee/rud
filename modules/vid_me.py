# Downloads vid.me links

import re								# re.search						-- Regex searching
import os								# os.path.exists, os.makedirs	-- Path existence, directory creation
from urllib import urlretrieve			# urlretrieve					-- Download from URL to local machine
from urllib2 import urlopen, HTTPError	# urlopen, HTTPError			-- Web page access, HTTP errors
import lxml.html						# lxml.html						-- HTML parsing

domain = 'vid.me'

def process(i, user, colors):
	vid_meURL = i['data']['url']
	vid_meID = re.search('(?<=vid.me/)[A-Za-z0-9]+', vid_meURL)
	vid_meID = vid_meID.group(0)
	links = lxml.html.parse(urlopen(vid_meURL)).xpath("//source/@src")
	for link in links:
		if not os.path.exists('./downloads/'+user+'/'+vid_meID+'.mp4'):
			print (colors.OKGREEN + 'Downloading ' + vid_meID + ' from ' + vid_meURL + ' to ./downloads/'+user+'/'+vid_meID+'.mp4' + colors.ENDC)
			urlretrieve(link, './downloads/'+user+'/'+vid_meID+'.mp4')
		else:
			print (colors.OKBLUE + 'Skipping previously downloaded vidme - ' + vid_meID + colors.ENDC)