#!/usr/bin/python

import requests
import sys
import json
import re
import os
import time
from urllib import urlretrieve
from urllib2 import urlopen, HTTPError

user_agent = {'User-Agent': 'rud v0.2 by /u/manic0892 (github.com/Manic0892/rid)'}

class colors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

# def vid_me(i, user):

# def vidible(i, user):


def imgur(i, user):
	imgurURL = ''
	imgurType = 0
	#imgurType
	#0 - Not Found
	#1 - Straight-ahead image
	#2 - .zip file
	imgurID = ''
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
			print (colors.OKGREEN + 'Downloading ' + imgurID + ' from ' + imgurURL + ' to ./downloads/'+user+'/'+imgurID+'.png' + colors.ENDC)
			urlretrieve(imgurURL, './downloads/'+user+'/'+imgurID+'.png')
		else:
			print (colors.OKBLUE + 'Skipping previously downloaded image - ' + imgurID + colors.ENDC)
	elif imgurType == 2:
		if not os.path.exists('./downloads/'+user+'/'+imgurID+'.zip'):
			print (colors.OKGREEN + 'Downloading ' + imgurID + ' from ' + imgurURL + ' to ./downloads/'+user+'/'+imgurID+'.zip' + colors.ENDC)
			urlretrieve(imgurURL, './downloads/'+user+'/'+imgurID+'.zip')
		else:
			print (colors.OKBLUE + 'Skipping previously downloaded album - ' + imgurID + colors.ENDC)
	else:
		print (colors.FAIL + '404 - ' + imgurURL + colors.ENDC)

def gfycat(i, user):
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

def getUsername(user):
	print '- - - - - - - - - - - - - - - - - - - - - - - - - - - - -'
	print '|'
	print '| ' + colors.UNDERLINE + user + colors.ENDC
	print '|'
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
				if i['data']['domain'] == 'i.imgur.com' or i['data']['domain'] == 'imgur.com' or i['data']['domain'] == 'm.imgur.com':
					imgur(i, user)
				elif i['data']['domain'] == 'gfycat.com':
					gfycat(i, user)
				else:
					try:
						f = open('./downloads/'+user+'/__URLS.txt','a')
						f.write(i['data']['url'] + '\n') # python will convert \n to os.linesep
						f.close() # you can omit in most cases as the destructor will call if
						print (colors.WARNING + 'Skipping non-Imgur link.  Check __URLS.txt for a list of unsupported URLs not downloaded.' + colors.ENDC)
					except:
						print(colors.FAIL + 'An error occurred when trying to add this non-Imgur link to __URLS.txt.' + colors.ENDC)
					
			currURL = baseURL + '&after=' + data['data']['children'][-1]['data']['name']

if not os.path.exists('./downloads'):
	os.makedirs('./downloads')
for i in sys.argv[1:]:
	getUsername(i)
