from mureq import get
from os import mkdir
class downloader:
	namedir = "Download"
	def picture(link, namedir=namedir):
		r = get(link)
		name = link.split("/")[-1]
		try: mkdir(namedir), open(f"{namedir}/picture-{name}", "wb").write(r.content)
		except FileExistsError: open(f"{namedir}/picture-{name}", "wb").write(r.content)
	def code(link, namedir=namedir):
		r = get(link)
		name = link.split("/")[-1]
		try: mkdir(namedir), open(f"{namedir}/code-{name}", "wb").write(r.content)
		except FileExistsError: open(f"{namedir}/code-{name}", "wb").write(r.content)
	def audio(link, namedir=namedir):
		r = get(link)
		name = link.split("/")[-1]
		try: mkdir(namedir), open(f"{namedir}/music-{name}", "wb").write(r.content)
		except FileExistsError: open(f"{namedir}/music-{name}", "wb").write(r.content)