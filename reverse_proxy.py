import os
import requests
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # Récupérer la clé API à partir de la variable d'environnement
    api_key = os.environ.get('SALAD_API_KEY')

    # Récupérer l'URL du serveur Ollama à partir de la variable d'environnement
    ollama_url = os.environ.get('OLLAMA_URL')

    # Construire l'URL de la requête au serveur Ollama
    url = f'{ollama_url}{request.path}' # Utiliser request.path pour obtenir le chemin d'accès complet

    print('Request URL:')
    print(url)

    # Ajouter la clé API à l'en-tête de la requête
    headers = {
        'Salad-Api-Key': api_key,
        'Content-Type': 'application/json'
    }

    # Afficher les en-têtes de la requête
    print('Request headers:')
    print(headers)

    # Transmettre la requête au serveur Ollama
    resp = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data()
    )

    # Afficher les en-têtes de la réponse
    print('Response headers:')
    print(resp.headers)

    # Renvoie la réponse du serveur Ollama au client
    return Response(
        response=resp.content,
        status=resp.status_code,
        mimetype=resp.headers.get('Content-Type')
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11434)
