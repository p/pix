#!/usr/bin/python

import sys, os, string

from Pic import Pic

class Album:

	def __init__(self, albumDir, recurse = 1):
		self.albumDir = albumDir

		self.albums = []
		self.pics   = []

		if (recurse):
			for entry in os.listdir(albumDir):
				if (entry[0] != '.'):
					pathAndEntry = '%s%s%s' % (albumDir, os.sep, entry)
					if os.path.isdir(pathAndEntry):
						self.albums.append(Album(pathAndEntry, 0))
					elif os.path.isfile(pathAndEntry):
						self.pics.append(Pic(pathAndEntry))


	def getAlbums(self):
		return self.albums


	def getNumPics(self):
		return len(self.pics)


	def getPics(self):
		try:
			metaFile = open('%s%s.meta' % (self.albumDir, os.sep))
		except:
			return self.pics

		copyOfPics = []
		copyOfPics = copyOfPics + self.pics

		displayPics = []
		for metaLine in metaFile:
			if string.find(metaLine, '=') != -1:
				splitMetaLine = string.split(metaLine, '=')
				currMetaImage = string.strip(splitMetaLine[0])
				for currPic in copyOfPics:
					if (currMetaImage == currPic.getFileName()):
						displayPics.append(currPic)
						copyOfPics.remove( currPic)

		# we got the ordered ones, now get the rest
		displayPics.extend(copyOfPics)
		return displayPics


	def getName(self):
		sepLoc = string.rfind(self.albumDir, os.sep) + 1
		return string.replace(self.albumDir[sepLoc:], '_', ' ')


	def getLinkPath(self):
		fullPath = self.albumDir
		loc = string.find(fullPath, os.sep) + 1
		return fullPath[loc:]


	def getBreadCrumb(self):
		linkPath = self.getLinkPath()
		breadCrumb   = ''
		runningCrumb = ''

		if linkPath != '':
			for crumb in string.split(linkPath, os.sep):
				runningCrumb = '%s%s%s' % (runningCrumb, os.sep, crumb)
				displayCrumb = string.replace(crumb, '_', ' ')
				breadCrumb = '%s | <a href="?album=%s">%s</a>' % (
					breadCrumb, 
					runningCrumb[1:],
					displayCrumb)

		return breadCrumb[3:]

	def getDescription(self):
		try:
			metaFile = open('%s%s.meta' % (self.albumDir, os.sep))
		except:
			return ''

		description = [] 
		startReading = 0
		for metaLine in metaFile:
			if string.find(metaLine, '<album description>') == 0:
				startReading = 1
			elif string.find(metaLine, '</album description>') == 0:
				startReading = 0 

			if startReading:
				description.append(metaLine)
		return string.join(description[1:])
