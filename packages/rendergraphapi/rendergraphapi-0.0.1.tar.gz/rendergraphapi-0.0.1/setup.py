import logging
import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='rendergraphapi',
    version='0.0.1',
    description='Render.com Graph API',
    url='https://github.com/idealoop/rendergraphapi',
    author='idealoop',
    author_email='noreply@idea-loop.com',
    license='MIT',
    packages=find_packages(exclude=["tests.*", "tests", "test*"]),
    long_description=README,
    long_description_content_type='text/markdown',
    package_data={'': ['*.html']},
    include_package_data=True,
    install_requires=[
        'pydantic',
        'requests',
        'authenticator',
    ],
    zip_safe=False
)
