# Downloads sendvid.com links

import re								# re.search						-- Regex searching
import os								# os.path.exists, os.makedirs	-- Path existence, directory creation
from urllib import urlretrieve			# urlretrieve					-- Download from URL to local machine

domain = 'sendvid.com'

def process(i, user, colors):
	sendvidURL = i['data']['url']
	sendvidID = re.search('(?<=sendvid.com/)[A-Za-z0-9]+', sendvidURL)
	sendvidID = sendvidID.group(0)
	if not os.path.exists('./downloads/'+user+'/'+sendvidID+'.mp4'):
		print(colors.OKGREEN + 'Downloading ' + sendvidID + ' from ' + sendvidURL + ' to ./downloads/'+user+'/'+sendvidID+'.mp4' + colors.ENDC)
		urlretrieve('http://sendvid.com/'+sendvidID+'.mp4', './downloads/'+user+'/'+sendvidID+'.mp4')
	else:
		print(colors.OKBLUE + 'Skipping previously downloaded Sendvid - ' + sendvidID + colors.ENDC)