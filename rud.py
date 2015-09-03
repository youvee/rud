#!/usr/bin/python

import requests
import sys
import json
import re
import os
import time
from urllib import urlretrieve
from urllib2 import urlopen, HTTPError

user_agent = {'User-Agent': 'rud v0.1 by /u/manic0892 (github.com/Manic0892/rid)'}

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
	f = open('./downloads/'+user+'/__URLS.txt','a')
	f.write('\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n')
	f.write(time.strftime("%c") + '\n')
	f.write('- - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n\n')
	f.close()

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
					imgurURL = i['data']['url'].split('://')[1] #Strip out http(s) to avoid errors with http vs https
					if i['data']['domain'] == 'i.imgur.com':
						imgurType = 1
						imgurID = re.search('(?<=i.imgur.com/)[A-Za-z0-9]+', imgurURL)
						imgurID = imgurID.group(0)
					elif i['data']['domain'] == 'm.imgur.com':
						imgurType = 1
						imgurID = re.search('(?<=m.imgur.com/)[A-Za-z0-9]+', imgurURL).group(0)
						imgurURL = 'i.imgur.com/' + imgurID + '.png'
					elif i['data']['domain'] == 'imgur.com':
						m = re.search('(?<=imgur.com/a/)[A-Za-z0-9]+', imgurURL)
						if m is None:
							m = re.search('(?<=imgur.com/)[A-Za-z0-9]+', imgurURL)
							if m is None:
								m = re.search('(?<=imgur.com/gallery/)[A-Za-z0-9]+', imgurURL)
								if m is not None:
									imgurType = 1
							else:
								imgurType = 1
						else:
							imgurType = 2
						
						if m is not None:
							imgurID = m.group(0)
							if imgurType == 2:
								imgurURL = 's.imgur.com/a/' + imgurID + '/zip'
							elif imgurType == 1:
								imgurURL = 'i.imgur.com/'+imgurID+'.png'
							else:
								imgurType = 0
						else:
							imgurType = 0

					imgurURL = 'http://' + imgurURL #Un-strip http(s)
					if imgurType == 1:
						if not os.path.exists('./downloads/'+user+'/'+imgurID+'.png'):
							print ('Downloading ' + imgurID + ' from ' + imgurURL + ' to ./downloads/'+user+'/'+imgurID+'.png')
							urlretrieve(imgurURL, './downloads/'+user+'/'+imgurID+'.png')
						else:
							print ('Skipping previously downloaded image - ' + imgurID)
					elif imgurType == 2:
						if not os.path.exists('./downloads/'+user+'/'+imgurID+'.zip'):
							print ('Downloading ' + imgurID + ' from ' + imgurURL + ' to ./downloads/'+user+'/'+imgurID+'.zip')
							urlretrieve(imgurURL, './downloads/'+user+'/'+imgurID+'.zip')
						else:
							print ('Skipping previously downloaded album - ' + imgurID)
					else:
						print ('404 - ' + imgurURL)
				elif i['data']['domain'] == 'gfycat.com':
					gfycatURL = i['data']['url']
					gfycatURL.replace('gfycat', 'giant.gfycat')
					gfycatURL.strip('#')
					gfycatID = re.search('(?<=gfycat.com/)[A-Za-z0-9]+', gfycatURL)
					gfycatID = gfycatID.group(0)
					gfycatURL = 'http://giant.gfycat.com/' + gfycatID + '.webm'
					if os.path.exists('./downloads/'+user+'/'+gfycatID+'.webm'):
						print ('Skipping previously downloaded gfy - ' + gfycatID)
					else:
						try:
							urlopen(gfycatURL)
						except HTTPError:
							print('Error using giant link.  Switching to fat...')
							try:
								gfycatURL = 'http://fat.gfycat.com/' + gfycatID + '.webm'
								urlopen(gfycatURL)
							except HTTPError:
								print ('Error using fat link.  Switching to zippy...')
								try:
									gfycatURL = 'http://zippy.gfycat.com/' + gfycatID + '.webm'
									urlopen(gfycatURL)
								except HTTPError:
									print ('Tried to request ' + gfycatID + ' but encountered issues.  Downloading anyway using giant.')
									gfycatURL = 'http://giant.gfycat.com/' + gfycatID + '.webm'

						print ('Downloading ' + gfycatID + ' from ' + gfycatURL + ' to ./downloads/'+user+'/'+gfycatID+'.webm')
						urlretrieve(gfycatURL, './downloads/'+user+'/'+gfycatID+'.webm')
				else:
					try:
						f = open('./downloads/'+user+'/__URLS.txt','a')
						f.write(i['data']['url'] + '\n') # python will convert \n to os.linesep
						f.close() # you can omit in most cases as the destructor will call if
						print('Skipping non-Imgur link.  Check __URLS.txt for a list of unsupported URLs not downloaded.')
					except:
						print('An error occurred when trying to add this non-Imgur link to __URLS.txt.')
					
					
					
					#print i['data']['title']
				#elif i['data']['domain'] == 'imgur.com':
			currURL = baseURL + '&after=' + data['data']['children'][-1]['data']['name']

#def getImgurDL

if not os.path.exists('./downloads'):
	os.makedirs('./downloads')
for i in sys.argv[1:]:
	getUsername(i)