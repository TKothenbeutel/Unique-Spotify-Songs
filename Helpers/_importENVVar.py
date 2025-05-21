import os

"""
https://developer.vonage.com/en/blog/python-environment-variables-a-primer
"""

def instantiate():
  os.environ['SPOTIPY_CLIENT_ID'] = '2bad936b5dec4ee286a3bed50cbb9a57'
  os.environ['SPOTIPY_CLIENT_SECRET'] = '56f4163387904965b66bf8130908e4fb'
  os.environ['SPOTIPY_REDIRECT_URI'] = 'https://127.0.0.1'