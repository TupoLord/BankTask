from utils.logger import app_logger


@app.middleware("http")
async def log_requests(request: Request, call_next):
    app_logger.info(f"Получен запрос: {request.method} {request.url}")
    response = await call_next(request)
    app_logger.info(f"Отправлен ответ: {response.status_code} {request.url}")
    return response
