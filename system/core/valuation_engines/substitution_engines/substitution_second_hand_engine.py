import datetime

from django.conf import settings

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib

from repository import Repository
from utils.date import monthdelta


def valuation_start(req_data_engine):

    input_form = req_data_engine["data"][0]

    if input_form['Date achat'] is None or input_form['Prix achat'] is None or\
            not input_form['Systeme dexploitation'] or not input_form['Marque']:
        return None

    type_repository = Repository.LOCAL_DB

    # Instancia de repositorio
    repository = Repository(type_repository=type_repository)

    job_id = req_data_engine["job_id"]

    debug = True
    new_model = False

    # Cargamos la base de datos
    db = pd.read_csv(settings.PATH_SMARTPHONES)

    if debug:
        print('Numero de elementos en la base de datos: {0}'.format(db.count()[0]))

    # Preparamos datos de entrenamiento

    # Input
    X = np.array(db.loc[:, ['Gamme', 'Mois', 'Neuf']])

    # Output
    Y = np.array(db.loc[:, ['TauxDep']]).reshape(db.count()[0])

    # transformar primeraa columna a numeros

    X_0 = pd.get_dummies(X[:, 0]).values

    # Concatenamos los demás datos con la columna ahora convertida en
    # un arreglo representando datos categoricos
    X = np.column_stack([X_0, X[:, 1:]])

    # RANDOM FOREST: preparamos el modelo

    if new_model:
        regressor = RandomForestRegressor(
            n_estimators=150, min_samples_split=2)
        regressor.fit(X, Y)
    else:
        try:
            regressor = joblib.load(settings.RF_PKL)
        except:
            regressor = RandomForestRegressor(
                n_estimators=150, min_samples_split=2)
            regressor.fit(X, Y)

    # PREDICCION: preparacion de datos que se suministran al modelo

    d1 = input_form['Date achat']
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.today()
    meses = monthdelta(d1, d2)

    x_aster = np.array([[input_form['Prix achat'],meses]])
    if input_form['Systeme dexploitation'] == 'Android':
        if float(input_form['Prix achat']) > 600:
            X_0 = np.array([[0,0,1]])
            x_aster = np.column_stack([X_0, x_aster])
        elif float(input_form['Prix achat']) <= 600:
            X_0 = np.array([[1,0,0]])
            x_aster = np.column_stack([X_0, x_aster])
    elif input_form['Marque'].upper() == 'APPLE':
        X_0 = np.array([[0, 1, 0]])
        x_aster = np.column_stack([X_0, x_aster])


    # OUTPUT
    # (1-TAUX_DEP)*PRIX_ACHAT
    second_hand = (1-regressor.predict(x_aster))*float(input_form['Prix achat'])

    repository.set_second_hand_value(job_id, second_hand)

    if new_model:
        joblib.dump(regressor, settings.RF_PKL, compress=1)

    if debug:
        print('Valor second hand: {0}'.format(second_hand))
        print('TauxDep predicha: {0}'.format(regressor.predict(x_aster)))

    return second_hand
