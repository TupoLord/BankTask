from config.config import Application_Config
from database.db import Database
from utils.logger import AppLogger


class BacisApp(object):
	def __init__(self):
		self.logger = AppLogger('bank_task').get_logger()
		self.conf = Application_Config()
		self.db = Database(self.conf)
