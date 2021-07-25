import webbrowser

from webinfo import WebInfo

class App:

	def __init__(self, data_processor, localizator):
		self.localizator = localizator
		self.data_processor = data_processor
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