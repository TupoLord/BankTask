from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from models.model import User
from utils.dictionary import dct, alf
from database.db import BankManager


class BankNameRequest(BaseModel):
	bank_name: str = Field(default="")


class CustomNameRequest(BaseModel):
	bank_name_rus: str = Field(default="")
	custom_name_eng: str = Field(default="")


class SDK:
	def __init__(self, logger, db, current_user_callback):
		self.logger = logger
		self.db = db
		self.current_user = current_user_callback
		self.router = APIRouter()

		# Register routes with the router
		self.router.post("/api/v1/bank-name/translate")(self.get_bank)
		self.router.post("/api/v1/bank-name/add")(self.add_bank)

	def current_user_callback(self):
		return self.current_user_callback()

	async def get_bank(
			self,
			request: BankNameRequest,
			response: Response,
			user: User = Depends(current_user_callback)
	):
		self.logger.debug(
			f"Processing bank translation request: {request.bank_name} for user {user.id}"
		)
		try:
			rez = ""
			response.status_code = 404
			for j in request.bank_name:
				if j in alf:
					self.logger.warning(
						f"Invalid character '{j}' in bank name '{request.bank_name}'"
					)
					return Response(status_code=404)
			for i in request.bank_name:
				rez += dct.get(i, '')
			rez = rez.upper()
			name = request.bank_name.lower()
			bank_manager = BankManager(self.db)
			result = bank_manager.select_bank(rez, name, user.id)
			if result:
				self.logger.info(f"Bank found for user {user.id}: {result}")
				return JSONResponse(content={"result": result})
			else:
				self.logger.info(
					f"Bank not found for translated name '{rez}' and original name '{name}'"
				)
				return Response(status_code=404)
		except Exception as e:
			self.logger.error(f"Error in get_bank: {e}", exc_info=True)
			raise HTTPException(status_code=500, detail="Internal Server Error")

	async def add_bank(
			self,
			request: CustomNameRequest,
			user: User = Depends(current_user_callback)
	):
		self.logger.debug(
			f"Adding bank: {request.custom_name_eng} with name {request.bank_name_rus} for user {user.id}"
		)
		try:
			custom_name_eng = request.custom_name_eng.lower()
			bank_name_rus = request.bank_name_rus.lower()
			bank_manager = BankManager(self.db)
			bank_manager.add_custom_bank(custom_name_eng, bank_name_rus, user.id)
			self.logger.info(f"Bank '{custom_name_eng}' added for user {user.id}")
			return JSONResponse(content={"result": "Bank has been added!"})
		except Exception as e:
			self.logger.error(f"Error in add_bank: {e}", exc_info=True)
			raise HTTPException(status_code=500, detail="Internal Server Error")
