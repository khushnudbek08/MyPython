#! python3
# mcb.pyw - Saves and Loads pieces of text to the clipboard
# Usage: py.exe  mcb.pyw save <keyword> - saves clipboard to keyword
#        py.exe mcb.pyw <keyword> - Loads keyword to clipboard
#       py.exe mcb.pyw list - loads all keywords to clipboard

import shelve, pyperclip, sys

mcbShelf = shelve.open("mcb")

# Save clipboard content
if len(sys.argv) == 3 and sys.argv[1].lower() == "save":
    mcbShelf[sys.argv[2]] = pyperclip.paste()
elif len(sys.argv) == 3 and sys.argv[1].lower() == 'delet':
    del mcbShelf[sys.argv[2]] 
    
elif len(sys.argv) == 2:
    # list keywords and load content
    if sys.argv[1].lower() == "list":
        pyperclip.copy(str(list(mcbShelf.keys())))
    elif sys.argv[1].lower() == 'deletall':
        mcbShelf.clear()
    elif sys.argv[1] in mcbShelf:
        pyperclip.copy(mcbShelf[sys.argv[1]])
mcbShelf.close()
