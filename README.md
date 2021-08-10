## POSTGIS

### Requisitos GIS

`sudo apt-get install binutils libproj-dev gdal-bin`

## DumpData

`python manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission > fixtures/all.json`

`python manage.py dumpdata --exclude=contenttypes --exclude=auth.Permission > /home/julioriffel/Dropbox/devs/adapar/adapar_rede/all.json`