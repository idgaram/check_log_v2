from flask import Flask, render_template, jsonify, request
import requests, datetime, time, threading, json

# fonction flask
app = Flask(__name__)
app.secret_key = "test"

# définition des variables 
temps = (datetime.datetime.now()).strftime('%H:%M:%S')

# création de la fonction de répétition
def periodic_execution():
    while True:
        update_json()
        time.sleep(3)

# accueil ou l'utilisateur rentre ses 2 url
@app.route('/', methods=["GET", "POST"])
def accueil():
    return render_template("index.html")

# deuxième écran où l'utilisateur constate le statut des 2 requetes à l'instant où il a validé
@app.route('/result', methods=["GET", "POST"])
def show_status():
    # création des variables du json
    global status_site_1, status_site_2, url_site_1, url_site_2, temps
    url_site_1 = "http://" + request.form["url_site_1"]
    url_site_2 = "http://" + request.form["url_site_2"]        
    status_site_1 = (requests.get(url_site_1)).status_code
    status_site_2 = (requests.get(url_site_2)).status_code
    temps = (datetime.datetime.now()).strftime('%H:%M:%S')
    
    # création du json et stockage des variables au moment de l'input utilisateur
    with open("logs.json", "w") as f:
        json.dump({
            "site_1": {
                "url": f"{url_site_1}",
                "status": [f"{status_site_1}"],
                "time_test": [f"{temps}"]
            },
            "site_2": {
                "url": f"{url_site_2}",
                "status": [f"{status_site_2}"],
                "time_test": [f"{temps}"]
            }
        }, f, indent=4)

    # démarrage de la répétition de la fonction update_json()
    thread = threading.Thread(target=periodic_execution)
    thread.daemon = True  # Daemonize the thread so it automatically stops when the main program exits
    thread.start()

    # affichage sur le site des résultats au moment de l'utilisation 
    return render_template("result.html", url_site_1=url_site_1, url_site_2=url_site_2,status_site_1=status_site_1, status_site_2=status_site_2, temps=temps )

# création de la fonction pour update le fichier json
def update_json():
    global status_site_1, status_site_2, url_site_1, url_site_2, temps
    temps = (datetime.datetime.now()).strftime('%H:%M:%S')
    with open("logs.json", "r") as f:
        contenu = json.load(f)

    contenu["site_1"]['status'].append(f"{status_site_1}")
    contenu["site_1"]['time_test'].append(f"{temps}")
    contenu["site_2"]['status'].append(f"{status_site_2}")
    contenu["site_2"]['time_test'].append(f"{temps}")

    if len(contenu["site_1"]['status']) > 48:
        del contenu["site_1"]['status'][0]
    if len(contenu["site_2"]['status']) > 48:
        del contenu["site_2"]['status'][0]
    if len(contenu["site_1"]['time_test']) > 48:
        del contenu["site_1"]['time_test'][0]
    if len(contenu["site_2"]['time_test']) > 48:
        del contenu["site_2"]['time_test'][0]
    with open("logs.json", "w") as f:
        json.dump(contenu, f, indent=4)
    

  
@app.route('/display_logs')
def display_logs():
    with open("logs.json", 'r') as f:
        logs = json.load(f)
    return jsonify(logs)
    return render_template('display_logs.html')


# initialisation
if __name__=="__main__":
    app.run(host="0.0.0.0", port= 9999, debug=True)