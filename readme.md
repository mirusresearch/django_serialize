# django_serialize #

Intended for django versions 1.8 and above.  

2/12/18 - Version 1.3.1 - Tested with Python 2.7 and 3.6 - django versions 1.8, 1.9, 1.10, 1.11

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

- `$ python3 setup.py bdist_wheel`
- `$ twine upload dist/*`

from [here](https://packaging.python.org/tutorials/distributing-packages/)

# Install Specific Version

`$ pip install --upgrade "django_serialize==<ver#>" --no-cache-dir`
