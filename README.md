## Pasos previos:

   - crear entorno de trabajo con Python 3
   - crear DATABASE local con nombre 'ma_value_db' y asignar
     USER y PASSWORD

     Nota: para no alterar el settings por defecto (ma_value.settings.local), se puede agregar settings por usuario. Ejemeplo:

     ma_value.settings.local_marco, o
     ma_value.settings.local_ricardo, o
     ma_value.settings.local_jesus

     y en ese documento agregar sus propias configuraciones locales

     A partir de entonces, todos sus comandos serian con --settings=ma_value.settings.local_XXXXX
   
   - Activar entorno de trabajo:
   
     a) En el caso de virtualenvwrapper:

        workon ENTORNO

     b) En el caso de virtualenv:

        source ENTORNO/bin/activate

     (VER RESPECTIVAS DOCUMENTACIONES)

## Pasos para instalación y ejecución

pip install -r requirements.txt

python manage.py migrate --settings=ma_value.settings.local

python manage.py init_useragents --settings=ma_value.settings.local

python manage.py init_stores --settings=ma_value.settings.local

python manage.py init_ma_items --settings=ma_value.settings.local

python manage.py createsuperuser --settings=ma_value.settings.local

# Ahora bien, en otra terminal, al mismo nivel del archivo manage.py, activar el entorno y ejecutar

python manage.py rqworker high default low --settings=ma_value.settings.local

# A su vez, en otra terminal, al mismo nivel del archivo manage.py, activar el entorno y ejecutar

python manage.py rqscheduler high default low --settings=ma_value.settings.local

# Luego

python manage.py init_proxies --settings=ma_value.settings.local

python manage.py runserver --settings=ma_value.settings.local

## SOLO LOCAL: En la carpeta system/tmp se generaran los archivos XLSX para TV, Neveras, Laptop y Moviles
