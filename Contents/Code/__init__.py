import os

### PhantomManga for Plex
### Copyright (c) Joshua Ozeri 2017
NAME = "PhantomManga"
PREFIX = "/photos/phantommanga"
### PhantomManga is a Plex channel meant to be ran alongside the PhantomManga for Windows application.
### PhantomManga for Plex simply acts as a reader for the mangas downloaded with the Windows application.

def Start():
	ObjectContainer.title1 = NAME

@handler(PREFIX, NAME, art=R("art-default.png"), thumb=R("icon-default.png"))
def MainMenu():
	oc = ObjectContainer()
	root = Prefs["install_path"] + "data\\"
	mangas = os.listdir(root)
	for manga in mangas:
		if os.path.isdir(root + manga):
			oc.add(DirectoryObject(key=Callback(MangaMenu, manga=manga), title=Core.storage.load(root + manga + "\\detail.txt"), summary=Core.storage.load(root + manga + "\\desc.txt"), thumb=(Prefs["install_url"] + "/data/" + manga + "/banner.jpg")))
	return oc

@route(PREFIX + "/mangamenu")
def MangaMenu(manga):
	root = Prefs["install_path"] + "data\\"
	chapters = os.listdir(root + manga + "\\manga\\")
	oc = ObjectContainer()
	oc.title1 = Core.storage.load(root + manga + "\\detail.txt")
	for chapter in chapters:
		if os.path.isdir(root + manga + "\\manga\\" + chapter):
			url = (Prefs["install_url"] + "/data/" + manga + "/manga/" + chapter)
			oc.add(PhotoAlbumObject(
				key=Callback(GetPhotoAlbum, url=(root + manga + "\\manga\\" + chapter), title=("Chapter " + chapter)),
				rating_key=url,
				title=("Chapter " + chapter),
				source_title=Core.storage.load(root + manga + "\\detail.txt"),
				tagline=None,
				originally_available_at=None,
				thumb=(url + "\\001.jpg"),
				art=R("art-default.png")))
	return oc

# GetPhotoAlbum
#   Create and return the contents of a photo album.
@route(PREFIX + "/get/album")
def GetPhotoAlbum(url, title):
	# setup objectcontainer
	oc = ObjectContainer()
	oc.title2 = title
	# setup vars
	pages = os.listdir(url)
	# loop pages
	for page in pages:
		# create new photo object for each page
		oc.add(CreatePhotoObject(
			title=("Page " + page.replace(".jpg", "")),
			url=Callback(GetPhoto, url=(url.replace(Prefs["install_path"], Prefs["install_url"] + "/")) + "/" + page)))
	# ret oc
	return oc
# CreatePhotoObject
#   Initialize and return a photo object.
@route(PREFIX + "/createphotoobject")
def CreatePhotoObject(title, url, include_container=False, *args, **kwargs):
	po = PhotoObject(
		key = Callback(CreatePhotoObject, title=title, url=url, include_container=True),
		rating_key = url,
		#source_title = "Reader",
		title = title,
		thumb = url,
		art = R("art-default.png"),
		items = [MediaObject(parts = [PartObject(key=url)])]
	)
	if include_container:
		return ObjectContainer(objects=[po])
	return po
# GetPhoto
#   ----
@route(PREFIX + "/get/photo")
def GetPhoto(url):
	return Redirect(url)