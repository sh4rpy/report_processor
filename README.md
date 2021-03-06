# Report processor

### Что ты такое?

Веб-сервис, позволяющий вести журнал выполненных задач, помечать их тегами и скачивать отчеты о проделанных работах.

### Как запустить?

Склонируйте репозиторий:

```bash
git clone https://github.com/sh4rpy/report_processor.git
```

Создайте файл .env в одной директории с файлом settings.py. Создайте в нем переменную окружения  SECRET_KEY, которой присвойте скопированный ключ с [сайта генерации ключей](https://djecrety.ir). Выглядеть файл должен так:

```python
SECRET_KEY=скопированный_ключ
```

Убедитесь, что Docker запущен, и  создайте образ:

```bash
docker build -t имя_образа .
```

Запустите контейнер командой:

```bash
docker run -it -p 8000:8000 имя_образа
```

Приложение станет доступно по адресу [http://0.0.0.0:8000](http://0.0.0.0:8000).