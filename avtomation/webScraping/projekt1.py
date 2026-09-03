#! python3
# project1.py - in this file we will erite code of program which helps us to find the web adresses and open on brauser

import sys, requests, webbrowser, bs4

print("Googling...")  # display the text while downloading the google page
res = requests.get("https://google.com/search?q=" + "".join(sys.argv[1:]))
res.raise_for_status()

# retrive top search resalts links.
soup = bs4.BeautifulSoup(res.text, "html.parser")

# Open browser tab for each resalt.
linkEmails = soup.select(".r a")
numOpen = min(5, len(linkEmails))
for i in range(numOpen):
    webbrowser.open("http://google.com" + linkEmails[i].get("hreaf"))
