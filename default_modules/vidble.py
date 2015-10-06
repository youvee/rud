# Downloads vidble.com links

import requests							# requests.get					-- JSON requests
import json								# json.loads					-- JSON response loading to requests
import re								# re.search						-- Regex searching
import os								# os.path.exists, os.makedirs	-- Path existence, directory creation
from urllib import urlretrieve			# urlretrieve					-- Download from URL to local machine
import lxml.html						# lxml.html						-- HTML parsing

user_agent = {'User-Agent': 'Vidble module for rud v0.3.1 by /u/manic0892 (github.com/Manic0892/rid)'}

domain = 'vidble.com'

# Downloads all images in a Vidble album.
def vidbleAlbum(i, user, vidbleID, vidbleURL, colors):
	if not os.path.exists('./downloads/' + user + '/' + vidbleID):
		print (colors.OKGREEN + 'Downloading ' + vidbleID + ' from ' + vidbleURL + ' to ./downloads/'+user+'/'+vidbleID + colors.ENDC)
		os.makedirs('./downloads/' + user + '/' + vidbleID)
	else:
		print (colors.OKBLUE + 'Downloading previously downloaded vidble album - ' + vidbleID)
	vidbleJSONURL = vidbleURL + '?json=1'
	r = requests.get(vidbleJSONURL, headers=user_agent)
	data = r.text;
	data = json.loads(data)
	for j in data['pics']:
		vidbleImageID = re.search('(?<=vidble.com/)[A-Za-z0-9]+', j)
		vidbleImageID = vidbleImageID.group(0)
		vidbleImageURL = 'http:' + j
		if not os.path.exists('./downloads/' + user + '/' + vidbleID + '/' + vidbleImageID + '.jpg'):
			print (colors.OKGREEN + ' - Downloading ' + vidbleImageID + ' from ' + vidbleImageURL + ' to ./downloads/'+user+'/'+vidbleID + '/' + vidbleImageID + '.jpg' + colors.ENDC)
			urlretrieve(vidbleImageURL, './downloads/'+user+'/'+vidbleID + '/' + vidbleImageID + '.jpg')
		else:
			print (colors.OKBLUE + ' - Skipping previously downloaded vidble image - ' + vidbleImageID + colors.ENDC)

def process(i, user, colors):
	vidbleURL = i['data']['url']
	vidbleID = re.search('(?<=vidble.com/album/)[A-Za-z0-9]+', vidbleURL)
	if vidbleID is not None:
			vidbleID = vidbleID.group(0)
			vidbleAlbum(i, user, vidbleID, vidbleURL, colors)
	else:
		vidbleID = re.search('(?<=vidble.com/)[A-Za-z0-9]+', vidbleURL)
		if vidbleID is not None:
			vidbleID = vidbleID.group(0)
			if not os.path.exists('./downloads/'+user+'/'+vidbleID+'.jpg'):
				print (colors.OKGREEN + 'Downloading ' + vidbleID + ' from ' + vidbleURL + ' to ./downloads/'+user+'/'+vidbleID+'.jpg' + colors.ENDC)
				urlretrieve(vidbleURL, './downloads/'+user+'/'+vidbleID+'.jpg')
			else:
				print (colors.OKBLUE + 'Skipping previously downloaded vidble image - ' + vidbleID + colors.ENDC)
		else:
			print (colors.FAIL + 'An error occurred in downloading ' + vidbleURL + colors.ENDC)