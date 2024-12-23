python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic 