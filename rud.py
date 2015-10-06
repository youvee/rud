#!/usr/bin/python

import requests							# requests.get					-- JSON requests
import sys								# sys.argv						-- Command line options
import json								# json.loads					-- JSON response loading to requests
import re								# re.search						-- Regex searching
import os								# os.path.exists, os.makedirs	-- Path existence, directory creation
import time								# time.strftime					-- Formatted string of system time
from urllib import urlretrieve			# urlretrieve					-- Download from URL to local machine
from urllib2 import urlopen, HTTPError	# urlopen, HTTPError			-- Web page access, HTTP errors
import lxml.html						# lxml.html						-- HTML parsing
import imp 								# imp.load_source()				-- Load modules dynamically



# The user agent required by Reddit, which is used in requests.
user_agent = {'User-Agent': 'rud v0.3.3 by /u/manic0892 (github.com/Manic0892/rid)'}



# Small class to determine console coloration.  Only works on consoles that support ASCII colors.
class colors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


# Loads additional modules
modules = []

if os.path.exists('./modules/'):
	for i in os.listdir('./modules'):
		if not i.endswith('.py'):
			continue
		i = i.strip('.py')
		print(colors.HEADER + "Loading module: " + i + colors.ENDC)
		module = imp.load_source(i, './modules/' + i + '.py')
		modules.append(module)


# Downloads links from Imgur.
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
	# elif i['data']['domain'] == 'm.imgur.com':
	# 	imgurType = 1
	# 	imgurID = re.search('(?<=m.imgur.com/)[A-Za-z0-9]+', imgurURL).group(0)
	# 	imgurURL = 'i.imgur.com/' + imgurID + '.png'
	elif i['data']['domain'] == 'imgur.com' or i['data']['domain'] == 'm.imgur.com':
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


# For each user listed when the script was launched, this function is called to crawl through their /submitted page and collect links.
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
		if (len(data['data']['children']) == 0): # No more links to check
			break
		else:
			for i in data['data']['children']:
				# Checks each link to see if the domain is supported
				if i['data']['domain'] == 'i.imgur.com' or i['data']['domain'] == 'imgur.com' or i['data']['domain'] == 'm.imgur.com':
					imgur(i, user)
					continue

				supportedByModule = False

				for j in modules:
					if i['data']['domain'] == j.domain:
						j.process(i, user, colors)
						supportedByModule = True
						break

				if not supportedByModule:
					try:
						f = open('./downloads/'+user+'/__URLS.txt','a')
						f.write(i['data']['url'] + '\n') # python will convert \n to os.linesep
						f.close() # you can omit in most cases as the destructor will call if
						print (colors.WARNING + 'Skipping unsupported link.  Check __URLS.txt for a list of unsupported URLs not downloaded.' + colors.ENDC)
					except:
						print(colors.FAIL + 'An error occurred when trying to add this unsupported link to __URLS.txt.' + colors.ENDC)
					
			currURL = baseURL + '&after=' + data['data']['children'][-1]['data']['name']

# Creates the downloads folder if one does not exist.
if not os.path.exists('./downloads'):
	os.makedirs('./downloads')

# Calls getUsername for each username listed when the script was launched.
for i in sys.argv[1:]:
	getUsername(i)
