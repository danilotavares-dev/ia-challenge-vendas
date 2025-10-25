import streamlit as st
import requests
import json

st.title('Modelo de Predição de Receita Gerada')

st.write('Quanto tempo de experiência o profissonal tem na empresa (em meses)?')
tempo_de_experiencia = st.slider('Meses', min_value=1, max_value=119, value=60, step=1)

st.write('Quantas vendas foram feitas pelo profissional?')
numero_de_vendas = st.slider('Vendas', min_value=10, max_value=100, value=10, step=1)

input_features = {
    'tempo_de_experiencia': tempo_de_experiencia,
    'numero_de_vendas': numero_de_vendas
}

if st.button('Estimar Receita'):
    try:
        res = requests.post(
            url='http://127.0.0.1:8000/predict',
            json=input_features
        )
    
        res.raise_for_status()
        res_json = res.json()
        st.write('Resposta do servidor:', res_json)
        chave_receita = 'receita_em_reais'

        if chave_receita in res_json:
            receita_em_reais = round(res_json[chave_receita], 2)
            st.subheader(f'Receitas estimada é de R$ {receita_em_reais}')
        else:
            st.error(f"A resposta não contém a chave '{chave_receita}'." 
                     f"Verifique o retorno do servidor acima.")
            
    except requests.exceptions.ConnectionError:
        st.error(f'Não foi possível conectar-se ao servidor FastAPI.'
                'Certifique-se que o servidor esteja rodando em http://127.0.0.1:8000 .')
    
    except Exception as e:
        st.error(f'Ocorreu um erro: {e}')