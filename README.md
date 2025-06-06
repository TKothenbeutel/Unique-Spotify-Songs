[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/TKothenbeutel/Unique-Spotify-Songs?quickstart=1)

# Unique Song Collector for Spotify

Parses through an account's extended streaming history and finds every unique song listened to in a given range. Spotipy is also utilized to add those results to a Spotify playlist.

## Description

This Python program parses through data files the user retrieves from Spotify, and collects any new and unique songs listened to in a given time range. Once run, the user interacts with the program through the terminal and follows the instructions to get desired results. How the program work is by creating two containers: one for the songs in the desired time range, and one that will it be comparing against. The program will look at the count of each song, combine the differing URIs for a song, and more. The user can also alter the program with 10 different settings, allowing for different timeframes or changing what constitutes as a new song, just to name a few. Afterwards, the user may save these results to a JSON file, such as how Spotify gives its stored data, or upload the collection to a playlist thanks to Spotipy and the Spotify API.

## Requirements

The program requires the user to supply files from their <ins>Extended Streaming History</ins> folder received from Spotify. This program is not designed for the lesser streaming history data, as obtained from choosing "Account Data" when downloading a user's Spotify data. The user also needs an accessible Spotify account if they would like to add results to a playlist.

## Using the Program

### Opening the Program

Due to environment variables storing secrets for this API, this program is made to run on GitHub's Codespace. To open up a Codespace, click the button above labeled **Open in GitHub Codespaces**.

You may also open the Codespace in VS Code Desktop:

1. Click on the hamburger menu on the left side of the Codespace
2. Click **Open in VS Code Desktop**
3. Click **Open** when prompted to let the 'GitHub Codespaces' extension open this project's URI

### Importing Files

The program must read your Spotify data files for it to function properly. Follow these steps to import the files into this codespace:

1. Ensure the Explorer tab is showing
2. Perform either of these actions:
   - Drag your file/folder from your File Explorer onto the explorer tab empty space
   - Right click on the empty space in the Explorer tab, and click upload to open your File Explorer for selection

### Running the Program

1. Open Main.py
2. Run the file. My go-to way of going about this is to click the play button at the upper-right corner of the editor
3. The program runs in the terminal. Feel free to stretch it to view more of it at once. You can also click the up arrow to the right of the terminal to take up the code's space
4. Follow the instructions displayed in the terminal

If you have a result file after running the program, you may download that file by right-clicking it in the Explorer tab and clicking "Download...". Any file uploaded or created will be saved on the Codespace as long as you do not delete the space.

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

##### &#9679; When right-clicking in the explorer menu, the only option that appears is **Paste**, and not the full menu that gives the ability to copy a file path or upload files.
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
  * Private Public Release

## License

This project is licensed under the MIT License — see the LICENSE.md file for details

## Acknowledgments

* [README Template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
