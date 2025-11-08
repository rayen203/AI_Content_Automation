from flask import Flask, request, render_template, jsonify
import ollama
import os
import json
import re
import logging
import requests
from PIL import Image
from io import BytesIO
import time
from dotenv import load_dotenv

# Charger les variables d'environnement (.env)
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# Configuration des logs
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# Initialisation de Flask
app = Flask(__name__, template_folder='templates', static_folder='static')
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"


# Nettoyage du JSON renvoyé par Llama
def clean_json(text):
    text = text.strip()
    text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'```$', '', text, flags=re.MULTILINE).strip()
    return text


# 🔹 Fonction de génération d'image (Hugging Face API)
def generate_image_hf(image_prompt):
    """Génère une image via Hugging Face (NOUVELLE URL 2025)"""
    API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    payload = {"inputs": image_prompt}

    log.debug(f"Génération image avec prompt : {image_prompt}")
    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)

    if response.status_code != 200:
        raise Exception(f"Erreur Hugging Face : {response.text}")

    image = Image.open(BytesIO(response.content))

    # Sauvegarde
    filename = f"img_{int(time.time())}.png"
    folder = os.path.join(app.static_folder, "generated")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    image.save(path)

    log.debug(f"Image sauvegardée : {path}")
    return f"/static/generated/{filename}"

@app.route("/")
def home():
    return render_template('index.html')


# 🔹 Route principale de génération
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    
    if not prompt:
        return jsonify({"error": "Prompt requis"}), 400

    # === DÉTECTION ENVIRONNEMENT ===
    if os.getenv('RAILWAY_ENVIRONMENT'):  # Cloud (Railway)
        result = {
            "title": "Démo Live sur Railway",
            "post": f"Vous avez tapé : \"{prompt}\".\n\n"
                    "Cette app tourne en ligne ! L'image est générée en temps réel par Hugging Face.\n\n"
                    "Prêt à automatiser votre contenu LinkedIn ?",
            "hashtags": ["#IA", "#LinkedIn", "#Railway", "#Demo", "#Freelance"]
        }
    else:  # Local (Ollama)
        try:
            # Prompt renforcé pour forcer JSON
            system_prompt = (
                "Tu es un assistant qui génère des posts LinkedIn. "
                "Retourne UNIQUEMENT un JSON valide avec les clés : title, post, hashtags (liste). "
                "Pas de texte avant ou après. Exemple : "
                '{"title": "Mon titre", "post": "Mon texte", "hashtags": ["#tag1", "#tag2"]}'
            )
            response = ollama.chat(model='llama3.2', messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"Sujet : {prompt}"}
            ])
            raw = response['message']['content'].strip()

            # Nettoie le JSON (enlève ```json, ```, etc.)
            json_match = re.search(r'\{.*\}', raw, re.DOTALL)
            if not json_match:
                raise ValueError("Aucun JSON trouvé")
            clean_json = json_match.group(0)

            result = json.loads(clean_json)

        except json.JSONDecodeError as e:
            log.error(f"JSON invalide : {e}\nRaw: {raw}")
            return jsonify({"error": "JSON invalide", "raw": raw[:200]}), 500
        except Exception as e:
            log.error(f"Ollama error: {e}")
            return jsonify({"error": "Ollama non disponible"}), 500

    # === IMAGE (HF) ===
    try:
        image_prompt = f"LinkedIn post about {prompt}, professional, clean, modern, blue tones"
        image_url = generate_image_hf(image_prompt)
        result["image_url"] = image_url
    except Exception as e:
        log.error(f"HF error: {e}")
        result["image_url"] = None

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)

