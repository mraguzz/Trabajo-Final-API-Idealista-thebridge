
from catboost import CatBoostRegressor
import joblib

def catboost_model(X, y):
    # Definir el modelo CatBoost
    model = CatBoostRegressor()

    # Ajustar el modelo con los datos de entrada
    model.fit(X, y, verbose=False)

    # Guardar el modelo entrenado en un archivo
    joblib.dump(model, 'modelo_entrenado.pkl')

    # Predecir sobre los mismos datos de entrada
    y_pred = model.predict(X)

    # Retornar las predicciones y el modelo
    return y_pred, model
