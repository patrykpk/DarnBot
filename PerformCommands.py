from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, HTTPError
from PIL import Image
import numpy as np
import io
import logging


def DiscordInput(Argument, Champ):
	if Argument in Commands:
		try:
			return Commands[Argument](Champ)
		except Exception as e:
			logging.warning(e.message, e.args)
	else:
		print ("No such command was found")

def FindChampionBuild(Champion):
	itemList = []
	source = Request("https://champion.gg/champion/{}".format(Champion.lower()), headers={'User-Agent': 'Mozilla/5.0'})
	with urlopen(source) as response:
		try:
			webpage = response.read()
		except HTTPError as e:
			logging.warning(e.response.text)

		soup = BeautifulSoup(webpage, 'lxml')
		coreBuild = soup.find(text="Core Final Build")

		buildItems = coreBuild.find_next("div").next_element
		for item in buildItems.findAll("div", recursive=False):
			itemList.append("{}".format(item.img["src"]))
	
	fullBuild = RetriveItemImage(itemList)
	return fullBuild


def RetriveItemImage(List):
	images = np.hstack([ Image.open(urlopen(ID)) for ID in List ])
	combinedImage = Image.fromarray(images)
	binaryStream = io.BytesIO()

	combinedImage.save(binaryStream, "png")
	binaryStream.seek(0)
	return binaryStream

Commands = {"build": FindChampionBuild}
