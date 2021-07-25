import os

from webinfo import WebInfo

class DataProcessor:

	def __init__(self, path):
		if not os.path.exists(path):
			with open(path, "w") as _: pass
		self.path = path

	def load(self):
		web_infos = []
		with open(self.path, "r") as stream:
			while (True):
				raw_info = stream.readline().split(' ')
				if len(raw_info) == 2:
					web_infos.append(WebInfo(raw_info[0], raw_info[1][:-1]))
				elif len(raw_info) == 1:
					break
		return web_infos

	def save(self, web_infos):
		with open(self.path, "w") as stream:
			for web_info in web_infos:
				stream.write("{0} {1}\n".format(web_info.name, web_info.url))