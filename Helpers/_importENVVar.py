import os

"""
https://developer.vonage.com/en/blog/python-environment-variables-a-primer
"""

def instantiate():
  os.environ['SPOTIPY_CLIENT_ID'] = '***REMOVED***'
  os.environ['SPOTIPY_CLIENT_SECRET'] = '***REMOVED***'
  os.environ['SPOTIPY_REDIRECT_URI'] = '***REMOVED***'