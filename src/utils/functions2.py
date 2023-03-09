
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from sklearn.preprocessing import StandardScaler

def data_report(df):
    '''FUNCION QUE DEFINE UN REPORTE DEL DATAFRAME'''
   # Sacamos los NOMBRES
    cols = pd.DataFrame(df.columns.values, columns=["COL_N"])

    # Sacamos los TIPOS
    types = pd.DataFrame(df.dtypes.values, columns=["DATA_TYPE"])

    # Sacamos los MISSINGS
    percent_missing = round(df.isnull().sum() * 100 / len(df), 2)
    percent_missing_df = pd.DataFrame(percent_missing.values, columns=["MISSINGS (%)"])

    # Sacamos los VALORES UNICOS
    unicos = pd.DataFrame(df.nunique().values, columns=["UNIQUE_VALUES"])
        
    percent_cardin = round(unicos['UNIQUE_VALUES']*100/len(df), 2)
    percent_cardin_df = pd.DataFrame(percent_cardin.values, columns=["CARDIN (%)"])

    concatenado = pd.concat([cols, types, percent_missing_df, unicos, percent_cardin_df], axis=1, sort=False)
    concatenado.set_index('COL_N', drop=True, inplace=True)


    return concatenado.T

# Función para la columna 'floor' del dataframe
def col_floor(X_train):
    
    # reemplazo 'bj' y 'en' por 0
    X_train['floor'].replace('bj','0',inplace=True)
    X_train['floor'].replace('en','0',inplace=True)
    # reemplazo 'ss' y 'st por 1
    X_train['floor'].replace('ss','-1',inplace=True)
    X_train['floor'].replace('st','-1',inplace=True)
    
    # valores 'NaN' - reemplazo los 'chalets' con 0
    X_train[(X_train.floor.isna()) | (X_train.propertyType=='chalet')]['floor'].fillna('0',inplace=True)
    
    # valores 'NaN' - reemplazo los 'flats' con 1 (que es la mediana)
    X_train.floor.fillna('1',inplace=True)
    X_train.floor = X_train.floor.astype(int)
    
    return X_train

def col_parking(X_train):
    
    # Si es NaN asumo que no tienen cochera.
    X_train.parkingSpace.fillna('0',inplace=True)
    parking = X_train.parkingSpace.str.split(",", expand = True)
    
    # Renombro columnas para no confundir
    parking = parking.rename(columns={0: 'hasParkingSpace', 1: 'IncludedInPrice'})
    
    # si no es 0, es 1
    parking['hasParkingSpace'] = parking['hasParkingSpace'].replace(["{'hasParkingSpace': True"], '1')
    
    # Convierto a integer
    parking['hasParkingSpace'] = parking['hasParkingSpace'].astype(int)
    
    # 1 si está incluido, 0 si no lo está
    parking['IncludedInPrice'].fillna('0',inplace=True) # los Nones no lo está.
    parking['IncludedInPrice'] = parking['IncludedInPrice'].replace([" 'isParkingSpaceIncludedInPrice': True}"], '1')
    parking['IncludedInPrice'] = parking['IncludedInPrice'].replace([" 'isParkingSpaceIncludedInPrice': False"], '0')
    
    # Convierto a integer
    parking['IncludedInPrice'] = parking['IncludedInPrice'].astype(int)
    
    # elimino la última columna ya que no me interesa el precio de la cochera
    parking.drop([2], axis=1, inplace=True)
    
    # Modifico el objeto original para incluir las nuevas columnas
    X_train['hasParkingSpace'] = parking['hasParkingSpace']
    X_train['IncludedInPrice'] = parking['IncludedInPrice']
    
    return X_train

# REEMPLAZO POR BOOLEANO A LISTA DE COLUMNAS
def booleanos(X_train):
    X_train['hasLift'] = X_train['hasLift'].fillna(0)
    X_train['hasLift'] = X_train['hasLift'].replace(True, 1).replace(False, 0)
    X_train['exterior'] = X_train['exterior'].replace(True, 1).replace(False, 0)
    
    return X_train



# STANDARD SCALER A LA LISTA DE COLUMNAS
def standard_scaler(df, escalar):
    """
    Aplica StandardScaler a una lista de columnas en un dataframe.

    Parámetros:
    df: El dataframe que contiene las columnas a escalar.
    cols: Una lista de columnas a las que se aplicará StandardScaler.

    Devuelve: El dataframe con las columnas escaladas.
    """
    scaler = StandardScaler()
    df[escalar] = scaler.fit_transform(df[escalar].values)
    return df


# ONE HOT ENCODER A LA LISTA DE COLUMNAS


def one_hot_encoder(df, one_hot):
    """
    Aplica One Hot Encoder a las columnas del dataframe.

    Parámetros:
    df:  El dataframe que contiene las columnas a codificar.
    one_hot:  Una lista de columnas a las que se aplicará get_dummies.

    Devuelve: El dataframe con las columnas codificadas.
    """
    df = pd.get_dummies(df, columns = one_hot)
    return df

# ELIMINAR COLUMNAS
def drop_columns(df, eliminar_cols):
    df.drop(eliminar_cols, axis=1, inplace=True)
    return df
