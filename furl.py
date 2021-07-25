import os

from localizator import Localizator
from dataprocessor import DataProcessor
from app import App

CURRENT_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(CURRENT_DIR_PATH, "fast_web_db.txt")
LOCALIZE_PATH = os.path.join(CURRENT_DIR_PATH, "fast_web_localize.txt")


if __name__ == '__main__':
	app = App(DataProcessor(DATA_PATH), Localizator(LOCALIZE_PATH))
	app.run()
