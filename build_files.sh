echo " Building the project..."
python3 -m pip install --system -r requirements.txt
python3 manage.py collectstatic --noinput --clear
echo " Build Configuration Completed!"