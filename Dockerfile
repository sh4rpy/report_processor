FROM python:3.9

WORKDIR /code
COPY . .
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt
CMD bash -c 'python manage.py makemigrations tasks && python manage.py makemigrations weekly_reports && python manage.py makemigrations individual_reports && python manage.py migrate && python manage.py runserver 0.0.0.0:8000'