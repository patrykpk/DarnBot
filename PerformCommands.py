from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, urlretrieve

import numpy as np
from PIL import Image
import os

def DiscordInput(Argument, Champ):
	if Argument in Commands:
		try:
			Commands[Argument](Champ)
		except Exception as e:
			print (e.message, e.args)
	else:
		print ("No such command was found")

def FindChampionBuild(Champion):
	ItemList = []
	source = Request("https://champion.gg/champion/{}".format(Champion.lower()), headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(source).read()
	soup = BeautifulSoup(webpage, 'lxml')
	FindTag = soup.find(class_="champion-stats", text="Most Frequent Completed Build")

	a = FindTag.next_sibling.next_sibling
	for ItemSlot in a.find_all("a"):
		ItemList.append("http:{}".format(ItemSlot.img['src']))
	RetriveItemImage(ItemList)

def RetriveItemImage(List):
	path = "./BuildItems/"
	for WebAddress in List:
		urlretrieve(WebAddress, "./BuildItems/{}".format(WebAddress.split("/")[-1]))

	Images = np.hstack([ Image.open(path + ID) for ID in os.listdir("./BuildItems/") ])
	CombinedImage = Image.fromarray(Images)
	CombinedImage.save(path + "FullBuild.png")

def DeleteImages():
	path = "./BuildItems/"
	for filename in os.listdir(path):
		file_path = os.path.join(path, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print ("Something went wrong. Couldn't delete %s due to %s" % (file_path, e))

Commands = {"build": FindChampionBuild}