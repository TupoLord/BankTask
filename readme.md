1. Клонирование репозитория 

```git clone https://github.com/TupoLord/BankTask.git```

2. Создание виртуального окружения

```python3 -m venv venv```

3. Активация виртуального окружения

```source venv/bin/activate```

4. Установка зависимостей

```pip3 install -r requirements.txt```

5. Настраиваем своё подключение к базе данных в данном случае ```PostgreSQL```, меняем данные в файле ```.env```(Пример: ```.env_example```)


6. Запускаем API
```uvicorn main:app --reload```

7. Переходим в раздел ```/docs```

7. Проходим процесс регистрации

8. Проходим процесс авторизации

9. На выбор имеется два эндпоинта:

   1. **get_bank** - Возвращает нам название банка при совпадении с тем что мы внесли в переменную bank_name
       1. Заполняем переменную ***bank_name***(на кириллице)
       2. Получаем ответ в виде названия банка
   2. **add_bank** - В случае если мы хотим добавить свой банк в базу данных
       1. Заполняем переменные ***bank_name***(на кириллице) и ***custom_name***(на латинице)
       2. Банк и его перевод добавлены в базу данных и могут быть возвращены при помощи эндпоинта **get_bank**


