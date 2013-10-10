#!/usr/bin/python

import requests
import sys
import json
import re
import os
from urllib import urlretrieve

user_agent = {'User-Agent': 'rid v0.1 by /u/manic0892 (github.com/Manic0892/rid)'}

def getUsername(user):
	print '- - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
	#print '|'
	print '| ' + user
	#print '|'
	print '- - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
	baseURL = 'http://www.reddit.com/user/' + user + '/submitted.json?limit=100'
	currURL = baseURL
	
	if not os.path.exists('./downloads/'+user):
		os.makedirs('downloads/'+user)

	while True:
		r = requests.get(currURL, headers=user_agent)
		data= r.text
		data = json.loads(data)
		if (len(data['data']['children']) == 0):
			break
		else:
			for i in data['data']['children']:
				imgurURL = ''
				imgurType = 0
				#imgurType
				#0 - Not Found
				#1 - Straight-ahead image
				#2 - .zip file
				imgurID = ''
				if i['data']['domain'] == 'i.imgur.com' or i['data']['domain'] == 'imgur.com' or i['data']['domain'] == 'm.imgur.com':
					if i['data']['domain'] == 'i.imgur.com':
						imgurURL = i['data']['url']
						imgurType = 1
						imgurID = re.search('(?<=http://i.imgur.com/)[A-Za-z0-9]+', imgurURL)
						if imgurID is None:
							imgurID = re.search('(?<=https://i.imgur.com/)[A-Za-z0-9]+', imgurURL)
						imgurID = imgurID.group(0)
						#print imgurID
						#print imgurURL
					elif i['data']['domain'] == 'm.imgur.com':
						imgurURL= i['data']['url']
						imgurType = 1
						imgurID = re.search('(?<=http://m.imgur.com/)[A-Za-z0-9]+', imgurURL).group(0)
						imgurURL = 'http://i.imgur.com/' + imgurID + '.png'
					elif i['data']['domain'] == 'imgur.com':
						imgurURL = i['data']['url']
						m = re.search('(?<=http://imgur.com/a/)[A-Za-z0-9]+', imgurURL)
						if m is None:
							m = re.search('(?<=http://imgur.com/)[A-Za-z0-9]+', imgurURL)
							if m is None:
								m = re.search('(?<=http://imgur.com/gallery/)[A-Za-z0-9]+', imgurURL)
								if m is not None:
									imgurType = 1
							else:
								imgurType = 1
						else:
							imgurType = 2
						
						if m is not None:
							imgurID = m.group(0)
							if imgurType == 2:
								imgurURL = 'http://s.imgur.com/a/' + imgurID + '/zip'
							elif imgurType == 1:
								imgurURL = 'http://i.imgur.com/'+imgurID+'.png'
							else:
								imgurType = 0
						else:
							imgurType = 0

						
					if imgurType == 1:
						if not os.path.exists('./downloads/'+user+'/'+imgurID+'.png'):
							urlretrieve(imgurURL, './downloads/'+user+'/'+imgurID+'.png')
							print ('Downloading ' + imgurID + ' from ' + imgurURL + ' to ./downloads/'+user+'/'+imgurID+'.png')
						else:
							print ('Skipping previously downloaded image - ' + imgurID)
					elif imgurType == 2:
						if not os.path.exists('./downloads/'+user+'/'+imgurID+'.zip'):
							urlretrieve(imgurURL, './downloads/'+user+'/'+imgurID+'.zip')
							print ('Downloading ' + imgurID + ' from ' + imgurURL + ' to ./downloads/'+user+'/'+imgurID+'.zip')
						else:
							print ('Skipping previously downloaded album - ' + imgurID)
					else:
						print ('404')
				else:
					print('Skipping non-Imgur link')
					
					
					
					#print i['data']['title']
				#elif i['data']['domain'] == 'imgur.com':
			currURL = baseURL + '&after=' + data['data']['children'][-1]['data']['name']

#def getImgurDL

if not os.path.exists('./downloads'):
	os.makedirs('./downloads')
for i in sys.argv[1:]:
	getUsername(i)