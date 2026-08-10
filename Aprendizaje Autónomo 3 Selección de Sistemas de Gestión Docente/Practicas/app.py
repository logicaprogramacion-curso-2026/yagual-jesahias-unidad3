from flask import Flask, render_template, request, url_for

app = Flask(__name__)

users = {}
print(users)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('app_prueba.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        users[nombres] = apellidos
        print(users)
        return render_template('login.html')
    return render_template('app_prueba.html')

@app.route('/categoría')
def categoría():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('app_prueba.html')
print("El usuario volvió")

@app.route('/prueba1')
def prueba1():
    return render_template('prueba1.html')

@app.route('/prueba2')
def prueba2():
    return render_template('prueba2.html')

@app.route('/prueba3')
def prueba3():
    return render_template('prueba3.html')

@app.route('/prueba4')
def prueba4():
    return render_template('prueba4.html')

@app.route('/prueba5')
def prueba5():
    return render_template('prueba5.html')

@app.route('/prueba6')
def prueba6():
    return render_template('prueba6.html')

@app.route('/prueba7')
def prueba7():
    return render_template('prueba7.html')

@app.route('/prueba8')
def prueba8():
    return render_template('prueba8.html')

@app.route('/pruebadeingenieríaensistemasdeinformación')
def pruebadeingenieríaensistemasdeinformación():
    return render_template('pruebadeingenieríaensistemasdeinformación.html')

@app.route('/pruebadeingenieríaautomotriz')
def pruebadeingenieríaautomotriz():
    return render_template('pruebadeingenieríaautomotriz.html')

@app.route('/pruebadederecho')
def pruebadederecho():
    return render_template('pruebadederecho.html')

@app.route('/pruebadeingenieríaindustrial')
def pruebadeingenieríaindustrial():
    return render_template('pruebadeingenieríaindustrial.html')

@app.route('/pruebadefinanzasynegociosdigitales')
def pruebadefinanzasynegociosdigitales():
    return render_template('pruebadefinanzasynegociosdigitales.html')

@app.route('/pruebadepsicologíaclínica')
def pruebadepsicologíaclínica():
    return render_template('pruebadepsicologíaclínica.html')

@app.route('/pruebadeenfermeríaconproyeccióninternacional')
def pruebadeenfermeríaconproyeccióninternacional():
    return render_template('pruebadeenfermeríaconproyeccióninternacional.html')

@app.route('/pruebadeadministracióndeempresas')
def pruebadeadministracióndeempresas():
    return render_template('pruebadeadministracióndeempresas.html')

@app.route('/finalización')
def finalización():
    return render_template('finalización.html')

if __name__ == '__main__':
    app.run(debug=True)