#!/usr/bin/python

import requests
import sys
import json

user_agent = {'User-Agent': 'rid v0.1 by /u/manic0892 (github.com/Manic0892/rid)'}
app_id = '31447b3acafcc65'

def getUsername(user):
	baseURL = 'http://www.reddit.com/user/' + user + '/submitted.json?limit=100'
	currURL = baseURL

	while True:
		r = requests.get(currURL, headers=user_agent)
		data= r.text
		data = json.loads(data)
		if (len(data['data']['children']) == 0):
			break
		else:
			for i in data['data']['children']:
				if i['data']['domain'] == 'i.imgur.com':
					print i['data']['title']
				elif i['data']['domain'] == 'imgur.com':
			currURL = baseURL + '&after=' + data['data']['children'][-1]['data']['name']

for i in sys.argv[1:]:
	getUsername(i)