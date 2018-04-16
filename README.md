# Setup Development Environment
* **⚠ NOTE! ⚠** : These instructions are targeting DEVELOPMENT machines and are **INSECURE** for production.

## Prerequisites:

* [Python](https://www.python.org/downloads/) (>= 3.6.3)
* PostgreSQL & PostGIS. Installation help [here](https://github.com/nonZero/setups).
* [pipenv](https://docs.pipenv.org/)

## Create DB
* Note:  This also creates a superuser user called `local_gallery`.
* Make sure your database is running.
* Linux:

        sudo -u postgres createuser -s local_gallery
        sudo -u postgres psql -c "alter user local_gallery with encrypted password 'local_gallery';"
        sudo -u postgres createdb local_gallery -O local_gallery

* Windows (supply password for postgres user):

        createuser --username=postgres -s local_gallery
        psql --username=postgres -c "alter user local_gallery with encrypted password 'local_gallery';"
        createdb --username=postgres local_gallery -O local_gallery

## Setup

1. Clone the repository:

        git clone https://github.com/LocalGallery/local_gallery.git

2. Create a virtual env and install required Python packages:

        pipenv install

3. Activate the virtualenv:

        pipenv shell

       Your python is here (needed for pycharm):

       * linux:

             which python

       * Windows:

             where python


4. Reset, migrate and populate database:

        python manage.py reset_db
        python manage.py migrate
        python manage.py populate_db

5. Create an admin account:

        python manage.py createsuperuser

## Run

Run the server:

    python manage.py runserver


## Developing the Vue.js app

### Setup

    cd logal
    npm install

### Run

    npx webpack --config build/webpack.dev.conf.js --watch

Access via <http://localhost:8000/pardes-hana/app/>