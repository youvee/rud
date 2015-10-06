# Downloads gfycat.com links

import re								# re.search						-- Regex searching
import os								# os.path.exists, os.makedirs	-- Path existence, directory creation
from urllib import urlretrieve			# urlretrieve					-- Download from URL to local machine
from urllib2 import urlopen, HTTPError	# urlopen, HTTPError			-- Web page access, HTTP errors

domain = 'gfycat.com'

def process(i, user, colors):
	gfycatURL = i['data']['url']
	gfycatURL.replace('gfycat', 'giant.gfycat')
	gfycatURL.strip('#')
	gfycatID = re.search('(?<=gfycat.com/)[A-Za-z0-9]+', gfycatURL)
	gfycatID = gfycatID.group(0)
	gfycatURL = 'http://giant.gfycat.com/' + gfycatID + '.webm'
	if os.path.exists('./downloads/'+user+'/'+gfycatID+'.webm'):
		print (colors.OKBLUE + 'Skipping previously downloaded gfy - ' + gfycatID + colors.ENDC)
	else:
		try:
			urlopen(gfycatURL)
		except HTTPError:
			print(colors.FAIL + 'Error using giant link.  Switching to fat...' + colors.ENDC)
			try:
				gfycatURL = 'http://fat.gfycat.com/' + gfycatID + '.webm'
				urlopen(gfycatURL)
			except HTTPError:
				print (colors.FAIL + 'Error using fat link.  Switching to zippy...' + colors.ENDC)
				try:
					gfycatURL = 'http://zippy.gfycat.com/' + gfycatID + '.webm'
					urlopen(gfycatURL)
				except HTTPError:
					print (colors.FAIL + 'Tried to request ' + gfycatID + ' but encountered issues.  Downloading anyway using giant.' + colors.ENDC)
					gfycatURL = 'http://giant.gfycat.com/' + gfycatID + '.webm'

		print (colors.OKGREEN + 'Downloading ' + gfycatID + ' from ' + gfycatURL + ' to ./downloads/'+user+'/'+gfycatID+'.webm' + colors.ENDC)
		urlretrieve(gfycatURL, './downloads/'+user+'/'+gfycatID+'.webm')