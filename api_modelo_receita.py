import joblib
from fastapi import FastAPI
import pandas as pd
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class request_body(BaseModel):
    tempo_de_experiencia: int
    numero_de_vendas: int 

modelo_regr = joblib.load('./modelo_receita.pkl')

@app.post('/predict')
def predict(data : request_body):
    input_features = {
        'tempo_de_experiencia': data.tempo_de_experiencia,
        'numero_de_vendas': data.numero_de_vendas
    }

    pred_df = pd.DataFrame(input_features, index=[1])

    # predição
    y_pred = modelo_regr.predict(pred_df)[0].astype(float)

    return {'receita_em_reais': y_pred.tolist()}