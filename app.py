from flask import Flask, render_template, session

app = Flask(__name__)
page_connexion = 'auth/connexion.html'

@app.route('/')
def connexion():
    if 'mail' in session:
        print("Connecté avec l'adresse : " + session['mail'])
    else:
        print("Non connecté")

    return render_template(page_connexion)