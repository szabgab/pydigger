Building an alternative view of the open source applications written in Python

HOW TO RUN - collecting data
-----------------------------
./bin/pydigger

This will fetch the RSS feed from PyPi, create a subdirectory called www, and download the zip files of the
most recently uploaded packages.

Once the zip file is downloaded it is unzipped.

web site
---------
./bin/app.py


OLDER
=========


PREREQUISITES
----------------
export PYTHONPATH=~/python
easy_install -d ~/python Genshi


HOW TO RUN
-----------
Create a JSON file in the conf/ directory similar to the already exising ones
and run
$ python bin/parse.py conf/yourfile.json




SOME PLANNING
---------------
- Have a json file describe the source that needs to be analyzed
  Where to download the files, how to update them
  (e.g. a packaged file having a new version or a git or SVN repository)

- process and analyze the files and create a static display with a few static
  json files with meta-data

DESCRIPTION
---------------
*) Syntax highlight the python files
*) Each project has its own directory
*) Each projects has a main page listing all the files in it
*) The main page has a listing of all the projects (for now) with links to the main page of each project
*) Parse other, non-python files as well and show them in some nice way
*) Allow listing directories that need to be excluded from the display
*) Has simple about page
*) Basic logging in the parser
*) Navigation link from each file back to the project page
*) Timeout for processing files

COMMENTS
----------
In order to find out which token has which token number the mapping can
be found here: /usr/lib/python2.7/token.py
Apparently if I type pydoc  tokenize on the command line, I get the list

TODO
-------
*) Change the page names so they will have the same name as the original file, but still serve correctly
*) Guessing the lexer better
*) Each directory in the project tree has an index file listing all the files and subdirectories in it
*) Create a configuration file to process several projects, including the source code of Python itself.
*) List the dependencies and link to the relevant project pages
*) Show the documentation of each file/project as a separate HTML page
*) Handle the file we cannot parse and highlight (e.g. .png files)
