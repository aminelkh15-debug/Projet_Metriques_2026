import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route("/contact")
def contact():
    return render_template("contact.html")
# Atelier de prévision météorologique

@app.route("/atelier")
def atelier():
    return render_template("atelier.html")

@app.get("/atelier-data")
def atelier_data():
    # URL pour Berlin avec toutes les variables demandées
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,pressure_msl,rain,relative_humidity_2m,visibility,weather_code,showers,snowfall,dew_point_2m,apparent_temperature,wind_speed_10m,wind_speed_80m,wind_speed_120m&start_date=2026-03-08&end_date=2026-03-22"

    print("Appel à l'API Open-Meteo pour /atelier-data...")

    try:
        # 1. Faire la requête à l'URL
        response = requests.get(url, timeout=15)
        response.raise_for_status()  # Vérifie si la requête a réussi
        data = response.json()       # Convertit la réponse en dictionnaire Python
        print("Données reçues avec succès.")

    except requests.exceptions.Timeout:
        print("ERREUR: Timeout")
        return jsonify({"error": "Timeout - L'API météo est trop lente"}), 504
    except requests.exceptions.ConnectionError:
        print("ERREUR: Connexion")
        return jsonify({"error": "Erreur de connexion à l'API météo"}), 502
    except requests.exceptions.RequestException as e:
        print(f"ERREUR Requête: {str(e)}")
        return jsonify({"error": f"Erreur lors de l'appel à l'API: {str(e)}"}), 502
    except ValueError as e:
        print(f"ERREUR JSON: {str(e)}")
        return jsonify({"error": f"Erreur de décodage JSON: {str(e)}"}), 502

    # 2. Vérifier que les données ont la structure attendue
    if "hourly" not in data:
        print("ERREUR: Pas de données 'hourly' dans la réponse")
        return jsonify({"error": "Format de données inattendu"}), 502

    hourly = data["hourly"]
    times = hourly.get("time", [])

    if not times:
        print("ERREUR: Aucune donnée temporelle")
        return jsonify({"error": "Aucune donnée temporelle disponible"}), 404

    print(f"Nombre d'enregistrements trouvés : {len(times)}")

    # 3. Construire le tableau JSON (un objet par heure avec toutes les variables)
    result = []
    for i in range(len(times)):
        # On crée un dictionnaire pour chaque heure
        entry = {
            "datetime": times[i],
            "temperature_2m": hourly.get("temperature_2m", [])[i] if i < len(hourly.get("temperature_2m", [])) else None,
            "pressure_msl": hourly.get("pressure_msl", [])[i] if i < len(hourly.get("pressure_msl", [])) else None,
            "rain": hourly.get("rain", [])[i] if i < len(hourly.get("rain", [])) else None,
            "relative_humidity_2m": hourly.get("relative_humidity_2m", [])[i] if i < len(hourly.get("relative_humidity_2m", [])) else None,
            "visibility": hourly.get("visibility", [])[i] if i < len(hourly.get("visibility", [])) else None,
            "weather_code": hourly.get("weather_code", [])[i] if i < len(hourly.get("weather_code", [])) else None,
            "showers": hourly.get("showers", [])[i] if i < len(hourly.get("showers", [])) else None,
            "snowfall": hourly.get("snowfall", [])[i] if i < len(hourly.get("snowfall", [])) else None,
            "dew_point_2m": hourly.get("dew_point_2m", [])[i] if i < len(hourly.get("dew_point_2m", [])) else None,
            "apparent_temperature": hourly.get("apparent_temperature", [])[i] if i < len(hourly.get("apparent_temperature", [])) else None,
            "wind_speed_10m": hourly.get("wind_speed_10m", [])[i] if i < len(hourly.get("wind_speed_10m", [])) else None,
            "wind_speed_80m": hourly.get("wind_speed_80m", [])[i] if i < len(hourly.get("wind_speed_80m", [])) else None,
            "wind_speed_120m": hourly.get("wind_speed_120m", [])[i] if i < len(hourly.get("wind_speed_120m", [])) else None,
        }
        result.append(entry)

    # 4. Vérifier que le tableau n'est pas vide
    if not result:
        print("ERREUR: Aucune donnée valide n'a pu être extraite")
        return jsonify({"error": "Aucune donnée météo valide"}), 404

    print(f"Succès: {len(result)} entrées générées.")
    # 5. RETOURNER LE TABLEAU JSON (C'EST LE RETURN QUI MANQUAIT !)
    return jsonify(result)
    
#Prévision météorologique pour Paris
@app.get("/paris")
def api_paris():
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"

    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return jsonify({"error": "Impossible de joindre l'API météo", "detail": str(e)}), 502
    except ValueError as e:
        return jsonify({"error": "Réponse météo invalide", "detail": str(e)}), 502

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    if not result:
        return jsonify({"error": "Aucune donnée météo disponible pour Paris"}), 204

    return jsonify(result)

# Rapport météo pour Paris
@app.route("/rapport")
def mongraphique():
    return render_template("graphique.html")

# Histogramme météo pour Paris
@app.route("/histogramme")
def monhistogramme():
    return render_template("histogramme.html")



# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
