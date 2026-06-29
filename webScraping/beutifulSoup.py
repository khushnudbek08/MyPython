import requests
from bs4 import BeautifulSoup

url = "https://jisho.org/search/日%20%23kanji"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

# Kanji
kanji = soup.find("h1", class_="character").text

# Meaning
meaning = soup.find("div", class_="kanji-details__main-meanings").text.strip()

# Onyomi
onyomi = [a.text for a in soup.select(".onyomi a")]

# Kunyomi
kunyomi = [a.text for a in soup.select(".kunyomi a")]

print("Kanji:", kanji)
print("Meaning:", meaning)
print("Onyomi:", onyomi)
print("Kunyomi:", kunyomi)