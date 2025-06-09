from setuptools import setup, find_packages

setup(
    name="unique_songs_spotify_helpers",
    
    version="0.1",

    url="https://github.com/TKothenbeutel/Unique-Spotify-Songs",

    author="Taylor Kothenbeutel",
    
    packages=['helpers'],
    
    python_requires=">=3.7, <4",
    
    install_requires=["python-dateutil","spotipy"],
)