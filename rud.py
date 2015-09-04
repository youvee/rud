#!/usr/bin/python

import requests
import sys
import json
import re
import os
import time
from urllib import urlretrieve
from urllib2 import urlopen, HTTPError
import lxml.html

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

def vid_me(i, user):
	vid_meURL = i['data']['url']
	vid_meID = re.search('(?<=vid.me/)[A-Za-z0-9]+', vid_meURL)
	vid_meID = vid_meID.group(0)
	links = lxml.html.parse(urlopen(vid_meURL)).xpath("//source/@src")
	for link in links:
		if not os.path.exists('./downloads/'+user+'/'+vid_meID+'.mp4'):
			print (colors.OKGREEN + 'Downloading ' + vid_meID + ' from ' + vid_meURL + ' to ./downloads/'+user+'/'+vid_meID+'.mp4' + colors.ENDC)
			urlretrieve(link, './downloads/'+user+'/'+vid_meID+'.mp4')
		else:
			print (colors.OKBLUE + 'Skipping previously downloaded vid - ' + vid_meID + colors.ENDC)

def vidbleAlbum(i, user, vidbleID, vidbleURL):
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

def vidble(i, user):
	vidbleURL = i['data']['url']
	vidbleID = re.search('(?<=vidble.com/album/)[A-Za-z0-9]+', vidbleURL)
	if vidbleID is not None:
			vidbleID = vidbleID.group(0)
			vidbleAlbum(i, user, vidbleID, vidbleURL)
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
			print (colors.OKBLUE + 'Skipping previously downloaded Imgur image - ' + imgurID + colors.ENDC)
	elif imgurType == 2:
		if not os.path.exists('./downloads/'+user+'/'+imgurID+'.zip'):
			print (colors.OKGREEN + 'Downloading ' + imgurID + ' from ' + imgurURL + ' to ./downloads/'+user+'/'+imgurID+'.zip' + colors.ENDC)
			urlretrieve(imgurURL, './downloads/'+user+'/'+imgurID+'.zip')
		else:
			print (colors.OKBLUE + 'Skipping previously downloaded Imgur album - ' + imgurID + colors.ENDC)
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
				elif i['data']['domain'] == 'vid.me':
					vid_me(i, user)
				elif i['data']['domain'] == 'vidble.com':
					vidble(i, user)
				else:
					try:
						f = open('./downloads/'+user+'/__URLS.txt','a')
						f.write(i['data']['url'] + '\n') # python will convert \n to os.linesep
						f.close() # you can omit in most cases as the destructor will call if
						print (colors.WARNING + 'Skipping unsupported link.  Check __URLS.txt for a list of unsupported URLs not downloaded.' + colors.ENDC)
					except:
						print(colors.FAIL + 'An error occurred when trying to add this unsupported link to __URLS.txt.' + colors.ENDC)
					
			currURL = baseURL + '&after=' + data['data']['children'][-1]['data']['name']

if not os.path.exists('./downloads'):
	os.makedirs('./downloads')
for i in sys.argv[1:]:
	getUsername(i)
