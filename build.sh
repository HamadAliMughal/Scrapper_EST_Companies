set -o errexit

pip install -r requirements.txt

python manage.py collectstatic -- fo-ipput
python manage.py migrate