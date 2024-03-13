chess.py
==============================

Classic chess in Python (using pygame).
It isn't 100% complete, but it's pretty much playable.
By default, the board is always viewed as the white player and the two
players play from the same PC, both having a 5 minute timer which starts
after the first move is played.  
There are a few options that can be changed; unfortunately it's currently not possible to edit those settings directly in the running program, but only by enabling them directly in the code.


When making this project I wanted to include an online mode (which is available in the chess.py-online repository, built on a way less "fancy" and outdated game version) and a vs-computer mode.
I then realized that if I wanted to make the project that big, then i should've probably switched to a compiled programming language.
Python and Pygame are fun to play with, but performance-wise, I probably need something more. That's because this repository is unlikely to receive any updates (in this repository, at least)