# -*- coding: utf-8 -*
import re
import shutil
import urllib
import os.path


import requests
from bs4 import BeautifulSoup

image_base_uri = "https://apod.nasa.gov/apod/"
base_uri = "https://apod.nasa.gov/apod/archivepix.html"
download_folder = "scrapy_images/download/"
amount_downloaded = 0

# get image urls
r = requests.get(base_uri)
soup = BeautifulSoup(r.content, "html.parser")

gen_images = [link['href'] for link in soup.find_all("a", href=True) if re.match("^ap[0-9]+.html$", link['href'])]

for link in gen_images:
    # skip if already downloaded
    # if os.path.isfile(download_folder + link + ".jpg"):
    #     print "skipping ", link
    #     continue
    try:
        r = requests.get("https://apod.nasa.gov/apod/{}".format(link))
        soup = BeautifulSoup(r.content, "html.parser")
        image_name = soup.find_all("img")[0].find_previous("p").text.strip().split("\n")[0]
        img_sub_path = soup.find_all("img")[0]['src']
    except IndexError as err:
        print "Cant download %s : %s" % (link, err)
        continue
    except requests.exceptions.ConnectionError as conerr:
        print conerr
        continue

    urllib.urlretrieve(image_base_uri + img_sub_path, "download/" + image_name + ".jpg")
    amount_downloaded += 1


print "%s images downloaded" % amount_downloaded
print "Zipping download folder..."
shutil.make_archive("nasa_images", 'zip', "download")
