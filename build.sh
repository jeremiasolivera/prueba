chmod 755 build.sh

set -o errexit

poetry install

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate