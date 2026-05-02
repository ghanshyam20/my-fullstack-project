FROM python:3.12

WORKDIR /app

# copy requirements , caching 
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy rest of project
COPY . .

# collect static
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "cms.wsgi:application", "--bind", "0.0.0.0:8000"]
