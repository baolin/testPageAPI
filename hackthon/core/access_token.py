def save_access_token(backend, user, response, *args, **kwargs):
    setattr(user, 'as', response['access_token'])
    f = open('/tmp/access_token', 'w')
    f.write(response['access_token'])
    f.close()
    if backend.name == 'facebook':
	return
