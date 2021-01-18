FROM python:3.9

WORKDIR /code
COPY . .
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
CMD bash -c 'python manage.py makemigrations processor && python manage.py migrate && python manage.py runserver 0.0.0.0:8000'