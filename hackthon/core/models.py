from django.db import models

import requests
import urllib

# Create your models here.
def get_all_pages(access_token):
	url = 'https://graph.facebook.com/v2.9/me/accounts?'
	values = {
		'access_token' : access_token,
	} 
	data = urllib.urlencode(values)
	result = requests.get(url, values).json()

	ret = [int(page[u'id']) for page in result[u'data']]
	print(ret)
	return ret

