from fastapi import FastAPI, Response, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, Field
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from utils.dictionary import dct, alf
from database.db import BankManager, Database
import utils.response


class BankNameRequest(BaseModel):
    bank_name: str = Field(default='')

class CustomNameRequest(BaseModel):
    bank_name_rus: str = Field(default='')
    custom_name_eng: str = Field(default='')

app = FastAPI()

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
async def get_bank(request: BankNameRequest, response: Response, user: User = Depends(current_user)):
    try:
        rez = ''
        response.status_code = 404
        for j in request.bank_name:
            if j in alf:
                return response.status_code
        for i in request.bank_name:
            rez += dct[i]
        rez = rez.upper()
        name = request.bank_name.lower()
        bank_manager = BankManager(db)
        result = bank_manager.select_bank(rez, name, user.id)
        if len(result) > 0:
            return JSONResponse(content={'result': result})
        else:
            return response.status_code
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/api/v1/bank-name/add", response_class=JSONResponse)
async def add_bank(request: CustomNameRequest, user: User = Depends(current_user)):
    custom_name_eng = request.custom_name_eng.lower()
    bank_name_rus = request.bank_name_rus.lower()
    bank_manager = BankManager(db)
    bank_manager.add_custom_bank(custom_name_eng, bank_name_rus, user.id)
    return JSONResponse(content={'result': 'The bank has been added!'})
