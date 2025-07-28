[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/TKothenbeutel/Unique-Spotify-Songs?quickstart=1)

# Unique Song Collector for Spotify

Parses through an account's extended streaming history and finds every unique song listened to in a given range. Spotipy is also utilized to add those results to a Spotify playlist.

## Description

This Python program parses data files retrieved from Spotify by the user and collects any new and unique songs listened to within a given time range. Once run, the user interacts with the program through the terminal and follows the instructions to get the desired results. How the program work is by creating two containers: one for the songs in the desired time range, and one that will it be comparing against. The program will look at the count of each song, combine the differing URIs for a song, and more. The user can also alter the program with 10 different settings, allowing for different timeframes or changing what constitutes as a new song, just to name a few. Afterwards, the user may save these results to a JSON file, such as how Spotify gives its stored data, or upload the collection to a playlist thanks to Spotipy and the Spotify API.

## Requirements

The program requires the user to supply files from their <ins>Extended Streaming History</ins> folder received from Spotify. This program is not designed for the lesser streaming history data, as obtained from choosing "Account Data" when downloading a user's Spotify data. The user also needs an accessible Spotify account if they would like to add results to a playlist.

## Using the Program

1. The program is well-suited for GitHub Codespaces. To open one, click the link at the top of this README labeled **Open in GitHub Codespaces**
2. Before running the program, open the file named **Environment_Variables.py**. Enter your Spotify API's client ID, client Secret, and redirect URI. If you do not have one but would like to use this program, then please check out my working demo on [my portfolio](https://tkothenbeutel.github.io/Portfolio/spotify)
3. Run Main.py and follow the instructions printed in the terminal

## Settings

* **Beginning Date**: The date that a song must be first listened to for it to be possible to be added to the collection. Please follow yyyy-mm-dd format. Default is one year from today.
* **Min Count**: Remove songs that have been listened to fewer times than this number. Default is 2.
* **Min MS**: Minimum number of milliseconds (1,000ms = 1 second) the song needs to be listened to in one sitting for it to count in this data. Note: track fully finishing will override this setting. Default is 30,000.
* **Song Preference**: If a song has multiple IDs (usually from it being on different albums), have it keep the oldest, newest, both copies, or ask which of the IDs to keep every time. Default is ask.
* **Min Count Override**: If a song has been listened to this many more times in the collection range than out of it, then it will be included in the collection. If this number is -1, it will not do this. Default is -1.
* **Earliest Date**: The earliest date this program will parse through in the given data. Please follow yyyy-mm-dd format. Default is 2000-01-01.
* **Last Date**: The last date this program will parse through in the given data. Please follow yyyy-mm-dd format. Default is tomorrow's date.
* **Playlist Add Timer**: Amount of time (in seconds) to wait in between adding each song to the given playlist so that the 'sort by date added' feature will work properly on Spotify. Default is 0.
* **Song Grace Period**: Period at which a song has a chance to be included in the playlist, regardless if it reaches **minCount** (will still be rejected if it was listened to before earlyRange). The range starts from the given day through today. Please follow yyyy-mm-dd format. Default is a week from today.
* **Universal Min Count**: Determines if songs before **beginningDate** should also meet the minimum count requirement to be looked at. Default is False.

## Issues

##### &#9679; When right-clicking in the explorer menu in a Codespace, the only option that appears is **Paste**, and not the full menu that gives the ability to copy a file path or upload files.
  * To fix this, right-click the desired file so that **Paste** appears
  * Right click again on the **Paste** box. The full menu should now appear
    - Note: The paste option takes a second before becoming a usable option. Wait for the paste option to be clickable before you right-click or use it
##### &#9679; The program opens a page that cannot be connected to.
  * This is the normal behavior of the API that this program uses
  * Once the webpage is done loading, you will need to copy and paste the link into the terminal to continue. After that, feel free to close that tab
  * If you are using the same login as done previously, this verification process should not appear

## Authors

Taylor Kothenbeutel

## Version History

* 0.1
  * Initial Release

## License

This project is licensed under the MIT License — see the LICENSE.md file for details

## Acknowledgments

* [README Template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
