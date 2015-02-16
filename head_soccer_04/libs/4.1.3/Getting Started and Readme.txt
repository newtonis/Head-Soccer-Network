Mastermind v.4.1.3
by Ian Mallett
Released June 2013

About:

	Mastermind is a library designed to take most of the guesswork out of network programming.  Essentially, it tries to handle as much as possible for you.  As such, it is very easy to get complete, fast, networked applications up and running.  Conversely, if you want to do deep-level networking, this is not your library.
	
	Mastermind is based on the client-server model because it is easiest to understand.  See Notes.txt.
	
	For licensing, see Notes.txt.
	
	The current version of Mastermind (unless I forgot to update it) is the version at the top of this file.  There have been at least one complete rewrites.

Files:

	examples/*:
		Examples of usage of Mastermind
	Documentation.txt:
		Complete documentation on Mastermind
	Notes.txt:
		Notes on how Mastermind works, tips, possible pitfalls, implementation notes
	Readme.txt:
		This file; getting started with Mastermind
	TODO.txt:
		Lists possible improvements and all known bugs with Mastermind

Getting Started:

	My recommendation is to reverse engineer the examples in the "examples" directory.
	
	The example "examples/basic test.py" sets up an echo server and then creates a client to send messages to it.
	
	The example "examples/chat/chat.py" tries to connect to a chat server.  If one is not available, it creates one and connects to that.  Running multiple instances of "chat.py" allows for multiple chat windows linked to the first's server.  If the first is closed, the others close automatically.  This example serves as a more advanced demonstration of a more complete application.

Credits:

	--Me, Ian Mallett (ian@geometrian.com) for writing all versions of this library, and being responsible for all aspects of development
	--Matthew Roe (RB[0], roebros@gmail.com) for giving me inspriration for this project, and for a lot of my code (particularly his pickle/unpickle code idea), a quit code tweak, and for help with select.select() in lag-reduction techniques
	--Paul Davey (plmdvy@gmail.com) for helping with subclassing, select.select(), and various other things
	--"PyMike" (pymike93@gmail.com) for the use of his testing facilities, server hosting, advice and tweaks, and idea to make UDP capabilities.
	--Robin Wellner (gyvox) for a tweak on the pickle/unpickle error checking
	--Various others for their encouragement, support, and testing help