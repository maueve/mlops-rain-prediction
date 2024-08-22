import numpy as np
import pickle
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



MODEL = None

def fill_model_cache():
    """
    Funcion para cargar el modelo en cache
    :return:
    """
    global MODEL
    MODEL_PATH = '../../data/models/model.pkl'
    #MODEL_PATH = 'model.pkl'
    print("Model Path: ", MODEL_PATH)
    MODEL = pickle.load(open(MODEL_PATH, 'rb'))


@app.get("/predict")
def predict_rain_tomorrow(humidity: float):

    VAL_LLOVERA = 1

    llovera = False
    mensaje = ''

    data = np.array([humidity])
    data = data.reshape(-1, 1)
    res = MODEL.predict(data)

    directorio_actual = os.getcwd()

    print("El directorio actual es:", directorio_actual)

    if (res[0] == VAL_LLOVERA):
        llovera = True
        mensaje = 'Mañana llovera con una probabilidad de 83%'
    else:
        llovera = False
        mensaje = 'Mañana NO llovera con una probabilidad de 83%'

    return  {
        'llovera': llovera,
        'mensaje': mensaje
    }


@app.get("/refresh_model/")
async def refresh_models():
    """
    Funcion para refrescar modelos mediante api
    :return:
    """
    fill_model_cache()
    return {"status": "success"}

fill_model_cache()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





