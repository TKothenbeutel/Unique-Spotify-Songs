# Enter your Spotify App information in the variables below:
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = ""




# The section below turns the variables above into environmental variables
# for the other files to reach.
from os import environ

def innit() -> int:
    if(SPOTIPY_CLIENT_ID == '' or SPOTIPY_CLIENT_SECRET == '' or SPOTIPY_REDIRECT_URI == ''):
        print("Please input your Spotify App's information in the corresponding variables located in the\nfile called 'Environmental_Variables.py'.\n")
        return 1
    else:
        environ['SPOTIPY_CLIENT_ID'] = SPOTIPY_CLIENT_ID
        environ['SPOTIPY_CLIENT_SECRET'] = SPOTIPY_CLIENT_SECRET
        environ['SPOTIPY_REDIRECT_URI'] = SPOTIPY_REDIRECT_URI
    return 0