import pickle
import numpy as np
from flask import Flask, request, render_template
import pandas as pd
from sklearn.impute import KNNImputer
from waitress import serve

app = Flask(__name__)

# Last inn den ferdigtrente modellen
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    # Viser skjemaet for å angi pasientdata
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Kopier verdier fra skjema til features-ordboken
        features = dict(request.form)

        # Liste over felter som skal konverteres til int
        cast_to_ints = ['alder', 'kjønn', 'inntekt', 'etnisitet', 'sykdomskategori', 'adl_stedfortreder', 
                        'kreft_sammenslått', 'diabetes', 'demens', 'antall_komorbiditeter', 'koma_score']
        
        # Liste over felter som skal konverteres til float
        cast_to_floats = ['hvite_blodlegemer', 'respirasjonsfrekvens', 'kroppstemperatur', 'lungefunksjon', 'serumalbumin',
                          'blod_ph', 'glukose', 'overlevelsesestimat_2mnd', 'overlevelsesestimat_6mnd',
                          'lege_overlevelsesestimat_2mnd', 'lege_overlevelsesestimat_6mnd', 'utdanning_kategori', 
                          'fysiologisk_score_merge', 'fysiologisk_komorbiditet_mult', 'nyrefunksjon', 'hjertefunksjon']

        # Standardverdier
        default_values = {
            'blod_ph': 7.40, 'lungefunksjon': 333.3, 'blodurea_nitrogen': 6.5, 'glukose': 85,
            'urinmengde': 2502, 'sykdomskategori': 1, 'adl_stedfortreder': 0.0, 'overlevelsesestimat_2mnd': 1.0,
            'overlevelsesestimat_6mnd': 1.0, 'lege_overlevelsesestimat_2mnd': 1.0, 'lege_overlevelsesestimat_6mnd': 1.0,
            'utdanning_kategori': 0.0, 'fysiologisk_score_merge': 0.0, 'fysiologisk_komorbiditet_mult': 0.0,
            'kroppstemperatur': 37.0, 'serumalbumin': 3.0, 'hvite_blodlegemer': 11.0, 'nyrefunksjon': 52.0,
            'hjertefunksjon': 90.0, 'koma_score': 0, 'respirasjonsfrekvens': 23.0, 'antall_komorbiditeter': 0
        }
        
        # Håndter tomme strenger og konverter til riktig type
        for k in cast_to_ints + cast_to_floats:
            value = request.form.get(k, '')
            if value.strip() == '':
                features[k] = default_values.get(k, np.nan)
            else:
                try:
                    features[k] = int(value) if k in cast_to_ints else float(value)
                except ValueError:
                    features[k] = default_values.get(k, np.nan)
        
        # Lag en DataFrame med kolonnenavn som modellen forventer
        columns = [
            'alder', 'inntekt', 'etnisitet', 'hvite_blodlegemer', 'respirasjonsfrekvens', 'kroppstemperatur',
            'lungefunksjon', 'serumalbumin', 'blod_ph', 'glukose', 'sykdomskategori', 'antall_komorbiditeter',
            'koma_score', 'adl_stedfortreder', 'overlevelsesestimat_2mnd', 'overlevelsesestimat_6mnd', 'diabetes',
            'demens', 'lege_overlevelsesestimat_2mnd', 'lege_overlevelsesestimat_6mnd', 'kjønn', 'utdanning_kategori',
            'fysiologisk_score_merge', 'fysiologisk_komorbiditet_mult', 'nyrefunksjon', 'hjertefunksjon', 'kreft_sammenslått'
        ]
        
        input_features_df = pd.DataFrame([features], columns=columns)

        print("Input Features DataFrame før prediksjon:")
        print(input_features_df)
        print("Antall funksjoner i modellen:", model.n_features_in_)
        print("Kolonner i input_features_df:", input_features_df.columns.tolist())

        # Gjør prediksjonen
        prediction = model.predict(input_features_df)


        # Returner prediksjonen til nettsiden
        prediction_text = f"Forventet sykehusopphold er: {round(prediction[0],3)} dager"
        return render_template('index.html', prediction=prediction_text)

    except Exception as e:
        # Logg feilen til konsollen
        print(f"Feil oppstod: {str(e)}")
        error_text = f"Det oppstod en feil: {str(e)}. Vennligst kontroller input."
        return render_template('index.html', error=error_text)

if __name__ == '__main__':
    print("http://localhost:8080")
    serve(app, host='0.0.0.0', port=8080)





'''        alder = int(request.form['alder'])
        kjønn = int(request.form['kjønn'])
        inntekt = int(request.form['inntekt'])
        etnisitet = request.form['etnisitet']  
        hvite_blodlegemer = float(request.form['hvite_blodlegemer'], default=np.nan)
        respirasjonsfrekvens = int(request.form['respirasjonsfrekvens'])
        kroppstemperatur = float(request.form['kroppstemperatur'])
        lungefunksjon = float(request.form['lungefunksjon'])
        serumalbumin = float(request.form['serumalbumin'])
        blod_ph = float(request.form['blod_ph'])
        glukose = int(request.form['glukose'])
        sykdomskategori = request.form['sykdomskategori'] 
        antall_komorbiditeter = int(request.form['antall_komorbiditeter'])
        koma_score = int(request.form['koma_score'])
        adl_stedfortreder = float(request.form['adl_stedfortreder'])  # Konverter til riktig datatype
        kreft_sammenslått = int(request.form['kreft']) 
        overlevelsesestimat_2mnd = float(request.form.get('overlevelsesestimat_2mnd', 0))
        overlevelsesestimat_6mnd = float(request.form.get('overlevelsesestimat_6mnd', 0)) 
        lege_overlevelsesestimat_2mnd = float(request.form['lege_overlevelsesestimat_2mnd'])
        lege_overlevelsesestimat_6mnd = float(request.form['lege_overlevelsesestimat_6mnd'])
        diabetes = int(request.form['diabetes'])
        demens = int(request.form['demens'])
        utdanning_kategori = float(request.form['utdanning_kategori'])
        fysiologisk_score_merge = float(request.form['fysiologisk_score_merge'])
        fysiologisk_komorbiditet_mult = float(request.form['fysiologisk_komorbiditet_mult'])
        nyrefunksjon = float(request.form['nyrefunksjon'])
        hjertefunksjon = float(request.form['hjertefunksjon'])
        
        
        
                if features['sykdomskategori'] == 3:
            features['sykdomskategori'] = features['koma_score']

        if not (0 <= features['overlevelsesestimat_2mnd'] <= 1):
            return render_template('index.html', error="Overlevelsesestimat (2 måneder) må være mellom 0 og 1")

        if not (0 <= features['overlevelsesestimat_6mnd'] <= 1):
            return render_template('index.html', error="Overlevelsesestimat (6 måneder) må være mellom 0 og 1")

        if not (0 <= features['lege_overlevelsesestimat_2mnd'] <= 1):
            return render_template('index.html', error="Lege Overlevelsesestimat (2 måneder) må være mellom 0 og 1")

        if not (0 <= features['lege_overlevelsesestimat_6mnd'] <= 1):
            return render_template('index.html', error="Lege Overlevelsesestimat (6 måneder) må være mellom 0 og 1")'''