from fastapi import Response, Depends, HTTPException
from fastapi.responses import JSONResponse
from auth.auth import auth_backend
from auth.database import User
from auth.schemas import UserRead, UserCreate
from m import App, BankNameRequest, CustomNameRequest
from utils.dictionary import dct, alf
from database.db import BankManager
from utils.logger import app_logger


if __name__ == "__main__":
    app = App()

    routers = (
        app.fastapi_users.get_register_router(UserRead, UserCreate),
        "/auth/jwt",
        ["auth"],
    ), (
        app.fastapi_users.get_auth_router(auth_backend),
        "/auth",
        ["auth"],
    )


    @app.middlewares.post("/api/v1/bank-name/translate", response_class=JSONResponse)
    async def get_bank(
            request: BankNameRequest, response: Response, user: User = Depends(app.get_current_user())
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
            bank_manager = BankManager(app.db)
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


    @app.middlewares.post("/api/v1/bank-name/add", response_class=JSONResponse)
    async def add_bank(request: CustomNameRequest, user: User = Depends(app.get_current_user())):
        app_logger.debug(
            f"Добавление банка: {request.custom_name_eng} с названием {request.bank_name_rus} для пользователя {user.id}"
        )
        try:
            custom_name_eng = request.custom_name_eng.lower()
            bank_name_rus = request.bank_name_rus.lower()
            bank_manager = BankManager(app.db)
            bank_manager.add_custom_bank(custom_name_eng, bank_name_rus, user.id)
            app_logger.info(f"Банк '{custom_name_eng}' добавлен для пользователя {user.id}")
            return JSONResponse(content={"result": "Банк был добавлен!"})
        except Exception as e:
            app_logger.error(f"Ошибка в add_bank: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal Server Error")