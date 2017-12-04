# Setup Development Environment
Prerequisites: [Python](https://www.python.org/downloads/) (>= 3.6.3), [pip](https://pip.pypa.io/en/stable/installing/) (>= 9.0.1), [PostgreSQL](https://www.postgresql.org/download/) (>= 10.1)

1. Clone the repository and create a virtual environment (activate it whenever you're working on the project):
```
git clone https://github.com/LocalGallery/local_gallery.git
cd local_gallery
python3 -m venv dev
source dev/bin/activate
```
2. Requirements:
```
```
3. Create database:
```
sudo -u postgres psql -c "create database local_gallery;"
sudo -u postgres psql local_gallery -c "alter user postgres with encrypted password 'postgres';"
sudo -u postgres psql local_gallery -c "create extension postgis;"
```
4. Migrate:
```
python manage.py migrate
```
5. Create an admin account:
```
python manage.py createsuperuser
```
6. Run the server:
```
python manage.py runserver
```
