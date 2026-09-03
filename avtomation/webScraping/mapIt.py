#! python3
# mapIt.py - Launchs a map in the browser using an address from the command line or clipboard

import webbrowser, sys, pyperclip

if len(sys.argv) > 1:
    # get addres from comand line
    address = ' '.join(sys.argv[1:])
else:
    # get address from clipboard
    address = pyperclip.paste()

webbrowser.open('https://www.google.com/maps/place/' + address)
