## Как установить

1. Скачай проект с GitHub:

```bash
git clone https://github.com/Igor231321/Store.git
cd Store
```

2. Создай виртуальное окружение и активируй его:

- Для Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

- Для Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установи зависимости:

```bash
pip install -r requirements.txt
```

4. Настрой базу данных (PostgreSQL):

По умолчанию используется PostgreSQL. Чтобы переключиться на SQLite:

- Открой файл `Store/mysite/settings.py`
- Найди блок с настройками `DATABASES`
- Замените

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "shop_db",
        "USER": "home",
        "PASSWORD": "admin",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

на

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

5. Выполни миграции:

```bash
python manage.py migrate
```

6. Запусти проект:

```bash
python manage.py runserver
```

7. Создай администратора:

```bash
python manage.py createsuperuser
```

Введи email и пароль по запросу.

---

## Готово!

Открой в браузере: http://127.0.0.1:8000
