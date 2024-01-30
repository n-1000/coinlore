from flask import Flask, render_template
import requests

app = Flask(__name__)

# Variable global para almacenar los datos de la criptomoneda
criptomonedas_global = []
carga_inicial_realizada = False

@app.before_request
def cargar_datos_iniciales():
    global criptomonedas_global, carga_inicial_realizada

    if not carga_inicial_realizada:
        api_url = "https://api.coinlore.net/api/ticker/?id=90"
        response = requests.get(api_url)

        if response.status_code == 200:
            criptomonedas_global = response.json()
            carga_inicial_realizada = True
        else:
            criptomonedas_global = []

@app.route('/')
def index():
    global criptomonedas_global
    return render_template('lista.cripto.html', criptomonedas=criptomonedas_global)

@app.route('/detalle/<id>')
def detalle(id):
    global criptomonedas_global
    cripto = next((c for c in criptomonedas_global if c['id'] == id), None)
    
    if cripto is None:
        api_url = f"https://api.coinlore.net/api/ticker/{id}/"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            cripto = response.json()
        else:
            cripto = {}

    return render_template('detalle.cripto.html', cripto=cripto)

if __name__ == '__main__':
    app.run(debug=True)