from flask import Flask, request, render_template_string
import requests
from datetime import datetime

app = Flask(__name__)

# API Key
API_KEY = "916cb9c4ef799fa508ee19a2d6020e58"

# Informacje startowe w logach
PORT = 5000
print(f"Aplikacja uruchomiona: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Autor: Michał Zarzecki")
print(f"Nasłuchiwanie na porcie TCP: {PORT}")

# Predefiniowana lista krajów i miast
cities = {
    "Polska": ["Warszawa", "Kraków", "Gdańsk"],
    "Niemcy": ["Berlin", "Monachium", "Hamburg"],
    "Francja": ["Paryż", "Marsylia", "Lyon"]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    selected_country = None
    selected_city = None

    if request.method == 'POST':
        selected_country = request.form.get('country')
        selected_city = request.form.get('city')

        if selected_city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={API_KEY}&units=metric&lang=pl"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather = {
                    'city': selected_city,
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'country': selected_country
                }
            else:
                weather = {'error': 'Nie znaleziono miasta.'}

    html = '''
    <!doctype html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <title>Aplikacja pogodowa</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f0f0f0; padding: 20px; }
            .container { background-color: white; padding: 20px; border-radius: 8px; max-width: 500px; margin: auto; }
            h1 { text-align: center; color: #333; }
            form { text-align: center; margin-bottom: 20px; }
            select, button { padding: 10px; margin: 5px; }
            .weather { text-align: center; font-size: 18px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Aplikacja pogodowa</h1>
            <form method="POST">
                <label for="country">Wybierz kraj:</label><br>
                <select name="country" id="country" required onchange="updateCities()">
                    <option value="">--Wybierz kraj--</option>
                    {% for country in cities %}
                        <option value="{{ country }}" {% if country == selected_country %}selected{% endif %}>{{ country }}</option>
                    {% endfor %}
                </select><br><br>
                
                <label for="city">Wybierz miasto:</label><br>
                <select name="city" id="city" required>
                    <option value="">--Wybierz miasto--</option>
                    {% if selected_country %}
                        {% for city in cities[selected_country] %}
                            <option value="{{ city }}" {% if city == selected_city %}selected{% endif %}>{{ city }}</option>
                        {% endfor %}
                    {% endif %}
                </select><br><br>

                <button type="submit">Sprawdź pogodę</button>
            </form>

            {% if weather %}
                {% if weather.error %}
                    <p class="weather">{{ weather.error }}</p>
                {% else %}
                    <div class="weather">
                        <h2>{{ weather.city }}, {{ weather.country }}</h2>
                        <p>Temperatura: {{ weather.temperature }}°C</p>
                        <p>Opis: {{ weather.description }}</p>
                    </div>
                {% endif %}
            {% endif %}
        </div>

        <script>
            const cities = {{ cities|tojson }};
            function updateCities() {
                const countrySelect = document.getElementById('country');
                const citySelect = document.getElementById('city');
                const selectedCountry = countrySelect.value;

                // Czyszczenie opcji miast
                citySelect.innerHTML = '<option value="">--Wybierz miasto--</option>';

                if (selectedCountry in cities) {
                    cities[selectedCountry].forEach(city => {
                        const option = document.createElement('option');
                        option.value = city;
                        option.textContent = city;
                        citySelect.appendChild(option);
                    });
                }
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html, weather=weather, cities=cities, selected_country=selected_country, selected_city=selected_city)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
