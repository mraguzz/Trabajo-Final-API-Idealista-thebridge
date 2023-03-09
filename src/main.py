## Librerías

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import sys, os


sys.path.append('utils/')
sys.path.append(os.path.realpath('utils/'))

import functions2
import operaciones

## DATOS RAW

ruta = 'data/raw_files/idealista16-2.csv'
df_tot = pd.read_csv(ruta)

## FILTRO POR CIUDAD - (MADRID EN ESTE CASO)
ciudad = 'Madrid'
pisos_madrid = df_tot.loc[df_tot.municipality == ciudad ]


## CARGA DE DATOS

X = pisos_madrid.drop('price', axis=1)
y = pisos_madrid['price']

## PROCESADO DE DATOS

# Función para la columna 'floor' del dataframe
functions2.col_floor(X)

# Función para la columna 'parking' del dataframe
functions2.col_parking(X)

# Función para las columnas ['hasLift'] y ['exterior'] del dataframe
# (Reemplaza por 1 y 0 las columnas)
functions2.booleanos(X)

# Función que aplica StandardScaler a las siguientes columnas del dataframe
escalar = ['size', 'rooms', 'bathrooms', 'latitude', 'longitude', 'floor']
functions2.standard_scaler(X, escalar)

# Función que aplica One Hot Encoder a las siguientes columnas del dataframe
one_hot = ['propertyType', 'status', 'district']
X = pd.get_dummies(X, columns = one_hot)
#functions2.one_hot_encoder(X, one_hot) <- ESTA FUNCION NO ME ESTARIA MODIFICANDO EL DATAFRAME.

# Función que elimina columnas del dataframe
eliminar_cols = ['Unnamed: 0', 'propertyCode', 'thumbnail', 'externalReference', 'numPhotos', 'url',
'hasPlan', 'has3DTour', 'has360', 'hasVideo', 'hasStaging', 'operation', 'address',
'showAddress', 'distance', 'country', 'labels', 'newDevelopmentFinished', 'neighborhood',
'newDevelopment', 'topNewDevelopment', 'superTopHighlight', 'municipality', 'province',
'priceByArea', 'suggestedTexts', 'description', 'detailedType', 'parkingSpace']
functions2.drop_columns(X,eliminar_cols)

## ENTRENAMIENTO DEL MODELO

# Modelo: CatBoostRegressor 
# (Según el notebook, el mejor resultado lo conseguí sin optimizar hyperparámetros)
# esta función entrena el modelo y además lo guarda

operaciones.catboost_model(X, y)

