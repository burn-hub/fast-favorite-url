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
