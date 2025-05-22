# Spotify's Unique Song Collector

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/TKothenbeutel/Unique-Spotify-Songs?quickstart=1)

Simple overview of use/purpose.
Parses through an accounts' extended streaming history and finds every unique song listened to in a given range. Spotipy is also utilized to add those results to a playlist.

## Description

An in-depth paragraph about your project and overview of use.
This Python progam parses through data files the user retrieves from Spotify, and collects any new songs listened to in a given time range. Once ran, the user interacts with the program through the terminal, and follows the instructions to get the desired results. This program currently only works with Spotify's extended streaming history, and not with the lesser account data package. The user can also alter the program with 10 different settings, allowing for different timeframes, changing what constitutes as a new song, and more! Afterwards, the user may save these results to a .json file such as how Spotify gives its stored data, or it can be uploaded to a playlist thanks to Spotipy and Spotify API.

## Using the Program

### Opening the Program

Due to environment variables storing secrets for this API, this program is made to run on GitHub's Codespace. To open up a Codespace, click the button labeled **Open in GitHub Codespaces**.

### Importing Files

The program must read your spotify data files for it to function properly. Follow these steps to import the files into this codespace

* Ensure the explorer tab is showing
* There are two ways to upload files to this space:
   * Drag your file/folder from your File Explorer onto the explorer tab empty space
   * Right click on the empty space in the expolorer tab, and click upload to open your File Explorer for selection

### Running the Program

* Open Main.py
* Run the file. My go-to way of going about this is to click the play button at the upper-right corner of the editor
* The program runs in the terminal. Feel free to stretch it to view more of it at once. You can also click the up arrow at the right of the terminal to take up the code's space
* Follow the instructions displayed in the terminal


## Issues

##### &#9679; When right-clicking in the explorer menu, the only option that appears is **Paste**, and not the full menu that gives the ability to copy a file path or upload files
  * To fix this, right click the desired file so that **Paste** appears
  * Right click again on either the **Paste** box or further right of it. The full menu should now appear
  * Side note: The paste option takes a second before becoming a usable option. Wait for the paste option to be clickable before right clicking it or pasting in general
##### &#9679; The program opens a page that cannot be connected to.
  * This is normal behavior of the API this program uses
  * Once the webpage is done loading, you will need to copy and paste the link into the terminal to continue. After that, feel free to close that tab
  * If you are using a same login as done previously, this verification process should not appear

## Authors

Taylor Kothenbeutel

## Version History

* 0.1
  * Initial release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

* [README Template](https://gist.github.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc)
