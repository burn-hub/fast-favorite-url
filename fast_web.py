import webbrowser

DATA_PATH = "/home/burn/MyUtilities/FastWeb/fast_web_db.txt"
LOCALIZE_PATH = "/home/burn/MyUtilities/FastWeb/fast_web_localize.txt"

class WebInfo:

	def __init__(self, name, url):
		self.name = name
		self.url = url

	def __str__(self):
		return "{0}: {1}".format(self.name, self.url)

class DataProcessor:

	def __init__(self, path):
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

class Localizator:

	def __init__(self, path):
		self.messages = {}
		with open(path, "r") as stream:
			while (True):
				raw_info = stream.readline().split('\t')
				if len(raw_info) == 2:
					self.messages[raw_info[0]] = raw_info[1][:-1]
				elif len(raw_info) == 1:
					break
		
		self.init_consts()

	def init_consts(self):
		self.unknown_command = self.messages["unknown_command"]
		self.add_command_info = self.messages["add_command_info"]
		self.remove_command_info = self.messages["remove_command_info"]
		self.get_command_info = self.messages["get_command_info"]
		self.exit_command_info = self.messages["exit_command_info"]
		self.open_command_info = self.messages["open_command_info"]
		self.help_command_info = self.messages["help_command_info"]
		self.wrong_count_arguments = self.messages["wrong_count_arguments"]
		self.url_list = self.messages["url_list"]
		self.help_list = self.messages["help_list"]
		self.not_found_web_info = self.messages["not_found_web_info"]
		self.index_out_of_range = self.messages["index_out_of_range"]

class App:

	def __init__(self):
		self.localizator = Localizator(LOCALIZE_PATH)
		self.data_processor = DataProcessor(DATA_PATH)
		self.web_infos = self.data_processor.load()
		self.init_actions()

	def init_actions(self):
		self.actions = {
			"get": self.print_web_infos,
			"add": self.add_web_info,
			"remove": self.remove_web_info,
			"open": self.open_url,
			"exit": self.exit_app,
			"help": self.print_help
		}

	def run(self):
		command = ["get"]
		while (command[0] != "exit"):
			try:
				self.actions[command[0]](command[1:])
			except KeyError:
				print(self.localizator.unknown_command)
				self.print_help()
			command = input().split(' ')

		self.data_processor.save(self.web_infos)

	def print_web_infos(self, params=None):
		print("---URL List---")
		for i, web_info in enumerate(self.web_infos):
			print(f"{i + 1})", web_info)

	def add_web_info(self, params):
		if len(params) != 2:
			print(self.localizator.wrong_count_arguments)
			print(self.localizator.add_command_info)
			return

		self.web_infos.append(WebInfo(params[0], params[1]))
		self.print_web_infos()

	def remove_web_info(self, params):
		if len(params) != 1:
			print(self.localizator.wrong_count_arguments)
			print(self.localizator.remove_command_info)
			return
		
		if params[0].isnumeric():
			index = int(params[0]) - 1
		else:
			index, web_info = self.find_web_info(params[0])
			if web_info is None:
				print(self.localizator.not_found_web_info)
				return

		self.web_infos = self.web_infos[:index] + self.web_infos[index + 1:]
		self.print_web_infos()

	def open_url(self, params):
		if len(params) != 1:
			print(self.localizator.wrong_count_arguments)
			print(self.localizator.open_command_info)
			return

		if params[0].isnumeric():
			index = int(params[0]) - 1
			if index in range(0, len(self.web_infos)):
				webbrowser.open(self.web_infos[index].url)
			else:
				print(self.localizator.index_out_of_range)
			return

		index, web_info = self.find_web_info(params[0])
		if web_info is None:
			print(self.localizator.not_found_web_info)
		
		webbrowser.open(web_info.url)

	def print_help(self, params=None):
		print(self.localizator.help_list)
		print(self.localizator.get_command_info)
		print(self.localizator.add_command_info)
		print(self.localizator.remove_command_info)
		print(self.localizator.exit_command_info)
		print(self.localizator.open_command_info)
		print(self.localizator.help_command_info)

	def exit_app(self, params):
		pass

	def find_web_info(self, name):
		for i, web_info in enumerate(self.web_infos):
			if web_info.name == name:
				return i, web_info
		return -1, None

if __name__ == '__main__':
	app = App()
	app.run()
