from fastapi import FastAPI, Response, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, Field
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from utils.dictionary import dct, alf
from database.db import BankManager, Database
from utils.response import check_banks
from utils.logger import app_logger
from middlewares.logging import log_requests


class BankNameRequest(BaseModel):
    bank_name: str = Field(default="")


class CustomNameRequest(BaseModel):
    bank_name_rus: str = Field(default="")
    custom_name_eng: str = Field(default="")


app = FastAPI()

check_banks()
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()
db = Database()
@app.post("/api/v1/bank-name/translate", response_class=JSONResponse)
@log_requests
async def get_bank(
    request: BankNameRequest, response: Response, user: User = Depends(current_user)
):
    app_logger.debug(
        f"Обработка запроса перевода банка: {request.bank_name} для пользователя {user.id}"
    )
    try:
        rez = ""
        response.status_code = 404
        for j in request.bank_name:
            if j in alf:
                app_logger.warning(
                    f"Недопустимый символ '{j}' в названии банка '{request.bank_name}'"
                )
                return response.status_code
        for i in request.bank_name:
            rez += dct.get(i, '')
        rez = rez.upper()
        name = request.bank_name.lower()
        bank_manager = BankManager(db)
        result = bank_manager.select_bank(rez, name, user.id)
        if len(result) > 0:
            app_logger.info(f"Найден банк для пользователя {user.id}: {result}")
            return JSONResponse(content={"result": result})
        else:
            app_logger.info(
                f"Банк не найден для переведенного названия '{rez}' и оригинального названия '{name}'"
            )
            return response.status_code
    except Exception as e:
        app_logger.error(f"Ошибка в get_bank: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/api/v1/bank-name/add", response_class=JSONResponse)
async def add_bank(request: CustomNameRequest, user: User = Depends(current_user)):
    app_logger.debug(
        f"Добавление банка: {request.custom_name_eng} с названием {request.bank_name_rus} для пользователя {user.id}"
    )
    try:
        custom_name_eng = request.custom_name_eng.lower()
        bank_name_rus = request.bank_name_rus.lower()
        bank_manager = BankManager(db)
        bank_manager.add_custom_bank(custom_name_eng, bank_name_rus, user.id)
        app_logger.info(f"Банк '{custom_name_eng}' добавлен для пользователя {user.id}")
        return JSONResponse(content={"result": "Банк был добавлен!"})
    except Exception as e:
        app_logger.error(f"Ошибка в add_bank: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
