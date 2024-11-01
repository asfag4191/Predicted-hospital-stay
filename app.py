import pickle
import numpy as np
from flask import Flask, request, render_template
import pandas as pd
from sklearn.impute import KNNImputer
from waitress import serve

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = dict(request.form)

        cast_to_ints = ['alder', 'kjønn', 'inntekt', 'etnisitet', 'sykdomskategori', 'adl_stedfortreder', 
                        'kreft_sammenslått', 'diabetes', 'demens', 'antall_komorbiditeter']
        
        cast_to_floats = ['hvite_blodlegemer', 'respirasjonsfrekvens', 'kroppstemperatur', 'lungefunksjon', 'serumalbumin',
                          'blod_ph', 'glukose', 'overlevelsesestimat_2mnd', 'overlevelsesestimat_6mnd',
                          'lege_overlevelsesestimat_2mnd', 'lege_overlevelsesestimat_6mnd', 'utdanning_kategori', 
                          'fysiologisk_score_merge', 'fysiologisk_komorbiditet_mult', 'nyrefunksjon', 'hjertefunksjon', 'urinmengde',
                          'koma_score']

        default_values = {
            'blod_ph': 7.40, 'lungefunksjon': 333.3, 'blodurea_nitrogen': 6.5, 'glukose': 85,
            'urinmengde': 2502, 'sykdomskategori': 1, 'adl_stedfortreder': 0.0, 'overlevelsesestimat_2mnd': 1.0,
            'overlevelsesestimat_6mnd': 1.0, 'lege_overlevelsesestimat_2mnd': 1.0, 'lege_overlevelsesestimat_6mnd': 1.0,
            'utdanning_kategori': 0.0, 'fysiologisk_score_merge': 0.0, 'fysiologisk_komorbiditet_mult': 0.0,
            'kroppstemperatur': 37.0, 'serumalbumin': 3.0, 'hvite_blodlegemer': 11.0, 'nyrefunksjon': 52.0,
            'hjertefunksjon': 90.0, 'respirasjonsfrekvens': 23.0, 'antall_komorbiditeter': 0, 'koma_score': 0.0,
            'urinmengde': 2502.0
        }
        
        for k in cast_to_ints + cast_to_floats:
            value = request.form.get(k, '')
            if value.strip() == '':
                features[k] = default_values.get(k, np.nan)
            else:
                try:
                    features[k] = int(value) if k in cast_to_ints else float(value)
                except ValueError:
                    features[k] = default_values.get(k, np.nan)
        
        columns = [
            'alder', 'inntekt', 'etnisitet', 'hvite_blodlegemer', 'respirasjonsfrekvens', 'kroppstemperatur',
            'lungefunksjon', 'serumalbumin', 'blod_ph', 'glukose', 'urinmengde', 'sykdomskategori', 'antall_komorbiditeter',
            'koma_score', 'adl_stedfortreder', 'overlevelsesestimat_2mnd', 'overlevelsesestimat_6mnd', 'diabetes',
            'demens', 'lege_overlevelsesestimat_2mnd', 'lege_overlevelsesestimat_6mnd', 'kjønn', 'utdanning_kategori',
            'fysiologisk_score_merge', 'fysiologisk_komorbiditet_mult', 'nyrefunksjon', 'hjertefunksjon', 'kreft_sammenslått'
        ]
        
        input_features_df = pd.DataFrame([features], columns=columns)

        print("Input Features DataFrame før prediksjon:")
        print(input_features_df)
        print("Antall funksjoner i modellen:", model.n_features_in_)
        print("Kolonner i input_features_df:", input_features_df.columns.tolist())

        prediction = model.predict(input_features_df)


        prediction_text = f"Forventet sykehusopphold er: {round(prediction[0],3)} dager"
        return render_template('index.html', prediction=prediction_text)

    except Exception as e:
        print(f"Feil oppstod: {str(e)}")
        error_text = f"Det oppstod en feil: {str(e)}. Vennligst kontroller input."
        return render_template('index.html', error=error_text)

if __name__ == '__main__':
    print("http://localhost:8080")
    serve(app, host='0.0.0.0', port=8080)



