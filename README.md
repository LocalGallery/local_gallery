# local_gallery
dev local_gallery

# some requirements
## TODO: check what of those are actually necessary (might be redundant)
python 3.6.3  
django 1.11.7  
postgresql 10.1  
postgresql-10-postgis-scripts  
postgresql-9.6-postgis-scripts  
postgis 2.4 (included in ubuntugis)  
libgdal-dev  
gdal  

## setup dev postgresql
sudo -u postgres psql -c "create database local_gallery;"  
sudo -u postgres psql local_gallery -c "alter user postgres with encrypted password 'postgres';"  
sudo -u postgres psql local_gallery -c "create extension postgis;"  