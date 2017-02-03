# django_serialize #

Intended for django versions 1.8 and above.  Tested with django 1.8 and django 1.9.

# Testing

- activate virtual env - `$ source <virtual_envs>/django_serialize/bin/activate`
- `$ cd <repositories>/django_serialize`
- `$ python testproject/manage.py test -s testproject`

## To test with multiple versions of django

- change django version in `<repositories>/django_serialize/reqs.txt`
- `$ pip install -r reqs.txt`
- `$ python testproject/manage.py test -s testproject`


## First time

- activate virtual env - `$ source <virtual_envs>/django_serialize/bin/activate`
- `$ cd <repositories>/django_serialize`
- `$ pip install -r reqs.txt`

# Deploy

`$ python setup.py sdist upload -r pypi` - from [here](http://peterdowns.com/posts/first-time-with-pypi.html)

# Install Specific Version

`$ pip install --upgrade "django_serialize==<ver#>" --no-cache-dir`
