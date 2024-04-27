# INSTALLING DEPENDECIES
echo "Installing python dependencies.."
python3.11.5 -m pip install -r requirements.txt
# make migrations
echo "Making migrations..."
python3.11.5 manage.py makemigrations --noinput
python3.11.5 manage.py migrate --noinput

# collect staticfiles
echo "Collect static..."
python3.11.5 manage.py collectstatic --noinput -- clear
echo "Build Process Completed"
