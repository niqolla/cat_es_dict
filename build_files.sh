# build_files.sh
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3.9 manage.py runserver