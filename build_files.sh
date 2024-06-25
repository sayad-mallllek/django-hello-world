echo "BUILD START"
sudo apt install wkhtmltopdf -y
python3.9 -m pip install -r requirements.txt
python3.9 manage.py collectstatic --noinput --clear
echo "BUILD END"
