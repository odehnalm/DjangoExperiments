python manage.py migrate --settings=ma_value.settings.local_marco &&
python manage.py init_useragents --settings=ma_value.settings.local_marco &&
python manage.py init_stores --settings=ma_value.settings.local_marco &&
python manage.py init_ma_items --settings=ma_value.settings.local_marco &&
python manage.py init_proxies --settings=ma_value.settings.local_marco &&
python manage.py init_cpus_gpus_list --settings=ma_value.settings.local_marco &&
python manage.py init_fake_companies --settings=ma_value.settings.local_marco &&
python manage.py init_fake_users --settings=ma_value.settings.local_marco &&
python manage.py createsuperuser --settings=ma_value.settings.local_marco