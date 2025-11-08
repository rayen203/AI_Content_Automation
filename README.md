# AI Content Generator  
**Génère des posts LinkedIn engageants avec Llama 3.2 (local) + Image IA (Hugging Face)**  
**100% privé (texte) • 0 API payante • Démo live en ligne**

![Demo](demo_tiny.gif)

---

## Fonctionnalités
- **Sujet → Post complet** : Titre + texte + hashtags + **image professionnelle**
- **Local** : Texte IA via **Ollama (Llama 3.2)** → **100% privé**
- **Cloud** : Démo live sur **Railway** → **scalable & accessible**
- **Image IA** : Générée par **Hugging Face (`FLUX.1-schnell`)** → **gratuit**
- Copie du post en 1 clic
- Téléchargement de l’image
- **Zéro coût, zéro abonnement**

---

## Stack Technique

| Tech | Rôle |
|------|------|
| `uv` | Gestionnaire de paquets ultra-rapide |
| `Flask` | Backend web |
| `Ollama` | IA texte locale (Llama 3.2) |
| `Hugging Face` | IA image (gratuit) |
| `HTML/CSS/JS` | Frontend moderne & responsive |

---

## Installation & Lancement (5 min)

```bash
# 1. Clone le projet
git clone https://github.com/rayen203/AI_Content_Automation.git
cd AI_Content_Automation

# 2. Installe les dépendances
uv sync

# 3. Lance Ollama (autre terminal)
ollama serve

# 4. Télécharge le modèle (1 fois)
ollama pull llama3.2

# 5. Ajoute ton token Hugging Face
echo "HF_TOKEN=hf_ton_token_ici" > .env

# 6. Lance l’app
uv run src/ai_content_automation/app.py