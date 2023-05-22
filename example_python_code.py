from bs4 import BeautifulSoup
import requests
import shutil
import time

url_base = "http://unstablegameswiki.com"

file_name = "cards_list29.txt"
with open(file_name, mode = "r") as file:
    cards_list = []
    while True:
        card = file.readline()
        if card == "":
            break
        cards_list.append(card.replace("\n",""))

##cards_list = ["Base Deck Rule Card"]

for index, card in enumerate(cards_list):
    url = url_base + "/index.php?title=UU_-_" + card.replace(" ","_")
    while True:
        req = requests.get(url)
        if req.status_code == 200:
            data = req.text
            break
        else:
            time.sleep(3)
##    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
    url_card = soup.find("a", {"title" : "Enlarge"}).get("href")

    first_split = url_card.split(".")
    second_split = first_split[-2].split("-")
    if second_split[-1] != "SE":
        second_split[-1] = "SE"
        first_split[-2] = "-".join(second_split)
        url_card = ".".join(first_split)

    url = url_base + url_card
    while True:
        req = requests.get(url)
        if req.status_code == 200:
            data = req.text
            break
        else:
            time.sleep(3)
##    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
    url_image = soup.find("a", text = "Original file").get("href")

    url = url_base + url_image
    while True:
        req = requests.get(url, stream = True)
        if req.status_code == 200:
            data = req
            break
        else:
            time.sleep(3)
##    data = requests.get(url, stream = True)
    data.raw.decode_content = True
    with open(str(index) + "_" + card.replace(" ","_") + "." + url_image.split(".")[-1], "wb") as image:
        shutil.copyfileobj(data.raw, image)
