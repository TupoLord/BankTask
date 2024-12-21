from src.config.config import Application_Config
from src.database.db import Database
from src.utils.logger import AppLogger


class BasicApp(object):
	def __init__(self):
		self.logger = AppLogger('bank_task').get_logger()
		self.conf = Application_Config()
		self.db = Database(self.conf)
