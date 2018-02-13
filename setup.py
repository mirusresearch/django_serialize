from setuptools import setup, find_packages

setup(
    name='django_serialize',
    version='1.3.2',
    description='Serialization utilities for django models',
    author='Mirus Research',
    author_email='frank@mirusresearch.com',
    packages=find_packages(),
    url='https://github.com/mirusresearch/django_serialize',
    license='MIT, see LICENSE',
    install_requires=[
        'packaging>=16.8',
        'six>=1.11.0',
    ],
    py_modules=['django_serialize'],
    # python_requires='>=2.7, <4',
)
