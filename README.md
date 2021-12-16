## FinalProject

A final project for EPSY 5122

Codes a card memory game using tkinter (MemoryGame.py) and allows for some simple analyses of data created by users playing the game (Analyze.py)

Analyze.py calls the log files from the "Logs_ToUse" folder, so be sure that you move the logs you create to that folder if you want to include them in the analyses

Future updates could include:
* More difficult levels (I attempted not to hard code the number of cards, so that shouldn't be too difficult)
* Instructions if people haven't played the game before
* Add more feedback to player (ex. checkmarks when the match is correct)
* An alternative version could have the incorrect matches automatically flip back over after a prescribed amount of time - this is currently done manually by the player choosing the next card. This allows the player unlimited time to analyze the current two cards flipped if they wanted.
* More detailed "errors" - current analyses only define an error as a card having been flipped more than twice
* More detailed analyses in general - correlations between measures, difficulty of specific images or positions, etc...
