# Spotify's Unique Song Collector

Simple overview of use/purpose.
Parses through an accounts' extended streaming history and finds every unique song listened to in a given range. Spotipy is also utilized to add those results to a playlist.

## Description

An in-depth paragraph about your project and overview of use.
This Python progam parses through data files the user retrieves from Spotify, and collects any new songs listened to in a given time range. Once ran, the user interacts with the program through the terminal, and follows the instructions to get the desired results. This program currently only works with Spotify's extended streaming history, and not with the lesser account data package. The user can also alter the program with 10 different settings, allowing for different timeframes, changing what constitutes as a new song, and more! Afterwards, the user may save these results to a .json file such as how Spotify gives its stored data, or it can be uploaded to a playlist thanks to Spotipy and Spotify API.

## Using the Program

### Opening the Program

Due to environment variables storing secrets for this API, this program is made to run on Github's Codespace. Follow the instructions below if you are unsure how to access codespaces.

* On the main page of the repository, click the green box that says **Code**
* On the **Codespaces** tab, click the plus sign to create a space
* You will now be sent to a new tab that, after loading, appears to looks like the web version of VSCode

### Importing Files

The program must read your spotify data files for it to function properly. Follow these steps to import the files into this codespace

* Ensure the explorer tab is showing
* There are two ways to upload files to this space:
   * Drag your file/folder from your File Explorer onto the empty space
   * Right click on the empty space, and click upload to open your File Explorer for selection

### Running the Program

* Open Main.py
* Run the file. My go-to way of going about this is to click the play button at the upper-right corner of the editor
* The program runs in the terminal. Feel free to stretch it to view more of it at once. You can also click the up arrow at the right of the terminal to take up the code's space
* Follow the instructions displayed in the terminal


### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10
NO
### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders
DONE
### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```
DONE

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
