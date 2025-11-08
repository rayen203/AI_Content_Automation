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
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "").strip() if data else ""

    if not prompt:
        return jsonify({"error": "Aucun prompt fourni."}), 400

    log.debug(f"Prompt reçu : {prompt}")

    try:
        # --- Étape 1 : Génération du texte via Ollama ---
        full_prompt = f"""
Tu es un expert LinkedIn.
Sujet : "{prompt}"
Génère un contenu inspirant.
Réponds UNIQUEMENT en JSON valide :
{{"title": "titre", "post": "post (200-300 caractères)", "hashtags": ["#tag1", "#tag2", "#tag3"]}}
"""

        log.debug("Envoi du prompt à Ollama...")
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": full_prompt}],
            stream=False
        )

        raw = response["message"]["content"]
        log.debug(f"Réponse brute Ollama : {raw}")

        cleaned = clean_json(raw)
        result = json.loads(cleaned)

        # --- Étape 2 : Génération de l’image via Hugging Face ---
        image_prompt = f"Illustration LinkedIn moderne et professionnelle sur le thème : {prompt}"
        result["image_url"] = generate_image_hf(image_prompt)

        return jsonify(result)

    except json.JSONDecodeError as e:
        log.error(f"Erreur JSON : {e}")
        return jsonify({"error": "JSON invalide", "raw": raw}), 500

    except Exception as e:
        log.error(f"Erreur : {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

